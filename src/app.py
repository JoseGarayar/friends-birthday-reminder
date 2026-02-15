# CSV
import csv

# Google API
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build as build_api_gcp
from googleapiclient.errors import HttpError

# Utils
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
DATA_DIR = os.path.join(BASE_DIR, 'data')

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    """Authenticate with Google OAuth and return valid credentials.

    Loads a saved token if available, refreshes it if expired, or starts
    a new browser-based OAuth flow if no valid token exists.
    """
    creds = None
    token_path = os.path.join(CONFIG_DIR, 'token.json')
    credentials_path = os.path.join(CONFIG_DIR, 'credentials.json')

    # Try to load existing token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        # Attempt to refresh an expired token
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                # Token is invalid (revoked or expired beyond recovery), delete it
                os.remove(token_path)
                creds = None

        # No valid token available, start a new OAuth flow via browser
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0, prompt='select_account')

        # Save the token for future runs
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def build_event(friend, emails):
    """Build a Google Calendar event dict for a friend's birthday.

    Args:
        friend: Dict with keys 'name', 'day', 'month', 'city', 'state'.
        emails: List of attendee dicts, each with an 'email' key.

    Returns:
        A dict representing a recurring yearly Google Calendar event.
    """
    return {
        'summary': 'Cumpleaños de %s' % (friend['name']),
        'location': '%s, %s' % (friend['city'], friend['state']),
        'description': 'Recordatorio para que le saludes por su cumple a %s' % (friend['name']),
        'start': {
            'dateTime': '2022-%s-%sT09:00:00-05:00' % (friend['month'], friend['day']),
            'timeZone': 'America/Lima',
        },
        'end': {
            'dateTime': '2022-%s-%sT23:00:00-05:00' % (friend['month'], friend['day']),
            'timeZone': 'America/Lima',
        },
        'recurrence': [
            'RRULE:FREQ=YEARLY'
        ],
        'attendees': emails,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 1 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }


def create_events():
    """Read birthday and attendee data, then create Google Calendar events.

    Authenticates with Google, reads friends and attendees from CSV files,
    and inserts a recurring yearly calendar event for each friend.
    """
    creds = get_credentials()
    service = build_api_gcp('calendar', 'v3', credentials=creds)
    list_friends = read_birthdays()
    emails = read_attendees()
    for friend in list_friends:
        event = build_event(friend, emails)
        try:
            event = service.events().insert(calendarId='primary', body=event).execute()
            print ('Event created: %s' % (event.get('htmlLink')))
        except HttpError as error:
            print('An error occurred: %s' % error)


def read_birthdays():
    """Read friend birthday data from CSV.

    Returns:
        A list of dicts with keys 'name', 'day', 'month', 'city', 'state',
        where 'day' and 'month' are zero-padded to two digits.
    """
    list_friends = []
    with open(os.path.join(DATA_DIR, 'birthdays.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['day'] = row['day'].zfill(2)
            row['month'] = row['month'].zfill(2)
            list_friends.append(row)
    return list_friends


def read_attendees():
    """Read attendee emails from CSV.

    Returns:
        A list of dicts with an 'email' key for each non-empty email entry.
    """
    emails = []
    with open(os.path.join(DATA_DIR, 'attendees.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['email']:
                emails.append({'email': row['email']})
    return emails

if __name__ == '__main__':
    create_events()