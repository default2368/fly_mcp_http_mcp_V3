"""
MCP GitHub Module
Contiene i metodi per interagire con l'API GitHub
"""
import json
import requests
from typing import Dict, Any


class MCPGitHub:
    """Classe per i metodi GitHub"""
    
    @staticmethod
    def execute_github_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
        """Esegue il tool GitHub specificato"""
        
        if tool_name == "get_github_repo_info":
            return MCPGitHub._get_github_repo_info(arguments)
        
        elif tool_name == "get_github_user_info":
            return MCPGitHub._get_github_user_info(arguments)
        
        elif tool_name == "search_github_repos":
            return MCPGitHub._search_github_repos(arguments)
        
        else:
            return f"Error: Unknown GitHub tool '{tool_name}'"

    @staticmethod
    def _get_github_repo_info(arguments: Dict[str, Any]) -> str:
        """Ottiene informazioni su un repository GitHub"""
        owner = arguments.get("owner", "")
        repo = arguments.get("repo", "")
        
        if not owner or not repo:
            return "Error: Both owner and repo parameters are required"
        
        url = f"https://api.github.com/repos/{owner}/{repo}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                return f"Error: Repository '{owner}/{repo}' not found"
            elif response.status_code != 200:
                return f"Error: GitHub API returned status {response.status_code}"
            
            data = response.json()
            
            repo_info = {
                "name": data["name"],
                "full_name": data["full_name"],
                "description": data["description"],
                "stars": data["stargazers_count"],
                "forks": data["forks_count"],
                "watchers": data["watchers_count"],
                "language": data["language"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
                "html_url": data["html_url"]
            }
            
            return json.dumps({
                "status": "success",
                "data": repo_info
            }, indent=2)
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching repository info: {e}"

    @staticmethod
    def _get_github_user_info(arguments: Dict[str, Any]) -> str:
        """Ottiene informazioni su un utente GitHub"""
        username = arguments.get("username", "")
        
        if not username:
            return "Error: Username parameter is required"
        
        url = f"https://api.github.com/users/{username}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                return f"Error: User '{username}' not found"
            elif response.status_code != 200:
                return f"Error: GitHub API returned status {response.status_code}"
            
            data = response.json()
            
            user_info = {
                "login": data["login"],
                "name": data["name"],
                "company": data["company"],
                "blog": data["blog"],
                "location": data["location"],
                "email": data["email"],
                "bio": data["bio"],
                "public_repos": data["public_repos"],
                "followers": data["followers"],
                "following": data["following"],
                "created_at": data["created_at"],
                "html_url": data["html_url"]
            }
            
            return json.dumps({
                "status": "success",
                "data": user_info
            }, indent=2)
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching user info: {e}"

    @staticmethod
    def _search_github_repos(arguments: Dict[str, Any]) -> str:
        """Cerca repository su GitHub"""
        query = arguments.get("query", "")
        
        if not query:
            return "Error: Query parameter is required"
        
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return f"Error: GitHub API returned status {response.status_code}"
            
            data = response.json()
            
            repos = []
            for repo in data["items"][:5]:  # Prime 5 repo
                repos.append({
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "description": repo["description"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "language": repo["language"],
                    "html_url": repo["html_url"]
                })
            
            return json.dumps({
                "status": "success",
                "total_count": data["total_count"],
                "results": repos
            }, indent=2)
            
        except requests.exceptions.RequestException as e:
            return f"Error searching repositories: {e}"

    @staticmethod
    def get_github_tools_list() -> list:
        """Restituisce la lista dei tools GitHub disponibili"""
        return [
            {
                "name": "get_github_repo_info",
                "description": "Get information about a GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "owner": {
                            "type": "string",
                            "description": "Repository owner (username or organization)"
                        },
                        "repo": {
                            "type": "string", 
                            "description": "Repository name"
                        }
                    },
                    "required": ["owner", "repo"]
                }
            },
            {
                "name": "get_github_user_info", 
                "description": "Get information about a GitHub user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "GitHub username"
                        }
                    },
                    "required": ["username"]
                }
            },
            {
                "name": "search_github_repos",
                "description": "Search repositories on GitHub",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (e.g., 'python machine learning')"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]