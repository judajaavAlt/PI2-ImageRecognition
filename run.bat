@echo off
REM === First console ===
start cmd /k "cd /d backend\app && python -m main"

REM === Second console ===
start cmd /k "cd /d frontend && npm run dev"