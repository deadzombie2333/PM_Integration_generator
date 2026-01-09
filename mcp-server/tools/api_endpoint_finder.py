"""
API Endpoint Finder Tool

Uses AWS Nova LLM to intelligently select the most relevant PayerMax API
based on structured parameters (task_type, payment_type, integration_mode).
"""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any
import boto3


class APIEndpointFinder:
    """
    Intelligent API endpoint finder using AWS Nova LLM.
    
    Provides consistent API selection based on structured parameters:
    - task_type: What the user wants to do
    - payment_type: Payment method preference
    - integration_mode: Integration approach
    """
    
    def __init__(self, base_path: Path, config: Dict[str, Any]):
        """
        Initialize the API Endpoint Finder.
        
        Args:
            base_path: Base directory path for documentation
            config: Configuration dictionary from tool_config.json
        """
        self.base_path = base_path
        self.api_docs_path = base_path / "api-docs"
        self.api_samples_path = base_path / "api-samples"
        self.config = config.get("tool_1_api_endpoint_finder", {})
        self.categories = self.config.get("document_categories", {})
        
        # Initialize AWS Bedrock client
        try:
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name='us-east-1'
            )
        except Exception as e:
            self.bedrock_runtime = None
            print(f"Warning: AWS Bedrock not available: {e}")
        
        # Task type to category mapping
        self.task_category_mapping = {
            "create_payment": ["payment_acceptance", "drop_in", "payment_link"],
            "query_payment": ["payment_acceptance"],
            "confirm_payment": ["payment_acceptance"],
            "refund": ["refund"],
            "query_refund": ["refund"],
            "payout": ["payout"],
            "query_payout": ["payout"],
            "tokenization": ["tokenization"],
            "subscription": ["subscription"],
            "payment_link": ["payment_link"],
            "dispute": ["dispute"],
            "balance": ["fund_management"],
            "exchange": ["fund_management"],
            "risk_control": ["risk_control"]
        }
    
    def read_file_safe(self, file_path: Path) -> Optional[str]:
        """Safely read a file and return its content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None
    
    def call_nova_model(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        """
        Call AWS Bedrock Nova model for intelligent document analysis.
        
        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens in response
        
        Returns:
            Model response text or None if error
        """
        if not self.bedrock_runtime:
            return None
        
        try:
            request_body = {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": max_tokens,
                    "temperature": 0.1,  # Low temperature for consistent results
                    "topP": 0.9
                }
            }
            
            response = self.bedrock_runtime.converse(
                modelId="us.amazon.nova-lite-v1:0",
                **request_body
            )
            
            return response['output']['message']['content'][0]['text']
        except Exception as e:
            print(f"Error calling Nova model: {e}")
            return None
    
    def find_endpoint(
        self,
        task_type: str,
        payment_type: Optional[str] = None,
        integration_mode: Optional[str] = None,
        additional_requirements: Optional[str] = None,
        include_samples: bool = True
    ) -> Dict[str, Any]:
        """
        Find the best API endpoint for the given requirements.
        
        Args:
            task_type: The type of task to perform
            payment_type: Optional payment method type
            integration_mode: Optional integration mode
            additional_requirements: Optional additional context
            include_samples: Whether to include sample code
        
        Returns:
            Dictionary containing selected API, reasoning, samples, and alternatives
        """
        # Get relevant categories for this task
        search_categories = self.task_category_mapping.get(
            task_type, 
            list(self.categories.keys())
        )
        
        # Collect candidate APIs
        candidate_apis = []
        
        for category_key in search_categories:
            category_info = self.categories.get(category_key, {})
            doc_paths = category_info.get("documents", [])
            
            for doc_path in doc_paths:
                content = self.read_file_safe(self.base_path / doc_path)
                if content:
                    # Extract first 500 characters as summary
                    summary = content[:500] if len(content) > 500 else content
                    
                    candidate_apis.append({
                        "api_name": Path(doc_path).stem,
                        "category": category_key,
                        "doc_path": doc_path,
                        "summary": summary,
                        "full_content": content
                    })
        
        if not candidate_apis:
            return {
                "error": f"No APIs found for task_type: {task_type}",
                "available_task_types": list(self.task_category_mapping.keys())
            }
        
        # Use Nova LLM to select the best API
        if self.bedrock_runtime and len(candidate_apis) > 1:
            selected_api, reasoning, alternatives, integration_notes = self._llm_select_api(
                candidate_apis,
                task_type,
                payment_type,
                integration_mode,
                additional_requirements
            )
            
            if selected_api:
                # Get sample code if requested
                sample_code = None
                if include_samples:
                    sample_code = self._get_sample_code(selected_api["doc_path"])
                
                return {
                    "task_type": task_type,
                    "payment_type": payment_type,
                    "integration_mode": integration_mode,
                    "selected_api": {
                        "api_name": selected_api["api_name"],
                        "category": selected_api["category"],
                        "doc_path": selected_api["doc_path"],
                        "specification": selected_api["full_content"]
                    },
                    "reasoning": reasoning,
                    "sample_code": sample_code,
                    "alternative_apis": alternatives,
                    "integration_notes": integration_notes,
                    "llm_powered": True
                }
        
        # Fallback: Simple selection
        return self._fallback_select_api(
            candidate_apis,
            task_type,
            payment_type,
            integration_mode,
            include_samples
        )
    
    def _llm_select_api(
        self,
        candidate_apis: List[Dict[str, Any]],
        task_type: str,
        payment_type: Optional[str],
        integration_mode: Optional[str],
        additional_requirements: Optional[str]
    ) -> tuple:
        """
        Use Nova LLM to select the best API.
        
        Returns:
            Tuple of (selected_api, reasoning, alternatives, integration_notes)
        """
        # Build prompt for Nova
        api_list = "\n\n".join([
            f"API {i+1}: {api['api_name']}\n"
            f"Category: {api['category']}\n"
            f"Summary: {api['summary'][:300]}..."
            for i, api in enumerate(candidate_apis[:10])  # Limit to top 10
        ])
        
        prompt = f"""You are an expert in PayerMax payment API integration. Analyze the following APIs and select the MOST appropriate one for the given requirements.

