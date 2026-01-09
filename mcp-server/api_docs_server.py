#!/usr/bin/env python3
"""
PayerMax API Documentation MCP Server

Intelligent MCP server with LLM-based document selection and semantic search.
Provides 4 specialized tools for different integration needs.
"""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP

# Import tools
from tools import (
    APIEndpointFinder,
    IntegrationAssistant,
    APIDocumentationSearch,
    IntegrationGuideSearch
)

# Initialize FastMCP server
mcp = FastMCP("PayerMax API Docs")

# Base paths
BASE_PATH = Path(__file__).parent
CONFIG_PATH = BASE_PATH / "tool_config.json"

# Load configuration
def load_config() -> Dict[str, Any]:
    """Load tool configuration from JSON file."""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {}

CONFIG = load_config()

# Initialize tools
api_endpoint_finder = APIEndpointFinder(BASE_PATH, CONFIG)
integration_assistant = IntegrationAssistant(BASE_PATH, CONFIG)

# Initialize OpenSearch-based tools (Tools 3 & 4)
api_documentation_search = None
integration_guide_search = None

try:
    api_documentation_search = APIDocumentationSearch(BASE_PATH, CONFIG)
    integration_guide_search = IntegrationGuideSearch(BASE_PATH, CONFIG)
except Exception as e:
    print(f"Warning: Could not initialize OpenSearch-based tools: {e}")
    print("Make sure OPENSEARCH_ENDPOINT environment variable is set")


@mcp.tool()
def find_api_endpoint(
    task_type: str,
    payment_type: Optional[str] = None,
    integration_mode: Optional[str] = None,
    additional_requirements: Optional[str] = None,
    include_samples: bool = True
) -> Dict[str, Any]:
    """
    Tool 1: API Endpoint Finder
    
    Finds the correct API endpoint specification and sample code using AWS Nova LLM for intelligent analysis.
    Uses structured parameters for consistent and accurate API selection.
    
    Args:
        task_type: The type of task to perform. Options:
                  - "create_payment": Create a new payment/transaction
                  - "query_payment": Query payment/transaction status
                  - "confirm_payment": Confirm a payment
                  - "refund": Process a refund
                  - "query_refund": Query refund status
                  - "payout": Send money to users (disbursement)
                  - "query_payout": Query payout status
                  - "tokenization": Manage payment tokens for saved cards
                  - "subscription": Manage subscription plans
                  - "payment_link": Create/manage payment links
                  - "dispute": Handle disputes/chargebacks
                  - "balance": Check account balance
                  - "exchange": Currency exchange operations
                  - "risk_control": Risk management operations
        
        payment_type: Optional payment method type. Options:
                     - "card": Credit/debit card payments
                     - "wallet": E-wallet payments
                     - "bank_transfer": Bank transfer
                     - "cash": Cash payments
                     - "any": Any payment method (default)
        
        integration_mode: Optional integration mode. Options:
                         - "cashier": Hosted checkout page
                         - "api": Pure API integration
                         - "drop_in": Drop-in component
                         - "link": Payment link
                         - "any": Any mode (default)
        
        additional_requirements: Optional additional context or requirements
        include_samples: Whether to include sample code (default: True)
    
    Returns:
        Dictionary containing:
        - selected_api: The best matching API with full specification
        - reasoning: LLM explanation of why this API was selected
        - sample_code: Sample request/response if include_samples=True
        - alternative_apis: Other potentially suitable APIs
        - integration_notes: Important notes for integration
    """
    return api_endpoint_finder.find_endpoint(
        task_type=task_type,
        payment_type=payment_type,
        integration_mode=integration_mode,
        additional_requirements=additional_requirements,
        include_samples=include_samples
    )


@mcp.tool()
def get_integration_recommendation(
    user_description: str
) -> Dict[str, Any]:
    """
    Tool 2: Integration Assistant
    
    Analyzes your integration requirements using AWS Nova LLM and recommends the best
    integration method with step-by-step guidance.
    
    This tool uses natural language processing to:
    1. Extract key specifications from your description
    2. Determine the most suitable integration method
    3. Provide detailed integration guidance
    4. List required APIs
    
    Args:
        user_description: Natural language description of your integration requirements.
                         Describe what you want to build, your constraints, and priorities.
                         
                         Examples:
                         - "I need to accept card payments on my e-commerce website. 
                            I want quick integration and don't have PCI compliance."
                         
                         - "Building a mobile app that needs full control over payment UI. 
                            We have experienced developers and need custom flows."
                         
                         - "Want to send payment links via WhatsApp to customers. 
                            No website, just need to collect payments quickly."
                         
                         - "Need to integrate payments with saved card functionality. 
                            Want balance between ease and customization."
    
    Returns:
        Dictionary containing:
        - extracted_specifications: Key specs extracted from your description
          (payment methods, constraints, features, technical environment)
        - recommended_method: Best integration method for your needs
          (cashier_mode, pure_api_mode, drop_in_mode, payment_link_mode)
        - reasoning: Detailed explanation of why this method was recommended
        - integration_guide: Complete integration documentation
        - required_apis: List of APIs you'll need to implement
        - considerations: Important points to consider
        - next_steps: Ordered list of what to do next
    """
    return integration_assistant.analyze_requirements(user_description)


