# GitHub Portfolio Analyzer

A lightweight Streamlit app that analyzes a GitHub user's public repositories and shows language usage, stars, and approximate commit counts.

## Quick start

1. Clone the repo and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. (Optional) Create a `.env` file with `GITHUB_TOKEN=ghp_...`

3. Run the app:

```bash
cd src
streamlit run app.py
```

4. Open http://localhost:8501 in your browser.
