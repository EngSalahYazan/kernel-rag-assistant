$ErrorActionPreference = "Stop"

Write-Host "Creating Python 3.11 virtual environment..."
py -3.11 -m venv .venv

Write-Host "Activating environment..."
& .\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing dependencies..."
pip install -r requirements.txt
pip install -e . --no-deps

Write-Host "Running offline tests..."
pytest

Write-Host "Inspecting the workshop PDF chunks..."
python scripts/inspect_chunks.py

Write-Host ""
Write-Host "Setup complete."
Write-Host "1) Add OPENAI_API_KEY to .env"
Write-Host "2) Run: python scripts/ingest.py --rebuild"
Write-Host "3) Run: streamlit run app/streamlit_app.py"
