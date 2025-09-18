# src/app.py
import streamlit as st
from github_client import get_user_repos, get_repo_languages, get_repo_commit_count_via_stats
from utils import aggregate_language_bytes, repos_to_dataframe
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="GitHub Portfolio Analyzer", layout="wide")

st.title("GitHub Portfolio Analyzer")

with st.sidebar:
    st.header("Inputs")
    username = st.text_input("GitHub username", value="")
    token = st.text_input("GitHub Personal Access Token (optional)", type="password", value=os.getenv("GITHUB_TOKEN", ""))
    analyze = st.button("Analyze")

if not analyze:
    st.info("Enter a GitHub username and click Analyze.")
    st.stop()

try:
    with st.spinner("Fetching repositories..."):
        repos = get_user_repos(username, token if token else None)
except Exception as e:
    st.error(str(e))
    st.stop()

if not repos:
    st.warning("No repos found or user has no owned public repos.")
    st.stop()

repo_df = repos_to_dataframe(repos)
st.subheader("Repository list")
st.dataframe(repo_df.sort_values("stargazers_count", ascending=False).reset_index(drop=True))

with st.spinner("Aggregating languages..."):
    lang_df = aggregate_language_bytes(repos, lambda o, n: get_repo_languages(o, n, token if token else None))

if not lang_df.empty:
    st.subheader("Most used languages (by bytes)")
    st.bar_chart(lang_df.set_index("language")["bytes"])
else:
    st.info("No language stats available.")

st.subheader("Top repositories by stars")
st.table(repo_df.sort_values("stargazers_count", ascending=False).head(10)[["name", "stargazers_count", "forks_count", "language"]])

st.subheader("Commit counts (approx via contributor stats)")
commit_rows = []
with st.spinner("Fetching commit stats (may be slow)..."):
    for r in repos:
        owner = r["owner"]["login"]
        name = r["name"]
        commits = get_repo_commit_count_via_stats(owner, name, token if token else None)
        commit_rows.append({"repo": name, "commits": commits if commits is not None else pd.NA})
commit_df = pd.DataFrame(commit_rows).sort_values("commits", ascending=False)
st.table(commit_df)

st.download_button("Download repo list CSV", repo_df.to_csv(index=False), file_name=f"{username}_repos.csv")

st.success("Done — enjoy your insights!")
