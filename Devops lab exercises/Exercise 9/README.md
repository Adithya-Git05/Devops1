# Exercise 9 — Jenkins Multi-Stage Python Pipeline

## Requirements

- Jenkins with the Pipeline and Git plugins.
- A Linux Jenkins agent with `python3`, `python3-venv`, and Git.
- A Git repository containing `app.py`, `requirements.txt`, `test_app.py`,
  `scripts/smoke_test.py`, and `Jenkinsfile`.

## Run the local checks

In PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s . -p "test_*.py"
```

## Run the Jenkins pipeline

Publish these files to a Git repository, then create a **Pipeline** job using
**Pipeline script from SCM** and configure the repository URL. Run **Build
Now**. The pipeline installs the pinned Flask dependencies, runs the unit test,
copies the app into `python-app-deploy`, starts it, and verifies the live HTTP
response. The pipeline stops its test server when the final stage exits.
