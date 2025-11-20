# Hospital Patient Management (FastAPI)

Quick steps to run the API locally (Windows PowerShell):

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update DB credentials:

```powershell
copy .env.example .env
# then edit .env with your DB credentials
```

4. Run the app with uvicorn (reload for development):

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

5. Visit `http://127.0.0.1:8000/docs` for interactive API docs.

If you see a file named `from fastapi import FastAPI, HTTPExcepti.py`, delete it to avoid confusion. In PowerShell:

```powershell
Remove-Item -LiteralPath 'd:\DATABASE\Hospital_Management\from fastapi import FastAPI, HTTPExcepti.py'
```
