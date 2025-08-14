@echo off
echo Starting AgriAgent Backend...
call .venv\Scripts\activate
uvicorn backend.main:app --reload
pause
