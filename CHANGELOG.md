# Changelog

## [2026-01-30] - Critical Fixes & Polish
### Fixed
- **Critical Server Error (500/405):** Removed accidental `PySide6` dependency from `logger.py` which was crashing the Serverless Function.
- **Client-Side Crash:** Updated `HoroscopeGrid.tsx` to safely handle Python Dictionary responses (previously crashed expecting Arrays).
- **Infinite AI Loading:** Fixed `KeyError` in `gemini_client.py` caused by JSON integer-to-string key conversion.
- **UI Readability:** Fixed "White text on white background" issue in AI reading card.
- **Markdown Rendering:** Installed `@tailwindcss/typography` and `react-markdown` for proper formatting of AI responses.

### Added
- **API Documentation:** Added `docs/api/endpoints.md`.
- **Debug Tools:** Added `api/debug_deps.py` (removed after use).
