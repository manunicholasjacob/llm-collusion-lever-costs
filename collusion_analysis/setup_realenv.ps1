# Build the sprint Python env in the REAL Windows environment (the env/ venv points at a uv Python that
# only existed inside Claude's tool sandbox). The harness needs Python 3.12 (PEP 701 f-strings), so uv
# installs 3.12 into the real user profile. $0, no API calls.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
uv python install 3.12
if (Test-Path envw) { Remove-Item -Recurse -Force envw }   # envw is this script's own output; rebuild it on 3.12
uv venv --python 3.12 envw
& envw\Scripts\python.exe -c "import sys; assert sys.version_info >= (3, 12), sys.version; print('envw on', sys.version.split()[0])"
uv pip install --python envw\Scripts\python.exe -r requirements.txt
uv pip install --python envw\Scripts\python.exe -e .
& envw\Scripts\python.exe -c "import numpy, scipy, pandas, matplotlib, openai, wandb, pydantic, jinja2, backoff, anthropic; print('REALENV IMPORTS OK')"
$env:WANDB_MODE = "disabled"
& envw\Scripts\python.exe -X utf8 collusion_analysis\mock_smoke_test.py | Select-String -Pattern "PASS|FAIL|Traceback"
Get-ChildItem results -Directory -Filter "*_mock-*" | Remove-Item -Recurse -Force
"SETUP DONE"
