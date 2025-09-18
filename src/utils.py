# src/utils.py
from collections import Counter
from typing import Dict, List
import pandas as pd

def aggregate_language_bytes(repos: List[Dict], fetch_lang_fn) -> pd.DataFrame:
    counter = Counter()
    for r in repos:
        owner = r["owner"]["login"]
        name = r["name"]
        langs = fetch_lang_fn(owner, name)
        for lang, b in langs.items():
            counter[lang] += b
    df = pd.DataFrame(counter.items(), columns=["language", "bytes"]).sort_values("bytes", ascending=False)
    return df

def repos_to_dataframe(repos: List[Dict]) -> pd.DataFrame:
    rows = []
    for r in repos:
        rows.append({
            "name": r.get("name"),
            "full_name": r.get("full_name"),
            "private": r.get("private"),
            "fork": r.get("fork"),
            "language": r.get("language"),
            "stargazers_count": r.get("stargazers_count", 0),
            "forks_count": r.get("forks_count", 0),
            "watchers_count": r.get("watchers_count", 0),
            "pushed_at": r.get("pushed_at"),
            "updated_at": r.get("updated_at"),
            "size_kb": r.get("size", 0),
        })
    return pd.DataFrame(rows)
