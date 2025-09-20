# Personal Productivity Manager

## Project Overview

A practical personal productivity tool developed using Python. This all-in-one productivity solution aims to integrate various features including task management, time tracking, file organization, web scraping, and system monitoring.

## Core Features

### 1. Todo Manager
- Add, edit, and delete tasks
- Priority setting (High/Medium/Low)
- Category-based classification
- Task completion status tracking
- Due date setting and notifications

### 2. Time Tracker
- Task-specific time measurement
- Daily/weekly/monthly time statistics
- Productivity analysis charts
- Work session recording

### 3. File Organizer
- Automatic download folder organization
- File type-based classification
- Duplicate file detection and removal
- Batch file renaming

### 4. Web Scraper
- News headline collection
- Weather information retrieval
- Exchange rate inquiry
- RSS feed reading

### 5. System Monitor
- CPU and memory usage display
- Disk capacity monitoring
- Network status monitoring
- System notifications

## Project Directory Structure

See the `productivity_manager/` folder for source code, assets, and data directories.

## Quick Start

- Install Python 3.8+
- Option A — run from source:
  - Install deps: `pip install -r productivity_manager/requirements.txt`
  - Run: `python -m productivity_manager.main`
- Option B — install as a package (recommended):
  - Build wheel: `python -m build` (requires `pip install build`)
  - Install: `pip install dist/personal_productivity_manager-*.whl`
  - Launch: `productivity-manager` (or `ppm`)

## Development

- Create venv: `python -m venv .venv && .venv\Scripts\activate` (Windows)
- Install dev tools: `pip install -r productivity_manager/requirements.txt`
- Run tests: `python -m unittest discover -s productivity_manager/tests -t .`
- Lint/format: choose your tools (e.g., ruff/black) as preferred

## Packaging and Distribution

- PEP 621 metadata defined in `pyproject.toml`
- Console script entry points: `productivity-manager`, `ppm`
- User data (config/db) stored in an OS‑proper location via `platformdirs`.
  - Windows: `%APPDATA%/Personal Productivity Manager`
  - macOS: `~/Library/Application Support/Personal Productivity Manager`
  - Linux: `~/.local/share/Personal Productivity Manager`

### Build Wheel / sdist

- `pip install build`
- `python -m build`

### Windows Executable (PyInstaller)

- Ensure deps: `pip install -r productivity_manager/requirements.txt`
- Build: `pyinstaller --clean -y productivity_manager.spec`
- Output EXE at `dist/productivity-manager.exe`
