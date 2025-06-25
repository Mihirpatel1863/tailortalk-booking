import datetime
import logging
import streamlit as st 
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'mp344974@gmail.com'


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

def check_availability(start_time, end_time):
    logger.info(f"Checking availability from {start_time} to {end_time}")
    try:
        events = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_time.isoformat() + 'Z',
            timeMax=end_time.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute().get('items', [])

        return len(events) == 0

    except HttpError as error:
        logger.error(f"[Availability Error] {error}")
        return False

def book_slot(start_time, end_time, summary="Meeting with TailorTalk"):
    logger.info(f"Attempting to book slot: {summary} from {start_time} to {end_time}")
    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
    }

    try:
        service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        logger.info(f"[Booked] {summary} at {start_time.isoformat()} UTC")
        return True

    except HttpError as error:
        logger.error(f"[Booking Error] {error}")
        return False
