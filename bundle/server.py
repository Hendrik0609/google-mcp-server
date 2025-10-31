#!/usr/bin/env python3
"""
Google MCP Server mit Schreibzugriff für Gmail und Calendar
Unterstützt: Email senden, Calendar Events erstellen/bearbeiten/löschen
"""

import json
import os
from datetime import datetime
from typing import Any, Optional
import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import sys
import time

# Scopes mit Schreibzugriff
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose',  # Für Drafts
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

# Pfade für Credentials
TOKEN_PATH = os.path.expanduser('~/.config/google-mcp/token.json')
# credentials.json wird im Bundle mitgeliefert (vom Admin konfiguriert)
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')

class GoogleMCPServer:
    def __init__(self):
        self.creds = None
        self.gmail_service = None
        self.calendar_service = None

    def authenticate_with_device_code(self):
        """OAuth 2.0 Device Code Flow - Benutzerfreundlich ohne Browser-Popup"""
        if not os.path.exists(CREDENTIALS_PATH):
            raise FileNotFoundError(
                f"Credentials nicht gefunden: {CREDENTIALS_PATH}\n"
                "Das Bundle wurde nicht korrekt konfiguriert."
            )

        # Device Code Flow starten
        from google.auth.transport.requests import Request as AuthRequest
        from google.oauth2.credentials import Credentials
        import requests

        # Client Credentials laden
        with open(CREDENTIALS_PATH, 'r') as f:
            creds_data = json.load(f)
            client_id = creds_data['installed']['client_id']
            client_secret = creds_data['installed']['client_secret']

        # Device Code anfordern
        device_code_url = 'https://oauth2.googleapis.com/device/code'
        device_code_data = {
            'client_id': client_id,
            'scope': ' '.join(SCOPES)
        }

        response = requests.post(device_code_url, data=device_code_data)
        device_code_response = response.json()

        # User Code und Verification URL ausgeben
        user_code = device_code_response['user_code']
        verification_url = device_code_response['verification_url']
        device_code = device_code_response['device_code']

        print("\n" + "="*60, file=sys.stderr)
        print("🔐 GOOGLE AUTHENTIFIZIERUNG ERFORDERLICH", file=sys.stderr)
        print("="*60, file=sys.stderr)
        print(f"\n1. Öffne: {verification_url}", file=sys.stderr)
        print(f"2. Gib diesen Code ein: {user_code}", file=sys.stderr)
        print("\n3. Autorisiere den Zugriff auf Gmail & Calendar", file=sys.stderr)
        print("\nWarte auf Autorisierung...\n", file=sys.stderr)

        # Polling - warte auf User-Autorisierung
        token_url = 'https://oauth2.googleapis.com/token'
        interval = device_code_response.get('interval', 5)

        while True:
            time.sleep(interval)

            token_data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'device_code': device_code,
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
            }

            token_response = requests.post(token_url, data=token_data)
            token_result = token_response.json()

            if 'error' in token_result:
                error = token_result['error']
                if error == 'authorization_pending':
                    continue  # Weiter warten
                elif error == 'slow_down':
                    interval += 1
                    continue
                else:
                    raise Exception(f"Authentifizierung fehlgeschlagen: {error}")

            # Erfolgreich!
            access_token = token_result['access_token']
            refresh_token = token_result.get('refresh_token')

            # Token speichern
            os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)

            creds_dict = {
                'token': access_token,
                'refresh_token': refresh_token,
                'token_uri': 'https://oauth2.googleapis.com/token',
                'client_id': client_id,
                'client_secret': client_secret,
                'scopes': SCOPES
            }

            with open(TOKEN_PATH, 'w') as token:
                json.dump(creds_dict, token)

            print("\n✅ Authentifizierung erfolgreich!", file=sys.stderr)
            print(f"Token gespeichert: {TOKEN_PATH}\n", file=sys.stderr)

            self.creds = Credentials.from_authorized_user_info(creds_dict, SCOPES)
            break

    def authenticate(self):
        """OAuth 2.0 Authentifizierung - verwendet existierendes Token oder startet Device Flow"""
        # Token laden falls vorhanden
        if os.path.exists(TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

            # Token erneuern falls abgelaufen
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                    # Token speichern
                    with open(TOKEN_PATH, 'w') as token:
                        token.write(self.creds.to_json())
                except Exception as e:
                    print(f"\n⚠️  Token refresh fehlgeschlagen: {e}", file=sys.stderr)
                    print("Starte neue Authentifizierung...\n", file=sys.stderr)
                    self.authenticate_with_device_code()
        else:
            # Kein Token vorhanden - Device Code Flow starten
            self.authenticate_with_device_code()

        # Services initialisieren
        self.gmail_service = build('gmail', 'v1', credentials=self.creds)
        self.calendar_service = build('calendar', 'v3', credentials=self.creds)

    def send_email(self, to: str, subject: str, body: str, cc: Optional[str] = None) -> dict:
        """Email senden mit HTML-Formatierung"""
        # Multipart Message für HTML + Plain Text
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['subject'] = subject
        if cc:
            message['cc'] = cc

        # Plain text version (Fallback)
        plain_part = MIMEText(body, 'plain')
        message.attach(plain_part)

        # HTML version (mit Zeilenumbrüchen konvertiert)
        html_body = body.replace('\n', '<br>\n')
        html_part = MIMEText(html_body, 'html')
        message.attach(html_part)

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message_body = {'raw': raw}

        result = self.gmail_service.users().messages().send(
            userId='me', body=message_body).execute()

        return {
            'success': True,
            'message_id': result['id'],
            'thread_id': result['threadId']
        }

    def create_draft(self, to: str, subject: str, body: str, cc: Optional[str] = None) -> dict:
        """Email als Entwurf speichern mit HTML-Formatierung"""
        # Multipart Message für HTML + Plain Text
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['subject'] = subject
        if cc:
            message['cc'] = cc

        # Plain text version (Fallback)
        plain_part = MIMEText(body, 'plain')
        message.attach(plain_part)

        # HTML version (mit Zeilenumbrüchen konvertiert)
        html_body = body.replace('\n', '<br>\n')
        html_part = MIMEText(html_body, 'html')
        message.attach(html_part)

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        draft_body = {'message': {'raw': raw}}

        result = self.gmail_service.users().drafts().create(
            userId='me', body=draft_body).execute()

        return {
            'success': True,
            'draft_id': result['id'],
            'message_id': result['message']['id']
        }

    def create_calendar_event(
        self,
        summary: str,
        start_time: str,
        end_time: str,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[list] = None,
        calendar_id: str = 'primary'
    ) -> dict:
        """Calendar Event erstellen"""
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time,
                'timeZone': 'Europe/Berlin',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Europe/Berlin',
            },
        }

        if description:
            event['description'] = description
        if location:
            event['location'] = location
        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]

        result = self.calendar_service.events().insert(
            calendarId=calendar_id, body=event).execute()

        return {
            'success': True,
            'event_id': result['id'],
            'html_link': result['htmlLink']
        }

    def update_calendar_event(
        self,
        event_id: str,
        calendar_id: str = 'primary',
        summary: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        description: Optional[str] = None
    ) -> dict:
        """Calendar Event aktualisieren"""
        # Event laden
        event = self.calendar_service.events().get(
            calendarId=calendar_id, eventId=event_id).execute()

        # Felder aktualisieren
        if summary:
            event['summary'] = summary
        if start_time:
            event['start']['dateTime'] = start_time
        if end_time:
            event['end']['dateTime'] = end_time
        if description:
            event['description'] = description

        result = self.calendar_service.events().update(
            calendarId=calendar_id, eventId=event_id, body=event).execute()

        return {
            'success': True,
            'event_id': result['id'],
            'updated': result['updated']
        }

    def delete_calendar_event(self, event_id: str, calendar_id: str = 'primary') -> dict:
        """Calendar Event löschen"""
        self.calendar_service.events().delete(
            calendarId=calendar_id, eventId=event_id).execute()

        return {
            'success': True,
            'message': f'Event {event_id} gelöscht'
        }

