# Release Anleitung

## GitHub Release erstellen

### 1. Repository auf GitHub erstellen

```bash
# Git initialisieren (falls noch nicht geschehen)
git init
git add .
git commit -m "Initial commit: Google MCP Server with MCPB bundle"

# Remote hinzufügen
git remote add origin https://github.com/USERNAME/google-mcp-server.git
git branch -M main
git push -u origin main
```

### 2. Release erstellen

1. Gehe zu GitHub → dein Repository → Releases
2. Klicke "Create a new release"
3. **Tag**: `v1.0.0`
4. **Release Title**: `Google MCP Server v1.0.0`
5. **Description**:
   ```markdown
   # Google MCP Server v1.0.0

   MCP Server für Gmail und Google Calendar mit Schreibzugriff.

   ## Features
   - E-Mails senden via Gmail
   - Entwürfe erstellen
   - Calendar Events erstellen, bearbeiten, löschen

   ## Installation
   1. .mcpb Bundle herunterladen
   2. Mit Claude Desktop öffnen
   3. OAuth Setup durchführen (siehe README)

   ## SHA-256
   ```
   605e44e94c082cd08433105ceacce2e1bf3558b0526ccc528290de09220c018a
   ```
   ```

6. **Assets**: `google-mcp-server.mcpb` hochladen

### 3. MCP Registry (Optional)

Falls du den Server im offiziellen MCP Registry veröffentlichen möchtest:

1. Erstelle `server.json`:
   ```json
   {
     "name": "io.github.USERNAME/google-mcp-server",
     "packages": [
       {
         "registry_type": "mcpb",
         "identifier": "https://github.com/USERNAME/google-mcp-server/releases/download/v1.0.0/google-mcp-server.mcpb",
         "file_sha256": "605e44e94c082cd08433105ceacce2e1bf3558b0526ccc528290de09220c018a"
       }
     ]
   }
   ```

2. Pull Request im MCP Registry Repository erstellen

## Für neue Releases

```bash
# Bundle neu bauen
cd bundle
mcpb pack . ../google-mcp-server.mcpb

# SHA-256 generieren
cd ..
sha256sum google-mcp-server.mcpb

# Version in manifest.json erhöhen
# Dann neues Release auf GitHub erstellen
```

## Bundle signieren (Optional)

Für zusätzliche Sicherheit kannst du das Bundle signieren:

```bash
# Schlüssel generieren (einmalig)
openssl genrsa -out private-key.pem 2048
openssl rsa -in private-key.pem -pubout -out public-key.pem

# Bundle signieren
mcpb sign --key private-key.pem google-mcp-server.mcpb

# Verifizieren
mcpb verify google-mcp-server.mcpb
```

Den Public Key dann im README veröffentlichen, damit Nutzer das Bundle verifizieren können.
