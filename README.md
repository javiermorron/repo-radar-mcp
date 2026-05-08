# Repo Radar MCP

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![MCP](https://img.shields.io/badge/MCP-Compatible-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Discover, rank and compare GitHub repositories from any MCP-compatible AI client.

**Repo Radar MCP** is a Python-based MCP server that connects AI agents to the GitHub API, allowing them to search, filter, rank and evaluate open-source repositories by topic, language, stars, license, activity and relevance.

It is designed for developers, builders and AI agents that need a structured way to research open-source projects.

---

## Why Repo Radar MCP?

AI agents can write code, but they also need good technical context.

Repo Radar MCP gives your MCP-compatible client a simple set of tools to answer questions like:

- What are the most popular Python repositories about RAG?
- Which MCP servers are worth studying?
- What GitHub projects are active, licensed and useful?
- Which repository should I use as a reference for my next project?
- How do several repositories compare by stars, forks, issues, license and recent activity?

---

## Features

- Search GitHub repositories by topic.
- Filter by programming language.
- Filter by minimum stars.
- Rank repositories with a simple usefulness score.
- Analyze a single repository.
- Compare multiple repositories.
- Fetch repository README content.
- Return results as JSON or Markdown.
- Uses your GitHub token safely from environment variables.
- Works with MCP Inspector, Claude Desktop, Cursor and other MCP-compatible clients.

---

## MCP Tools

| Tool | Description |
|---|---|
| `search_repositories` | Search GitHub repositories by topic, language, stars and sorting mode. |
| `search_repositories_markdown` | Same as above, but returns a clean Markdown report. |
| `rank_repositories` | Search repositories and add a practical repository score. |
| `rank_repositories_markdown` | Search, rank and return repositories as Markdown. |
| `analyze_repository` | Analyze one repository by `owner/name`. |
| `analyze_repository_markdown` | Analyze one repository and return a Markdown report. |
| `compare_repositories` | Compare several repositories by `owner/name`. |
| `compare_repositories_markdown` | Compare several repositories and return a Markdown table. |
| `get_repository_readme` | Fetch the README of a repository. |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/javiermorron/repo-radar-mcp.git
cd repo-radar-mcp
```

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
pip install -e .
```

Copy the environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
copy .env.example .env
```

Edit `.env` and add your GitHub token:

```env
GITHUB_TOKEN=your_github_token_here
GITHUB_API_VERSION=2022-11-28
GITHUB_USER_AGENT=repo-radar-mcp/1.0.0
```

Never commit your real `.env` file.

---

## Run with MCP Inspector

From the project root:

```bash
mcp dev server.py
```

If the Inspector does not find `uv`, use this configuration in the Inspector:

```text
Transport Type: STDIO
Command: python
Arguments: server.py
```

Then open the **Tools** tab and run:

```json
{
  "topic": "mcp server",
  "language": "Python",
  "limit": 5,
  "min_stars": 10
}
```

---

## Claude Desktop Example

A sample configuration is available in:

```text
examples/claude_desktop_config.example.json
```

Example Windows entry:

```json
{
  "mcpServers": {
    "repo-radar-mcp": {
      "command": "C:\\Users\\YOUR_USER\\repo-radar-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YOUR_USER\\repo-radar-mcp\\server.py"
      ]
    }
  }
}
```

---

## Example Prompts

```text
Search the 5 most popular Python repositories about "mcp server" and explain which one is best to study.
```

```text
Compare these repositories: freqtrade/freqtrade, ccxt/ccxt, hummingbot/hummingbot.
```

```text
Find popular repositories about "rag chatbot" in Python with more than 500 stars and rank them by usefulness.
```

```text
Analyze microsoft/autogen and tell me if it is active, useful and worth studying.
```

More prompts are available in:

```text
examples/prompts.md
```

---

## Repository Score

Repo Radar MCP includes a simple scoring system based on:

- Stars
- Forks
- Recent activity
- License availability
- Open issues
- Archived status

The score is not meant to replace human judgment. It is a quick signal to help agents and developers prioritize what to inspect first.

---

## Project Structure

```text
repo-radar-mcp/
├── src/
│   └── repo_radar_mcp/
│       ├── __init__.py
│       ├── server.py
│       ├── github_client.py
│       ├── scoring.py
│       ├── formatters.py
│       └── models.py
├── examples/
│   ├── claude_desktop_config.example.json
│   └── prompts.md
├── tests/
│   └── test_scoring.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── pyproject.toml
└── server.py
```

---

## Roadmap

- Add repository release analysis.
- Add issue quality analysis.
- Add contributor activity metrics.
- Add support for GitHub topics recommendations.
- Add repository health report.
- Add CSV and JSON export helpers.
- Add Docker support.
- Add GitHub Actions for tests and linting.

---

## Security

Repo Radar MCP uses a GitHub token from environment variables.

Do not commit:

- `.env`
- Personal access tokens
- Private API keys
- Local virtual environments

The `.gitignore` file already excludes common sensitive and generated files.

---

## Contributing

Contributions are welcome.

Good first issues:

- Improve scoring logic.
- Add more output formats.
- Add tests.
- Improve MCP client examples.
- Add Docker support.

---

## License

This project is licensed under the MIT License.

Created by Javier Morrón. Connect with me on LinkedIn: https://www.linkedin.com/in/javiermorron.
