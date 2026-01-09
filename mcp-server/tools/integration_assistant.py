"""
Integration Assistant Tool

Uses AWS Nova LLM to analyze user requirements and recommend the best
integration method with step-by-step guidance.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
import boto3


class IntegrationAssistant:
    """
    Intelligent integration assistant using AWS Nova LLM.
    
    Analyzes user description to:
    1. Extract key specifications (payment methods, features, constraints)
    2. Determine the best integration method
    3. Provide step-by-step integration guidance
    """
    
    def __init__(self, base_path: Path, config: Dict[str, Any]):
        """
        Initialize the Integration Assistant.
        
        Args:
            base_path: Base directory path for documentation
            config: Configuration dictionary from tool_config.json
        """
        self.base_path = base_path
        self.integration_path = base_path / "integration_process"
        self.config = config.get("tool_2_integration_assistant", {})
        
        # Initialize AWS Bedrock client
        try:
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name='us-east-1'
            )
        except Exception as e:
            self.bedrock_runtime = None
            print(f"Warning: AWS Bedrock not available: {e}")
        
        # Integration methods with their characteristics
        self.integration_methods = {
            "cashier_mode": {
                "name": "Cashier Mode (Hosted Checkout)",
                "description": "PayerMax hosted checkout page",
                "best_for": [
                    "Quick integration with minimal frontend work",
                    "No PCI DSS compliance required",
                    "Support for multiple payment methods",
                    "Built-in 3DS authentication",
                    "Saved card functionality"
                ],
                "complexity": "Low",
                "pci_required": False,
                "frontend_work": "Minimal",
                "customization": "Limited"
            },
            "pure_api_mode": {
                "name": "Pure API Mode",
                "description": "Direct API integration with full control",
                "best_for": [
                    "Full control over payment UI/UX",
                    "Custom payment flows",
                    "Mobile app integration",
                    "Advanced customization needs"
                ],
                "complexity": "High",
                "pci_required": True,
                "frontend_work": "Extensive",
                "customization": "Full"
            },
            "drop_in_mode": {
                "name": "Drop-in Component Mode",
                "description": "Embedded payment component",
                "best_for": [
                    "Balance between control and ease",
                    "Custom UI with pre-built components",
                    "No PCI DSS compliance required",
                    "Saved card functionality"
                ],
                "complexity": "Medium",
                "pci_required": False,
                "frontend_work": "Moderate",
                "customization": "Moderate"
            },
            "payment_link_mode": {
                "name": "Payment Link Mode",
                "description": "Share payment links with customers",
                "best_for": [
                    "No website/app required",
                    "Quick payment collection",
                    "Social media/email payments",
                    "Invoice payments"
                ],
                "complexity": "Very Low",
                "pci_required": False,
                "frontend_work": "None",
                "customization": "Minimal"
            }
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
        Call AWS Bedrock Nova model for intelligent analysis.
        
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
                    "temperature": 0.2,
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
    
    def analyze_requirements(self, user_description: str) -> Dict[str, Any]:
        """
        Analyze user description and recommend integration method.
        
        Args:
            user_description: Natural language description of integration requirements
        
        Returns:
            Dictionary containing:
            - extracted_specs: Key specifications extracted from description
            - recommended_method: Best integration method
            - reasoning: Why this method was recommended
            - integration_guide: Step-by-step integration instructions
            - required_apis: List of APIs needed
            - considerations: Important points to consider
        """
        if not self.bedrock_runtime:
            return self._fallback_analysis(user_description)
        
        # Step 1: Extract specifications using LLM
        extracted_specs = self._extract_specifications(user_description)
        
        if not extracted_specs:
            return self._fallback_analysis(user_description)
        
        # Step 2: Determine best integration method
        recommended_method = self._determine_integration_method(
            user_description,
            extracted_specs
        )
        
        if not recommended_method:
            return self._fallback_analysis(user_description)
        
        # Step 3: Load integration guide for recommended method
        integration_guide = self._load_integration_guide(
            recommended_method["method_key"]
        )
        
        # Step 4: Get required APIs
        required_apis = self._get_required_apis(
            recommended_method["method_key"]
        )
        
        return {
            "user_description": user_description,
            "extracted_specifications": extracted_specs,
            "recommended_method": {
                "method": recommended_method["method_key"],
                "name": recommended_method["method_name"],
                "description": recommended_method["description"],
                "complexity": recommended_method["complexity"]
            },
            "reasoning": recommended_method["reasoning"],
            "integration_guide": integration_guide,
            "required_apis": required_apis,
            "considerations": recommended_method["considerations"],
            "next_steps": recommended_method["next_steps"],
            "llm_powered": True
        }
    
    def _extract_specifications(self, user_description: str) -> Optional[Dict[str, Any]]:
        """
        Extract key specifications from user description using LLM.
        
        Returns:
            Dictionary with extracted specifications or None
        """
        prompt = f"""Analyze the following user description of their payment integration requirements and extract key specifications.

