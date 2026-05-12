# Packaging Guide — LottoCanvas Workstation

This document explains how to build and distribute the LottoCanvas Workstation app as a
**desktop app** (via Electron), as an **Android/Huawei installable app** (via Capacitor),
and as an **iOS installable app** (via PWA or Capacitor).

---

## 1 — Progressive Web App (iOS & macOS Safari install)

The repository already ships the PWA assets:

| File | Purpose |
|---|---|
| `manifest.json` | App metadata, icons, display mode |
| `service-worker.js` | Offline caching / installability |
| `icons/` | PNG icons for all required sizes |

### How users install (iOS)
1. Open the hosted URL in **Safari** on iPhone/iPad.
2. Tap the **Share** button → **"Add to Home Screen"**.
3. The app icon appears on the home screen and opens without browser chrome.

### How users install (macOS)
1. Open the hosted URL in **Safari** on macOS 14+.
2. Click **File → Add to Dock…** (or use the Share menu in Safari).

### Hosting requirement
The PWA must be served over **HTTPS**. If you are using Firebase Hosting, this is
already satisfied.

---

## 2 — macOS Desktop App (Electron)

### Prerequisites
- Node.js ≥ 18 (`node --version`)
- npm ≥ 9

### Install dependencies

```bash
npm install
```

### Run in development

```bash
npm start
```

This opens the app in a native macOS window.

### Build the macOS .app and .dmg installer

```bash
npm run dist
```

Output is placed in the `dist/` directory:
- `dist/LottoCanvas Workstation-1.0.0-arm64.dmg` — Apple Silicon installer
- `dist/LottoCanvas Workstation-1.0.0-x64.dmg` — Intel installer

### Code signing & notarisation (required for distribution outside direct download)
To distribute on the **Mac App Store** or to pass Gatekeeper without a warning:
1. Enrol in the [Apple Developer Program](https://developer.apple.com/programs/) ($99/yr).
2. Create a **Developer ID Application** certificate in Xcode or the Apple Developer portal.
3. Set the environment variables before building:
   ```
   CSC_LINK=<path-to-p12>
   CSC_KEY_PASSWORD=<p12-password>
   APPLE_ID=<your-apple-id>
   APPLE_APP_SPECIFIC_PASSWORD=<app-specific-password>
   APPLE_TEAM_ID=<team-id>
   ```
4. Add `"notarize": true` to the `mac` section of `package.json`.
5. Run `npm run dist` again.

### Icon files required for macOS
electron-builder converts `icons/icon.icns` into the macOS app icon.
Generate `icon.icns` from `icons/icon.svg` using the helper script:

```bash
node scripts/generate-icons.js
```

See **Section 5** for details.

---

## 3 — Android & Huawei Native App (Capacitor)

Capacitor wraps the web app in a native Android WebView and produces installable APK/AAB
builds. Huawei phones can install the same Android APK directly, or you can submit an AAB/APK
to Huawei AppGallery.

### Prerequisites
- Node.js ≥ 18
- Android Studio (latest stable)
- Android SDK + build tools installed in Android Studio
- Java 17 (recommended by current Android Gradle plugin)

### Steps

```bash
# 1. Install dependencies (includes Capacitor Android packages)
npm install

# 2. Add Android platform (first time only)
npm run cap:add:android

# 3. Sync web assets into native Android project
npm run cap:sync:android

# 4. Build a release APK (downloadable install file)
npm run dist:android
```

Release APK output:
- `android/app/build/outputs/apk/release/app-release.apk`

For Huawei phones:
- Use the same APK from `dist:android`, or run `npm run dist:huawei` (same build output).
- Enable **Install unknown apps** on-device for direct APK install, or publish to AppGallery.

### Build AAB for Play Store / AppGallery (optional)

```bash
cd android
./gradlew bundleRelease
```

AAB output:
- `android/app/build/outputs/bundle/release/app-release.aab`

---

## 4 — iOS Native App (Capacitor)

Capacitor wraps the web app in a native WKWebView and produces a real iOS app
that can be submitted to the App Store.

### Prerequisites
- macOS with **Xcode 15+** installed
- Node.js ≥ 18
- An **Apple Developer Program** membership ($99/yr)

### Steps

```bash
# 1. Install dependencies (including Capacitor)
npm install
npm install @capacitor/core @capacitor/cli @capacitor/ios @capacitor/splash-screen

# 2. Initialise Capacitor (first time only)
# Skip this step if `capacitor.config.json` already exists in the repository.
npx cap init "LottoCanvas Workstation" "com.g88416.lottocanvas" --web-dir www

# 3. Add the iOS platform
npx cap add ios

# 4. Build/copy web assets and sync to iOS
npm run prepare:web
npx cap sync ios

# 5. Open in Xcode
npx cap open ios
```

Inside Xcode:
- Set your **Team** and **Bundle Identifier** under *Signing & Capabilities*.
- Select a simulator or connected device and press **Run**.
- To submit to the App Store: **Product → Archive → Distribute App**.

The `capacitor.config.json` file in this repo already contains the correct
`appId` and `appName`.

---

## 5 — Generating PNG & ICNS Icons

Place your source artwork as `icons/icon.svg` (already included), then run:

```bash
node scripts/generate-icons.js
```

This requires **sharp** (`npm install --save-dev sharp`). The script produces:
- `icons/icon-{72,96,128,144,152,192,384,512}.png` — PWA / Capacitor icons
- `icons/icon-512.png` — Electron Linux/Windows icon
- `icons/icon.icns` — macOS app icon (via `iconutil` on macOS only)
- `icons/icon.ico` — Windows installer icon (via `png-to-ico` on Windows/Linux)

If you are not running macOS, skip `.icns` generation; the Electron build will
still work on non-macOS platforms using the PNG fallback.

---

## 6 — File Overview

```
├── index.html           # Main app (single-file HTML/JS/CSS)
├── manifest.json        # PWA web app manifest
├── service-worker.js    # PWA service worker (offline support)
├── main.js              # Electron main process
├── package.json         # npm / Electron-builder config
├── capacitor.config.json# Capacitor iOS/Android config
├── firebase-config.js   # Firebase configuration
├── icons/               # App icons (SVG source + generated PNGs)
│   ├── icon.svg
│   ├── icon-72.png … icon-512.png
│   ├── icon.icns        # (generated on macOS)
│   └── icon.ico         # (generated on Windows/Linux)
└── scripts/
    └── generate-icons.js# Icon generation helper
```
