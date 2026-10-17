# Install and connect

## 1. Deploy the Trilium Notes MCP server

The plugin talks to Trilium Notes through a running [Trilium Notes MCP server](https://trilium-mcp.marceltov.de/). Set it up with its [quick start](https://trilium-mcp.marceltov.de/getting-started/) and enable OAuth on it (`MCP_BASE_URL` and `MCP_OAUTH_SECRET`), so Claude signs in with your Trilium Notes password and you don't need an ETAPI token.

## 2. Install the plugin

=== "Claude Code"

    ```
    /plugin marketplace add Marceltov/trilium-llm-wiki
    /plugin install trilium-llm-wiki
    ```

=== "claude.ai, desktop app, Cowork"

    1. Connect the Trilium Notes MCP server as a custom connector. Claude.ai signs in with OAuth, so the server needs `MCP_BASE_URL` and `MCP_OAUTH_SECRET` set and a public HTTPS URL. The steps are in [Claude.ai](https://trilium-mcp.marceltov.de/claude-ai/) in the MCP server docs.
    2. Open *Customize → Plugins*, click **Add**, choose *Add marketplace → Add from a repository* and enter `Marceltov/trilium-llm-wiki`.
    3. Open the `trilium-llm-wiki` plugin and click **Add**.

## 3. Connect your Trilium Notes instance (Claude Code)

Start a new session. If no Trilium Notes instance is configured, the plugin's `SessionStart` hook notices and Claude offers, once, to run the `trilium-manage-instances` skill. It asks for the MCP server URL and registers the instance as `trilium` with `claude mcp add`, scoped to your user. Restart Claude Code, run `/mcp`, pick `trilium` and choose **Authenticate**: a browser opens and you sign in with your Trilium Notes password.

If your MCP server has no OAuth, the skill asks for an ETAPI token (*Options → ETAPI* in Trilium Notes) instead and sends it as a header.

Already using the [Trilium Notes plugin](https://trilium-plugin.marceltov.de/)? Then the connection exists and nothing needs doing: both plugins use the same `trilium` server.

Several instances (for example `trilium-work`) work the same way as in the Trilium Notes plugin; see its [Multiple instances](https://trilium-plugin.marceltov.de/multiple-instances/) page. The wiki lives in one of them, and Claude asks which when it isn't clear.

On claude.ai the setup hook does nothing; the connector is the connection.

## 4. Create the wiki

Ask Claude to "set up the LLM wiki", then continue with [Set up the wiki](setup.md).
