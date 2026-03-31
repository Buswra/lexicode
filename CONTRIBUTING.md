# Contributing to LexiCode

Thank you for contributing. Please keep changes small, tested, and documented.

## Development flow

1. Create a feature branch.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the app locally with `python features/app.py` (web mode) or `python features/desktop_launcher.py` (desktop mode).
4. Run tests with `pytest`.
5. Build distributable with `BUILD_EXE.bat` (creates `dist/LexiCode-Setup.exe` if Inno Setup is installed).
6. Open a pull request with a short summary and screenshots if UI changed.

## Code style

- Prefer clear Turkish-friendly UX text.
- Keep functions focused and readable.
- Avoid breaking local fallback behavior for AI and TTS.
- Update `README.md` or `CHANGELOG.md` when features change.

## Reporting issues

When filing a bug, include:
- steps to reproduce
- expected behavior
- actual behavior
- screenshots or console output if available
