@echo off
REM ============================================================================
REM Hospital Patient Flow Intelligence - Interactive Streamlit Dashboard Launcher
REM Course: Data Visualization Lab (Course Code: GR24A3144)
REM ============================================================================

echo ==========================================================================
echo Launching Hospital Patient Flow Intelligence Interactive Dashboard...
echo ==========================================================================

cd /d "%~dp0"

python -m streamlit run dashboard\app.py

pause
