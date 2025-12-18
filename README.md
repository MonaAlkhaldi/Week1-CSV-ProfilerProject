# CSV Profiler

Generate a profiling report for a CSV file.

## Features
- Generate reports in:
  - JSON
  - Markdown
- Streamlit GUI: upload CSV + export reports

## Setup
   - uv venv -p 3.11
   - uv pip install -r requirements.txt

## Run CLI
    # If you have a src/ folder:
    # Go to the src file and the write this command in the powershell
    #uv run python -m csv_profiler.cli ../data/sample.csv

## Run GUI
    # If you have a src/ folder:
    #   Mac/Linux: export PYTHONPATH=src
    #   Windows:   $env:PYTHONPATH="src"
    uv run streamlit run app.py