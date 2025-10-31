# Google MCP Server Bundle

Dieses Verzeichnis enthält alle Dateien, die ins MCPB Bundle gepackt werden.

## Dateien

- `server.py` - Haupt-MCP-Server
- `authenticate.py` - OAuth Authentifizierungs-Script
- `setup.py` - Dependency-Installation
- `start.py` - Startup-Wrapper
- `requirements.txt` - Python Dependencies
- `manifest.json` - Bundle Metadaten
- `credentials.json` - **OAuth Credentials (vom Admin eingefügt)**
- `credentials.json.template` - Template für credentials.json

## Für Admins: Bundle erstellen

1. **Credentials einfügen:**
   ```bash
   # Kopiere deine credentials.json ins Bundle-Verzeichnis
   cp ~/Downloads/credentials.json ./credentials.json
   ```

2. **Bundle packen:**
   ```bash
   cd ..
   mcpb pack bundle google-mcp-server.mcpb
   ```

3. **Hash generieren:**
   ```bash
   sha256sum google-mcp-server.mcpb
   ```

## Wichtig

- `credentials.json` wird **nicht** ins Git eingecheckt (siehe .gitignore)
- `credentials.json` wird **nur** im finalen Bundle enthalten sein
- Jeder Nutzer muss trotzdem individuell autorisieren (`authenticate.py`)
