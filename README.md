# CSV Profiler

Generate a profiling report for a CSV file.



## Setup
   - uv venv -p 3.11
   - uv pip install -r requirements.txt

## Run CLI
  - If you have a src/ folder:
  - Go to the src file and run this command in the powershell : 
  -uv run python -m csv_profiler.cli ../data/sample.csv

## Run GUI
  - If you have a src/ folder:
- Mac/Linux: export PYTHONPATH=src
-  Windows:   $env:PYTHONPATH="src"
 -  uv run streamlit run app.py

# Outputs

- Generates reports in JSON and Markdown formats

- Displays a CSV preview in the Streamlit interface

- Shows profiling results in a web interface

- Allows downloading reports as files

- Allows saving reports locally to the outputs/ folder
