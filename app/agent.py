from datetime import datetime, timedelta
import streamlit as st  
from langchain.chat_models import ChatOpenAI
from app.calendar_utils import check_availability, book_slot


llm = ChatOpenAI(openai_api_key=st.secrets["api_keys"]["openai_api_key"])

def parse_datetime(text):
    now = datetime.utcnow()
    text = text.lower()

    if "tomorrow morning" in text:
        start = now + timedelta(days=1)
        start = start.replace(hour=10, minute=0)
    elif "tomorrow afternoon" in text:
        start = now + timedelta(days=1)
        start = start.replace(hour=14, minute=0)
    elif "tomorrow evening" in text:
        start = now + timedelta(days=1)
        start = start.replace(hour=18, minute=0)
    elif "today morning" in text:
        start = now.replace(hour=10, minute=0)
    elif "today evening" in text:
        start = now.replace(hour=18, minute=0)
    elif "this friday" in text:
        days_until_friday = (4 - now.weekday() + 7) % 7 or 7
        start = now + timedelta(days=days_until_friday)
        start = start.replace(hour=15, minute=0)
    elif "next week" in text:
        start = now + timedelta(days=7)
        start = start.replace(hour=15, minute=0)
    elif "next monday" in text:
        days_until_monday = ((0 - now.weekday() + 7) % 7) + 7
        start = now + timedelta(days=days_until_monday)
        start = start.replace(hour=10, minute=0)
    elif "this weekend" in text:
        days_until_saturday = (5 - now.weekday() + 7) % 7 or 7
        start = now + timedelta(days=days_until_saturday)
        start = start.replace(hour=11, minute=0)
    else:
        return None, None

    end = start + timedelta(hours=1)
    return start, end

def booking_agent(user_input):
    start, end = parse_datetime(user_input)

    if not start:
        return (
            "⚠️ Sorry, I couldn't understand your time request.\n"
            "Try something like 'tomorrow morning', 'this Friday', or 'next week'."
        )

    if check_availability(start, end):
        book_slot(start, end)
        ist_time = start + timedelta(hours=5, minutes=30)
        return (
            f"✅ Your meeting is booked!\n\n"
            f"🕒 UTC: {start.strftime('%A, %B %d at %I:%M %p')}\n"
            f"🕒 IST: {ist_time.strftime('%A, %B %d at %I:%M %p')}"
        )

    return (
        "❌ That slot is already booked.\n"
        "Please try another time like 'next week' or 'Friday afternoon'."
    )
