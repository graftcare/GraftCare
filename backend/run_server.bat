@echo off
REM Set your Supabase credentials here
set SUPABASE_URL=https://your-actual-url.supabase.co
set SUPABASE_SERVICE_KEY=your-actual-service-role-secret

REM Run the server
echo Starting Graftcare Backend...
uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
