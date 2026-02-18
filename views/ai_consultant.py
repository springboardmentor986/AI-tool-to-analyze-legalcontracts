import streamlit as st
import speech_recognition as sr
import edge_tts
import asyncio
import base64
import os
import time
from utils.universal_llm import universal_llm 

# --- 1. LANGUAGE CONFIGURATION ---
LANGUAGES = {
    "English (India)": {
        "stt": "en-IN", 
        "tts": "en-IN-PrabhatNeural", 
        "prompt": "You are the ClauseAI Legal Consultant. Answer in professional English."
    },
    "Hindi (India)": {
        "stt": "hi-IN", 
        "tts": "hi-IN-MadhurNeural", 
        "prompt": "You are the ClauseAI Legal Consultant. Answer in Hindi (Devanagari)."
    },
    "Tamil (India)": {
        "stt": "ta-IN", 
        "tts": "ta-IN-ValluvarNeural", 
        "prompt": "You are the ClauseAI Legal Consultant. Answer in Tamil."
    },
    "Telugu (India)": {
        "stt": "te-IN", 
        "tts": "te-IN-MohanNeural", 
        "prompt": "You are the ClauseAI Legal Consultant. Answer in Telugu."
    },
    "Spanish": {
        "stt": "es-ES", 
        "tts": "es-ES-AlvaroNeural", 
        "prompt": "You are the ClauseAI Legal Consultant. Answer in Spanish."
    },
    "French": {
        "stt": "fr-FR", 
        "tts": "fr-FR-HenriNeural", 
        "prompt": "You are the ClauseAI Legal Consultant. Answer in French."
    }
}

# PATHS
IDLE_VIDEO = "assets/idle.mp4"
TALK_VIDEO = "assets/talking.mp4"
FALLBACK_IDLE = "https://cdn.dribbble.com/users/32512/screenshots/5668419/ai-assistant-2.gif"
FALLBACK_TALK = "https://cdn.dribbble.com/users/32512/screenshots/5668419/ai-assistant-2.gif"

# --- HELPER: FINE-TUNED DURATION CALCULATOR ---
def calculate_duration(text, lang_code):
    """
    Calculates duration with specific tuning for Indian Languages.
    """
    words = len(text.split())
    
    # INDIAN LANGUAGES (Tamil, Telugu, Hindi) take significantly longer per word
    if "ta" in lang_code or "te" in lang_code or "hi" in lang_code:
        rate = 1.5  # Very conservative speed (1.5 words per second)
    else:
        # English/European
        rate = 2.4  # Slightly slower than avg to be safe
    
    # Pause for punctuation
    punctuation_time = (text.count(',') * 0.4) + (text.count('.') * 0.8) + (text.count('?') * 0.8) + (text.count('।') * 0.8)
    
    base_time = words / rate
    
    # SAFETY BUFFER: Increased to 1.5 seconds to prevent last-word cutoff
    total_duration = base_time + punctuation_time + 1.0
    return total_duration

# --- HELPER: GENERATE AUDIO ---
async def generate_audio_file(text, voice_id):
    try:
        communicate = edge_tts.Communicate(text, voice_id)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return audio_data
    except:
        return None

