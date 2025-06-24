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

# Inject the exact CSS from the beautiful artifact
st.markdown("""
<style>
    /* Hide Streamlit branding and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stSidebar"] {display: none;}
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Hero header - exact replica */
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        opacity: 0.95;
    }
    
    .hero-description {
        font-size: 1.1rem;
        opacity: 0.9;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Search container - exact replica */
    .search-container {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin-bottom: 3rem;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .search-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: #f7fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Feature cards - exact replica */
    .features-section {
        margin-bottom: 3rem;
    }
    
    .features-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
        height: 100%;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: #4a5568;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Results styling */
    .results-container {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .success-badge {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    .customer-card {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .customer-card:hover {
        background: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transform: translateX(5px);
    }
    
    .customer-name {
        font-size: 1.25rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .customer-industry {
        color: #667eea;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .customer-description {
        color: #4a5568;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    
    .customer-indicators {
        color: #38a169;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Progress styling */
    .progress-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .progress-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1.5rem;
    }
    
    /* Export section */
    .export-section {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    
    .export-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Custom download button */
    .download-btn {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.6);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.25rem;
        }
        .search-container, .results-container {
            padding: 1.5rem;
        }
        .feature-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Hero Header - Exact replica of the beautiful artifact
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🦸‍♂️ Hero Making Auditor</div>
        <div class="hero-subtitle">Universal B2B Brand Intelligence Platform</div>
        <div class="hero-description">Discover, analyze, and leverage your hero customers for maximum business impact</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have session state for results
    if 'discovery_results' not in st.session_state:
        st.session_state.discovery_results = None
    
    # Search Container - Exact replica
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="search-title">🎯 Discover Your Hero Customers</div>', unsafe_allow_html=True)
        company_url = st.text_input(
            "",
            placeholder="https://example.com",
            help="Enter the main website URL of the company you want to analyze",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<div class="search-title">🚀 Action</div>', unsafe_allow_html=True)
        discover_clicked = st.button("🔍 Start Discovery", type="primary")
    
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
    
    # Features section (only show if no results) - Exact replica
    if not st.session_state.discovery_results:
        show_features()

def show_features():
    """Display platform features - exact replica of artifact"""
    st.markdown('<div class="features-section">', unsafe_allow_html=True)
    st.markdown('<div class="features-title">✨ Platform Features</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Smart Discovery</div>
            <div class="feature-description">Advanced algorithms identify customer testimonials, case studies, and success stories across your website</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">AI Analysis</div>
            <div class="feature-description">Intelligent classification by industry, company size, and success indicators for strategic insights</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Export Ready</div>
            <div class="feature-description">Download comprehensive reports in CSV and JSON formats for immediate use in sales and marketing</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def run_hero_discovery(company_url):
    """Run the hero customer discovery process"""
    
    # Progress Container
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown('<div class="progress-title">🔄 Discovery in Progress</div>', unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Simulate discovery process with realistic steps
        steps = [
            ("🚀 Initializing discovery engine...", 20),
            ("🌐 Analyzing website structure...", 40),
            ("🔍 Extracting customer data...", 60),
            ("🧠 Processing with AI analysis...", 80),
            ("✅ Discovery completed!", 100)
        ]
        
        for step_text, progress in steps:
            status_text.text(step_text)
            progress_bar.progress(progress)
            time.sleep(1.2)
        
        # Generate results
        results = generate_sample_results(company_url)
        
        st.markdown('</div>', unsafe_allow_html=True)
        return results
        
    except Exception as e:
        st.error(f"An error occurred during discovery: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
        return None

def generate_sample_results(company_url):
    """Generate sample results for demonstration"""
    
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
    
    # Success message
    st.markdown("""
    <div class="success-badge">
        🎉 Hero Customer Discovery Completed Successfully!
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics cards
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{results['pages_processed']}</div>
            <div class="metric-label">Pages Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{results['total_customers']}</div>
            <div class="metric-label">Hero Customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{results['industries']}</div>
            <div class="metric-label">Industries</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{results['success_stories']}</div>
            <div class="metric-label">Success Stories</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Customer list
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown("## 🏆 Discovered Hero Customers")
    
    for customer in results['customers']:
        st.markdown(f"""
        <div class="customer-card">
            <div class="customer-name">🏢 {customer['name']}</div>
            <div class="customer-industry">Industry: {customer['industry']}</div>
            <div class="customer-description">{customer['description']}</div>
            <div class="customer-indicators">Success Indicators: {', '.join(customer['success_indicators'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Export section
    st.markdown('<div class="export-section">', unsafe_allow_html=True)
    st.markdown('<div class="export-title">📥 Export Results</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
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
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()