# MCP Server Setup
app = Server("google-mcp-server")
google_server = GoogleMCPServer()

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Verfügbare Tools auflisten"""
    return [
        Tool(
            name="send_email",
            description="Email über Gmail senden",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Empfänger Email"},
                    "subject": {"type": "string", "description": "Betreff"},
                    "body": {"type": "string", "description": "Email Text"},
                    "cc": {"type": "string", "description": "CC Empfänger (optional)"}
                },
                "required": ["to", "subject", "body"]
            }
        ),
        Tool(
            name="create_draft",
            description="Email als Entwurf in Gmail speichern",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Empfänger Email"},
                    "subject": {"type": "string", "description": "Betreff"},
                    "body": {"type": "string", "description": "Email Text"},
                    "cc": {"type": "string", "description": "CC Empfänger (optional)"}
                },
                "required": ["to", "subject", "body"]
            }
        ),
        Tool(
            name="create_calendar_event",
            description="Neues Calendar Event erstellen",
            inputSchema={
                "type": "object",
                "properties": {
                    "summary": {"type": "string", "description": "Event Titel"},
                    "start_time": {"type": "string", "description": "Start (ISO 8601, z.B. 2025-10-10T10:00:00)"},
                    "end_time": {"type": "string", "description": "Ende (ISO 8601)"},
                    "description": {"type": "string", "description": "Beschreibung (optional)"},
                    "location": {"type": "string", "description": "Ort (optional)"},
                    "attendees": {"type": "array", "items": {"type": "string"}, "description": "Teilnehmer Emails (optional)"},
                    "calendar_id": {"type": "string", "description": "Calendar ID (default: primary)"}
                },
                "required": ["summary", "start_time", "end_time"]
            }
        ),
        Tool(
            name="update_calendar_event",
            description="Bestehendes Calendar Event aktualisieren",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "string", "description": "Event ID"},
                    "calendar_id": {"type": "string", "description": "Calendar ID (default: primary)"},
                    "summary": {"type": "string", "description": "Neuer Titel (optional)"},
                    "start_time": {"type": "string", "description": "Neue Startzeit (optional)"},
                    "end_time": {"type": "string", "description": "Neue Endzeit (optional)"},
                    "description": {"type": "string", "description": "Neue Beschreibung (optional)"}
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="delete_calendar_event",
            description="Calendar Event löschen",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "string", "description": "Event ID"},
                    "calendar_id": {"type": "string", "description": "Calendar ID (default: primary)"}
                },
                "required": ["event_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Tool ausführen"""
    try:
        if name == "send_email":
            result = google_server.send_email(
                to=arguments["to"],
                subject=arguments["subject"],
                body=arguments["body"],
                cc=arguments.get("cc")
            )
        elif name == "create_draft":
            result = google_server.create_draft(
                to=arguments["to"],
                subject=arguments["subject"],
                body=arguments["body"],
                cc=arguments.get("cc")
            )
        elif name == "create_calendar_event":
            result = google_server.create_calendar_event(
                summary=arguments["summary"],
                start_time=arguments["start_time"],
                end_time=arguments["end_time"],
                description=arguments.get("description"),
                location=arguments.get("location"),
                attendees=arguments.get("attendees"),
                calendar_id=arguments.get("calendar_id", "primary")
            )
        elif name == "update_calendar_event":
            result = google_server.update_calendar_event(
                event_id=arguments["event_id"],
                calendar_id=arguments.get("calendar_id", "primary"),
                summary=arguments.get("summary"),
                start_time=arguments.get("start_time"),
                end_time=arguments.get("end_time"),
                description=arguments.get("description")
            )
        elif name == "delete_calendar_event":
            result = google_server.delete_calendar_event(
                event_id=arguments["event_id"],
                calendar_id=arguments.get("calendar_id", "primary")
            )
        else:
            raise ValueError(f"Unknown tool: {name}")

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Server starten"""
    # Authentifizierung beim Start
    google_server.authenticate()

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
