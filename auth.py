import streamlit as st
import hashlib

def check_password():
    """Returns True if user entered correct password"""
    
    def password_entered():
        """Checks whether password entered by user is correct"""
        salt = "4895222017aeae29ff6c659f85da69eb"
        stored_hash = "9c5ce5e165a8ae432e451fcd85abcae2597db3e60cd33e7a6b7ed82b4f1ee2eb"
        
        entered_password = st.session_state["password"]
        entered_hash = hashlib.pbkdf2_hmac(
            'sha256', 
            entered_password.encode(), 
            salt.encode(), 
            100000
        ).hex()
        
        if entered_hash == stored_hash:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    # Return True if password already validated
    if st.session_state.get("password_correct", False):
        return True

    # Show login form
    st.markdown("### 🔐 CRM Analytics Dashboard")
    st.markdown("Please enter your password to access the dashboard.")
    
    st.text_input(
        "Password", 
        type="password", 
        on_change=password_entered, 
        key="password"
    )
    
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Password incorrect")
    
    return False