User Description:
{user_description}

Extract and categorize the following information:
1. Payment methods needed (card, wallet, bank transfer, etc.)
2. Integration constraints (PCI compliance, development resources, timeline)
3. Required features (saved cards, subscriptions, refunds, etc.)
4. Technical environment (web, mobile app, backend only, etc.)
5. Customization needs (UI/UX control, branding, etc.)
6. Business requirements (transaction volume, markets, etc.)

Respond in JSON format:
{{
    "payment_methods": ["list of payment methods"],
    "constraints": {{
        "pci_compliance": true/false,
        "development_resources": "limited/moderate/extensive",
        "timeline": "urgent/normal/flexible"
    }},
    "required_features": ["list of features"],
    "technical_environment": ["web/mobile/backend"],
    "customization_level": "minimal/moderate/full",
    "business_context": "brief summary",
    "key_priorities": ["list of top priorities"]
}}"""
        
        llm_response = self.call_nova_model(prompt, max_tokens=1500)
        
        if llm_response:
            try:
                # Parse LLM response
                llm_response = llm_response.strip()
                if llm_response.startswith("```"):
                    llm_response = llm_response.split("```")[1]
                    if llm_response.startswith("json"):
                        llm_response = llm_response[4:]
                llm_response = llm_response.strip()
                
                return json.loads(llm_response)
            except json.JSONDecodeError as e:
                print(f"Error parsing specification extraction: {e}")
        
        return None
    
    def _determine_integration_method(
        self,
        user_description: str,
        extracted_specs: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Determine the best integration method based on specifications.
        
        Returns:
            Dictionary with recommended method details or None
        """
        # Build method descriptions for LLM
        methods_desc = "\n\n".join([
            f"Method: {key}\n"
            f"Name: {info['name']}\n"
            f"Description: {info['description']}\n"
            f"Best for: {', '.join(info['best_for'])}\n"
            f"Complexity: {info['complexity']}\n"
            f"PCI Required: {info['pci_required']}\n"
            f"Frontend Work: {info['frontend_work']}\n"
            f"Customization: {info['customization']}"
            for key, info in self.integration_methods.items()
        ])
        
        prompt = f"""You are a PayerMax integration expert. Based on the user's requirements and extracted specifications, recommend the BEST integration method.

User Description:
{user_description}

Extracted Specifications:
{json.dumps(extracted_specs, indent=2)}

Available Integration Methods:
{methods_desc}

Instructions:
1. Analyze the user's requirements and constraints
2. Match them against each integration method's characteristics
3. Select the SINGLE best method
4. Provide clear reasoning
5. List important considerations
6. Suggest next steps

Respond in JSON format:
{{
    "recommended_method": "method_key",
    "reasoning": "detailed explanation of why this method is best",
    "considerations": ["important points to consider"],
    "next_steps": ["ordered list of next steps"],
    "alternative_methods": ["other viable options if any"]
}}"""
        
        llm_response = self.call_nova_model(prompt, max_tokens=2000)
        
        if llm_response:
            try:
                # Parse LLM response
                llm_response = llm_response.strip()
                if llm_response.startswith("```"):
                    llm_response = llm_response.split("```")[1]
                    if llm_response.startswith("json"):
                        llm_response = llm_response[4:]
                llm_response = llm_response.strip()
                
                recommendation = json.loads(llm_response)
                method_key = recommendation.get("recommended_method")
                
                if method_key in self.integration_methods:
                    method_info = self.integration_methods[method_key]
                    
                    return {
                        "method_key": method_key,
                        "method_name": method_info["name"],
                        "description": method_info["description"],
                        "complexity": method_info["complexity"],
                        "reasoning": recommendation.get("reasoning", ""),
                        "considerations": recommendation.get("considerations", []),
                        "next_steps": recommendation.get("next_steps", []),
                        "alternative_methods": recommendation.get("alternative_methods", [])
                    }
            except json.JSONDecodeError as e:
                print(f"Error parsing method recommendation: {e}")
        
        return None
    
    def _load_integration_guide(self, method_key: str) -> Dict[str, Any]:
        """
        Load integration guide documents for the recommended method.
        
        Args:
            method_key: Integration method key
        
        Returns:
            Dictionary with guide content
        """
        # Map method keys to document paths
        method_docs = {
            "cashier_mode": [
                "integration_process/收银台支付/收银台支付集成概览.md",
                "integration_process/收银台支付/收银台支付集成.md",
                "integration_process/收银台支付/收银台支付流程.md"
            ],
            "pure_api_mode": [
                "integration_process/纯API模式/纯API支付集成.md"
            ],
            "drop_in_mode": [
                "integration_process/开发者工具/卡支付前端接口.md"
            ],
            "payment_link_mode": [
                "integration_process/链接支付/链接支付集成.md"
            ]
        }
        
        doc_paths = method_docs.get(method_key, [])
        guide_content = {}
        
        for doc_path in doc_paths:
            content = self.read_file_safe(self.base_path / doc_path)
            if content:
                guide_content[doc_path] = content
        
        return {
            "documents": guide_content,
            "document_paths": doc_paths
        }
    
    def _get_required_apis(self, method_key: str) -> list:
        """
        Get list of required APIs for the integration method.
        
        Args:
            method_key: Integration method key
        
        Returns:
            List of required API names
        """
        # Map method keys to required APIs
        method_apis = {
            "cashier_mode": [
                "收银台-下单",
                "交易查询",
                "支付结果通知",
                "页面回跳"
            ],
            "pure_api_mode": [
                "纯API支付",
                "交易查询",
                "支付确认",
                "支付结果通知"
            ],
            "drop_in_mode": [
                "Apply Drop-in Session",
                "前置组件支付",
                "交易查询",
                "支付结果通知"
            ],
            "payment_link_mode": [
                "创建链接",
                "查询链接详情",
                "失效支付链接",
                "支付链接更新回调"
            ]
        }
        
        return method_apis.get(method_key, [])
    
    def _fallback_analysis(self, user_description: str) -> Dict[str, Any]:
        """
        Fallback analysis when LLM is not available.
        
        Returns:
            Dictionary with basic recommendation
        """
        # Simple keyword-based recommendation
        description_lower = user_description.lower()
        
        if any(word in description_lower for word in ["quick", "simple", "easy", "fast"]):
            method_key = "cashier_mode"
        elif any(word in description_lower for word in ["custom", "control", "mobile app"]):
            method_key = "pure_api_mode"
        elif any(word in description_lower for word in ["component", "embed", "moderate"]):
            method_key = "drop_in_mode"
        elif any(word in description_lower for word in ["link", "share", "email", "social"]):
            method_key = "payment_link_mode"
        else:
            method_key = "cashier_mode"  # Default to easiest option
        
        method_info = self.integration_methods[method_key]
        integration_guide = self._load_integration_guide(method_key)
        required_apis = self._get_required_apis(method_key)
        
        return {
            "user_description": user_description,
            "extracted_specifications": {
                "note": "LLM not available, using keyword-based analysis"
            },
            "recommended_method": {
                "method": method_key,
                "name": method_info["name"],
                "description": method_info["description"],
                "complexity": method_info["complexity"]
            },
            "reasoning": f"Based on keyword analysis, {method_info['name']} appears to be a good fit.",
            "integration_guide": integration_guide,
            "required_apis": required_apis,
            "considerations": method_info["best_for"],
            "next_steps": [
                "Review the integration guide",
                "Set up development environment",
                "Obtain API credentials",
                "Implement required APIs"
            ],
            "llm_powered": False
        }