Task Type: {task_type}
Payment Type: {payment_type or 'any'}
Integration Mode: {integration_mode or 'any'}
Additional Requirements: {additional_requirements or 'none'}

Available APIs:
{api_list}

Instructions:
1. Analyze each API's purpose and capabilities
2. Select the SINGLE best matching API for the requirements
3. Provide clear reasoning for your selection
4. Suggest 1-2 alternative APIs if applicable

Respond in JSON format:
{{
    "selected_api_number": <number>,
    "reasoning": "<detailed explanation>",
    "alternative_api_numbers": [<numbers>],
    "integration_notes": "<important notes for using this API>"
}}"""
        
        llm_response = self.call_nova_model(prompt, max_tokens=1000)
        
        if llm_response:
            try:
                # Parse LLM response
                llm_response = llm_response.strip()
                if llm_response.startswith("```"):
                    llm_response = llm_response.split("```")[1]
                    if llm_response.startswith("json"):
                        llm_response = llm_response[4:]
                llm_response = llm_response.strip()
                
                selection = json.loads(llm_response)
                selected_idx = selection.get("selected_api_number", 1) - 1
                
                if 0 <= selected_idx < len(candidate_apis):
                    selected_api = candidate_apis[selected_idx]
                    reasoning = selection.get("reasoning", "")
                    integration_notes = selection.get("integration_notes", "")
                    
                    # Get alternatives
                    alternatives = []
                    for alt_idx in selection.get("alternative_api_numbers", []):
                        if 0 <= alt_idx - 1 < len(candidate_apis):
                            alt_api = candidate_apis[alt_idx - 1]
                            alternatives.append({
                                "api_name": alt_api["api_name"],
                                "category": alt_api["category"],
                                "doc_path": alt_api["doc_path"]
                            })
                    
                    return selected_api, reasoning, alternatives, integration_notes
            except json.JSONDecodeError as e:
                print(f"Error parsing LLM response: {e}")
        
        return None, None, None, None
    
    def _fallback_select_api(
        self,
        candidate_apis: List[Dict[str, Any]],
        task_type: str,
        payment_type: Optional[str],
        integration_mode: Optional[str],
        include_samples: bool
    ) -> Dict[str, Any]:
        """
        Fallback selection when LLM is not available.
        
        Returns:
            Dictionary with selected API and metadata
        """
        selected_api = candidate_apis[0]
        
        # Get sample code if requested
        sample_code = None
        if include_samples:
            sample_code = self._get_sample_code(selected_api["doc_path"])
        
        return {
            "task_type": task_type,
            "payment_type": payment_type,
            "integration_mode": integration_mode,
            "selected_api": {
                "api_name": selected_api["api_name"],
                "category": selected_api["category"],
                "doc_path": selected_api["doc_path"],
                "specification": selected_api["full_content"]
            },
            "reasoning": f"Selected based on task_type '{task_type}' and category matching",
            "sample_code": sample_code,
            "alternative_apis": [
                {
                    "api_name": api["api_name"],
                    "category": api["category"],
                    "doc_path": api["doc_path"]
                }
                for api in candidate_apis[1:3]
            ],
            "integration_notes": "Review the specification for detailed integration requirements",
            "llm_powered": False
        }
    
    def _get_sample_code(self, doc_path: str) -> Optional[str]:
        """
        Get sample code for an API.
        
        Args:
            doc_path: Path to the API documentation
        
        Returns:
            Sample code content or None
        """
        sample_path = doc_path.replace("api-docs", "api-samples")
        return self.read_file_safe(self.base_path / sample_path)
