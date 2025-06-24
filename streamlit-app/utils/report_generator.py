import json

class ReportGenerator:
    def __init__(self):
        pass
        
    def generate_report(self, data):
        """Generate HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hero Customer Report - {data.get('companyName', 'Unknown')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .customer {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
                .confidence {{ font-weight: bold; color: #007bff; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Hero Customer Report</h1>
                <h2>{data.get('companyName', 'Unknown Company')}</h2>
                <p>Generated: {data.get('timestamp', 'Unknown')}</p>
                <p>Total Customers Found: {len(data.get('customers', []))}</p>
            </div>
            
            <div class="customers">
                <h3>Discovered Hero Customers</h3>
        """
        
        for customer in data.get('customers', []):
            html += f"""
                <div class="customer">
                    <h4>{customer.get('name', 'Unknown')}</h4>
                    <p><span class="confidence">Confidence: {customer.get('confidence', 0):.3f}</span></p>
                    <p>Source: {customer.get('source', 'Unknown')}</p>
                    <p>Context: {customer.get('context', 'No context available')[:200]}...</p>
                </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html