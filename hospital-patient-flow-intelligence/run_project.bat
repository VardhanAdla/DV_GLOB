@echo off
REM ============================================================================
REM Hospital Patient Flow Intelligence - Master Pipeline Execution Script
REM Course: Data Visualization Lab (Course Code: GR24A3144)
REM ============================================================================

echo ==========================================================================
echo Starting Hospital Patient Flow Intelligence Automated Pipeline...
echo ==========================================================================

cd /d "%~dp0"

echo [1/8] Generating synthetic dataset...
python src\generate_data.py
if %ERRORLEVEL% NEQ 0 (
    echo Error in generate_data.py
    pause
    exit /b %ERRORLEVEL%
)

echo [2/8] Cleaning and standardizing data...
python src\clean_data.py
if %ERRORLEVEL% NEQ 0 (
    echo Error in clean_data.py
    pause
    exit /b %ERRORLEVEL%
)

echo [3/8] Engineering operational features and bottleneck scoring...
python src\feature_engineering.py
if %ERRORLEVEL% NEQ 0 (
    echo Error in feature_engineering.py
    pause
    exit /b %ERRORLEVEL%
)

echo [4/8] Running automated data validation audit...
python src\validate_data.py
if %ERRORLEVEL% NEQ 0 (
    echo Error in validate_data.py
    pause
    exit /b %ERRORLEVEL%
)

echo [5/8] Running patient journey and operational analytics...
python src\analytics.py
if %ERRORLEVEL% NEQ 0 (
    echo Error in analytics.py
    pause
    exit /b %ERRORLEVEL%
)

echo [6/8] Detecting department bottlenecks and constructing matrices...
python src\bottleneck_detection.py
if %ERRORLEVEL% NEQ 0 (
    echo Error in bottleneck_detection.py
    pause
    exit /b %ERRORLEVEL%
)

echo [7/8] Detecting operational anomalies (IQR + Isolation Forest)...
python src\anomaly_detection.py
if %ERRORLEVEL% NEQ 0 (
    echo Error in anomaly_detection.py
    pause
    exit /b %ERRORLEVEL%
)

echo [8/8] Performing advanced analytics (PCA and K-Means Clustering)...
python src\advanced_analytics.py
if %ERRORLEVEL% NEQ 0 (
    echo Error in advanced_analytics.py
    pause
    exit /b %ERRORLEVEL%
)

echo ==========================================================================
echo Full pipeline executed successfully! All datasets and assets are ready.
echo ==========================================================================
pause
