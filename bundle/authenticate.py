#!/usr/bin/env python3
"""
Authentifizierungs-Script für Google MCP Server (Device Code Flow)
Alternativ: Nutze einfach Claude - die Authentifizierung startet automatisch!
"""

import os
import json
import time
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes mit Schreibzugriff
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

# Pfade für Credentials
TOKEN_PATH = os.path.expanduser('~/.config/google-mcp/token.json')
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')

def authenticate_device_code():
    """OAuth 2.0 Device Code Flow - Benutzerfreundlich!"""
    if not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError(
            f"Credentials nicht gefunden: {CREDENTIALS_PATH}\n"
            "Das Bundle wurde nicht korrekt konfiguriert."
        )

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

    print("\n" + "="*60)
    print("🔐 GOOGLE AUTHENTIFIZIERUNG")
    print("="*60)
    print(f"\n1. Öffne: {verification_url}")
    print(f"2. Gib diesen Code ein: {user_code}")
    print("\n3. Autorisiere den Zugriff auf Gmail & Calendar")
    print("\nWarte auf Autorisierung...")

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
                print(".", end="", flush=True)
                continue
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

        print("\n\n✅ Authentifizierung erfolgreich!")
        print(f"✅ Token gespeichert: {TOKEN_PATH}")
        print("\n🚀 Starte Claude Desktop - der Server ist jetzt einsatzbereit!")
        break

def authenticate():
    """Hauptfunktion - prüft Token oder startet Device Flow"""
    # Token laden wenn vorhanden
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        # Prüfen ob Token noch gültig
        if creds and creds.valid:
            print("✅ Token ist bereits gültig!")
            print(f"📍 Token: {TOKEN_PATH}")
            print("\n🚀 Du kannst Claude Desktop nutzen.")
            return

        # Token erneuern wenn abgelaufen
        if creds and creds.expired and creds.refresh_token:
            try:
                print("🔄 Token abgelaufen, erneuere...")
                creds.refresh(Request())
                with open(TOKEN_PATH, 'w') as token:
                    token.write(creds.to_json())
                print("✅ Token erfolgreich erneuert!")
                print("\n🚀 Du kannst Claude Desktop nutzen.")
                return
            except Exception as e:
                print(f"⚠️  Token refresh fehlgeschlagen: {e}")
                print("Starte neue Authentifizierung...\n")

    # Neue Authentifizierung nötig
    authenticate_device_code()

if __name__ == "__main__":
    try:
        authenticate()
    except Exception as e:
        print(f"\n✗ Fehler: {e}")
        exit(1)
