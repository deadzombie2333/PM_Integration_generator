#!/usr/bin/env python3
"""
Wrapper script to run the document embedder with proper environment setup
"""
import os
import sys
from pathlib import Path

# Set environment variables for us-west-2 OpenSearch
os.environ['OPENSEARCH_ENDPOINT'] = 'o9kek6fj2tk5hgs2b3z4.us-west-2.aoss.amazonaws.com'
os.environ['AWS_REGION'] = 'us-west-2'
os.environ['TOOL_3_INDEX'] = 'payermax-api-docs'
os.environ['TOOL_4_INDEX'] = 'payermax-integration-guides'

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the embedder
from document_embedder.document_embedder import main

if __name__ == "__main__":
    main()
