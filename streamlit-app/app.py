import streamlit as st
import requests
import json
import time
import pandas as pd
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Hero Making Auditor",
    page_icon="🦸‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .customer-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .confidence-high { color: #28a745; font-weight: bold; }
    .confidence-medium { color: #ffc107; font-weight: bold; }
    .confidence-low { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

class HeroCustomerAPI:
    """API client for hero customer discovery"""
    
    def __init__(self):
        self.base_url = "https://api.apify.com/v2"
        
    def discover_customers_web_scraper(self, company_name, company_website, apify_token):
        """Use Apify Web Scraper for customer discovery"""
        
        # Configure web scraper for customer discovery
        page_function = f'''
async function pageFunction(context) {{
    const $ = context.jQuery;
    const url = context.request.url;
    
    console.log(`Processing: ${{url}}`);
    
    const customers = [];
    
    // Method 1: Look for customer sections
    const customerSections = $('[class*="customer"], [class*="client"], [class*="testimonial"], [class*="case"], [class*="logo"]');
    
    customerSections.each((i, element) => {{
        const $element = $(element);
        const text = $element.text().trim();
        
        // Extract company names
        const companyPattern = /\\b([A-Z][a-zA-Z\\s&.,-]{{2,40}}(?:\\s(?:Inc|LLC|Corp|Company|Ltd))?)\\b/g;
        let match;
        
        while ((match = companyPattern.exec(text)) !== null) {{
            const customerName = match[1].trim();
            
            if (customerName.length > 2 && 
                customerName.length < 50 && 
                !customerName.toLowerCase().includes("{company_name.lower()}")) {{
                
                customers.push({{
                    name: customerName,
                    source: url,
                    context: text.substring(0, 200),
                    confidence: calculateConfidence(text, customerName),
                    discoveredAt: new Date().toISOString(),
                    extractionMethod: "web_scraper"
                }});
            }}
        }}
    }});
    
    // Method 2: Look for testimonials
    const testimonials = $('blockquote, [class*="testimonial"], [class*="quote"]');
    testimonials.each((i, element) => {{
        const $element = $(element);
        const text = $element.text().trim();
        const author = $element.find('[class*="author"], [class*="name"], cite').text().trim();
        
        if (author) {{
            const companyMatch = author.match(/,\\s*(.+?)$/);
            if (companyMatch) {{
                const companyName = companyMatch[1].trim();
                if (companyName.length > 2 && !companyName.toLowerCase().includes("{company_name.lower()}")) {{
                    customers.push({{
                        name: companyName,
                        source: url,
                        context: text.substring(0, 200),
                        author: author,
                        confidence: calculateConfidence(text, companyName),
                        discoveredAt: new Date().toISOString(),
                        extractionMethod: "testimonial"
                    }});
                }}
            }}
        }}
    }});
    
    function calculateConfidence(text, customerName) {{
        let confidence = 0.5;
        
        const positiveKeywords = ['customer', 'client', 'testimonial', 'case study', 'success'];
        positiveKeywords.forEach(keyword => {{
            if (text.toLowerCase().includes(keyword)) {{
                confidence += 0.1;
            }}
        }});
        
        if (/\\b(Inc|LLC|Corp|Company|Ltd)\\b/.test(customerName)) {{
            confidence += 0.1;
        }}
        
        return Math.min(confidence, 0.99);
    }}
    
    console.log(`Found ${{customers.length}} customers on ${{url}}`);
    
    return {{
        url: url,
        companyName: "{company_name}",
        customersFound: customers.length,
        customers: customers,
        timestamp: new Date().toISOString()
    }};
}}
'''
        
        # Configure start URLs for customer discovery
        start_urls = []
        if company_website:
            base_url = company_website.rstrip('/')
            start_urls = [
                {"url": f"{base_url}/customers"},
                {"url": f"{base_url}/case-studies"},
                {"url": f"{base_url}/testimonials"},
                {"url": f"{base_url}/success-stories"},
                {"url": f"{base_url}/clients"}
            ]
        
        # Web scraper configuration
        run_input = {
            "startUrls": start_urls,
            "pageFunction": page_function,
            "maxPagesPerCrawl": 10,
            "maxConcurrency": 2,
            "pageLoadTimeoutSecs": 30,
            "injectJQuery": True,
            "proxyConfiguration": {"useApifyProxy": True}
        }
        
        # Run the web scraper
        headers = {
            "Authorization": f"Bearer {apify_token}",
            "Content-Type": "application/json"
        }
        
        try:
            # Start actor run
            response = requests.post(
                f"{self.base_url}/acts/apify~web-scraper/runs",
                headers=headers,
                json=run_input,
                timeout=10
            )
            
            if response.status_code != 201:
                return {"error": f"Failed to start actor: {response.text}"}
            
            run_data = response.json()["data"]
            run_id = run_data["id"]
            
            return {"run_id": run_id, "status": "started"}
            
        except Exception as e:
            return {"error": f"API error: {str(e)}"}
    
    def get_run_status(self, run_id, apify_token):
        """Get status of actor run"""
        headers = {"Authorization": f"Bearer {apify_token}"}
        
        try:
            response = requests.get(
                f"{self.base_url}/actor-runs/{run_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()["data"]
            else:
                return {"error": "Failed to get run status"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def get_run_results(self, run_id, apify_token):
        """Get results from completed run"""
        headers = {"Authorization": f"Bearer {apify_token}"}
        
        try:
            response = requests.get(
                f"{self.base_url}/actor-runs/{run_id}/dataset/items",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Failed to get results"}
                
        except Exception as e:
            return {"error": str(e)}

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🦸‍♂️ Hero Making Auditor</h1>
        <h3>Universal B2B Brand Intelligence Platform</h3>
        <p>Discover, analyze, and leverage your hero customers for maximum business impact</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Token input
        apify_token = st.text_input(
            "Apify API Token",
            type="password",
            help="Get your token from https://console.apify.com/account#/integrations"
        )
        
        if not apify_token:
            st.warning("⚠️ Please enter your Apify API token to continue")
            st.info("💡 Don't have an Apify account? Sign up at https://apify.com")
            st.stop()
        
        st.success("✅ API token configured")
        
        # Pricing info
        st.header("💰 Pricing")
        st.info("""
        **Free tier includes:**
        - 10 customer discoveries/month
        - Basic reports
        
        **Pro tier ($29/month):**
        - Unlimited discoveries
        - Advanced analytics
        - Priority support
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Company Analysis")
        
        # Input form
        with st.form("customer_discovery_form"):
            company_name = st.text_input(
                "Company Name *",
                placeholder="e.g., Shopify, HubSpot, Salesforce"
            )
            
            company_website = st.text_input(
                "Company Website *",
                placeholder="https://example.com"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                max_results = st.slider("Max Results", 5, 50, 20)
            with col_b:
                include_testimonials = st.checkbox("Include Testimonials", True)
            
            submitted = st.form_submit_button("🚀 Discover Hero Customers", type="primary")
        
        if submitted and company_name and company_website:
            # Initialize API client
            api = HeroCustomerAPI()
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Start customer discovery
                status_text.text("🚀 Starting customer discovery...")
                progress_bar.progress(20)
                
                result = api.discover_customers_web_scraper(
                    company_name, company_website, apify_token
                )
                
                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                    st.stop()
                
                run_id = result["run_id"]
                status_text.text("⏳ Processing customer data...")
                progress_bar.progress(40)
                
                # Wait for completion
                max_wait = 120  # 2 minutes max
                wait_time = 0
                
                while wait_time < max_wait:
                    time.sleep(5)
                    wait_time += 5
                    progress_bar.progress(40 + (wait_time / max_wait) * 40)
                    
                    status = api.get_run_status(run_id, apify_token)
                    
                    if isinstance(status, dict) and status.get("status") == "SUCCEEDED":
                        break
                    elif isinstance(status, dict) and status.get("status") in ["FAILED", "ABORTED", "TIMED-OUT"]:
                        st.error(f"❌ Run failed with status: {status.get('status')}")
                        st.stop()
                
                # Get results
                status_text.text("📊 Retrieving results...")
                progress_bar.progress(90)
                
                results = api.get_run_results(run_id, apify_token)
                
                if "error" in results:
                    st.error(f"❌ Error getting results: {results['error']}")
                    st.stop()
                
                progress_bar.progress(100)
                status_text.text("✅ Discovery complete!")
                
                # Process and display results
                all_customers = []
                for item in results:
                    if isinstance(item, dict) and "customers" in item:
                        all_customers.extend(item["customers"])
                
                if all_customers:
                    # Remove duplicates
                    seen = {}
                    unique_customers = []
                    for customer in all_customers:
                        key = customer['name'].lower().strip()
                        if key not in seen or customer['confidence'] > seen[key]['confidence']:
                            seen[key] = customer
                            unique_customers.append(customer)
                    
                    # Sort by confidence
                    unique_customers.sort(key=lambda x: x['confidence'], reverse=True)
                    final_customers = unique_customers[:max_results]
                    
                    # Display results
                    st.success(f"🎉 Found {len(final_customers)} hero customers!")
                    
                    # Summary metrics
                    st.header("📊 Discovery Summary")
                    
                    col_1, col_2, col_3, col_4 = st.columns(4)
                    
                    with col_1:
                        st.metric("Total Customers", len(final_customers))
                    
                    with col_2:
                        avg_confidence = sum(c['confidence'] for c in final_customers) / len(final_customers)
                        st.metric("Avg Confidence", f"{avg_confidence:.3f}")
                    
                    with col_3:
                        high_conf = len([c for c in final_customers if c['confidence'] > 0.8])
                        st.metric("High Confidence", high_conf)
                    
                    with col_4:
                        sources = len(set(c['source'] for c in final_customers))
                        st.metric("Sources Found", sources)
                    
                    # Customer list
                    st.header("🦸‍♂️ Discovered Hero Customers")
                    
                    for i, customer in enumerate(final_customers, 1):
                        confidence_class = "confidence-high" if customer['confidence'] > 0.8 else "confidence-medium" if customer['confidence'] > 0.6 else "confidence-low"
                        
                        st.markdown(f"""
                        <div class="customer-card">
                            <h4>{i}. {customer['name']} <span class="{confidence_class}">({customer['confidence']:.3f})</span></h4>
                            <p><strong>Source:</strong> {customer['source']}</p>
                            <p><strong>Context:</strong> {customer['context'][:150]}...</p>
                            <p><strong>Method:</strong> {customer.get('extractionMethod', 'unknown')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Download results
                    st.header("📥 Export Results")
                    
                    # Prepare data for download
                    df = pd.DataFrame(final_customers)
                    csv = df.to_csv(index=False)
                    json_data = json.dumps(final_customers, indent=2)
                    
                    col_dl1, col_dl2 = st.columns(2)
                    
                    with col_dl1:
                        st.download_button(
                            "📊 Download CSV",
                            csv,
                            file_name=f"hero_customers_{company_name.lower().replace(' ', '_')}.csv",
                            mime="text/csv"
                        )
                    
                    with col_dl2:
                        st.download_button(
                            "📋 Download JSON",
                            json_data,
                            file_name=f"hero_customers_{company_name.lower().replace(' ', '_')}.json",
                            mime="application/json"
                        )
                
                else:
                    st.warning("⚠️ No customers found. Try adjusting your search parameters or check if the company website has customer pages.")
                    
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
        
        elif submitted:
            st.error("❌ Please fill in all required fields")
    
    with col2:
        st.header("📈 Recent Analyses")
        
        # Sample recent analyses (in production, this would come from a database)
        recent_analyses = [
            {"company": "Shopify", "customers": 23, "date": "2025-06-24"},
            {"company": "HubSpot", "customers": 18, "date": "2025-06-23"},
            {"company": "Salesforce", "customers": 31, "date": "2025-06-23"}
        ]
        
        for analysis in recent_analyses:
            st.markdown(f"""
            <div class="metric-card">
                <strong>{analysis['company']}</strong><br>
                {analysis['customers']} customers found<br>
                <small>{analysis['date']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.header("🎯 How It Works")
        st.info("""
        1. **Enter company details**
        2. **AI scans** customer pages, case studies, testimonials
        3. **Extracts** customer names with confidence scores
        4. **Generates** actionable customer intelligence
        5. **Export** results for your sales/marketing team
        """)
        
        st.header("💡 Use Cases")
        st.markdown("""
        - **Sales prospecting**
        - **Competitive analysis** 
        - **Market research**
        - **Customer acquisition**
        - **Partnership identification**
        """)

if __name__ == "__main__":
    main()