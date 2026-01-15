"""
Parallel Document Embedder Service for Tools 3 & 4

Pre-deployment service that embeds PayerMax documentation into separate indices using parallel processing:
- Tool 3: API Documentation Search (api-docs + api-samples)
- Tool 4: Integration Guide Search (integration_process + payermax_doc)

Usage:
    python document_embedder/parallel_embedder.py              # Index all documents
    python document_embedder/parallel_embedder.py --recreate   # Delete and recreate indices
    python document_embedder/parallel_embedder.py --verify     # Verify indexing status
    python document_embedder/parallel_embedder.py --tool3      # Index only Tool 3 documents
    python document_embedder/parallel_embedder.py --tool4      # Index only Tool 4 documents
    python document_embedder/parallel_embedder.py --workers 8  # Use 8 parallel workers
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import hashlib
from datetime import datetime
from multiprocessing import Pool, cpu_count
from functools import partial
import time


# Global variables for worker processes
_bedrock_client = None
_opensearch_client = None
_opensearch_endpoint = None
_aws_region = None


def init_worker(opensearch_endpoint: str, aws_region: str):
    """Initialize AWS clients in worker process."""
    global _bedrock_client, _opensearch_client, _opensearch_endpoint, _aws_region
    
    _opensearch_endpoint = opensearch_endpoint
    _aws_region = aws_region
    
    try:
        _bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=aws_region
        )
        
        credentials = boto3.Session().get_credentials()
        auth = AWSV4SignerAuth(credentials, aws_region, 'aoss')
        
        _opensearch_client = OpenSearch(
            hosts=[{'host': opensearch_endpoint, 'port': 443}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            timeout=300
        )
    except Exception as e:
        print(f"Worker init error: {e}")
        raise


def get_embedding(text: str) -> List[float]:
    """Get embedding vector for text using AWS Bedrock Titan Embeddings."""
    global _bedrock_client
    
    try:
        request_body = json.dumps({
            "inputText": text[:8000],
            "dimensions": 1024,
            "normalize": True
        })
        
        response = _bedrock_client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=request_body,
            contentType="application/json",
            accept="application/json"
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['embedding']
    except Exception as e:
        print(f"Error getting embedding: {e}")
        raise



def chunk_document(content: str, max_chunk_size: int = 3000) -> List[Dict[str, Any]]:
    """
    Split document into chunks based on markdown structure (sections).
    Respects natural boundaries like headers, preserving document hierarchy.
    """
    chunks = []
    lines = content.split('\n')
    
    current_chunk = []
    current_size = 0
    current_section = "Introduction"
    section_level = 0
    section_hierarchy = []
    
    for i, line in enumerate(lines):
        line_size = len(line) + 1
        
        if line.strip().startswith('#'):
            level = 0
            for char in line:
                if char == '#':
                    level += 1
                else:
                    break
            
            section_title = line.strip('#').strip()
            
            if level <= len(section_hierarchy):
                section_hierarchy = section_hierarchy[:level-1]
            section_hierarchy.append(section_title)
            
            if current_chunk and (current_size > 500 or level <= 2):
                chunk_content = '\n'.join(current_chunk).strip()
                if chunk_content:
                    chunks.append({
                        'content': chunk_content,
                        'section': current_section,
                        'section_hierarchy': section_hierarchy[:-1].copy(),
                        'section_level': section_level,
                        'size': current_size
                    })
                
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size
            
            current_section = section_title
            section_level = level
        
        elif current_size + line_size > max_chunk_size:
            chunk_content = '\n'.join(current_chunk).strip()
            if chunk_content:
                chunks.append({
                    'content': chunk_content,
                    'section': current_section,
                    'section_hierarchy': section_hierarchy.copy(),
                    'section_level': section_level,
                    'size': current_size
                })
            
            current_chunk = [line]
            current_size = line_size
        else:
            current_chunk.append(line)
            current_size += line_size
    
    if current_chunk:
        chunk_content = '\n'.join(current_chunk).strip()
        if chunk_content:
            chunks.append({
                'content': chunk_content,
                'section': current_section,
                'section_hierarchy': section_hierarchy.copy(),
                'section_level': section_level,
                'size': current_size
            })
    
    if not chunks and content.strip():
        chunks.append({
            'content': content.strip(),
            'section': 'Document',
            'section_hierarchy': [],
            'section_level': 0,
            'size': len(content)
        })
    
    return chunks



def process_document(args: Tuple[Path, str, str, str, Path]) -> Dict[str, Any]:
    """
    Process a single document: read, chunk, embed, and prepare for indexing.
    This function runs in parallel worker processes.
    
    Args:
        args: Tuple of (file_path, doc_type, category, index_name, base_path)
    
    Returns:
        Dictionary with processing results and prepared documents
    """
    file_path, doc_type, category, index_name, base_path = args
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {
            'success': False,
            'file_path': str(file_path),
            'error': f"Error reading file: {e}"
        }
    
    if not content.strip():
        return {
            'success': False,
            'file_path': str(file_path),
            'error': "Empty file"
        }
    
    relative_path = str(file_path.relative_to(base_path))
    doc_id = hashlib.md5(relative_path.encode()).hexdigest()
    content_hash = hashlib.md5(content.encode()).hexdigest()
    
    chunks = chunk_document(content)
    api_name = file_path.stem
    
    prepared_docs = []
    
    for i, chunk_data in enumerate(chunks):
        try:
            embedding = get_embedding(chunk_data['content'])
            
            doc = {
                "chunk_id": f"{doc_id}_{i}",
                "doc_id": doc_id,
                "doc_type": doc_type,
                "category": category,
                "api_name": api_name,
                "file_path": relative_path,
                "content": chunk_data['content'],
                "content_hash": content_hash,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "section": chunk_data['section'],
                "section_hierarchy": chunk_data['section_hierarchy'],
                "section_level": chunk_data['section_level'],
                "embedding": embedding,
                "metadata": {
                    "file_name": file_path.name,
                    "file_size": len(content),
                    "chunk_size": chunk_data['size']
                },
                "indexed_at": datetime.utcnow().isoformat()
            }
            
            prepared_docs.append(doc)
            
        except Exception as e:
            return {
                'success': False,
                'file_path': relative_path,
                'error': f"Error processing chunk {i}: {e}"
            }
    
    return {
        'success': True,
        'file_path': relative_path,
        'doc_id': doc_id,
        'content_hash': content_hash,
        'chunks': len(chunks),
        'documents': prepared_docs,
        'index_name': index_name
    }



class ParallelDocumentEmbedder:
    """
    Parallel Document Embedder Service for Tools 3 & 4.
    Uses multiprocessing to speed up embedding generation.
    """
    
    def __init__(
        self,
        base_path: Path,
        opensearch_endpoint: str,
        tool_3_index: str = "payermax-api-docs",
        tool_4_index: str = "payermax-integration-guides",
        num_workers: Optional[int] = None
    ):
        self.base_path = base_path
        self.api_docs_path = base_path / "api-docs"
        self.api_samples_path = base_path / "api-samples"
        self.integration_path = base_path / "integration_process"
        self.payermax_doc_path = base_path / "payermax_doc"
        self.tool_3_index = tool_3_index
        self.tool_4_index = tool_4_index
        self.opensearch_endpoint = opensearch_endpoint
        self.aws_region = os.environ.get('AWS_REGION', 'us-west-2')
        self.num_workers = num_workers or max(1, cpu_count() - 1)
        
        print(f"Parallel Document Embedder Service for Tools 3 & 4")
        print(f"Base Path: {base_path}")
        print(f"OpenSearch Endpoint: {opensearch_endpoint}")
        print(f"Tool 3 Index (API Docs): {tool_3_index}")
        print(f"Tool 4 Index (Integration Guides): {tool_4_index}")
        print(f"Parallel Workers: {self.num_workers}")
        print()
        
        try:
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.aws_region
            )
            print("✓ AWS Bedrock client initialized")
        except Exception as e:
            raise Exception(f"Failed to initialize Bedrock client: {e}")
        
        try:
            credentials = boto3.Session().get_credentials()
            auth = AWSV4SignerAuth(credentials, self.aws_region, 'aoss')
            
            self.opensearch_client = OpenSearch(
                hosts=[{'host': opensearch_endpoint, 'port': 443}],
                http_auth=auth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
                timeout=300
            )
            print("✓ OpenSearch client initialized")
        except Exception as e:
            raise Exception(f"Failed to initialize OpenSearch client: {e}")
        
        print()

    
    def verify_prerequisites(self) -> bool:
        """Verify all prerequisites are met before indexing."""
        print("Verifying Prerequisites")
        print("=" * 60)
        
        checks_passed = True
        
        try:
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            print(f"✓ AWS Credentials: {identity['Arn']}")
        except Exception as e:
            print(f"✗ AWS Credentials: {e}")
            checks_passed = False
        
        try:
            request_body = json.dumps({
                "inputText": "test",
                "dimensions": 1024,
                "normalize": True
            })
            response = self.bedrock_runtime.invoke_model(
                modelId="amazon.titan-embed-text-v2:0",
                body=request_body,
                contentType="application/json",
                accept="application/json"
            )
            response_body = json.loads(response['body'].read())
            if response_body.get('embedding'):
                print(f"✓ Bedrock Titan Embeddings: Accessible (dimension: {len(response_body['embedding'])})")
            else:
                print("✗ Bedrock Titan Embeddings: Failed to generate test embedding")
                checks_passed = False
        except Exception as e:
            print(f"✗ Bedrock Titan Embeddings: {e}")
            checks_passed = False
        
        try:
            self.opensearch_client.cat.indices(format='json')
            print(f"✓ OpenSearch Connection: Endpoint accessible")
        except Exception as e:
            if '404' in str(e) or 'NotFoundError' in str(type(e).__name__):
                print(f"✓ OpenSearch Connection: Endpoint ready (no indices yet)")
            else:
                print(f"✗ OpenSearch Connection: {e}")
                checks_passed = False
        
        print("\nTool 3 (API Documentation Search):")
        for path_name, path in [
            ("  API Docs", self.api_docs_path),
            ("  API Samples", self.api_samples_path)
        ]:
            if path.exists():
                count = len(list(path.rglob("*.md")))
                print(f"✓ {path_name}: {count} files found")
            else:
                print(f"✗ {path_name}: Directory not found")
                checks_passed = False
        
        print("\nTool 4 (Integration Guide Search):")
        for path_name, path in [
            ("  Integration Process", self.integration_path),
            ("  PayerMax Docs", self.payermax_doc_path)
        ]:
            if path.exists():
                count = len(list(path.rglob("*.md")))
                print(f"✓ {path_name}: {count} files found")
            else:
                print(f"✗ {path_name}: Directory not found")
                checks_passed = False
        
        print()
        return checks_passed

    
    def create_index(self, index_name: str):
        """Create OpenSearch index with appropriate mappings for vector search."""
        index_body = {
            "settings": {
                "index": {
                    "knn": True,
                    "knn.algo_param.ef_search": 512
                }
            },
            "mappings": {
                "properties": {
                    "chunk_id": {"type": "keyword"},
                    "doc_id": {"type": "keyword"},
                    "doc_type": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    "api_name": {"type": "text"},
                    "file_path": {"type": "keyword"},
                    "content": {"type": "text"},
                    "content_hash": {"type": "keyword"},
                    "chunk_index": {"type": "integer"},
                    "total_chunks": {"type": "integer"},
                    "section": {"type": "text"},
                    "section_hierarchy": {"type": "keyword"},
                    "section_level": {"type": "integer"},
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": 1024,
                        "method": {
                            "name": "hnsw",
                            "space_type": "cosinesimil",
                            "engine": "nmslib",
                            "parameters": {
                                "ef_construction": 512,
                                "m": 16
                            }
                        }
                    },
                    "metadata": {"type": "object"},
                    "indexed_at": {"type": "date"}
                }
            }
        }
        
        try:
            if self.opensearch_client.indices.exists(index=index_name):
                print(f"Index '{index_name}' already exists")
                return
            
            self.opensearch_client.indices.create(index=index_name, body=index_body)
            print(f"✓ Created index '{index_name}'")
        except Exception as e:
            print(f"✗ Error creating index '{index_name}': {e}")
            raise

    
    def bulk_index_documents(self, results: List[Dict[str, Any]]) -> int:
        """Bulk index prepared documents to OpenSearch."""
        indexed_count = 0
        
        for result in results:
            if not result['success']:
                print(f"  ✗ Skipped: {result['file_path']} - {result.get('error', 'Unknown error')}")
                continue
            
            index_name = result['index_name']
            
            try:
                existing = self.opensearch_client.search(
                    index=index_name,
                    body={
                        "query": {
                            "bool": {
                                "must": [
                                    {"term": {"doc_id": result['doc_id']}},
                                    {"term": {"content_hash": result['content_hash']}}
                                ]
                            }
                        },
                        "size": 1
                    }
                )
                
                if existing['hits']['total']['value'] > 0:
                    print(f"  Already indexed: {result['file_path']}")
                    continue
            except:
                pass
            
            for doc in result['documents']:
                try:
                    self.opensearch_client.index(index=index_name, body=doc)
                    indexed_count += 1
                except Exception as e:
                    print(f"  ✗ Error indexing chunk {doc['chunk_index']} of {result['file_path']}: {e}")
            
            print(f"  ✓ Indexed: {result['file_path']} ({result['chunks']} chunks)")
        
        return indexed_count
    
    def process_documents_parallel(
        self,
        file_paths: List[Path],
        doc_type: str,
        index_name: str
    ) -> int:
        """Process multiple documents in parallel."""
        if not file_paths:
            return 0
        
        tasks = []
        for file_path in file_paths:
            category = file_path.parent.name
            tasks.append((file_path, doc_type, category, index_name, self.base_path))
        
        print(f"Processing {len(tasks)} documents with {self.num_workers} workers...")
        
        with Pool(
            processes=self.num_workers,
            initializer=init_worker,
            initargs=(self.opensearch_endpoint, self.aws_region)
        ) as pool:
            results = pool.map(process_document, tasks)
        
        return self.bulk_index_documents(results)

    
    def index_tool_3_documents(self) -> Dict[str, int]:
        """Index Tool 3 documents (API docs and samples) in parallel."""
        stats = {"api_docs": 0, "api_samples": 0, "total_chunks": 0}
        
        print("\n=== Tool 3: Indexing API Documentation ===")
        api_doc_files = list(self.api_docs_path.rglob("*.md"))
        chunks = self.process_documents_parallel(api_doc_files, "api_doc", self.tool_3_index)
        stats["api_docs"] = len(api_doc_files)
        stats["total_chunks"] += chunks
        
        print("\n=== Tool 3: Indexing API Samples ===")
        api_sample_files = list(self.api_samples_path.rglob("*.md"))
        chunks = self.process_documents_parallel(api_sample_files, "api_sample", self.tool_3_index)
        stats["api_samples"] = len(api_sample_files)
        stats["total_chunks"] += chunks
        
        return stats
    
    def index_tool_4_documents(self) -> Dict[str, int]:
        """Index Tool 4 documents (integration guides and PayerMax docs) in parallel."""
        stats = {"integration_guides": 0, "payermax_docs": 0, "total_chunks": 0}
        
        print("\n=== Tool 4: Indexing Integration Guides ===")
        integration_files = list(self.integration_path.rglob("*.md"))
        chunks = self.process_documents_parallel(integration_files, "integration_guide", self.tool_4_index)
        stats["integration_guides"] = len(integration_files)
        stats["total_chunks"] += chunks
        
        print("\n=== Tool 4: Indexing PayerMax Documentation ===")
        payermax_files = list(self.payermax_doc_path.rglob("*.md"))
        chunks = self.process_documents_parallel(payermax_files, "payermax_doc", self.tool_4_index)
        stats["payermax_docs"] = len(payermax_files)
        stats["total_chunks"] += chunks
        
        return stats
    
    def get_indexing_status(self, index_name: str) -> Dict[str, Any]:
        """Get current indexing status for an index."""
        try:
            if not self.opensearch_client.indices.exists(index=index_name):
                return {"index_exists": False, "message": f"Index '{index_name}' does not exist"}
            
            stats = self.opensearch_client.indices.stats(index=index_name)
            count_response = self.opensearch_client.count(index=index_name)
            
            doc_types = {}
            for doc_type in ["api_doc", "api_sample", "integration_guide", "payermax_doc"]:
                try:
                    type_count = self.opensearch_client.count(
                        index=index_name,
                        body={"query": {"term": {"doc_type": doc_type}}}
                    )
                    if type_count['count'] > 0:
                        doc_types[doc_type] = type_count['count']
                except:
                    pass
            
            return {
                "index_exists": True,
                "total_documents": count_response['count'],
                "document_types": doc_types,
                "index_size_bytes": stats['_all']['total']['store']['size_in_bytes'],
                "index_size_mb": round(stats['_all']['total']['store']['size_in_bytes'] / 1024 / 1024, 2)
            }
        except Exception as e:
            return {"error": str(e)}

    
    def print_status_report(self):
        """Print a detailed status report for both indices."""
        print("\n" + "=" * 60)
        print("Indexing Status Report")
        print("=" * 60)
        
        print("\nTool 3: API Documentation Search")
        print(f"Index: {self.tool_3_index}")
        print("-" * 60)
        status_3 = self.get_indexing_status(self.tool_3_index)
        
        if not status_3.get("index_exists"):
            print(f"Status: {status_3.get('message', 'Unknown')}")
        elif "error" in status_3:
            print(f"Error: {status_3['error']}")
        else:
            print(f"Total Documents: {status_3['total_documents']}")
            print(f"Index Size: {status_3['index_size_mb']} MB")
            print("Documents by Type:")
            for doc_type, count in status_3['document_types'].items():
                print(f"  - {doc_type}: {count}")
        
        print("\nTool 4: Integration Guide Search")
        print(f"Index: {self.tool_4_index}")
        print("-" * 60)
        status_4 = self.get_indexing_status(self.tool_4_index)
        
        if not status_4.get("index_exists"):
            print(f"Status: {status_4.get('message', 'Unknown')}")
        elif "error" in status_4:
            print(f"Error: {status_4['error']}")
        else:
            print(f"Total Documents: {status_4['total_documents']}")
            print(f"Index Size: {status_4['index_size_mb']} MB")
            print("Documents by Type:")
            for doc_type, count in status_4['document_types'].items():
                print(f"  - {doc_type}: {count}")
        
        print()
    
    def delete_index(self, index_name: str):
        """Delete an index (use with caution)."""
        try:
            if self.opensearch_client.indices.exists(index=index_name):
                self.opensearch_client.indices.delete(index=index_name)
                print(f"✓ Deleted index '{index_name}'")
            else:
                print(f"Index '{index_name}' does not exist")
        except Exception as e:
            print(f"✗ Error deleting index '{index_name}': {e}")



def main():
    """Main function to run the parallel embedder service."""
    print("=" * 60)
    print("PayerMax Parallel Document Embedder Service")
    print("Tools 3 & 4 - Pre-Deployment Indexing")
    print("=" * 60)
    print()
    
    import argparse
    parser = argparse.ArgumentParser(
        description='PayerMax Parallel Document Embedder Service - Pre-deployment indexing for Tools 3 & 4'
    )
    parser.add_argument('--recreate', action='store_true', help='Delete existing indices and recreate')
    parser.add_argument('--delete', action='store_true', help='Delete indices only (no recreation)')
    parser.add_argument('--verify', action='store_true', help='Verify indexing status only')
    parser.add_argument('--tool3', action='store_true', help='Index only Tool 3 documents (API docs and samples)')
    parser.add_argument('--tool4', action='store_true', help='Index only Tool 4 documents (integration guides and PayerMax docs)')
    parser.add_argument('--workers', type=int, default=None, help='Number of parallel workers (default: CPU count - 1)')
    args = parser.parse_args()
    
    opensearch_endpoint = os.environ.get('OPENSEARCH_ENDPOINT')
    if not opensearch_endpoint:
        print("✗ Error: OPENSEARCH_ENDPOINT environment variable not set")
        print()
        print("Please set it to your OpenSearch Serverless endpoint:")
        print("  export OPENSEARCH_ENDPOINT=your-collection.us-west-2.aoss.amazonaws.com")
        print()
        sys.exit(1)
    
    base_path = Path(__file__).parent.parent
    tool_3_index = os.environ.get('TOOL_3_INDEX', 'payermax-api-docs')
    tool_4_index = os.environ.get('TOOL_4_INDEX', 'payermax-integration-guides')
    
    try:
        embedder = ParallelDocumentEmbedder(
            base_path, 
            opensearch_endpoint, 
            tool_3_index, 
            tool_4_index,
            num_workers=args.workers
        )
    except Exception as e:
        print(f"✗ Failed to initialize service: {e}")
        sys.exit(1)
    
    if not embedder.verify_prerequisites():
        print("✗ Prerequisites check failed")
        print()
        print("Please fix the issues above before proceeding.")
        sys.exit(1)
    
    print("✓ All prerequisites met")
    print()
    
    if args.verify:
        embedder.print_status_report()
        sys.exit(0)
    
    if args.delete:
        print("Deleting indices...")
        embedder.delete_index(tool_3_index)
        embedder.delete_index(tool_4_index)
        print()
        sys.exit(0)
    
    if args.recreate:
        print("Recreating indices...")
        embedder.delete_index(tool_3_index)
        embedder.delete_index(tool_4_index)
        print()
    
    index_tool3 = args.tool3 or not (args.tool3 or args.tool4)
    index_tool4 = args.tool4 or not (args.tool3 or args.tool4)
    
    start_time = datetime.now()
    all_stats = {}
    
    if index_tool3:
        print(f"\nCreating Tool 3 index: {tool_3_index}")
        embedder.create_index(tool_3_index)
        print()
        
        print("Starting Tool 3 document indexing...")
        stats_3 = embedder.index_tool_3_documents()
        all_stats['tool_3'] = stats_3
    
    if index_tool4:
        print(f"\nCreating Tool 4 index: {tool_4_index}")
        embedder.create_index(tool_4_index)
        print()
        
        print("Starting Tool 4 document indexing...")
        stats_4 = embedder.index_tool_4_documents()
        all_stats['tool_4'] = stats_4
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print()
    print("=" * 60)
    print("Indexing Complete")
    print("=" * 60)
    
    if 'tool_3' in all_stats:
        print("\nTool 3 (API Documentation Search):")
        print(f"  API Docs: {all_stats['tool_3']['api_docs']} documents")
        print(f"  API Samples: {all_stats['tool_3']['api_samples']} documents")
        print(f"  Total Chunks: {all_stats['tool_3']['total_chunks']} chunks")
    
    if 'tool_4' in all_stats:
        print("\nTool 4 (Integration Guide Search):")
        print(f"  Integration Guides: {all_stats['tool_4']['integration_guides']} documents")
        print(f"  PayerMax Docs: {all_stats['tool_4']['payermax_docs']} documents")
        print(f"  Total Chunks: {all_stats['tool_4']['total_chunks']} chunks")
    
    print(f"\nDuration: {int(duration // 60)} minutes {int(duration % 60)} seconds")
    print()
    
    embedder.print_status_report()
    
    print("✓ Parallel document embedder service completed successfully")
    print()
    print("Next Steps:")
    print("1. Verify the indexing status above")
    print("2. Test search functionality")
    print("3. Deploy the MCP server with these index names:")
    print(f"   - TOOL_3_INDEX={tool_3_index}")
    print(f"   - TOOL_4_INDEX={tool_4_index}")
    print()


if __name__ == "__main__":
    main()
