"""
Document Embedder Service for Tools 3 & 4

Pre-deployment service that embeds PayerMax documentation into separate indices:
- Tool 3: API Documentation Search (api-docs + api-samples)
- Tool 4: Integration Guide Search (integration_process + payermax_doc)

Usage:
    python document_embedder/document_embedder.py              # Index all documents
    python document_embedder/document_embedder.py --recreate   # Delete and recreate indices
    python document_embedder/document_embedder.py --verify     # Verify indexing status
    python document_embedder/document_embedder.py --tool3      # Index only Tool 3 documents
    python document_embedder/document_embedder.py --tool4      # Index only Tool 4 documents
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import hashlib
from datetime import datetime


class DocumentEmbedderService:
    """
    Pre-deployment service for embedding and indexing documentation for Tools 3 & 4.
    
    Tool 3: API Documentation Search
    - api-docs/**/*.md
    - api-samples/**/*.md
    
    Tool 4: Integration Guide Search
    - integration_process/**/*.md
    - payermax_doc/**/*.md
    """
    
    def __init__(
        self,
        base_path: Path,
        opensearch_endpoint: str,
        tool_3_index: str = "payermax-api-docs",
        tool_4_index: str = "payermax-integration-guides"
    ):
        """
        Initialize the Document Embedder Service.
        
        Args:
            base_path: Base directory path for documentation
            opensearch_endpoint: OpenSearch Serverless endpoint
            tool_3_index: Index name for Tool 3 (API docs and samples)
            tool_4_index: Index name for Tool 4 (Integration guides and PayerMax docs)
        """
        self.base_path = base_path
        self.api_docs_path = base_path / "api-docs"
        self.api_samples_path = base_path / "api-samples"
        self.integration_path = base_path / "integration_process"
        self.payermax_doc_path = base_path / "payermax_doc"
        self.tool_3_index = tool_3_index
        self.tool_4_index = tool_4_index
        
        print(f"Initializing Document Embedder Service for Tools 3 & 4")
        print(f"Base Path: {base_path}")
        print(f"OpenSearch Endpoint: {opensearch_endpoint}")
        print(f"Tool 3 Index (API Docs): {tool_3_index}")
        print(f"Tool 4 Index (Integration Guides): {tool_4_index}")
        print()
        
        # Initialize AWS Bedrock client for embeddings
        try:
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=os.environ.get('AWS_REGION', 'us-east-1')
            )
            print("✓ AWS Bedrock client initialized")
        except Exception as e:
            raise Exception(f"Failed to initialize Bedrock client: {e}")
        
        # Initialize OpenSearch client
        try:
            credentials = boto3.Session().get_credentials()
            auth = AWSV4SignerAuth(credentials, os.environ.get('AWS_REGION', 'us-east-1'), 'aoss')
            
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
        """
        Verify all prerequisites are met before indexing.
        
        Returns:
            True if all checks pass, False otherwise
        """
        print("Verifying Prerequisites")
        print("=" * 60)
        
        checks_passed = True
        
        # Check AWS credentials
        try:
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            print(f"✓ AWS Credentials: {identity['Arn']}")
        except Exception as e:
            print(f"✗ AWS Credentials: {e}")
            checks_passed = False
        
        # Check Bedrock access
        try:
            test_embedding = self.get_embedding("test")
            if test_embedding:
                print(f"✓ Bedrock Titan Embeddings: Accessible (dimension: {len(test_embedding)})")
            else:
                print("✗ Bedrock Titan Embeddings: Failed to generate test embedding")
                checks_passed = False
        except Exception as e:
            print(f"✗ Bedrock Titan Embeddings: {e}")
            checks_passed = False
        
        # Check OpenSearch connection
        try:
            # For OpenSearch Serverless, we can't use info() API
            # Instead, try to list indices (will return empty list if none exist)
            self.opensearch_client.cat.indices(format='json')
            print(f"✓ OpenSearch Connection: Endpoint accessible")
        except Exception as e:
            # 404 is actually OK - it means endpoint is ready but no indices yet
            if '404' in str(e) or 'NotFoundError' in str(type(e).__name__):
                print(f"✓ OpenSearch Connection: Endpoint ready (no indices yet)")
            else:
                print(f"✗ OpenSearch Connection: {e}")
                checks_passed = False
        
        # Check documentation directories for Tool 3
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
        
        # Check documentation directories for Tool 4
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
        """
        Create OpenSearch index with appropriate mappings for vector search.
        
        Args:
            index_name: Name of the index to create
        """
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
            
            response = self.opensearch_client.indices.create(
                index=index_name,
                body=index_body
            )
            print(f"✓ Created index '{index_name}'")
        except Exception as e:
            print(f"✗ Error creating index '{index_name}': {e}")
            raise
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector for text using AWS Bedrock Titan Embeddings.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector (1024 dimensions)
        """
        try:
            # Use Titan Embeddings V2
            request_body = json.dumps({
                "inputText": text[:8000],  # Limit to 8000 chars
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
            return response_body['embedding']
        except Exception as e:
            print(f"Error getting embedding: {e}")
            raise
    
    def chunk_document(
        self,
        content: str,
        max_chunk_size: int = 3000
    ) -> List[Dict[str, Any]]:
        """
        Split document into chunks based on markdown structure (sections).
        Respects natural boundaries like headers, preserving document hierarchy.
        
        Args:
            content: Document content in markdown format
            max_chunk_size: Maximum size of each chunk in characters
        
        Returns:
            List of chunk dictionaries with content and metadata
        """
        chunks = []
        lines = content.split('\n')
        
        current_chunk = []
        current_size = 0
        current_section = "Introduction"
        section_level = 0
        section_hierarchy = []
        
        for i, line in enumerate(lines):
            line_size = len(line) + 1  # +1 for newline
            
            # Detect markdown headers
            if line.strip().startswith('#'):
                # Count header level
                level = 0
                for char in line:
                    if char == '#':
                        level += 1
                    else:
                        break
                
                # Extract section title
                section_title = line.strip('#').strip()
                
                # Update section hierarchy
                if level <= len(section_hierarchy):
                    section_hierarchy = section_hierarchy[:level-1]
                section_hierarchy.append(section_title)
                
                # If current chunk is large enough or we hit a major section, save it
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
                    
                    # Start new chunk with the header
                    current_chunk = [line]
                    current_size = line_size
                else:
                    # Add header to current chunk
                    current_chunk.append(line)
                    current_size += line_size
                
                current_section = section_title
                section_level = level
            
            # Check if adding this line would exceed max size
            elif current_size + line_size > max_chunk_size:
                # Save current chunk
                chunk_content = '\n'.join(current_chunk).strip()
                if chunk_content:
                    chunks.append({
                        'content': chunk_content,
                        'section': current_section,
                        'section_hierarchy': section_hierarchy.copy(),
                        'section_level': section_level,
                        'size': current_size
                    })
                
                # Start new chunk
                current_chunk = [line]
                current_size = line_size
            else:
                # Add line to current chunk
                current_chunk.append(line)
                current_size += line_size
        
        # Add final chunk
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
        
        # If no chunks created (no headers), create one chunk
        if not chunks and content.strip():
            chunks.append({
                'content': content.strip(),
                'section': 'Document',
                'section_hierarchy': [],
                'section_level': 0,
                'size': len(content)
            })
        
        return chunks
    
    def index_document(
        self,
        file_path: Path,
        doc_type: str,
        category: str,
        index_name: str
    ) -> int:
        """
        Index a single document with embeddings.
        
        Args:
            file_path: Path to the document
            doc_type: Type of document (api_doc, api_sample, integration_guide, payermax_doc)
            category: Category/folder name
            index_name: Target index name
        
        Returns:
            Number of chunks indexed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return 0
        
        if not content.strip():
            return 0
        
        # Generate document ID and hash
        relative_path = str(file_path.relative_to(self.base_path))
        doc_id = hashlib.md5(relative_path.encode()).hexdigest()
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Check if document already indexed with same content
        try:
            search_result = self.opensearch_client.search(
                index=index_name,
                body={
                    "query": {
                        "bool": {
                            "must": [
                                {"term": {"doc_id": doc_id}},
                                {"term": {"content_hash": content_hash}}
                            ]
                        }
                    },
                    "size": 1
                }
            )
            
            if search_result['hits']['total']['value'] > 0:
                print(f"  Already indexed: {relative_path}")
                return 0
        except Exception as e:
            # Index might not exist yet, continue
            pass
        
        # Chunk the document based on markdown structure
        chunks = self.chunk_document(content)
        api_name = file_path.stem
        
        indexed_count = 0
        
        for i, chunk_data in enumerate(chunks):
            try:
                # Get embedding for chunk
                embedding = self.get_embedding(chunk_data['content'])
                
                # Prepare document
                doc = {
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
                
                # Index document
                # OpenSearch Serverless doesn't support custom IDs in the same way
                # Let it auto-generate IDs, but include our chunk_id in the document
                doc['chunk_id'] = f"{doc_id}_{i}"
                self.opensearch_client.index(
                    index=index_name,
                    body=doc
                )
                
                indexed_count += 1
                section_info = f" [{chunk_data['section']}]" if chunk_data['section'] else ""
                print(f"  ✓ Chunk {i+1}/{len(chunks)}: {relative_path}{section_info}")
                
            except Exception as e:
                print(f"  ✗ Error indexing chunk {i} of {relative_path}: {e}")
        
        return indexed_count
    
    def index_tool_3_documents(self) -> Dict[str, int]:
        """
        Index Tool 3 documents (API docs and samples).
        
        Returns:
            Dictionary with counts of indexed documents
        """
        stats = {
            "api_docs": 0,
            "api_samples": 0,
            "total_chunks": 0
        }
        
        # Index API documentation
        print("\n=== Tool 3: Indexing API Documentation ===")
        for md_file in self.api_docs_path.rglob("*.md"):
            category = md_file.parent.name
            chunks = self.index_document(md_file, "api_doc", category, self.tool_3_index)
            if chunks > 0:
                stats["api_docs"] += 1
                stats["total_chunks"] += chunks
        
        # Index API samples
        print("\n=== Tool 3: Indexing API Samples ===")
        for md_file in self.api_samples_path.rglob("*.md"):
            category = md_file.parent.name
            chunks = self.index_document(md_file, "api_sample", category, self.tool_3_index)
            if chunks > 0:
                stats["api_samples"] += 1
                stats["total_chunks"] += chunks
        
        return stats
    
    def index_tool_4_documents(self) -> Dict[str, int]:
        """
        Index Tool 4 documents (integration guides and PayerMax docs).
        
        Returns:
            Dictionary with counts of indexed documents
        """
        stats = {
            "integration_guides": 0,
            "payermax_docs": 0,
            "total_chunks": 0
        }
        
        # Index integration guides
        print("\n=== Tool 4: Indexing Integration Guides ===")
        for md_file in self.integration_path.rglob("*.md"):
            category = md_file.parent.name
            chunks = self.index_document(md_file, "integration_guide", category, self.tool_4_index)
            if chunks > 0:
                stats["integration_guides"] += 1
                stats["total_chunks"] += chunks
        
        # Index PayerMax documentation
        print("\n=== Tool 4: Indexing PayerMax Documentation ===")
        for md_file in self.payermax_doc_path.rglob("*.md"):
            category = md_file.parent.name
            chunks = self.index_document(md_file, "payermax_doc", category, self.tool_4_index)
            if chunks > 0:
                stats["payermax_docs"] += 1
                stats["total_chunks"] += chunks
        
        return stats
    
    def get_indexing_status(self, index_name: str) -> Dict[str, Any]:
        """
        Get current indexing status for an index.
        
        Args:
            index_name: Name of the index to check
        
        Returns:
            Dictionary with index statistics
        """
        try:
            if not self.opensearch_client.indices.exists(index=index_name):
                return {
                    "index_exists": False,
                    "message": f"Index '{index_name}' does not exist"
                }
            
            # Get index stats
            stats = self.opensearch_client.indices.stats(index=index_name)
            count_response = self.opensearch_client.count(index=index_name)
            
            # Get document counts by type
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
            return {
                "error": str(e)
            }
    
    def print_status_report(self):
        """Print a detailed status report for both indices."""
        print("\n" + "=" * 60)
        print("Indexing Status Report")
        print("=" * 60)
        
        # Tool 3 status
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
        
        # Tool 4 status
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
    """Main function to run the embedder service."""
    print("=" * 60)
    print("PayerMax Document Embedder Service")
    print("Tools 3 & 4 - Pre-Deployment Indexing")
    print("=" * 60)
    print()
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(
        description='PayerMax Document Embedder Service - Pre-deployment indexing for Tools 3 & 4'
    )
    parser.add_argument(
        '--recreate',
        action='store_true',
        help='Delete existing indices and recreate'
    )
    parser.add_argument(
        '--delete',
        action='store_true',
        help='Delete indices only (no recreation)'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify indexing status only'
    )
    parser.add_argument(
        '--tool3',
        action='store_true',
        help='Index only Tool 3 documents (API docs and samples)'
    )
    parser.add_argument(
        '--tool4',
        action='store_true',
        help='Index only Tool 4 documents (integration guides and PayerMax docs)'
    )
    args = parser.parse_args()
    
    # Get configuration from environment
    opensearch_endpoint = os.environ.get('OPENSEARCH_ENDPOINT')
    if not opensearch_endpoint:
        print("✗ Error: OPENSEARCH_ENDPOINT environment variable not set")
        print()
        print("Please set it to your OpenSearch Serverless endpoint:")
        print("  export OPENSEARCH_ENDPOINT=your-collection.us-east-1.aoss.amazonaws.com")
        print()
        sys.exit(1)
    
    base_path = Path(__file__).parent.parent
    tool_3_index = os.environ.get('TOOL_3_INDEX', 'payermax-api-docs')
    tool_4_index = os.environ.get('TOOL_4_INDEX', 'payermax-integration-guides')
    
    try:
        embedder = DocumentEmbedderService(base_path, opensearch_endpoint, tool_3_index, tool_4_index)
    except Exception as e:
        print(f"✗ Failed to initialize service: {e}")
        sys.exit(1)
    
    # Verify prerequisites
    if not embedder.verify_prerequisites():
        print("✗ Prerequisites check failed")
        print()
        print("Please fix the issues above before proceeding.")
        sys.exit(1)
    
    print("✓ All prerequisites met")
    print()
    
    # Handle commands
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
    
    # Determine which tools to index
    index_tool3 = args.tool3 or not (args.tool3 or args.tool4)
    index_tool4 = args.tool4 or not (args.tool3 or args.tool4)
    
    start_time = datetime.now()
    all_stats = {}
    
    # Index Tool 3 documents
    if index_tool3:
        print(f"\nCreating Tool 3 index: {tool_3_index}")
        embedder.create_index(tool_3_index)
        print()
        
        print("Starting Tool 3 document indexing...")
        stats_3 = embedder.index_tool_3_documents()
        all_stats['tool_3'] = stats_3
    
    # Index Tool 4 documents
    if index_tool4:
        print(f"\nCreating Tool 4 index: {tool_4_index}")
        embedder.create_index(tool_4_index)
        print()
        
        print("Starting Tool 4 document indexing...")
        stats_4 = embedder.index_tool_4_documents()
        all_stats['tool_4'] = stats_4
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Print summary
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
    
    # Print final status
    embedder.print_status_report()
    
    print("✓ Document embedder service completed successfully")
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
