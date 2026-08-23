# NoticeGuard

NoticeGuard is a Chrome extension that helps users check suspicious government notices before acting on them. Users can paste notice text or select a PDF/image, then receive a clear verdict and the warning signs behind it.

## Why it matters

Fraudulent notices often use urgent language, unofficial links, payment requests, or suspicious contact details. NoticeGuard is designed to make those warning signs easier to spot.

## Current MVP features

- Paste a government notice, SMS, email, or letter into the extension.
- Select a PDF, PNG, JPG, or JPEG file.
- Validate that the user has provided text or a file.
- Show an analysis loading state.
- Display a demo verdict, confidence level, and reasons.
- Present a polished popup interface for the Chrome extension.

## Technology

- HTML
- CSS
- JavaScript
- Chrome Extension Manifest V3

## Run the extension locally

1. Download or clone this repository.
2. Open Chrome and visit `chrome://extensions`.
3. Enable **Developer mode**.
4. Select **Load unpacked**.
5. Choose the `extension` folder in this repository.
6. Open NoticeGuard from the Chrome extensions toolbar.

## Demo flow

1. Paste a notice/message or select a supported file.
2. Click **Analyze Notice**.
3. The extension shows a brief loading state.
4. A demo result is displayed with a verdict, confidence, and reasons.

## Future backend connection

The frontend is prepared to connect to a Flask endpoint at `http://localhost:5000/analyze`. The current version uses a dummy response only; it does not yet perform OCR, AI analysis, or file uploads.

## Project structure

```text
extension/
├── manifest.json   # Chrome extension configuration
├── popup.html      # Popup structure and UI
├── popup.js        # Input handling and analysis flow
└── style.css       # Popup styling
```
