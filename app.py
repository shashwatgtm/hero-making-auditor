import streamlit as st
import streamlit.components.v1 as components

# Set page config
st.set_page_config(
    page_title="Hero Making Brand Audit",
    page_icon="🦸‍♂️",
    layout="wide"
)

# Hide Streamlit default elements
st.markdown("""
<style>
    .reportview-container .main .block-container {
        padding-top: 0rem;
        padding-right: 0rem;
        padding-left: 0rem;
        padding-bottom: 0rem;
    }
    
    .reportview-container .main {
        padding: 0rem;
    }
    
    header[data-testid="stHeader"] {
        display: none;
    }
    
    div[data-testid="stToolbar"] {
        display: none;
    }
    
    div[data-testid="stDecoration"] {
        display: none;
    }
    
    footer {
        display: none;
    }
    
    #MainMenu {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Read the HTML file
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Display the HTML (full viewport)
    components.html(html_content, height=800, scrolling=True)
    
except FileNotFoundError:
    st.error("index.html file not found. Please make sure it's in the same directory as app.py")