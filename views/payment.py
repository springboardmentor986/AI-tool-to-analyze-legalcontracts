import streamlit as st
import time
from utils import db

def show():
    st.markdown("<h1 style='color: #00f2ff;'>💎 Upgrade Your Plan</h1>", unsafe_allow_html=True)
    
    current_plan = st.session_state.get('plan', 'Free')
    st.info(f"Current Plan: **{current_plan}**")
    
    c1, c2, c3 = st.columns(3)
    
    # FREE
    with c1:
        st.markdown("""
        <div style="background: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155;">
            <h3>Free Tier</h3>
            <h1>₹0</h1>
            <ul style="font-size: 14px; color: #94a3b8;">
                <li>Basic Contract Scan</li>
                <li>No AI Consultant</li>
                <li>Limited Analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if current_plan == 'Free':
            st.button("Current Plan", disabled=True, key="btn_free")

    # PRO
    with c2:
        st.markdown("""
        <div style="background: #1e293b; padding: 20px; border-radius: 10px; border: 2px solid #00f2ff; box-shadow: 0 0 15px rgba(0,242,255,0.3);">
            <h3 style="color: #00f2ff;">Pro Tier</h3>
            <h1>₹4,999<span style="font-size: 16px;">/mo</span></h1>
            <ul style="font-size: 14px; color: #e2e8f0;">
                <li>✅ <b>AI Consultant (Avatar)</b></li>
                <li>✅ <b>Unlimited Deep Scans</b></li>
                <li>✅ <b>Advanced Vault</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if current_plan == 'Free':
            if st.button("🚀 Upgrade to Pro", key="btn_pro", type="primary"):
                with st.spinner("Processing Payment via UPI..."):
                    time.sleep(2)
                db.update_plan(st.session_state['username'], 'Pro')
                st.session_state['plan'] = 'Pro'
                st.balloons()
                st.success("Upgraded to PRO! Unlocking features...")
                time.sleep(2)
                st.rerun()
        else:
            st.button("✅ Active", disabled=True, key="btn_pro_active")

    # ENTERPRISE
    with c3:
        st.markdown("""
        <div style="background: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155;">
            <h3>Enterprise</h3>
            <h1>Custom</h1>
            <ul style="font-size: 14px; color: #94a3b8;">
                <li>On-Premise Server</li>
                <li>API Access</li>
                <li>Dedicated Manager</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.button("Contact Sales", key="btn_ent")