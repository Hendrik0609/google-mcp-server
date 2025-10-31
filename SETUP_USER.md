# Team-Mitglied Setup: Google MCP Server installieren

Diese Anleitung ist für **Team-Mitglieder**, die den MCP Server nutzen möchten.

## Voraussetzungen

- Claude Desktop installiert
- Python 3.11 oder höher
- Bundle `google-mcp-server.mcpb` vom Admin erhalten

## Schritt 1: Bundle installieren

### Option A: Via Claude Desktop (Empfohlen)

1. Öffne Claude Desktop
2. Doppelklicke auf `google-mcp-server.mcpb`
3. Claude Desktop fragt nach Installation → Bestätige
4. Fertig!

### Option B: Manuell

1. Öffne Claude Desktop Config:
   ```bash
   # macOS/Linux
   ~/.config/Claude/claude_desktop_config.json

   # Windows
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Füge den Server hinzu:
   ```json
   {
     "mcpServers": {
       "google": {
         "command": "python3",
         "args": ["/pfad/zum/server.py"]
       }
     }
   }
   ```

## Schritt 2: OAuth Autorisierung

Nach der Installation musst du **einmalig** deinen Google Account autorisieren:

1. Öffne Terminal/Kommandozeile

2. Führe das Authentifizierungs-Script aus:
   ```bash
   # Navigiere zum Bundle-Verzeichnis
   cd /pfad/wo/bundle/installiert/wurde

   # Führe authenticate.py aus
   python3 authenticate.py
   ```

3. **Browser öffnet sich automatisch:**
   - Wähle deinen Google Account (dein persönliches Gmail/Calendar)
   - Google fragt: "Team MCP Server möchte auf Gmail & Calendar zugreifen"
   - Klicke auf **"Zulassen"**

4. **Fertig!**
   - Terminal zeigt: "Authentifizierung erfolgreich!"
   - Dein Token wurde gespeichert unter: `~/.config/google-mcp/token.json`

## Schritt 3: Claude Desktop neu starten

1. Schließe Claude Desktop komplett
2. Starte Claude Desktop neu
3. Der Google MCP Server sollte jetzt verfügbar sein

## Schritt 4: Testen

Teste die Funktionalität in Claude Desktop:

```
"Sende eine Test-Email an mich selbst mit dem Betreff 'MCP Test'"
```

oder

```
"Erstelle einen Kalender-Termin für morgen um 14 Uhr: 'MCP Test Meeting'"
```

## Verfügbare Funktionen

Nach der Installation kann Claude:

### Gmail:
- ✉️ E-Mails senden
- 📝 Entwürfe erstellen
- 🎨 HTML-Formatierung nutzen
- 📧 CC/BCC verwenden

### Google Calendar:
- 📅 Events erstellen
- ✏️ Events bearbeiten
- 🗑️ Events löschen
- 👥 Teilnehmer einladen

## Troubleshooting

### "Token nicht gefunden"
→ Führe `python3 authenticate.py` aus (siehe Schritt 2)

### "Permission denied"
→ Stelle sicher, dass die Scopes korrekt autorisiert wurden. Lösche `~/.config/google-mcp/token.json` und autorisiere erneut.

### "Module not found"
→ Installiere Dependencies:
```bash
pip install -r requirements.txt
```

### Server erscheint nicht in Claude Desktop
→ Überprüfe die Config-Datei und starte Claude Desktop neu

## Sicherheit

- ✅ Dein `token.json` ist **persönlich** und nur auf deinem Rechner
- ✅ Nur **du** hast Zugriff auf dein Gmail/Calendar
- ✅ Der Admin kann **nicht** auf deine E-Mails/Kalender zugreifen
- ✅ Das Token läuft nach einiger Zeit ab und wird automatisch erneuert

## Support

Bei Problemen wende dich an deinen Team-Admin oder erstelle ein Issue im Repository.
