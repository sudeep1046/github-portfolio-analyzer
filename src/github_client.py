# src/github_client.py
import requests
import time
from typing import List, Dict, Optional

GITHUB_API = "https://api.github.com"

def auth_headers(token: Optional[str] = None) -> Dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers

def get_user_repos(username: str, token: Optional[str] = None) -> List[Dict]:
    repos = []
    page = 1
    per_page = 100
    while True:
        url = f"{GITHUB_API}/users/{username}/repos"
        params = {"per_page": per_page, "page": page, "type": "owner", "sort": "pushed"}
        r = requests.get(url, headers=auth_headers(token), params=params, timeout=20)
        if r.status_code == 404:
            raise ValueError("User not found")
        if r.status_code != 200:
            raise RuntimeError(f"GitHub API error {r.status_code}: {r.text}")
        batch = r.json()
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return repos

def get_repo_languages(owner: str, repo: str, token: Optional[str] = None) -> Dict[str, int]:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/languages"
    r = requests.get(url, headers=auth_headers(token), timeout=10)
    if r.status_code != 200:
        return {}
    return r.json()

def get_repo_contributor_stats(owner: str, repo: str, token: Optional[str] = None, max_retries: int = 6):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/stats/contributors"
    for i in range(max_retries):
        r = requests.get(url, headers=auth_headers(token), timeout=20)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 202:
            time.sleep(1 + 2 ** i)
            continue
        return None
    return None

def get_repo_commit_count_via_stats(owner: str, repo: str, token: Optional[str] = None) -> Optional[int]:
    stats = get_repo_contributor_stats(owner, repo, token)
    if not stats:
        return None
    return sum(c.get("total", 0) for c in stats)
