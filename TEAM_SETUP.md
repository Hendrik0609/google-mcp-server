# Team Setup - Übersicht

Dieses Dokument erklärt das neue Team-Setup-Modell für den Google MCP Server.

## Konzept

**Ein zentrales Google Cloud Projekt für das ganze Team**, aber **jeder Nutzer authentifiziert individuell** seinen eigenen Gmail/Calendar-Account.

## Vorteile

✅ **Für den Admin:**
- Einmalige Konfiguration des Google Cloud Projekts
- Zentrale Verwaltung der OAuth Credentials
- Keine individuellen Projekte für jedes Team-Mitglied

✅ **Für Team-Mitglieder:**
- Kein Google Cloud Projekt erstellen nötig
- Einfache Installation via Bundle
- Volle Kontrolle über eigenes Gmail/Calendar
- Keine geteilten Zugangsdaten

✅ **Sicherheit:**
- Jeder Nutzer hat sein eigenes Token
- Tokens sind lokal auf jedem Rechner gespeichert
- Admin kann nicht auf E-Mails/Kalender der Nutzer zugreifen
- OAuth Credentials (Client ID/Secret) sind nicht kritisch

## Ablauf

### 1. Admin (einmalig)

1. Erstellt Google Cloud Projekt
2. Aktiviert Gmail & Calendar APIs
3. Konfiguriert OAuth Consent Screen
4. Erstellt OAuth 2.0 Client (Desktop App)
5. Lädt `credentials.json` herunter
6. Fügt `credentials.json` ins Bundle ein
7. Packt Bundle neu
8. Verteilt Bundle ans Team

📖 **Detaillierte Anleitung:** [SETUP_ADMIN.md](SETUP_ADMIN.md)

### 2. Team-Mitglieder (jeder einzeln)

1. Erhält Bundle vom Admin
2. Installiert Bundle in Claude Desktop
3. Führt `authenticate.py` aus
4. Browser öffnet sich → mit eigenem Google Account einloggen
5. Autorisiert Zugriff auf eigenes Gmail/Calendar
6. Fertig! Claude kann jetzt Gmail/Calendar nutzen

📖 **Detaillierte Anleitung:** [SETUP_USER.md](SETUP_USER.md)

## Dateien

```
google-mcp-server/
├── SETUP_ADMIN.md          # Für Team-Admins
├── SETUP_USER.md           # Für Team-Mitglieder
├── TEAM_SETUP.md           # Diese Übersicht
├── README.md               # Haupt-Dokumentation
├── bundle/
│   ├── credentials.json    # ← Wird vom Admin eingefügt
│   ├── server.py           # Sucht credentials.json im gleichen Verzeichnis
│   ├── authenticate.py     # Sucht credentials.json im gleichen Verzeichnis
│   └── ...
└── google-mcp-server.mcpb  # Fertiges Bundle mit credentials.json
```

## Technische Details

### credentials.json

- Enthält: Client ID, Client Secret, OAuth Endpoints
- Ist: Öffentlich teilbar innerhalb des Teams
- Ist nicht: Personenbezogen oder kritisch
- Ermöglicht: OAuth-Flow für beliebige Google Accounts

### token.json (pro Nutzer)

- Enthält: Access Token, Refresh Token
- Ist: Persönlich und vertraulich
- Wird gespeichert: `~/.config/google-mcp/token.json`
- Ermöglicht: Zugriff auf den spezifischen Gmail/Calendar-Account

### OAuth Flow

1. Nutzer startet `authenticate.py`
2. Script liest `credentials.json` (vom Admin bereitgestellt)
3. Browser öffnet sich mit Google Login
4. Nutzer wählt seinen Account und autorisiert
5. Google gibt Access Token zurück
6. Token wird lokal als `token.json` gespeichert
7. Server nutzt dieses Token für API-Calls

## Sicherheitshinweise

⚠️ **Bundle intern verteilen**
- Teile das Bundle nur intern im Team
- Veröffentliche es nicht öffentlich (GitHub Public, etc.)

✅ **Credentials sind nicht kritisch**
- `credentials.json` enthält keine Passwörter
- Selbst wenn jemand die Client-Credentials hat, muss er trotzdem OAuth autorisieren
- Google zeigt dabei deutlich, welcher App Zugriff gegeben wird

✅ **Tokens sind geschützt**
- Jedes `token.json` ist individuell und lokal
- Admin hat keinen Zugriff auf User-Tokens
- Tokens können jederzeit widerrufen werden (Google Account → Sicherheit)

## FAQ

**Q: Kann der Admin meine E-Mails lesen?**
A: Nein. Der Admin stellt nur die OAuth Credentials bereit. Dein Token ist lokal und nur du hast Zugriff darauf.

**Q: Was passiert, wenn credentials.json geleakt wird?**
A: Das ist nicht kritisch. Ein Angreifer müsste trotzdem jeden Google Account individuell autorisieren lassen, was in der Google Consent-Screen-UI sichtbar wäre.

**Q: Kann ich den Zugriff widerrufen?**
A: Ja. Gehe zu myaccount.google.com → Sicherheit → Apps mit Kontozugriff → "Team MCP Server" entfernen.

**Q: Muss ich authenticate.py jedes Mal ausführen?**
A: Nein, nur einmal. Das Token wird automatisch erneuert wenn es abläuft.

**Q: Funktioniert das mit G Suite / Workspace?**
A: Ja! Der Admin sollte beim OAuth Consent Screen "Intern" wählen, dann ist die App nur für die Organisation verfügbar.
