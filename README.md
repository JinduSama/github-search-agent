# GitHub Search Agent

A GitHub Copilot Agent that helps you discover and evaluate GitHub repositories based on natural language queries. The agent uses a Python tool to interact with the GitHub API and provides intelligent recommendations.

## Features

- 🔍 **Natural Language Search**: Describe what you're looking for in plain English
- 🎯 **Smart Filtering**: Filter by language, stars, topics, and more
- 📖 **README Analysis**: Automatically fetches and analyzes repository READMEs
- 📊 **Quality Metrics**: Evaluates repositories based on stars, activity, and maintenance
- 📝 **Detailed Recommendations**: Get ranked suggestions with justifications

## Project Structure

```
github-search-agent/
├── .github/
│   └── agents/
│       └── github-search.agent.md    # Agent definition and instructions
├── scripts/
│   └── github_search_tool.py         # Python tool for GitHub API
├── pyproject.toml                    # Package configuration (uv)
├── plan.md                           # Project planning document
└── README.md                         # This file
```

## Setup

### Prerequisites

- Python 3.10 or later
- GitHub account with API access
- GitHub CLI (`gh`) installed (optional, for easy authentication)

### Installation

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd github-search-agent
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Activate the virtual environment**:
   ```bash
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

### Using pip

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd github-search-agent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install .
   ```

### Authentication

The tool requires GitHub API access. Choose one of these methods:

#### Option 1: GitHub CLI (Recommended)

If you have the GitHub CLI installed and authenticated:
```bash
gh auth login
```

The tool will automatically use your `gh` authentication.

#### Option 2: Environment Variable

Set a personal access token:
```bash
# On Windows (PowerShell)
$env:GITHUB_TOKEN = "ghp_your_token_here"

# On Windows (Command Prompt)
set GITHUB_TOKEN=ghp_your_token_here

# On macOS/Linux
export GITHUB_TOKEN="ghp_your_token_here"
```

**Note**: For basic repository search, you can use the API without authentication, but you'll have lower rate limits.

## Usage

### Using the Agent

The agent is defined in `.github/agents/github-search.agent.md` and can be used with GitHub Copilot in compatible environments.

Example prompts:
- "Find me a Python library for working with Excel files"
- "I need a lightweight React component library with TypeScript support"
- "Looking for a well-maintained Go framework for building REST APIs"

### Using the Python Tool Directly

You can also run the search tool directly:

```bash
# Basic search
python scripts/github_search_tool.py '{"keywords": "python web framework"}'

# With filters
python scripts/github_search_tool.py '{"keywords": "react components", "language": "typescript", "min_stars": 1000}'

# Pretty-printed output
python scripts/github_search_tool.py --pretty '{"keywords": "rust cli", "min_stars": 500}'

# Using the installed script (if using uv sync or pip install)
github-search '{"keywords": "python web framework"}'
```

### Search Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keywords` | string | Yes | - | Search keywords or phrases |
| `language` | string | No | - | Filter by programming language |
| `min_stars` | integer | No | 0 | Minimum number of stars |
| `topic` | string | No | - | Filter by GitHub topic tag |
| `sort_by` | string | No | "stars" | Sort order: `stars`, `forks`, `updated`, `help-wanted-issues` |
| `max_results` | integer | No | 5 | Maximum results (max 10) |
| `include_readme` | boolean | No | true | Fetch README content |

### Example Output

```json
{
  "success": true,
  "count": 2,
  "repositories": [
    {
      "name": "example-repo",
      "full_name": "owner/example-repo",
      "description": "An example repository",
      "url": "https://github.com/owner/example-repo",
      "stars": 15000,
      "forks": 2000,
      "language": "Python",
      "topics": ["python", "example"],
      "created_at": "2020-01-01T00:00:00Z",
      "updated_at": "2024-12-20T00:00:00Z",
      "pushed_at": "2024-12-20T00:00:00Z",
      "open_issues": 50,
      "license": "MIT",
      "readme": "# Example Repo\n\nThis is the README content..."
    }
  ]
}
```

## How It Works

1. **User Query**: You describe what kind of repository you're looking for
2. **Agent Processing**: The GitHub Search Agent interprets your request
3. **Tool Execution**: The Python script queries the GitHub Search API
4. **Data Retrieval**: Repository metadata and READMEs are fetched
5. **Analysis**: The agent analyzes the results
6. **Recommendations**: You receive ranked suggestions with explanations

## Rate Limits

- **Unauthenticated**: 10 requests per minute for search API
- **Authenticated**: 30 requests per minute for search API

The tool is designed to be efficient and typically needs only one search request per query.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

MIT License - see LICENSE file for details.
