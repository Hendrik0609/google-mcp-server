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
CREDENTIALS_PATH = os.path.expanduser('~/.config/google-mcp/credentials.json')

class GoogleMCPServer:
    def __init__(self):
        self.creds = None
        self.gmail_service = None
        self.calendar_service = None

    def authenticate(self):
        """OAuth 2.0 Authentifizierung - verwendet existierendes Token"""
        # Token laden
        if not os.path.exists(TOKEN_PATH):
            raise FileNotFoundError(
                f"Token nicht gefunden: {TOKEN_PATH}\n"
                "Führe zuerst 'python3 authenticate.py' aus, um dich zu authentifizieren."
            )

        self.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        # Token erneuern falls abgelaufen
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
            # Token speichern
            with open(TOKEN_PATH, 'w') as token:
                token.write(self.creds.to_json())

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
