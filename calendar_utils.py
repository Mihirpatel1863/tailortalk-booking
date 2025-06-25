import datetime
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
CALENDAR_ID = 'mp344974@gmail.com'  


credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

def check_availability(start_time, end_time):
    """
    Checks if the given time slot is free on the calendar.

    Args:
        start_time (datetime): Proposed start time in UTC.
        end_time (datetime): Proposed end time in UTC.

    Returns:
        bool: True if time slot is available, False if busy or error occurs.
    """
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
    """
    Books a new event on the calendar.

    Args:
        start_time (datetime): Start datetime in UTC.
        end_time (datetime): End datetime in UTC.
        summary (str): Title of the calendar event.

    Returns:
        bool: True if booking succeeds, False otherwise.
    """
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
