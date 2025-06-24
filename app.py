import streamlit as st
import streamlit.components.v1 as components

# Set page config
st.set_page_config(
    page_title="Hero Making Brand Audit",
    page_icon="🦸‍♂️",
    layout="wide"
)

# Read the HTML file
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Display the HTML (full height)
    components.html(html_content, height=3000, scrolling=True)
    
except FileNotFoundError:
    st.error("index.html file not found. Please make sure it's in the same directory as app.py")