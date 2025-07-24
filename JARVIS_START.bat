@echo off
:: Enhanced JARVIS AI 2.0 - Improved AI Voice Assistant

:: Initialize environment
setlocal enabledelayedexpansion
title JARVIS AI 2.0 - Enhanced AI Voice Assistant

:: Default configurations
set "PRIMARY_COLOR=0B"
set "ERROR_COLOR=0C"
set "LOADING_COLOR=09"
set "TTS_VOICE=Microsoft David Desktop"
set "LOG_FILE=jarvis.log"

:: Load configuration from file if exists
if exist config.ini (
    for /f "tokens=1,2 delims==" %%a in (config.ini) do (
        set "%%a=%%b"
    )
)

:: Apply primary color
color %PRIMARY_COLOR%

:: Logging function
call :Log "Starting JARVIS AI 2.0"

:: JARVIS ASCII Art
call :DisplayHeader



:: Check prerequisites
call :CheckPrerequisites
if %ERRORLEVEL% neq 0 (
    call :Log "Prerequisite check failed"
    call :HandleError "Prerequisite check failed" %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

:: Voice greeting
call :VoiceGreeting "Welcome back, Sir. All systems are online and ready."
if %ERRORLEVEL% neq 0 call :Log "TTS initialization failed"

:: System checks
call :SystemChecks
if %ERRORLEVEL% neq 0 (
    call :Log "System checks failed"
    call :HandleError "System checks failed" %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

:: Start AI core
call :StartAICore
if %ERRORLEVEL% neq 0 (
    call :Log "AI core startup failed"
    call :HandleError "Failed to launch main.py" %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

:: Session end
call :VoiceGreeting "Session terminated. Have a nice day, Sir."
call :Log "JARVIS session ended"
call :DisplayFooter
pause
exit /b 0

:: Functions
:Log
    echo [%DATE% %TIME%] %~1 >> %LOG_FILE%
    goto :eof

:DisplayHeader
    echo.
    echo      ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
    echo      ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
    echo      ██║███████║██████╔╝██║   ██║██║███████╗
    echo ██   ██║██╔══██║██╔══██╗██║   ██║██║╚════██║
    echo ╚█████╔╝██║  ██║██║  ██║╚██████╔╝██║███████║
    echo  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝
    echo.
    echo ==================================================
    echo         WELCOME, Boss. JARVIS SYSTEMS ONLINE.
    echo ==================================================
    echo.
    goto :eof

:CheckPrerequisites
    :: Check Python
    where python >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        call :HandleError "Python 3.7+ not found in PATH" 1
        exit /b 1
    )
    :: Check main.py
    if not exist main.py (
        call :HandleError "main.py not found in current directory" 2
        exit /b 2
    )
    goto :eof

:VoiceGreeting
    if "%SKIP_ANIMATION%"=="Y" goto :eof
    powershell -c "try {Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.SelectVoice('%TTS_VOICE%'); $synth.Speak('%~1')} catch {Write-Host 'Warning: Text-to-Speech failed.'}" 2>nul
    if %ERRORLEVEL% neq 0 (
        echo Warning: Unable to initialize TTS. Proceeding without voice.
        exit /b 1
    )
    goto :eof

:SystemChecks
    if "%SKIP_ANIMATION%"=="Y" goto :eof
    set checks=AssistantCore Automation Chatbot ImageGeneration Model Navigation RealtimeSearch SpeechToText TextToSpeech GUI
    for %%c in (%checks%) do (
        <nul set /p="Checking %%c "
        for /l %%i in (1,1,5) do (
            <nul set /p="."
            ping -n 1 127.0.0.1 >nul
        )
        echo  [OK]
    )
    echo.
    goto :eof

:StartAICore
    color %LOADING_COLOR%
    if "%SKIP_ANIMATION%"=="N" (
        echo Initiating AI core...
        set "bar=----------"
        for /l %%i in (1,1,10) do (
            set "bar=!bar:~0,-1:#"
            cls
            call :DisplayHeader
            echo Initiating AI core...
            echo [!bar!]
            ping -n 1 127.0.0.1 >nul
        )
        echo [COMPLETE]
        echo.
    )
    color %PRIMARY_COLOR%
    echo Launching JARVIS AI...
    python main.py
    exit /b %ERRORLEVEL%

:HandleError
    color %ERROR_COLOR%
    echo ERROR: %~1
    echo Error code: %~2
    echo Please check the log file (%LOG_FILE%) for details.
    pause
    goto :eof

:DisplayFooter
    echo.
    echo ==================================================
    echo         JARVIS SESSION ENDED. HAVE A NICE DAY!
    echo ==================================================
    echo.
    goto :eof