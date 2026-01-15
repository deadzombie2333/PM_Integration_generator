#!/usr/bin/env python3
"""
Wrapper script to run the parallel document embedder with proper environment setup
"""
import os
import sys
from pathlib import Path

# Set environment variables for us-west-2 OpenSearch
os.environ['OPENSEARCH_ENDPOINT'] = 'dy9xqlp8blzu7vpd4d30.us-west-2.aoss.amazonaws.com'
os.environ['AWS_REGION'] = 'us-west-2'
os.environ['TOOL_3_INDEX'] = 'payermax-api-docs'
os.environ['TOOL_4_INDEX'] = 'payermax-integration-guides'

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the parallel embedder
from document_embedder.parallel_embedder import main

if __name__ == "__main__":
    main()
