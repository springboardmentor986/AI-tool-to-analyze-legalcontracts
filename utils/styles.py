import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        /* 1. FONTS */
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');
        * { font-family: 'Space Grotesk', sans-serif !important; }

        /* 2. CUSTOM BUBBLE CURSOR */
        body {
            cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="10" fill="rgba(0, 242, 255, 0.5)" stroke="white" stroke-width="2"/></svg>') 16 16, auto;
        }

        /* 3. DARK NEBULA BACKGROUND */
        .stApp {
            background: radial-gradient(circle at 10% 20%, rgb(18, 5, 46) 0%, rgb(4, 4, 18) 90%);
            background-image: 
                radial-gradient(at 80% 0%, hsla(189,100%,56%,0.2) 0px, transparent 50%),
                radial-gradient(at 0% 50%, hsla(355,100%,93%,0.1) 0px, transparent 50%),
                radial-gradient(at 80% 50%, hsla(340,100%,76%,0.1) 0px, transparent 50%),
                radial-gradient(at 0% 100%, hsla(22,100%,77%,0.1) 0px, transparent 50%),
                radial-gradient(at 80% 100%, hsla(242,100%,70%,0.1) 0px, transparent 50%),
                radial-gradient(at 0% 0%, hsla(343,100%,76%,0.1) 0px, transparent 50%);
            background-size: 200% 200%;
            animation: aurora 20s ease infinite;
        }
        @keyframes aurora { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

        /* 4. DARK GLASS CARDS */
        .agent-card, .glass-panel, .stChatMessage {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            color: #e2e8f0 !important;
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
        }

        /* 5. NEON BORDERS */
        .border-gold   { border-left: 4px solid #fce38a; box-shadow: -5px 0 15px -5px rgba(252, 227, 138, 0.1); }
        .border-blue   { border-left: 4px solid #00f2ff; box-shadow: -5px 0 15px -5px rgba(0, 242, 255, 0.1); }
        .border-green  { border-left: 4px solid #00ff87; box-shadow: -5px 0 15px -5px rgba(0, 255, 135, 0.1); }
        .border-pink   { border-left: 4px solid #ff00cc; box-shadow: -5px 0 15px -5px rgba(255, 0, 204, 0.1); }

        /* 6. TYPOGRAPHY */
        h1, h2, h3 {
            background: linear-gradient(to right, #fff, #a5f3fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* 7. WIDGETS */
        div[data-testid="stFileUploader"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px dashed rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 30px;
        }
        .stDataFrame { margin-top: -20px; }

        /* 8. 3D CUBE ANIMATION */
        .cube-container { perspective: 800px; width: 50px; height: 50px; margin: 20px auto; }
        .cube { width: 100%; height: 100%; position: relative; transform-style: preserve-3d; animation: spin 8s infinite linear; }
        .face { position: absolute; width: 50px; height: 50px; background: rgba(0, 242, 255, 0.1); border: 1px solid rgba(0, 242, 255, 0.6); box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }
        .front  { transform: rotateY(  0deg) translateZ(25px); }
        .back   { transform: rotateY(180deg) translateZ(25px); }
        .right  { transform: rotateY( 90deg) translateZ(25px); }
        .left   { transform: rotateY(-90deg) translateZ(25px); }
        .top    { transform: rotateX( 90deg) translateZ(25px); }
        .bottom { transform: rotateX(-90deg) translateZ(25px); }
        @keyframes spin { from { transform: rotateX(0deg) rotateY(0deg); } to { transform: rotateX(360deg) rotateY(360deg); } }

        /* 9. SIDEBAR */
        section[data-testid="stSidebar"] {
            background: rgba(5, 5, 10, 0.95);
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        
        /* --- 10. FLOATING CHAT BUTTON (FINAL FIX) --- */
        
        /* Positioning Container */
        div[data-testid="stPopover"] {
            position: fixed !important;
            bottom: 30px !important;
            right: 30px !important;
            left: unset !important;
            top: unset !important;
            width: auto !important;
            height: auto !important;
            z-index: 999999 !important;
        }

        /* The Blue Circle Button */
        div[data-testid="stPopover"] > button {
            width: 60px !important;
            height: 60px !important;
            border-radius: 50% !important;
            background: linear-gradient(135deg, #00f2ff, #0072ff) !important;
            border: 2px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 0 20px rgba(0, 242, 255, 0.6) !important;
            padding: 0 !important;
            
            /* CRITICAL: KILL TEXT */
            color: transparent !important;
            font-size: 0px !important;
            
            /* Alignment */
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        /* HIDE ANY INTERNAL SPANS OR DIVS (This kills the "expan" text) */
        div[data-testid="stPopover"] > button > * {
            display: none !important;
        }

        /* RE-INSERT THE ICON MANUALLY */
        div[data-testid="stPopover"] > button::after {
            content: "💬" !important;
            font-size: 28px !important;
            color: white !important;
            display: block !important;
            visibility: visible !important;
            line-height: 1 !important;
            margin-top: -3px !important;
        }

        /* Hover Effect */
        div[data-testid="stPopover"] > button:hover {
            transform: scale(1.1) !important;
            box-shadow: 0 0 35px rgba(0, 242, 255, 0.9) !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_3d_cube():
    st.markdown("""
    <div class="cube-container">
        <div class="cube">
            <div class="face front"></div>
            <div class="face back"></div>
            <div class="face right"></div>
            <div class="face left"></div>
            <div class="face top"></div>
            <div class="face bottom"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)