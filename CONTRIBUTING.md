# Contributing

Thanks for your interest in improving Personal Productivity Manager!

## Getting Started

- Use Python 3.8+ and create a virtual environment.
- Install dependencies: `pip install -r productivity_manager/requirements.txt`
- Run tests: `python -m unittest discover -s productivity_manager/tests -t .`

## Development Workflow

- Keep changes focused and small; one feature or fix per PR.
- Add or update tests for your changes when applicable.
- Ensure the app launches: `python -m productivity_manager.main`.
- Follow existing code style and module layout.

## Pull Requests

- Describe the problem and solution clearly.
- Include screenshots/gifs for UI changes when helpful.
- Reference related issues.

## Release and Packaging

- Packaging metadata lives in `pyproject.toml`.
- Entry points: `productivity-manager` and `ppm`.
- Windows exe builds can be produced with PyInstaller.

