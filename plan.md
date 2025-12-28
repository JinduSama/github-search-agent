# Github Search Agent (Tool-Based Architecture)

This document outlines the plan to create a Github search agent defined as a configuration in `.github/agents/` that utilizes local Python scripts as tools.

## Basic Features

1. **Agent Definition**: The agent lives in `.github/agents/github-search.agent.md`. This file defines the agent's persona, instructions, and the schema for the tools it can call.
2. **Python Search Tool**: A Python script that handles the complex logic of interacting with the GitHub Search API, filtering results, and fetching README content.
3. **Dynamic Filtering**: The agent (LLM) extracts search parameters (language, stars, keywords) from user natural language and passes them as arguments to the Python tool.
4. **Content Analysis**: Once the Python tool returns the raw data (READMEs and metadata), the agent analyzes the content to determine the best fit for the user's request.
5. **Markdown Output**: The agent generates a final, polished response in Markdown format, including justifications for each suggestion.

## Technical Architecture & Strategy

1.  **Agent Configuration**: 
    *   **File**: `.github/agents/github-search.agent.md`
    *   **Role**: Orchestrator. It interprets user intent and decides when and how to call the search tool.
2.  **Tool Execution (Python)**:
    *   **File**: `scripts/github_search_tool.py`
    *   **Function**: Performs authenticated requests to GitHub API using `PyGithub` or `httpx`.
    *   **Local Execution**: The script runs on the user's local resources, avoiding the need for centralized hosting.
3.  **Data Flow**:
    *   **User Query** -> **Agent** (LLM)
    *   **Agent** -> **Python Tool** (with JSON arguments: `keywords`, `filters`)
    *   **Python Tool** -> **GitHub API** -> **Raw Data**
    *   **Raw Data** -> **Agent** (LLM for analysis)
    *   **Agent** -> **User** (Final Markdown Response)
4.  **Authentication**: The Python tool uses the user's local environment variables or GitHub CLI (`gh auth token`) to authenticate API requests.

## Used Technologies

- **GitHub Copilot Agent**: Defined via Markdown instructions.
- **Python 3.x**: For the core search and data preparation logic.
- **PyGithub / httpx**: For robust GitHub API interaction.
- **GitHub CLI (gh)**: (Optional) For seamless local authentication.
- **JSON**: For structured communication between the Agent and the Python tool.
