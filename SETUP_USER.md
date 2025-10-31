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

Nach der Installation musst du **einmalig** deinen Google Account autorisieren.

### Option A: Automatisch beim ersten Start (Empfohlen!)

1. **Starte Claude Desktop einfach**
2. **Versuche den Server zu nutzen** (z.B. "Sende eine Test-Email an mich")
3. **Claude Desktop Logs zeigen:**
   ```
   🔐 GOOGLE AUTHENTIFIZIERUNG ERFORDERLICH
   ============================================================

   1. Öffne: https://www.google.com/device
   2. Gib diesen Code ein: ABCD-EFGH

   3. Autorisiere den Zugriff auf Gmail & Calendar

   Warte auf Autorisierung...
   ```

4. **Gehe zu google.com/device:**
   - Gib den angezeigten Code ein
   - Wähle deinen Google Account
   - Klicke auf **"Zulassen"**

5. **Fertig!** Claude Desktop funktioniert jetzt automatisch.

### Option B: Manuell vorab (Optional)

Wenn du die Authentifizierung vorab durchführen möchtest:

```bash
# Navigiere zum Bundle-Verzeichnis
cd /pfad/wo/bundle/installiert/wurde

# Führe authenticate.py aus
python3 authenticate.py
```

Das Script zeigt dir den gleichen Code und Link an.

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

### "Token nicht gefunden" / Authentifizierung wird angefordert
→ Das ist normal beim ersten Start! Folge einfach den Anweisungen in den Claude Desktop Logs (siehe Schritt 2, Option A)

### "Permission denied"
→ Stelle sicher, dass die Scopes korrekt autorisiert wurden. Lösche `~/.config/google-mcp/token.json` und autorisiere erneut.

### Wo finde ich die Claude Desktop Logs?
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log

# Linux
tail -f ~/.config/Claude/logs/mcp*.log
```

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
