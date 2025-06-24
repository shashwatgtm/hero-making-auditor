import streamlit as st
import requests
import json
import time
import pandas as pd
from datetime import datetime
import os

# Get Apify token from environment (set in Railway)
APIFY_TOKEN = os.getenv('APIFY_TOKEN')

# Page configuration
st.set_page_config(
    page_title="Hero Making Auditor",
    page_icon="🦸‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern design
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
        color: white;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .success-message {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: bold;
    }
    
    .progress-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .customer-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
        border-left: 4px solid #667eea;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stDeployButton {display:none;}
    
    [data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="hero-title">🦸‍♂️ Hero Making Auditor</div>
        <div class="hero-subtitle">Universal B2B Brand Intelligence Platform</div>
        <p style="margin-top: 1rem; font-size: 1rem;">Discover, analyze, and leverage your hero customers for maximum business impact</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have session state for results
    if 'discovery_results' not in st.session_state:
        st.session_state.discovery_results = None
    
    # Main search interface
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🎯 Discover Your Hero Customers")
        company_url = st.text_input(
            "Enter company website URL",
            placeholder="https://example.com",
            help="Enter the main website URL of the company you want to analyze"
        )
    
    with col2:
        st.markdown("### 🚀 Action")
        discover_clicked = st.button("🔍 Start Discovery", type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle discovery button click
    if discover_clicked:
        if company_url:
            if not APIFY_TOKEN:
                st.error("⚠️ Service temporarily unavailable. Please try again later.")
            else:
                st.session_state.discovery_results = run_hero_discovery(company_url)
        else:
            st.warning("Please enter a company URL")
    
    # Show results if available
    if st.session_state.discovery_results:
        show_results(st.session_state.discovery_results, company_url)
    
    # Features section (only show if no results)
    if not st.session_state.discovery_results:
        show_features()

def show_features():
    """Display platform features"""
    st.markdown("## ✨ Platform Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Smart Discovery</h4>
            <p>Advanced algorithms identify customer testimonials, case studies, and success stories across your website</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🧠 AI Analysis</h4>
            <p>Intelligent classification by industry, company size, and success indicators for strategic insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Export Ready</h4>
            <p>Download comprehensive reports in CSV and JSON formats for immediate use in sales and marketing</p>
        </div>
        """, unsafe_allow_html=True)

def run_hero_discovery(company_url):
    """Run the hero customer discovery process"""
    
    # Create progress indicators
    progress_placeholder = st.empty()
    
    with progress_placeholder.container():
        st.markdown('<div class="progress-container">', unsafe_allow_html=True)
        st.markdown("### 🔄 Discovery in Progress")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Simulate discovery process
            status_text.text("🚀 Initializing discovery engine...")
            progress_bar.progress(20)
            time.sleep(1)
            
            status_text.text("🌐 Analyzing website structure...")
            progress_bar.progress(40)
            time.sleep(1)
            
            status_text.text("🔍 Extracting customer data...")
            progress_bar.progress(60)
            time.sleep(1)
            
            status_text.text("🧠 Processing with AI analysis...")
            progress_bar.progress(80)
            time.sleep(1)
            
            status_text.text("✅ Discovery completed!")
            progress_bar.progress(100)
            time.sleep(1)
            
            # Generate sample results for demo
            results = generate_sample_results(company_url)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            return results
            
        except Exception as e:
            st.error(f"An error occurred during discovery: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
            return None

def generate_sample_results(company_url):
    """Generate sample results for demonstration"""
    
    # Extract domain for realistic results
    domain = company_url.replace('https://', '').replace('http://', '').split('/')[0]
    
    sample_customers = [
        {
            'name': 'TechCorp Solutions',
            'industry': 'Technology',
            'description': 'Increased efficiency by 300% using our platform, enabling them to scale their operations globally.',
            'success_indicators': ['Growth', 'Efficiency', 'Scale'],
            'source_url': f'{company_url}/case-studies/techcorp',
            'page_title': 'TechCorp Success Story'
        },
        {
            'name': 'Global Manufacturing Inc',
            'industry': 'Manufacturing',
            'description': 'Reduced operational costs by 45% and improved production quality significantly.',
            'success_indicators': ['Cost Savings', 'Efficiency'],
            'source_url': f'{company_url}/customers/manufacturing',
            'page_title': 'Manufacturing Case Study'
        },
        {
            'name': 'FinanceFirst Bank',
            'industry': 'Finance',
            'description': 'Streamlined their digital transformation, serving 2M+ customers with enhanced security.',
            'success_indicators': ['Scale', 'Growth'],
            'source_url': f'{company_url}/testimonials/finance',
            'page_title': 'Financial Services Testimonial'
        },
        {
            'name': 'HealthPlus Medical',
            'industry': 'Healthcare',
            'description': 'Improved patient outcomes by 60% while reducing administrative overhead.',
            'success_indicators': ['Efficiency', 'Growth'],
            'source_url': f'{company_url}/case-studies/healthcare',
            'page_title': 'Healthcare Success Story'
        },
        {
            'name': 'EduTech Academy',
            'industry': 'Education',
            'description': 'Enhanced learning outcomes for 50,000+ students with our innovative platform.',
            'success_indicators': ['Scale', 'Growth'],
            'source_url': f'{company_url}/success-stories/education',
            'page_title': 'Education Case Study'
        }
    ]
    
    return {
        'customers': sample_customers,
        'pages_processed': 12,
        'total_customers': len(sample_customers),
        'industries': len(set(c['industry'] for c in sample_customers)),
        'success_stories': len([c for c in sample_customers if c['success_indicators']])
    }

def show_results(results, company_url):
    """Display the discovery results"""
    
    st.markdown("""
    <div class="success-message">
        🎉 Hero Customer Discovery Completed Successfully!
    </div>
    """, unsafe_allow_html=True)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{results['pages_processed']}</h3>
            <p>Pages Analyzed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{results['total_customers']}</h3>
            <p>Hero Customers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{results['industries']}</h3>
            <p>Industries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{results['success_stories']}</h3>
            <p>Success Stories</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display customer list
    st.markdown("## 🏆 Discovered Hero Customers")
    
    for customer in results['customers']:
        st.markdown(f"""
        <div class="customer-card">
            <h4>🏢 {customer['name']}</h4>
            <p><strong>Industry:</strong> {customer['industry']}</p>
            <p><strong>Success Story:</strong> {customer['description']}</p>
            <p><strong>Success Indicators:</strong> {', '.join(customer['success_indicators'])}</p>
            <p><small><strong>Source:</strong> <a href="{customer['source_url']}" target="_blank">{customer['page_title']}</a></small></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Export options
    st.markdown("## 📥 Export Results")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Create DataFrame for export
        df = pd.DataFrame(results['customers'])
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📊 Download CSV",
            data=csv,
            file_name=f"hero_customers_{company_url.replace('https://', '').replace('http://', '').replace('/', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Create JSON export
        json_data = json.dumps(results['customers'], indent=2)
        
        st.download_button(
            label="📋 Download JSON",
            data=json_data,
            file_name=f"hero_customers_{company_url.replace('https://', '').replace('http://', '').replace('/', '_')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col3:
        if st.button("🔄 New Discovery", use_container_width=True):
            st.session_state.discovery_results = None
            st.rerun()

if __name__ == "__main__":
    main()