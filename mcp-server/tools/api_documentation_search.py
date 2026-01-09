"""
API Documentation Search Tool (Tool 3)

Semantic search using embeddings across all API specifications, samples, 
and endpoint documentation. Finds detailed API parameters, request/response 
formats, error codes, and code examples.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


class APIDocumentationSearch:
    """
    Semantic search tool for API documentation using OpenSearch Serverless.
    
    Searches across:
    - API specifications (api-docs/**/*.md)
    - API samples (api-samples/**/*.md)
    """
    
    def __init__(self, base_path: Path, config: Dict[str, Any]):
        """
        Initialize the API Documentation Search tool.
        
        Args:
            base_path: Base directory path for documentation
            config: Configuration dictionary from tool_config.json
        """
        self.base_path = base_path
        self.config = config.get("tool_3_api_documentation_search", {})
        
        # Get OpenSearch configuration from environment
        self.opensearch_endpoint = os.environ.get('OPENSEARCH_ENDPOINT')
        self.aws_region = os.environ.get('AWS_REGION', 'us-east-1')
        self.index_name = os.environ.get('TOOL_3_INDEX', 'payermax-api-docs')
        
        if not self.opensearch_endpoint:
            raise ValueError("OPENSEARCH_ENDPOINT environment variable not set")
        
        # Initialize AWS Bedrock client for embeddings
        try:
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.aws_region
            )
        except Exception as e:
            raise Exception(f"Failed to initialize Bedrock client: {e}")
        
        # Initialize OpenSearch client
        try:
            credentials = boto3.Session().get_credentials()
            auth = AWSV4SignerAuth(credentials, self.aws_region, 'aoss')
            
            self.opensearch_client = OpenSearch(
                hosts=[{'host': self.opensearch_endpoint, 'port': 443}],
                http_auth=auth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
                timeout=30
            )
        except Exception as e:
            raise Exception(f"Failed to initialize OpenSearch client: {e}")
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector for text using AWS Bedrock Titan Embeddings.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector (1024 dimensions)
        """
        try:
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
            raise Exception(f"Error getting embedding: {e}")
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        doc_type_filter: Optional[str] = None,
        category_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform semantic search across API documentation.
        
        Args:
            query: Natural language search query
            top_k: Number of results to return
            doc_type_filter: Optional filter by doc_type (api_doc, api_sample)
            category_filter: Optional filter by category
        
        Returns:
            Dictionary containing search results with relevance scores
        """
        try:
            # Get query embedding
            query_embedding = self.get_embedding(query)
            
            # Build search query
            search_body = {
                "size": top_k,
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": query_embedding,
                            "k": top_k
                        }
                    }
                },
                "_source": [
                    "file_path",
                    "doc_type",
                    "category",
                    "api_name",
                    "section",
                    "section_hierarchy",
                    "content",
                    "chunk_index",
                    "total_chunks"
                ]
            }
            
            # Add filters if specified
            if doc_type_filter or category_filter:
                filters = []
                if doc_type_filter:
                    filters.append({"term": {"doc_type": doc_type_filter}})
                if category_filter:
                    filters.append({"term": {"category": category_filter}})
                
                search_body["query"] = {
                    "bool": {
                        "must": [search_body["query"]],
                        "filter": filters
                    }
                }
            
            # Perform search
            results = self.opensearch_client.search(
                index=self.index_name,
                body=search_body
            )
            
            # Format results
            formatted_results = []
            for hit in results['hits']['hits']:
                source = hit['_source']
                formatted_results.append({
                    "relevance_score": hit['_score'],
                    "api_name": source.get('api_name'),
                    "doc_type": source.get('doc_type'),
                    "category": source.get('category'),
                    "file_path": source.get('file_path'),
                    "section": source.get('section'),
                    "section_hierarchy": source.get('section_hierarchy', []),
                    "content": source.get('content'),
                    "chunk_info": f"{source.get('chunk_index', 0) + 1}/{source.get('total_chunks', 1)}"
                })
            
            return {
                "query": query,
                "total_results": results['hits']['total']['value'],
                "returned_results": len(formatted_results),
                "results": formatted_results,
                "search_metadata": {
                    "index": self.index_name,
                    "doc_type_filter": doc_type_filter,
                    "category_filter": category_filter,
                    "top_k": top_k
                }
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "query": query,
                "results": []
            }
    
    def search_by_api_name(
        self,
        api_name: str,
        include_samples: bool = True
    ) -> Dict[str, Any]:
        """
        Search for specific API by name.
        
        Args:
            api_name: Name of the API to search for
            include_samples: Whether to include sample code
        
        Returns:
            Dictionary containing API specification and samples
        """
        try:
            # Build search query
            search_body = {
                "size": 20,
                "query": {
                    "bool": {
                        "should": [
                            {"match": {"api_name": {"query": api_name, "boost": 2}}},
                            {"match": {"file_path": api_name}}
                        ],
                        "minimum_should_match": 1
                    }
                },
                "_source": [
                    "file_path",
                    "doc_type",
                    "category",
                    "api_name",
                    "section",
                    "content",
                    "chunk_index",
                    "total_chunks"
                ],
                "sort": [
                    {"chunk_index": "asc"}
                ]
            }
            
            # Add doc_type filter if not including samples
            if not include_samples:
                search_body["query"]["bool"]["filter"] = [
                    {"term": {"doc_type": "api_doc"}}
                ]
            
            # Perform search
            results = self.opensearch_client.search(
                index=self.index_name,
                body=search_body
            )
            
            # Group results by doc_type
            api_docs = []
            api_samples = []
            
            for hit in results['hits']['hits']:
                source = hit['_source']
                result_item = {
                    "file_path": source.get('file_path'),
                    "section": source.get('section'),
                    "content": source.get('content'),
                    "chunk_info": f"{source.get('chunk_index', 0) + 1}/{source.get('total_chunks', 1)}"
                }
                
                if source.get('doc_type') == 'api_doc':
                    api_docs.append(result_item)
                elif source.get('doc_type') == 'api_sample':
                    api_samples.append(result_item)
            
            return {
                "api_name": api_name,
                "found": len(api_docs) > 0 or len(api_samples) > 0,
                "specification": {
                    "chunks": api_docs,
                    "total_chunks": len(api_docs)
                },
                "samples": {
                    "chunks": api_samples,
                    "total_chunks": len(api_samples)
                } if include_samples else None
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "api_name": api_name,
                "found": False
            }
    
    def list_available_apis(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        List all available APIs, optionally filtered by category.
        
        Args:
            category: Optional category filter
        
        Returns:
            Dictionary containing list of available APIs
        """
        try:
            # Build aggregation query
            search_body = {
                "size": 0,
                "aggs": {
                    "unique_apis": {
                        "terms": {
                            "field": "api_name.keyword",
                            "size": 1000
                        },
                        "aggs": {
                            "categories": {
                                "terms": {
                                    "field": "category.keyword"
                                }
                            },
                            "doc_types": {
                                "terms": {
                                    "field": "doc_type.keyword"
                                }
                            }
                        }
                    }
                }
            }
            
            # Add category filter if specified
            if category:
                search_body["query"] = {
                    "term": {"category.keyword": category}
                }
            
            # Perform search
            results = self.opensearch_client.search(
                index=self.index_name,
                body=search_body
            )
            
            # Format results
            apis = []
            for bucket in results['aggregations']['unique_apis']['buckets']:
                api_info = {
                    "api_name": bucket['key'],
                    "document_count": bucket['doc_count'],
                    "categories": [cat['key'] for cat in bucket['categories']['buckets']],
                    "has_specification": any(
                        dt['key'] == 'api_doc' 
                        for dt in bucket['doc_types']['buckets']
                    ),
                    "has_samples": any(
                        dt['key'] == 'api_sample' 
                        for dt in bucket['doc_types']['buckets']
                    )
                }
                apis.append(api_info)
            
            return {
                "total_apis": len(apis),
                "category_filter": category,
                "apis": sorted(apis, key=lambda x: x['api_name'])
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "apis": []
            }
