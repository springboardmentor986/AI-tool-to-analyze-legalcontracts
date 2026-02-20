import streamlit as st
from streamlit_lottie import st_lottie
import requests
import urllib3

# Suppress SSL warnings due to corporate proxies
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_lottie_url(url: str):
    """
    Loads a Lottie animation from a URL.
    """
    try:
        r = requests.get(url, verify=False)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def display_lottie(url: str, height: int = 300, key: str = "lottie"):
    """
    Displays a Lottie animation.
    """
    lottie_json = load_lottie_url(url)
    if lottie_json:
        st_lottie(lottie_json, height=height, key=key)
    else:
        st.error("Failed to load animation.")

def inject_custom_css():
    """
    Injects additional CSS for animations not covered in style.css.
    """
    st.markdown("""
    <style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translate3d(0, 40px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }
    
    .animate-enter {
        animation-name: fadeInUp;
        animation-duration: 0.8s;
        animation-fill-mode: both;
    }
    
    .stMetric {
        animation: fadeInUp 0.5s ease-out backwards;
    }
    
    .stButton button:hover {
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)
