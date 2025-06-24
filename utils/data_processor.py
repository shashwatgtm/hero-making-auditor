import pandas as pd

class DataProcessor:
    def __init__(self):
        pass
        
    def process_customers(self, customers_data):
        """Process raw customer data"""
        if not customers_data:
            return pd.DataFrame()
            
        df = pd.DataFrame(customers_data)
        
        # Clean and enhance data
        if "confidence" in df.columns:
            df["confidence"] = df["confidence"].round(3)
            
        if "discoveredAt" in df.columns:
            df["discoveredAt"] = pd.to_datetime(df["discoveredAt"])
            
        return df
        
    def generate_summary(self, customers_data):
        """Generate summary statistics"""
        if not customers_data:
            return {}
            
        df = pd.DataFrame(customers_data)
        
        return {
            "total_customers": len(df),
            "avg_confidence": df["confidence"].mean() if "confidence" in df.columns else 0,
            "high_confidence_count": len(df[df["confidence"] > 0.8]) if "confidence" in df.columns else 0
        }