# Google MCP Server

MCP Server für Gmail und Google Calendar mit Schreibzugriff.

## Features

- **Gmail**
  - E-Mails senden
  - Entwürfe erstellen
  - HTML-Formatierung

- **Google Calendar**
  - Events erstellen
  - Events aktualisieren
  - Events löschen

## Installation

### Voraussetzungen

- Python 3.11 oder höher
- Google Cloud Project mit aktivierten APIs (Gmail, Calendar)
- OAuth 2.0 Credentials

### Option 1: MCPB Bundle (Empfohlen)

1. **Bundle herunterladen**
   ```bash
   # Von GitHub Releases
   wget https://github.com/USERNAME/REPO/releases/download/v1.0.0/google-mcp-server.mcpb
   ```

2. **In Claude Desktop installieren**
   - Bundle-Datei mit Claude Desktop öffnen
   - Installation bestätigen
   - Fertig!

3. **Google OAuth einrichten**

   Erstelle OAuth Credentials in der Google Cloud Console:
   - Gehe zu https://console.cloud.google.com
   - Erstelle ein neues Projekt oder wähle ein bestehendes
   - Aktiviere Gmail API und Calendar API
   - Erstelle OAuth 2.0 Credentials (Desktop App)
   - Lade `credentials.json` herunter

   Speichere die Credentials:
   ```bash
   mkdir -p ~/.config/google-mcp
   cp credentials.json ~/.config/google-mcp/
   ```

4. **Erste Authentifizierung**
   ```bash
   python3 authenticate.py
   ```
   Dies öffnet einen Browser für die OAuth-Autorisierung und erstellt `~/.config/google-mcp/token.json`.

### Option 2: Manuelle Installation

1. **Repository klonen**
   ```bash
   git clone https://github.com/USERNAME/REPO.git
   cd google-mcp-server
   ```

2. **Dependencies installieren**
   ```bash
   pip install -r requirements.txt
   ```

3. **Google OAuth einrichten** (wie oben)

4. **In Claude Desktop Config eintragen**
   ```json
   {
     "mcpServers": {
       "google": {
         "command": "python3",
         "args": ["/pfad/zu/server.py"]
       }
     }
   }
   ```

## Verwendung

Nach der Installation stehen folgende Tools in Claude zur Verfügung:

### `send_email`
```json
{
  "to": "empfaenger@example.com",
  "subject": "Betreff",
  "body": "Nachricht",
  "cc": "cc@example.com"  // optional
}
```

### `create_draft`
```json
{
  "to": "empfaenger@example.com",
  "subject": "Betreff",
  "body": "Nachricht"
}
```

### `create_calendar_event`
```json
{
  "summary": "Meeting Titel",
  "start_time": "2025-10-27T14:00:00",
  "end_time": "2025-10-27T15:00:00",
  "description": "Beschreibung",  // optional
  "location": "Ort",  // optional
  "attendees": ["person@example.com"]  // optional
}
```

### `update_calendar_event`
```json
{
  "event_id": "abc123",
  "summary": "Neuer Titel",  // optional
  "start_time": "2025-10-27T15:00:00"  // optional
}
```

### `delete_calendar_event`
```json
{
  "event_id": "abc123"
}
```

## Entwicklung

### MCPB Bundle erstellen

1. **MCPB CLI installieren**
   ```bash
   npm install -g @anthropic-ai/mcpb
   ```

2. **Bundle packen**
   ```bash
   cd bundle
   mcpb pack . ../google-mcp-server.mcpb
   ```

3. **SHA-256 Hash generieren**
   ```bash
   sha256sum google-mcp-server.mcpb
   ```

### Bundle validieren
```bash
mcpb validate manifest.json
mcpb info google-mcp-server.mcpb
```

## Sicherheit

- OAuth Tokens werden lokal gespeichert (`~/.config/google-mcp/`)
- Tokens werden niemals im Code oder Bundle gespeichert
- Jeder Nutzer muss eigene Google Cloud Credentials verwenden
- Scopes: `gmail.send`, `gmail.readonly`, `gmail.compose`, `calendar`, `calendar.events`

## Lizenz

MIT

## Support

Bei Problemen bitte ein Issue auf GitHub erstellen.

## SHA-256 Hash

```
605e44e94c082cd08433105ceacce2e1bf3558b0526ccc528290de09220c018a
```

Verwende diesen Hash um die Integrität des Bundles zu verifizieren.
