# Installationsanleitung für Endnutzer

## Schnellstart

### 1. Bundle herunterladen

Lade `google-mcp-server.mcpb` von den [GitHub Releases](https://github.com/USERNAME/google-mcp-server/releases) herunter.

### 2. Google OAuth einrichten

**Wichtig:** Du benötigst eigene Google Cloud Credentials!

#### 2.1 Google Cloud Project erstellen

1. Gehe zu https://console.cloud.google.com
2. Erstelle ein neues Projekt (oder wähle ein bestehendes)
3. Notiere dir die Projekt-ID

#### 2.2 APIs aktivieren

1. Gehe zu "APIs & Services" → "Library"
2. Suche und aktiviere:
   - **Gmail API**
   - **Google Calendar API**

#### 2.3 OAuth Credentials erstellen

1. Gehe zu "APIs & Services" → "Credentials"
2. Klicke "+ CREATE CREDENTIALS" → "OAuth client ID"
3. Wähle "Desktop app" als Application type
4. Name: "Google MCP Server"
5. Klicke "Create"
6. **Download** die credentials.json Datei

#### 2.4 Credentials speichern

```bash
# Ordner erstellen
mkdir -p ~/.config/google-mcp

# credentials.json dahin kopieren
cp ~/Downloads/credentials.json ~/.config/google-mcp/
```

### 3. Bundle in Claude Desktop installieren

#### macOS / Windows:
1. Doppelklick auf `google-mcp-server.mcpb`
2. Claude Desktop öffnet sich automatisch
3. Klicke "Install"
4. Fertig!

#### Linux / Manuell:
Falls die automatische Installation nicht funktioniert, kannst du das Bundle manuell entpacken:

```bash
# MCPB CLI installieren
npm install -g @anthropic-ai/mcpb

# Bundle entpacken
mcpb unpack google-mcp-server.mcpb ~/.local/share/google-mcp-server

# In Claude Desktop Config eintragen
```

Füge in `~/.config/claude/claude_desktop_config.json` hinzu:
```json
{
  "mcpServers": {
    "google": {
      "command": "python3",
      "args": ["~/.local/share/google-mcp-server/start.py"]
    }
  }
}
```

### 4. Erste Authentifizierung

**Wichtig:** Dieser Schritt muss VOR der ersten Nutzung durchgeführt werden!

```bash
# Zum entpackten Bundle navigieren
cd ~/.local/share/google-mcp-server  # Linux
# oder: C:\Users\USERNAME\AppData\Local\google-mcp-server  # Windows
# oder: ~/Library/Application Support/google-mcp-server  # macOS

# Python Dependencies installieren
pip3 install -r requirements.txt

# Authentifizierung durchführen
python3 authenticate.py
```

Dies öffnet einen Browser, wo du:
1. Dich mit deinem Google-Account anmeldest
2. Die Berechtigungen bestätigst (Gmail, Calendar)
3. Das Token wird automatisch gespeichert

### 5. Claude Desktop neu starten

Starte Claude Desktop neu, damit der MCP Server geladen wird.

## Verwendung

Nach erfolgreicher Installation kannst du Claude z.B. fragen:

- "Sende eine E-Mail an person@example.com mit dem Betreff 'Meeting' und dem Text 'Hallo'"
- "Erstelle einen Calendar-Termin für morgen um 14 Uhr"
- "Erstelle einen E-Mail-Entwurf für..."

## Troubleshooting

### "Token not found" Fehler
→ Du hast Schritt 4 (Erste Authentifizierung) übersprungen. Führe `python3 authenticate.py` aus.

### "credentials.json not found"
→ Du hast die Google OAuth Credentials nicht korrekt gespeichert. Siehe Schritt 2.4.

### "Module 'mcp' not found"
→ Dependencies wurden nicht installiert. Führe `pip3 install -r requirements.txt` aus.

### Python nicht gefunden
→ Installiere Python 3.11 oder höher von https://python.org

### Bundle lässt sich nicht öffnen
→ Nutze die manuelle Installation (siehe "Linux / Manuell" unter Schritt 3)

## Sicherheit

- Deine Google Credentials bleiben lokal auf deinem Computer
- Tokens werden verschlüsselt in `~/.config/google-mcp/` gespeichert
- Der MCP Server hat nur Zugriff auf die von dir autorisierten APIs
- Du kannst den Zugriff jederzeit widerrufen unter https://myaccount.google.com/permissions

## Deinstallation

### Claude Desktop:
Settings → Connectors → Google MCP Server → Remove

### Manuell:
```bash
# Bundle entfernen
rm -rf ~/.local/share/google-mcp-server  # Linux
# oder entsprechender Pfad für Windows/macOS

# Tokens entfernen (optional)
rm -rf ~/.config/google-mcp
```

## Support

Bei Problemen erstelle bitte ein Issue auf GitHub: https://github.com/USERNAME/google-mcp-server/issues
