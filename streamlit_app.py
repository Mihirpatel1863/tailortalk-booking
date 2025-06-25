import streamlit as st
from app.agent import booking_agent
import time


st.set_page_config(page_title="TailorTalk AI", page_icon="🧵", layout="centered")


st.markdown("""
<style>
body { background-color: #f0f4f8; font-family: 'Segoe UI', sans-serif; }
.chat-container {
    background: white;
    padding: 1.5rem;
    border-radius: 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}
.user-msg, .bot-msg {
    border-radius: 12px;
    padding: 0.9rem;
    margin: 0.5rem 0;
    line-height: 1.6;
    max-width: 85%;
}
.user-msg { background: #d1e7ff; text-align: right; }
.bot-msg { background: #e8e9eb; text-align: left; }
.footer {
    margin-top: 2rem;
    text-align: center;
    font-size: 0.85rem;
    color: #888;
}
</style>
""", unsafe_allow_html=True)


st.markdown("<h2 style='text-align:center;'>🧵 TailorTalk AI</h2>", unsafe_allow_html=True)
st.caption("Your Personalized Calendar Booking Assistant")


with st.expander("💡 Try saying things like:"):
    st.markdown("""
    - *Schedule a call tomorrow afternoon*  
    - *Book a meeting next week at 3 PM*  
    - *Can you check this Friday at 10?*
    """)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


user_input = st.chat_input("Ask me to schedule a meeting...")

if user_input:
    st.session_state.chat_history.append(("You", user_input))

    with st.spinner("🤖 TailorTalk is typing..."):
        time.sleep(0.8)
        response = booking_agent(user_input)

    st.session_state.chat_history.append(("TailorTalk", response))


if st.session_state.chat_history:
    for speaker, message in st.session_state.chat_history:
        css_class = "user-msg" if speaker == "You" else "bot-msg"
        st.markdown(
            f"<div class='chat-container'><div class='{css_class}'><strong>{speaker}</strong><br>{message}</div></div>",
            unsafe_allow_html=True
        )
else:
    st.info("Type something above to begin chatting.")


st.markdown("""
<div class='footer'>
    🚀 Built with ❤️ by TailorTalk using Streamlit, LangChain, and Google Calendar API.
</div>
""", unsafe_allow_html=True)
