## Context manager - managed API client ##
'''
Real scenario: every agentic AI system talks to external APIs — LLMs, 
vector DBs, tool endpoints. 
You need a client that opens a connection on entry, 
guarantees cleanup on exit (even if an exception occurs mid-run), 
and optionally retries on failure. This pattern is everywhere in LangChain, 
LlamaIndex, and custom agent frameworks.
'''

import requests
import time

class ManagedClient:
    def __init__(self, base_url, retries):
        self.base_url = base_url
        self.retries = retries
        self.session = None

    def __enter__(self):
        self.session = requests.Session()
        return self  

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        return False  
        
    def get(self, endpoint):
        for attempt in range(self.retries):
            try:
                response = self.session.get(self.base_url + endpoint)
                return response
            except requests.exceptions.ConnectionError:
                if attempt == self.retries - 1:
                    raise
                time.sleep(1)