@mcp.tool()
def search_api_documentation(
    query: str,
    top_k: int = 5,
    doc_type_filter: Optional[str] = None,
    category_filter: Optional[str] = None
) -> Dict[str, Any]:
    """
    Tool 3: API Documentation Search (Semantic Search)
    
    Uses embedding-based semantic search to find the most relevant API documentation.
    Searches through all PayerMax API specifications and samples using vector similarity.
    
    This tool is powered by:
    - AWS Bedrock Titan Embeddings for semantic understanding
    - OpenSearch Serverless for vector search
    
    Args:
        query: Natural language query describing what you're looking for.
               Examples:
               - "How do I handle 3DS authentication for card payments?"
               - "What are the required parameters for creating a refund?"
               - "Show me error codes for payment failures"
               - "How to implement webhook notifications?"
        
        top_k: Number of results to return (default: 5)
        
        doc_type_filter: Optional filter by document type:
                        - "api_doc": API specifications only
                        - "api_sample": Sample code only
                        - None: Search all (default)
        
        category_filter: Optional filter by category (e.g., "payment_acceptance", "refund")
    
    Returns:
        Dictionary containing:
        - query: Your original query
        - total_results: Total number of matching documents
        - returned_results: Number of results returned
        - results: List of relevant API documentation with:
          - relevance_score: Similarity score
          - api_name: Name of the API
          - doc_type: Type of document
          - category: API category
          - file_path: Path to documentation
          - section: Section name
          - content: Relevant content
          - chunk_info: Chunk position
        - search_metadata: Search configuration used
    """
    if not api_documentation_search:
        return {
            "error": "API Documentation Search not available",
            "reason": "OpenSearch endpoint not configured",
            "solution": "Set OPENSEARCH_ENDPOINT environment variable"
        }
    
    return api_documentation_search.search(
        query=query,
        top_k=top_k,
        doc_type_filter=doc_type_filter,
        category_filter=category_filter
    )


@mcp.tool()
def search_integration_guides(
    query: str,
    top_k: int = 5,
    doc_type_filter: Optional[str] = None,
    category_filter: Optional[str] = None
) -> Dict[str, Any]:
    """
    Tool 4: Integration Guide Search (Semantic Search)
    
    Uses embedding-based semantic search to find integration processes and workflows.
    Searches through integration guides and PayerMax product documentation.
    
    This tool is powered by:
    - AWS Bedrock Titan Embeddings for semantic understanding
    - OpenSearch Serverless for vector search
    
    Args:
        query: Natural language description of what you want to integrate.
               Examples:
               - "I want to integrate card payments with hosted checkout"
               - "How do I implement refund functionality?"
               - "Need to add saved card feature to my payment flow"
               - "Want to integrate Apple Pay in my mobile app"
               - "How to set up subscription payments?"
        
        top_k: Number of results to return (default: 5)
        
        doc_type_filter: Optional filter by document type:
                        - "integration_guide": Integration process guides
                        - "payermax_doc": PayerMax product documentation
                        - None: Search all (default)
        
        category_filter: Optional filter by category
    
    Returns:
        Dictionary containing:
        - query: Your original query
        - total_results: Total number of matching documents
        - returned_results: Number of results returned
        - results: List of relevant integration guides with:
          - relevance_score: Similarity score
          - guide_name: Name of the guide
          - doc_type: Type of document
          - category: Guide category
          - file_path: Path to documentation
          - section: Section name
          - content: Relevant content
          - chunk_info: Chunk position
        - search_metadata: Search configuration used
    """
    if not integration_guide_search:
        return {
            "error": "Integration Guide Search not available",
            "reason": "OpenSearch endpoint not configured",
            "solution": "Set OPENSEARCH_ENDPOINT environment variable"
        }
    
    return integration_guide_search.search(
        query=query,
        top_k=top_k,
        doc_type_filter=doc_type_filter,
        category_filter=category_filter
    )


if __name__ == "__main__":
    mcp.run()
