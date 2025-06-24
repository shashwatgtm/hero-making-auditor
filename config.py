import os
from pathlib import Path

# Configuration settings for the Hero Making Auditor
class Config:
    APIFY_TOKEN = os.getenv("APIFY_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Actor IDs (update these with your actual actor IDs)
    CUSTOMER_DISCOVERY_ACTOR = "your-username/hero-customer-discovery"
    LINKEDIN_ANALYZER_ACTOR = "your-username/hero-linkedin-analyzer"
    CONTENT_ANALYZER_ACTOR = "your-username/hero-content-analyzer"
    SIGNAL_DETECTOR_ACTOR = "your-username/hero-signal-detector"
    REPORT_GENERATOR_ACTOR = "your-username/hero-report-generator"
    
    # Application settings
    MAX_CONCURRENT_ACTORS = 3
    DEFAULT_TIMEOUT = 300  # 5 minutes
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.APIFY_TOKEN:
            raise ValueError("APIFY_TOKEN environment variable is required")
        return True