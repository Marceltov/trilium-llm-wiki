# Install and connect

## 1. Turn on Trilium Notes' MCP server

The plugin talks to the MCP server built into Trilium Notes 0.106+. Turn it on under *Options → AI / LLM → MCP server*; it serves `/mcp` on your Trilium Notes URL. Then pick how Claude signs in:

- **With an ETAPI token:** create one under *Options → ETAPI*. Nothing else to run.
- **With your Trilium Notes password (recommended):** put [trilium-mcp-proxy](https://trilium-mcp-proxy.marceltov.de/) in front of it, on your own server next to Trilium. It adds an OAuth login: you add its URL to any MCP client and log in once, with no token to create or paste. The login page is the proxy's own, so the password only goes from your browser to the proxy and on to your Trilium, never to Claude. Its README has the compose snippet.

## 2. Install the plugin

=== "Claude Code"

    ```
    /plugin marketplace add Marceltov/trilium-llm-wiki
    /plugin install trilium-llm-wiki
    ```

=== "claude.ai, desktop app, Cowork"

    1. Connect Trilium Notes as a custom connector: *Customize → Connectors → Add custom connector*, with trilium-mcp-proxy's public HTTPS URL ending in `/mcp`, then sign in with your Trilium Notes password on the proxy's login page.
    2. Open *Customize → Plugins*, click **Add**, choose *Add marketplace → Add from a repository* and enter `Marceltov/trilium-llm-wiki`.
    3. Open the `trilium-llm-wiki` plugin and click **Add**.

## 3. Connect your Trilium Notes instance (Claude Code)

Start a new session. If no Trilium Notes instance is configured, the plugin's `SessionStart` hook notices and Claude offers, once, to run the `trilium-manage-instances` skill. It asks how you connect and for the URL, and registers the instance as `trilium` with `claude mcp add`, scoped to your user. Through the proxy: restart Claude Code, run `/mcp`, pick `trilium` and choose **Authenticate**; a browser opens on the proxy's login page and you sign in with your Trilium Notes password. Directly: the skill asks for the ETAPI token and sends it as an `Authorization: Bearer` header.

Already using the [Trilium Notes plugin](https://trilium-plugin.marceltov.de/), or connected a `trilium` server some other way? Then nothing needs doing: both plugins use the same `trilium` server.

Several instances work the same way as in the Trilium Notes plugin: each one after the first gets a label and is registered as `trilium-<label>` (for example `trilium-work`); see its [Multiple instances](https://trilium-plugin.marceltov.de/multiple-instances/) page. The wiki lives in one of them, and Claude asks which when it isn't clear.

On claude.ai the setup hook does nothing; the connector is the connection.

## 4. Create the wiki

Ask Claude to "set up the LLM wiki", then continue with [Set up the wiki](setup.md).
