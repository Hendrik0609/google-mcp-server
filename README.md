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

### Für Team-Admins

Wenn du diesen Server für dein Team bereitstellen möchtest:

👉 **Siehe [SETUP_ADMIN.md](SETUP_ADMIN.md)** für die vollständige Anleitung zum Einrichten eines zentralen Google Cloud Projekts.

### Für Team-Mitglieder

Wenn dein Admin bereits ein Bundle bereitgestellt hat:

👉 **Siehe [SETUP_USER.md](SETUP_USER.md)** für die Installationsanleitung.

### Für Einzelnutzer (eigenes Google Cloud Projekt)

<details>
<summary>Klicke hier für die Einzelnutzer-Anleitung</summary>

#### Voraussetzungen

- Python 3.11 oder höher
- Google Cloud Project mit aktivierten APIs (Gmail, Calendar)
- OAuth 2.0 Credentials

#### Schritt 1: Google Cloud Projekt einrichten

1. Gehe zu [Google Cloud Console](https://console.cloud.google.com)
2. Erstelle ein neues Projekt
3. Aktiviere Gmail API und Calendar API
4. Erstelle OAuth 2.0 Credentials (Desktop App)
5. Lade `credentials.json` herunter

#### Schritt 2: Installation

**Option A: MCPB Bundle**

1. Bundle herunterladen
2. `credentials.json` ins Bundle-Verzeichnis kopieren
3. Bundle neu packen: `mcpb pack bundle google-mcp-server.mcpb`
4. Bundle in Claude Desktop installieren
5. `python3 authenticate.py` ausführen

**Option B: Manuelle Installation**

1. Repository klonen:
   ```bash
   git clone https://github.com/USERNAME/REPO.git
   cd google-mcp-server
   ```

2. Dependencies installieren:
   ```bash
   pip install -r requirements.txt
   ```

3. Credentials konfigurieren:
   ```bash
   mkdir -p ~/.config/google-mcp
   cp credentials.json ~/.config/google-mcp/
   ```

4. Authentifizieren:
   ```bash
   python3 authenticate.py
   ```

5. Claude Desktop Config:
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

</details>

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
c8be61569d8605d15413c46522e4705ee7b25409b8143d0aeeef77bcc85f0843
```

Verwende diesen Hash um die Integrität des Bundles zu verifizieren.

**Hinweis:** Dieses Bundle enthält die OAuth Credentials für das Team. Verteile es nur intern.
