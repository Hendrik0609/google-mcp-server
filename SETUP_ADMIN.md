# Admin Setup: Google Cloud Projekt einrichten

Diese Anleitung ist **nur für den Team-Admin** gedacht. Führe diese Schritte **einmalig** aus, um das zentrale Google Cloud Projekt zu konfigurieren.

## Schritt 1: Google Cloud Projekt erstellen

1. Gehe zu [Google Cloud Console](https://console.cloud.google.com)
2. Klicke auf **"Neues Projekt"** (oben links)
3. Name: `Team MCP Server` (oder beliebiger Name)
4. Klicke auf **"Erstellen"**

## Schritt 2: APIs aktivieren

1. Wähle dein neues Projekt aus (oben in der Navigation)
2. Gehe zu **"APIs & Dienste" → "Bibliothek"**
3. Suche und aktiviere:
   - **Gmail API**
   - **Google Calendar API**

## Schritt 3: OAuth Consent Screen konfigurieren

1. Gehe zu **"APIs & Dienste" → "OAuth-Zustimmungsbildschirm"**
2. Wähle **"Intern"** (wenn G Suite/Workspace) oder **"Extern"**
3. Fülle aus:
   - App-Name: `Team MCP Server`
   - Support-E-Mail: Deine E-Mail
   - Entwickler-Kontakt: Deine E-Mail
4. Klicke auf **"Speichern und fortfahren"**

5. **Scopes hinzufügen:**
   - Klicke auf **"Scopes hinzufügen oder entfernen"**
   - Wähle folgende Scopes:
     - `https://www.googleapis.com/auth/gmail.send`
     - `https://www.googleapis.com/auth/gmail.readonly`
     - `https://www.googleapis.com/auth/gmail.compose`
     - `https://www.googleapis.com/auth/calendar`
     - `https://www.googleapis.com/auth/calendar.events`
   - Klicke auf **"Aktualisieren"**

6. Klicke auf **"Speichern und fortfahren"**

## Schritt 4: OAuth 2.0 Credentials erstellen

1. Gehe zu **"APIs & Dienste" → "Anmeldedaten"**
2. Klicke auf **"+ Anmeldedaten erstellen"**
3. Wähle **"OAuth-Client-ID"**
4. Anwendungstyp: **"Desktop-App"**
5. Name: `MCP Server Client`
6. Klicke auf **"Erstellen"**

7. **Credentials herunterladen:**
   - Klicke auf das Download-Symbol (⬇️) neben dem neuen Client
   - Speichere als `credentials.json`

## Schritt 5: Credentials ins Bundle integrieren

1. **Kopiere die heruntergeladene `credentials.json` ins Bundle-Verzeichnis:**
   ```bash
   # macOS/Linux
   cp ~/Downloads/credentials.json /pfad/zum/google-mcp-server/bundle/credentials.json

   # Windows
   copy %USERPROFILE%\Downloads\credentials.json C:\pfad\zum\google-mcp-server\bundle\credentials.json
   ```

2. **Überprüfe, dass die Datei korrekt ist:**
   ```bash
   cat bundle/credentials.json
   ```

   Sie sollte etwa so aussehen:
   ```json
   {
     "installed": {
       "client_id": "123456789.apps.googleusercontent.com",
       "project_id": "your-project-id",
       "client_secret": "GOCSPX-...",
       ...
     }
   }
   ```

3. **Erstelle das Bundle neu:**
   ```bash
   cd /pfad/zum/google-mcp-server
   mcpb pack bundle google-mcp-server.mcpb
   ```

4. **Generiere neuen SHA-256 Hash:**
   ```bash
   # macOS/Linux
   sha256sum google-mcp-server.mcpb

   # Windows
   certutil -hashfile google-mcp-server.mcpb SHA256
   ```

5. **Aktualisiere den Hash in `README.md`:**
   Ersetze den alten Hash mit dem neuen Wert

## Schritt 6: Bundle verteilen

Das Bundle `google-mcp-server.mcpb` enthält jetzt die gemeinsamen OAuth Credentials.

**Verteile das Bundle an dein Team via:**
- Internes Fileshare
- Git Repository (privat!)
- Oder direkter Download-Link

**Wichtig:**
- ⚠️ Teile das Bundle **nur intern** im Team
- ⚠️ Veröffentliche es **nicht öffentlich** (GitHub Public, etc.)
- ✅ Jedes Team-Mitglied muss trotzdem individuell autorisieren
- ✅ Jeder nutzt sein eigenes Gmail/Calendar

## Nächste Schritte

Sende deinem Team:
1. Das Bundle `google-mcp-server.mcpb`
2. Die Anleitung `SETUP_USER.md`

Fertig! Dein Team kann jetzt den MCP Server nutzen.
