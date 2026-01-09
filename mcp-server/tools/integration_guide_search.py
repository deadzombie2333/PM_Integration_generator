"""
Integration Guide Search Tool (Tool 4)

Semantic search using embeddings across all integration guides, workflows, 
payment method specifications, and product documentation. Finds step-by-step 
integration processes, payment method details, and implementation guides.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


class IntegrationGuideSearch:
    """
    Semantic search tool for integration guides using OpenSearch Serverless.
    
    Searches across:
    - Integration processes (integration_process/**/*.md)
    - PayerMax documentation (payermax_doc/**/*.md)
    """
    
    def __init__(self, base_path: Path, config: Dict[str, Any]):
        """
        Initialize the Integration Guide Search tool.
        
        Args:
            base_path: Base directory path for documentation
            config: Configuration dictionary from tool_config.json
        """
        self.base_path = base_path
        self.config = config.get("tool_4_integration_guide_search", {})
        
        # Get OpenSearch configuration from environment
        self.opensearch_endpoint = os.environ.get('OPENSEARCH_ENDPOINT')
        self.aws_region = os.environ.get('AWS_REGION', 'us-east-1')
        self.index_name = os.environ.get('TOOL_4_INDEX', 'payermax-integration-guides')
        
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
        Perform semantic search across integration guides.
        
        Args:
            query: Natural language search query
            top_k: Number of results to return
            doc_type_filter: Optional filter by doc_type (integration_guide, payermax_doc)
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
                    "guide_name": source.get('api_name'),
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
    
    def search_by_integration_mode(
        self,
        integration_mode: str
    ) -> Dict[str, Any]:
        """
        Search for guides related to a specific integration mode.
        
        Args:
            integration_mode: Integration mode (e.g., "cashier", "pure_api", "drop_in", "payment_link")
        
        Returns:
            Dictionary containing relevant integration guides
        """
        # Map integration modes to search queries
        mode_queries = {
            "cashier": "收银台支付集成 cashier mode hosted checkout",
            "pure_api": "纯API支付集成 pure API mode direct integration",
            "drop_in": "前置组件 drop-in component embedded payment",
            "payment_link": "链接支付 payment link share link",
            "auth_capture": "Auth-Capture 授权请款",
            "tokenization": "Tokenization 代扣 saved card",
            "subscription": "订阅 subscription recurring payment"
        }
        
        query = mode_queries.get(integration_mode.lower(), integration_mode)
        
        return self.search(
            query=query,
            top_k=10,
            doc_type_filter="integration_guide"
        )
    
    def search_by_payment_method(
        self,
        payment_method: str
    ) -> Dict[str, Any]:
        """
        Search for guides related to a specific payment method.
        
        Args:
            payment_method: Payment method (e.g., "card", "applepay", "googlepay", "apm")
        
        Returns:
            Dictionary containing relevant payment method guides
        """
        # Map payment methods to search queries
        method_queries = {
            "card": "卡支付 card payment credit debit",
            "applepay": "ApplePay Apple Pay wallet",
            "googlepay": "GooglePay Google Pay wallet",
            "apm": "APM alternative payment method local payment"
        }
        
        query = method_queries.get(payment_method.lower(), payment_method)
        
        return self.search(
            query=query,
            top_k=10,
            doc_type_filter="payermax_doc"
        )
    
    def get_integration_workflow(
        self,
        workflow_name: str
    ) -> Dict[str, Any]:
        """
        Get complete integration workflow by name.
        
        Args:
            workflow_name: Name of the workflow/guide
        
        Returns:
            Dictionary containing complete workflow documentation
        """
        try:
            # Build search query
            search_body = {
                "size": 50,
                "query": {
                    "bool": {
                        "should": [
                            {"match": {"api_name": {"query": workflow_name, "boost": 2}}},
                            {"match": {"file_path": workflow_name}}
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
                    "section_hierarchy",
                    "content",
                    "chunk_index",
                    "total_chunks"
                ],
                "sort": [
                    {"chunk_index": "asc"}
                ]
            }
            
            # Perform search
            results = self.opensearch_client.search(
                index=self.index_name,
                body=search_body
            )
            
            # Group results by file
            workflows = {}
            for hit in results['hits']['hits']:
                source = hit['_source']
                file_path = source.get('file_path')
                
                if file_path not in workflows:
                    workflows[file_path] = {
                        "file_path": file_path,
                        "doc_type": source.get('doc_type'),
                        "category": source.get('category'),
                        "chunks": []
                    }
                
                workflows[file_path]["chunks"].append({
                    "section": source.get('section'),
                    "section_hierarchy": source.get('section_hierarchy', []),
                    "content": source.get('content'),
                    "chunk_index": source.get('chunk_index', 0)
                })
            
            # Sort chunks within each workflow
            for workflow in workflows.values():
                workflow["chunks"].sort(key=lambda x: x['chunk_index'])
            
            return {
                "workflow_name": workflow_name,
                "found": len(workflows) > 0,
                "workflows": list(workflows.values())
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "workflow_name": workflow_name,
                "found": False
            }
    
    def list_available_guides(
        self,
        doc_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all available integration guides.
        
        Args:
            doc_type: Optional filter by doc_type (integration_guide, payermax_doc)
        
        Returns:
            Dictionary containing list of available guides
        """
        try:
            # Build aggregation query
            search_body = {
                "size": 0,
                "aggs": {
                    "unique_guides": {
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
            
            # Add doc_type filter if specified
            if doc_type:
                search_body["query"] = {
                    "term": {"doc_type.keyword": doc_type}
                }
            
            # Perform search
            results = self.opensearch_client.search(
                index=self.index_name,
                body=search_body
            )
            
            # Format results
            guides = []
            for bucket in results['aggregations']['unique_guides']['buckets']:
                guide_info = {
                    "guide_name": bucket['key'],
                    "document_count": bucket['doc_count'],
                    "categories": [cat['key'] for cat in bucket['categories']['buckets']],
                    "doc_types": [dt['key'] for dt in bucket['doc_types']['buckets']]
                }
                guides.append(guide_info)
            
            return {
                "total_guides": len(guides),
                "doc_type_filter": doc_type,
                "guides": sorted(guides, key=lambda x: x['guide_name'])
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "guides": []
            }
