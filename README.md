# CSV Profiler

Generate a profiling report for a CSV file.



## Setup
   - uv venv -p 3.11
   - .venv\Scripts\activate 
   - uv pip install -r requirements.txt

## Run CLI
  - make sure you are in the src folder :
  - Go to the src file a run this command in the powershell : 
  -uv run python -m csv_profiler.cli ../data/sample.csv

## Run GUI
 -  uv run streamlit run app.py
 -   If you have a src/ folder:
 - Go to the src file and run this command in the powershell : 

# Outputs

- Generates reports in JSON and Markdown formats

- Displays a CSV preview in the Streamlit interface

- Shows profiling results in a web interface

- Allows downloading reports as files

- Allows saving reports locally to the outputs/ folder
