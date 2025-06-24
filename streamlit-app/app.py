import streamlit as st
import pandas as pd
from utils.apify_client import ApifyClient
from utils.data_processor import DataProcessor
from utils.report_generator import ReportGenerator

st.set_page_config(
    page_title="Hero Making Auditor",
    page_icon="🦸‍♂️",
    layout="wide"
)

def main():
    st.title("Hero Making Auditor")
    st.subheader("Universal B2B Brand Intelligence Platform")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    apify_token = st.sidebar.text_input("Apify API Token", type="password")
    
    if not apify_token:
        st.warning("Please enter your Apify API token in the sidebar.")
        return
    
    # Initialize clients
    apify_client = ApifyClient(apify_token)
    data_processor = DataProcessor()
    report_generator = ReportGenerator()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Company Analysis")
        company_name = st.text_input("Company Name")
        company_website = st.text_input("Company Website")
        
        if st.button("Discover Hero Customers", type="primary"):
            if company_name:
                with st.spinner("Discovering hero customers..."):
                    try:
                        # Run customer discovery actor
                        result = apify_client.run_customer_discovery({
                            "companyName": company_name,
                            "companyWebsite": company_website,
                            "maxResults": 50
                        })
                        
                        if result and result.get("customers"):
                            st.success(f"Found {len(result['customers'])} hero customers!")
                            
                            # Display results
                            customers_df = pd.DataFrame(result["customers"])
                            st.dataframe(customers_df)
                            
                            # Generate report
                            report = report_generator.generate_report(result)
                            st.download_button(
                                "Download Report",
                                report,
                                file_name=f"{company_name}_hero_customers.html",
                                mime="text/html"
                            )
                        else:
                            st.error("No customers found or actor failed.")
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.error("Please enter a company name.")
    
    with col2:
        st.header("Recent Analyses")
        st.info("Analysis history will appear here.")

if __name__ == "__main__":
    main()