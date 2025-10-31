#!/usr/bin/env python3
"""
Separates Authentifizierungs-Script für Google MCP Server
Führe dieses Script aus, BEVOR du Claude Desktop startest
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

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

def authenticate():
    """OAuth 2.0 Authentifizierung"""
    creds = None

    # Token laden wenn vorhanden
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        print(f"✓ Token gefunden: {TOKEN_PATH}")

    # Token erneuern oder neu authentifizieren
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Token abgelaufen, erneuere...")
            creds.refresh(Request())
            print("✓ Token erfolgreich erneuert")
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    f"Credentials nicht gefunden: {CREDENTIALS_PATH}\n"
                    "Erstelle eine OAuth App in Google Cloud Console und "
                    "lade credentials.json herunter."
                )
            print("Starte neue Authentifizierung...")
            print("Ein Browser-Fenster wird sich öffnen...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            print("✓ Authentifizierung erfolgreich!")

        # Token speichern
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
        print(f"✓ Token gespeichert: {TOKEN_PATH}")
    else:
        print("✓ Token ist gültig")

    print("\n✓ Authentifizierung abgeschlossen!")
    print("Du kannst jetzt Claude Desktop starten.")

if __name__ == "__main__":
    try:
        authenticate()
    except Exception as e:
        print(f"\n✗ Fehler: {e}")
        exit(1)
