import streamlit as st
import speech_recognition as sr
import edge_tts
import asyncio
import base64
import os
import time
from utils.universal_llm import universal_llm 

# --- CONFIGURATION ---
VOICE_ID = "en-IN-PrabhatNeural"

# PATHS
IDLE_VIDEO = "assets/idle.mp4"
TALK_VIDEO = "assets/talking.mp4"

# Fallbacks
FALLBACK_IDLE = "https://cdn.dribbble.com/users/32512/screenshots/5668419/ai-assistant-2.gif"
FALLBACK_TALK = "https://cdn.dribbble.com/users/32512/screenshots/5668419/ai-assistant-2.gif"

# --- HELPER: GENERATE AUDIO ---
async def generate_audio_file(text):
    try:
        communicate = edge_tts.Communicate(text, VOICE_ID)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return audio_data
    except:
        return None

def get_video_player(state, audio_b64=None):
    """
    Returns HTML that forces a 9:16 video to look professional in a 16:9 frame.
    """
    # 1. Select Video Source
    if state == "SPEAKING":
        video_path = TALK_VIDEO
        fallback = FALLBACK_TALK
    else:
        video_path = IDLE_VIDEO
        fallback = FALLBACK_IDLE

    # 2. Base64 Encoding
    if os.path.exists(video_path):
        with open(video_path, "rb") as f:
            video_bytes = f.read()
            b64 = base64.b64encode(video_bytes).decode()
            src = f"data:video/mp4;base64,{b64}"
    else:
        src = fallback

    # 3. Audio Player Logic
    audio_html = ""
    if state == "SPEAKING" and audio_b64:
        audio_html = f"""
            <audio id="ai-voice" autoplay>
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
        """

    # 4. LAYOUT
    return f"""
    <style>
        .monitor-frame {{
            width: 100%;
            max-width: 850px;
            aspect-ratio: 16/9;
            background: #000;
            border-radius: 12px;
            border: 1px solid #333;
            box-shadow: 0 4px 30px rgba(0,0,0,0.6);
            position: relative;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto;
        }}
        .avatar-video {{
            height: 100%;
            width: auto; 
            max-width: 100%;
            object-fit: contain;
            z-index: 2;
        }}
        .blur-bg {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: #111;
            z-index: 1;
        }}
    </style>

    <div class="monitor-frame">
        <div class="blur-bg"></div>
        <video class="avatar-video" autoplay loop muted playsinline>
            <source src="{src}" type="video/mp4">
        </video>
    </div>
    {audio_html}
    """

def show():
    if 'state' not in st.session_state: st.session_state['state'] = "IDLE"

    st.markdown("<h2 style='text-align: center;'>📞 AI Legal Consultant</h2>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([0.2, 3, 0.2])
    
    with c2:
        # --- VIDEO WINDOW ---
        html_code = get_video_player(
            st.session_state['state'], 
            st.session_state.get('audio_data')
        )
        st.components.v1.html(html_code, height=550)

        # --- STATUS INDICATORS ---
        if st.session_state['state'] == "LISTENING":
             st.warning("🔴 Microphone Active! Speak Now...")
        elif st.session_state['state'] == "THINKING":
             st.warning("🧠 Thinking...")
        elif st.session_state['state'] == "SPEAKING":
             st.success(f"🤖 {st.session_state.get('ai_text', '')}")
        else:
             st.info("🟢 Online & Ready")

        # --- CONTROLS ---
        # Only show button if IDLE to prevent double-clicking
        if st.session_state['state'] == "IDLE":
            if st.button("🎙️ START TALKING", type="primary", use_container_width=True):
                st.session_state['state'] = "LISTENING"
                st.rerun()

    # --- LOGIC LOOP ---
    
    # 1. LISTENING PHASE
    if st.session_state['state'] == "LISTENING":
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.toast("🎤 Adjusting for noise...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                
                st.toast("🗣️ Listening...")
                audio = r.listen(source, timeout=6, phrase_time_limit=6)
                
                st.toast("⏳ Processing...")
                text = r.recognize_google(audio)
                
                st.session_state['user_query'] = text
                st.session_state['state'] = "THINKING"
                st.rerun()
                
        except Exception as e:
            st.error(f"Error: {e}")
            time.sleep(2)
            st.session_state['state'] = "IDLE"
            st.rerun()

    # 2. THINKING PHASE
    elif st.session_state['state'] == "THINKING":
        try:
            context = ""
            if 'results' in st.session_state and st.session_state['results']:
                context = f"Context: {str(st.session_state['results'].get('synthesis', ''))[:300]}..."
            
            prompt = f"{context}\n\nUser: {st.session_state['user_query']}\n\nAnswer in 2 short sentences."
            response = universal_llm.invoke(prompt).content
            
            # Generate Audio
            audio_bytes = asyncio.run(generate_audio_file(response))
            
            if audio_bytes:
                st.session_state['audio_data'] = base64.b64encode(audio_bytes).decode()
                st.session_state['ai_text'] = response
                
                # --- CALCULATE DURATION ---
                # Avg speaking rate is ~15 chars per second. 
                # We add 1.5s buffer for pauses.
                estimated_duration = (len(response) / 15) + 1.5
                st.session_state['duration'] = estimated_duration
                
                st.session_state['state'] = "SPEAKING"
                st.rerun()
            else:
                st.error("Audio Failed")
                st.session_state['state'] = "IDLE"
                st.rerun()
                
        except Exception:
            st.session_state['state'] = "IDLE"
            st.rerun()

    # 3. SPEAKING PHASE (The Auto-Reset Logic)
    elif st.session_state['state'] == "SPEAKING":
        # The HTML player above is already playing the video/audio.
        # Python just needs to wait for it to finish.
        
        duration = st.session_state.get('duration', 3)
        time.sleep(duration)
        
        # AUTO RESET TO IDLE
        st.session_state['state'] = "IDLE"
        st.rerun()