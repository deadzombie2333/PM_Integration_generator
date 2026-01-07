#!/usr/bin/env python3
"""
PayerMax API Documentation MCP Server

This MCP server provides access to PayerMax API documentation,
allowing agents to query API formats, requirements, and samples.
"""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("PayerMax API Docs")

# Base paths for documentation
API_DOCS_PATH = Path(__file__).parent / "api-docs"
API_SAMPLES_PATH = Path(__file__).parent / "api-samples"


def find_api_files(category: Optional[str] = None, api_name: Optional[str] = None) -> List[Dict[str, str]]:
    """Find API documentation files based on category and/or API name."""
    results = []
    
    search_path = API_DOCS_PATH / category if category else API_DOCS_PATH
    
    if not search_path.exists():
        return results
    
    for md_file in search_path.rglob("*.md"):
        relative_path = md_file.relative_to(API_DOCS_PATH)
        category_name = relative_path.parts[0] if len(relative_path.parts) > 1 else "root"
        file_name = md_file.stem
        
        if api_name and api_name.lower() not in file_name.lower():
            continue
            
        results.append({
            "category": category_name,
            "api_name": file_name,
            "doc_path": str(md_file),
            "sample_path": str(API_SAMPLES_PATH / relative_path)
        })
    
    return results


def read_file_safe(file_path: str) -> Optional[str]:
    """Safely read a file and return its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


@mcp.tool()
def list_api_categories() -> List[str]:
    """
    List all available API categories in the documentation.
    
    Returns:
        List of category names (e.g., "付款", "收单", "多币种资金管理")
    """
    categories = []
    if API_DOCS_PATH.exists():
        for item in API_DOCS_PATH.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                categories.append(item.name)
    return sorted(categories)


@mcp.tool()
def list_apis_in_category(category: str) -> List[Dict[str, str]]:
    """
    List all APIs in a specific category.
    
    Args:
        category: The category name (e.g., "付款", "收单")
    
    Returns:
        List of API information including name and paths
    """
    category_path = API_DOCS_PATH / category
    apis = []
    
    if category_path.exists():
        for md_file in category_path.glob("*.md"):
            apis.append({
                "api_name": md_file.stem,
                "category": category,
                "doc_path": str(md_file.relative_to(API_DOCS_PATH.parent)),
                "sample_path": str((API_SAMPLES_PATH / category / md_file.name).relative_to(API_SAMPLES_PATH.parent))
            })
    
    return apis


@mcp.tool()
def search_apis(query: str) -> List[Dict[str, str]]:
    """
    Search for APIs by name or keyword across all categories.
    
    Args:
        query: Search term (e.g., "付款", "查询", "payment")
    
    Returns:
        List of matching APIs with their information
    """
    results = []
    
    for md_file in API_DOCS_PATH.rglob("*.md"):
        relative_path = md_file.relative_to(API_DOCS_PATH)
        category_name = relative_path.parts[0] if len(relative_path.parts) > 1 else "root"
        file_name = md_file.stem
        
        # Search in filename and content
        if query.lower() in file_name.lower():
            results.append({
                "api_name": file_name,
                "category": category_name,
                "doc_path": str(relative_path),
                "sample_path": str(API_SAMPLES_PATH / relative_path),
                "match_type": "filename"
            })
        else:
            # Search in content
            content = read_file_safe(str(md_file))
            if content and query.lower() in content.lower():
                results.append({
                    "api_name": file_name,
                    "category": category_name,
                    "doc_path": str(relative_path),
                    "sample_path": str(API_SAMPLES_PATH / relative_path),
                    "match_type": "content"
                })
    
    return results[:20]  # Limit to 20 results


@mcp.tool()
def get_api_documentation(category: str, api_name: str) -> Dict[str, Any]:
    """
    Get complete API documentation including specification and sample code.
    
    Args:
        category: The API category (e.g., "付款", "收单")
        api_name: The API name (e.g., "付款查询", "交易查询")
    
    Returns:
        Dictionary containing:
        - documentation: Full API specification
        - sample: Sample request/response code
        - has_documentation: Whether documentation was found
        - has_sample: Whether sample was found
    """
    doc_path = API_DOCS_PATH / category / f"{api_name}.md"
    sample_path = API_SAMPLES_PATH / category / f"{api_name}.md"
    
    documentation = read_file_safe(str(doc_path))
    sample = read_file_safe(str(sample_path))
    
    return {
        "category": category,
        "api_name": api_name,
        "documentation": documentation or "Documentation not found",
        "sample": sample or "Sample not found",
        "has_documentation": documentation is not None,
        "has_sample": sample is not None,
        "doc_path": str(doc_path.relative_to(API_DOCS_PATH.parent)) if doc_path.exists() else None,
        "sample_path": str(sample_path.relative_to(API_SAMPLES_PATH.parent)) if sample_path.exists() else None
    }


@mcp.tool()
def get_api_sample(category: str, api_name: str) -> Dict[str, Any]:
    """
    Get only the sample code for a specific API (faster than full documentation).
    
    Args:
        category: The API category (e.g., "付款", "收单")
        api_name: The API name (e.g., "付款查询", "交易查询")
    
    Returns:
        Dictionary containing sample request/response code
    """
    sample_path = API_SAMPLES_PATH / category / f"{api_name}.md"
    sample = read_file_safe(str(sample_path))
    
    return {
        "category": category,
        "api_name": api_name,
        "sample": sample or "Sample not found",
        "has_sample": sample is not None,
        "sample_path": str(sample_path.relative_to(API_SAMPLES_PATH.parent)) if sample_path.exists() else None
    }


@mcp.tool()
def get_api_spec(category: str, api_name: str) -> Dict[str, Any]:
    """
    Get only the API specification/documentation (faster than including samples).
    
    Args:
        category: The API category (e.g., "付款", "收单")
        api_name: The API name (e.g., "付款查询", "交易查询")
    
    Returns:
        Dictionary containing API specification
    """
    doc_path = API_DOCS_PATH / category / f"{api_name}.md"
    documentation = read_file_safe(str(doc_path))
    
    return {
        "category": category,
        "api_name": api_name,
        "documentation": documentation or "Documentation not found",
        "has_documentation": documentation is not None,
        "doc_path": str(doc_path.relative_to(API_DOCS_PATH.parent)) if doc_path.exists() else None
    }


if __name__ == "__main__":
    mcp.run()
