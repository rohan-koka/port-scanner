# 🔍 Port Scanner

A web app that scans a target host for open ports and identifies running services.

## Features
- Scans any hostname or IP address for open ports
- Customizable port range and timeout settings
- Identifies common services (HTTP, SSH, FTP, DNS, etc.)
- Real time progress bar during scan
- Multi-threaded for fast scanning

## Live Demo
[Try it here](https://port-scanner-gawmunopzpprexsm3mqe9e.streamlit.app/)

## Built With
- Python
- Streamlit
- Python socket library

## Usage
Safe hosts to test with:
- `scanme.nmap.org` — designed for scanning practice
- `localhost` — scans your own machine

## Run Locally
```bash
pip3 install streamlit
streamlit run app.py
```

## ⚠️ Disclaimer
Only scan hosts you own or have explicit permission to scan. Unauthorized port scanning is illegal.
