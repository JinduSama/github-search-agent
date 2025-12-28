#!/usr/bin/env python3
"""
GitHub Search Tool

A command-line tool for searching GitHub repositories with advanced filtering
and README content retrieval. Designed to be used as a tool by AI agents.

Usage:
    python github_search_tool.py '<json_parameters>'

Example:
    python github_search_tool.py '{"keywords": "python web framework", "min_stars": 1000}'
"""

import argparse
import base64
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from urllib.parse import quote

import httpx


@dataclass
class SearchParameters:
    """Parameters for GitHub repository search."""
    keywords: str
    language: Optional[str] = None
    min_stars: int = 0
    topic: Optional[str] = None
    sort_by: str = "stars"
    max_results: int = 5
    include_readme: bool = True


@dataclass
class Repository:
    """Represents a GitHub repository with metadata."""
    name: str
    full_name: str
    description: Optional[str]
    url: str
    stars: int
    forks: int
    language: Optional[str]
    topics: list[str]
    created_at: str
    updated_at: str
    pushed_at: str
    open_issues: int
    license: Optional[str]
    readme_content: Optional[str] = None


class GitHubSearchTool:
    """Tool for searching GitHub repositories and fetching details."""
    
    API_BASE = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize the GitHub search tool.
        
        Args:
            token: GitHub personal access token. If not provided,
                   attempts to get it from environment or GitHub CLI.
        """
        self.token = token or self._get_token()
        self.client = httpx.Client(
            base_url=self.API_BASE,
            headers=self._build_headers(),
            timeout=30.0
        )
    
    def _get_token(self) -> Optional[str]:
        """Get GitHub token from environment or GitHub CLI."""
        # Try environment variable first
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            return token
        
        # Try GitHub CLI
        try:
            result = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return None
    
    def _build_headers(self) -> dict[str, str]:
        """Build HTTP headers for GitHub API requests."""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "GitHub-Search-Agent-Tool/1.0"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _build_search_query(self, params: SearchParameters) -> str:
        """Build GitHub search query string from parameters."""
        query_parts = [params.keywords]
        
        if params.language:
            query_parts.append(f"language:{params.language}")
        
        if params.min_stars > 0:
            query_parts.append(f"stars:>={params.min_stars}")
        
        if params.topic:
            query_parts.append(f"topic:{params.topic}")
        
        return " ".join(query_parts)
    
    def search_repositories(self, params: SearchParameters) -> list[Repository]:
        """
        Search GitHub repositories based on parameters.
        
        Args:
            params: Search parameters including keywords, filters, and options.
            
        Returns:
            List of Repository objects matching the search criteria.
        """
        query = self._build_search_query(params)
        
        # Map sort_by to GitHub API format
        sort_mapping = {
            "stars": "stars",
            "forks": "forks",
            "updated": "updated",
            "help-wanted-issues": "help-wanted-issues"
        }
        sort = sort_mapping.get(params.sort_by, "stars")
        
        try:
            response = self.client.get(
                "/search/repositories",
                params={
                    "q": query,
                    "sort": sort,
                    "order": "desc",
                    "per_page": min(params.max_results, 10)
                }
            )
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"GitHub API error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise RuntimeError(f"Request failed: {str(e)}")
        
        repositories = []
        for item in data.get("items", []):
            repo = Repository(
                name=item["name"],
                full_name=item["full_name"],
                description=item.get("description"),
                url=item["html_url"],
                stars=item["stargazers_count"],
                forks=item["forks_count"],
                language=item.get("language"),
                topics=item.get("topics", []),
                created_at=item["created_at"],
                updated_at=item["updated_at"],
                pushed_at=item["pushed_at"],
                open_issues=item["open_issues_count"],
                license=item.get("license", {}).get("spdx_id") if item.get("license") else None
            )
            
            # Fetch README if requested
            if params.include_readme:
                repo.readme_content = self._fetch_readme(item["full_name"])
            
            repositories.append(repo)
        
        return repositories
    
    def _fetch_readme(self, full_name: str) -> Optional[str]:
        """
        Fetch README content for a repository.
        
        Args:
            full_name: Repository full name (owner/repo).
            
        Returns:
            README content as string, or None if not found.
        """
        try:
            response = self.client.get(f"/repos/{full_name}/readme")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            
            # Decode base64 content
            content = data.get("content", "")
            if content:
                # Remove newlines from base64 string
                content = content.replace("\n", "")
                decoded = base64.b64decode(content).decode("utf-8")
                # Truncate very long READMEs
                max_length = 5000
                if len(decoded) > max_length:
                    decoded = decoded[:max_length] + "\n\n[README truncated...]"
                return decoded
        except Exception:
            pass
        
        return None
    
    def format_output(self, repositories: list[Repository]) -> dict:
        """
        Format repository list as JSON output.
        
        Args:
            repositories: List of Repository objects.
            
        Returns:
            Dictionary with formatted repository data.
        """
        results = []
        for repo in repositories:
            results.append({
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "url": repo.url,
                "stars": repo.stars,
                "forks": repo.forks,
                "language": repo.language,
                "topics": repo.topics,
                "created_at": repo.created_at,
                "updated_at": repo.updated_at,
                "pushed_at": repo.pushed_at,
                "open_issues": repo.open_issues,
                "license": repo.license,
                "readme": repo.readme_content
            })
        
        return {
            "success": True,
            "count": len(results),
            "repositories": results
        }
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()


def parse_parameters(json_str: str) -> SearchParameters:
    """
    Parse JSON string into SearchParameters.
    
    Args:
        json_str: JSON string with search parameters.
        
    Returns:
        SearchParameters object.
        
    Raises:
        ValueError: If required parameters are missing or invalid.
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {str(e)}")
    
    if "keywords" not in data:
        raise ValueError("'keywords' is required")
    
    return SearchParameters(
        keywords=data["keywords"],
        language=data.get("language"),
        min_stars=data.get("min_stars", 0),
        topic=data.get("topic"),
        sort_by=data.get("sort_by", "stars"),
        max_results=min(data.get("max_results", 5), 10),
        include_readme=data.get("include_readme", True)
    )


def main():
    """Main entry point for the GitHub search tool."""
    parser = argparse.ArgumentParser(
        description="Search GitHub repositories with advanced filtering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python github_search_tool.py '{"keywords": "python web framework"}'
  python github_search_tool.py '{"keywords": "react components", "language": "typescript", "min_stars": 1000}'
        """
    )
    parser.add_argument(
        "parameters",
        help="JSON string with search parameters"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print JSON output"
    )
    
    args = parser.parse_args()
    
    try:
        # Parse parameters
        params = parse_parameters(args.parameters)
        
        # Create tool and search
        tool = GitHubSearchTool()
        try:
            repositories = tool.search_repositories(params)
            output = tool.format_output(repositories)
        finally:
            tool.close()
        
        # Output results
        indent = 2 if args.pretty else None
        print(json.dumps(output, indent=indent, ensure_ascii=False))
        
    except ValueError as e:
        error_output = {
            "success": False,
            "error": str(e),
            "error_type": "validation_error"
        }
        print(json.dumps(error_output), file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        error_output = {
            "success": False,
            "error": str(e),
            "error_type": "api_error"
        }
        print(json.dumps(error_output), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            "success": False,
            "error": str(e),
            "error_type": "unexpected_error"
        }
        print(json.dumps(error_output), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
