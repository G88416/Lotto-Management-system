# Bophelong Lotto Management System

Advanced multi-format lottery management tool with real-time cloud sync powered by **Firebase**.

## Features

- **Quick Pick** – Generate random tickets with true random, crypto-grade, or seed-based PRNG methods.
- **Manual Pick** – Select your own numbers on an interactive number grid.
- **My Tickets** – Save, view, filter, and export tickets as CSV.
- **Statistics** – Number frequency heatmap and hot/cold analysis.
- **Seed Engine** – Reverse-engineer seeds from draw results and generate forward seeds.
- **Budget Tracker** – Monthly spending limit with a visual usage bar.
- **Draw Schedule** – Live countdowns to the next draw for every supported lottery.
- **Live Draws** – Record draw results; synced in real time across all your devices via Firebase.
- **Pattern Detector** – Hot/cold analysis, even/odd balance, range distribution, pair frequency, and smart suggestions.

---

## Firebase Setup

The app works fully offline using `localStorage`.  
To enable **cross-device sync** and **real-time live draw data**, connect it to a Firebase project:

### 1. Create a Firebase project

1. Go to [https://console.firebase.google.com/](https://console.firebase.google.com/) and create a new project (or open an existing one).

### 2. Add a Web app

1. In **Project Settings → General**, click **Add app** and choose the **Web (`</>`)** platform.
2. Register the app (no need to add Firebase Hosting).
3. Copy the `firebaseConfig` object shown.

### 3. Enable Firestore

1. In the Firebase console go to **Build → Firestore Database**.
2. Click **Create database** and choose **Native mode**.
3. Pick any location and click **Enable**.

### 4. Enable Anonymous Authentication

1. Go to **Build → Authentication → Sign-in method**.
2. Enable **Anonymous**.

### 5. Set Firestore Security Rules

In **Firestore Database → Rules**, replace the default rules with:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null
                         && request.auth.uid == userId;
    }
  }
}
```

Click **Publish**.

### 6. Fill in `firebase-config.js`

Open `firebase-config.js` and replace every `YOUR_…` placeholder with the values from your app's `firebaseConfig`:

```js
var FIREBASE_CONFIG = {
    apiKey:            'AIzaSy...',
    authDomain:        'my-project.firebaseapp.com',
    projectId:         'my-project',
    storageBucket:     'my-project.appspot.com',
    messagingSenderId: '123456789',
    appId:             '1:123456789:web:abcdef'
};
```

> **Note on Firebase web API keys:** Unlike private backend keys, Firebase web API
> keys are designed to be included in client-side code and are safe to publish.
> Your **Firestore Security Rules** (step 5 above) are what restrict access to your
> data — not the API key.  Do not, however, commit a key that is also used as a
> backend/service-account secret or in other non-Firebase contexts.

### 7. Open the app

Open `index.html` in a browser (or serve it with any static web server).  
The sync indicator in the top-right corner will turn **green** (🟢 Synced) once Firebase is connected.

---

## Firestore Data Structure

```
users/
  {uid}/
    data/
      main        ← tickets, budget, stats, customDraws, seedHistory, reverseHistory
    draws/
      {drawId}    ← individual draw results (real-time listener)
```

- **`data/main`** is written with a 1.5 s debounce every time state changes.
- **`draws/{drawId}`** is written immediately when you add/delete a draw result, and a real-time `onSnapshot` listener keeps the Live Draws tab up to date across all open tabs and devices.

---

## Running Locally

No build step required – the app is a single self-contained HTML file.

```bash
# Python 3
python3 -m http.server 8080

# Node.js (npx)
npx serve .
```

Then open [http://localhost:8080](http://localhost:8080).

---

## Supported Lotteries

| Flag | Name | Format | Draw Days |
|------|------|--------|-----------|
| 🇿🇦 | SA Lotto | 6/52 + 1 bonus | Wed, Sat |
| 🇿🇦 | SA PowerBall | 5/50 + 1 PB/20 | Tue, Fri |
| 🇿🇦 | SA Daily Lotto | 5/36 | Daily |
| 🇺🇸 | US Powerball | 5/69 + 1 PB/26 | Mon, Wed, Sat |
| 🇺🇸 | Mega Millions | 5/70 + 1 MB/25 | Tue, Fri |
| 🇪🇺 | EuroMillions | 5/50 + 2 LS/12 | Tue, Fri |
| 🇬🇧 | UK Lotto | 6/59 + 1 bonus | Wed, Sat |
| 🇬🇧 | UK 49s | 6/49 + 1 booster | Mon–Sat |
| 🇬🇧 | UK 39s | 5/39 | Mon, Wed, Fri |
| 🇱🇹 | Lithuania Jega | 6/30 | Wed, Sat |