def get_video_player(state, audio_b64=None):
    if state == "SPEAKING":
        video_path = TALK_VIDEO
        fallback = FALLBACK_TALK
    else:
        video_path = IDLE_VIDEO
        fallback = FALLBACK_IDLE

    if os.path.exists(video_path):
        with open(video_path, "rb") as f:
            video_bytes = f.read()
            b64 = base64.b64encode(video_bytes).decode()
            src = f"data:video/mp4;base64,{b64}"
    else:
        src = fallback

    audio_html = ""
    if state == "SPEAKING" and audio_b64:
        audio_html = f"""
            <audio id="ai-voice" autoplay>
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
        """

    return f"""
    <style>
        .monitor-frame {{
            width: 100%; max-width: 850px; aspect-ratio: 16/9;
            background: #000; border-radius: 12px; border: 1px solid #333;
            box-shadow: 0 4px 30px rgba(0,0,0,0.6); position: relative;
            overflow: hidden; display: flex; justify-content: center; align-items: center; margin: 0 auto;
        }}
        .avatar-video {{ height: 100%; width: auto; max-width: 100%; object-fit: contain; z-index: 2; }}
        .blur-bg {{ position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: #111; z-index: 1; }}
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
    if 'selected_lang' not in st.session_state: st.session_state['selected_lang'] = "English (India)"

    st.markdown("<h2 style='text-align: center;'>📞 AI Legal Consultant</h2>", unsafe_allow_html=True)

    # --- LANGUAGE SELECTOR ---
    c_head_1, c_head_2 = st.columns([3, 1])
    with c_head_2:
        st.session_state['selected_lang'] = st.selectbox(
            "Select Language", 
            list(LANGUAGES.keys()), 
            index=0,
            label_visibility="collapsed"
        )
    
    current_lang_config = LANGUAGES[st.session_state['selected_lang']]

    c1, c2, c3 = st.columns([0.2, 3, 0.2])
    with c2:
        # VIDEO PLAYER
        html_code = get_video_player(st.session_state['state'], st.session_state.get('audio_data'))
        st.components.v1.html(html_code, height=550)

        # STATUS
        if st.session_state['state'] == "LISTENING":
             st.warning(f"🔴 Listening in {st.session_state['selected_lang']}...")
        elif st.session_state['state'] == "THINKING":
             st.warning("🧠 Thinking...")
        elif st.session_state['state'] == "SPEAKING":
             st.success(f"🤖 {st.session_state.get('ai_text', '')}")
             if st.button("⏹️ Stop Speaking"):
                 st.session_state['state'] = "IDLE"
                 st.rerun()
        else:
             st.info(f"🟢 Ready. Select language: {st.session_state['selected_lang']}")

        if st.session_state['state'] == "IDLE":
            if st.button("🎙️ START TALKING", type="primary", use_container_width=True):
                st.session_state['state'] = "LISTENING"
                st.rerun()

    # --- LOGIC LOOP ---
    if st.session_state['state'] == "LISTENING":
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.toast(f"Mic Active. Speak {st.session_state['selected_lang']}...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                
                audio = r.listen(source, timeout=8, phrase_time_limit=8)
                text = r.recognize_google(audio, language=current_lang_config['stt'])
                
                st.session_state['user_query'] = text
                st.session_state['state'] = "THINKING"
                st.rerun()

        except sr.UnknownValueError:
            st.error(f"🤷 I heard sound, but could not identify {st.session_state['selected_lang']} words. Please speak clearly.")
            time.sleep(3)
            st.session_state['state'] = "IDLE"
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")
            time.sleep(3)
            st.session_state['state'] = "IDLE"
            st.rerun()

    elif st.session_state['state'] == "THINKING":
        try:
            context = ""
            if 'results' in st.session_state and st.session_state['results']:
                context = f"Context: {str(st.session_state['results'].get('synthesis', ''))[:300]}..."
            
            # --- SYSTEM PERSONA INJECTION ---
            system_instruction = (
                f"Your Persona: You are the ClauseAI Senior Legal Consultant. "
                f"You are professional, precise, and helpful. "
                f"Do not act like a generic AI. Act like a human lawyer. "
                f"Context: {context} "
                f"User Question: {st.session_state['user_query']} "
                f"Instruction: {current_lang_config['prompt']} Keep response under 100 words."
            )
            
            response = universal_llm.invoke(system_instruction).content
            
            audio_bytes = asyncio.run(generate_audio_file(response, current_lang_config['tts']))
            
            if audio_bytes:
                st.session_state['audio_data'] = base64.b64encode(audio_bytes).decode()
                st.session_state['ai_text'] = response
                
                # Use updated duration logic
                st.session_state['duration'] = calculate_duration(response, current_lang_config['stt'])
                
                st.session_state['state'] = "SPEAKING"
                st.rerun()
            else:
                st.error("Audio Failed")
                st.session_state['state'] = "IDLE"
                st.rerun()
        except Exception as e:
            st.error(f"AI Error: {e}")
            st.session_state['state'] = "IDLE"
            st.rerun()

    elif st.session_state['state'] == "SPEAKING":
        duration = st.session_state.get('duration', 5)
        time.sleep(duration)
        st.session_state['state'] = "IDLE"
        st.rerun()