YATRADHAM SEO PIPELINE - ONE-CLICK SETUP
==========================================

STEP 1: EXTRACT
---------------
Extract this zip to any folder, e.g.:
  C:\yatradham-seo-pipeline

Avoid paths with special characters. Good paths:
  C:\yatradham
  D:	ools\seo-pipeline

STEP 2: TEST MODE (No API key needed)
--------------------------------------
Double-click:  start.bat

This runs with MOCK data to test the dashboard.
No internet required. No API key needed.

STEP 3: LIVE MODE (Real AI output)
-----------------------------------
1. Rename .env.example to .env
2. Open .env and replace:
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   with your actual OpenRouter API key
3. Double-click:  start-real.bat

TROUBLESHOOTING
---------------
Q: Batch file opens and closes instantly?
A: Run debug.bat instead. It will show exactly what is wrong.

Q: "Python not found" error?
A: Install Python 3.10+ from https://python.org
   Make sure to check "Add Python to PATH" during installation.

Q: "Failed to install dependencies"?
A: Check your internet connection. First install needs ~50MB download.

Q: Server starts but browser shows nothing?
A: Manually open: http://localhost:8000/static/index.html

Q: Where are my generated outputs saved?
A: In the file seo_pipeline.db (SQLite database in the same folder).

FREE TIER LIMITS (OpenRouter)
------------------------------
- 20 requests per minute
- 200 requests per day (unfunded account)
- 1,000 requests per day (after $10 deposit, one-time)

Your 250 packages x 4 agents = ~1,000 API calls.
Deposit $10 once to process all 250 in one day.

FILES
-----
start.bat       = Test mode (mock data, no API key)
start-real.bat  = Live mode (real AI, needs .env with API key)
debug.bat       = Diagnostic mode (shows what is wrong)
startup.log     = Auto-created log file if anything fails

SUPPORT
-------
If the batch still closes instantly, do this:
1. Hold Shift + Right-click in the folder
2. Choose "Open PowerShell window here" or "Open Command Prompt"
3. Type:  .\start.bat
4. You will see the exact error message
