/**
 * Firebase Configuration for Bophelong Lotto Management System
 *
 * Setup Instructions:
 * 1. Go to https://console.firebase.google.com/ and create (or select) a project.
 * 2. In Project Settings > General, click "Add app" and choose the Web (</>)  platform.
 *    Copy the firebaseConfig object that is shown and paste the values below.
 * 3. Enable Firestore Database under Build > Firestore Database (Native mode).
 * 4. Enable Anonymous Authentication under Build > Authentication > Sign-in method.
 * 5. Apply the Firestore Security Rules shown below in the Rules tab of your
 *    Firestore Database console.
 * 6. Replace every "YOUR_…" placeholder below with your actual project values.
 *
 * ── Recommended Firestore Security Rules ──────────────────────────────────────
 *
 *   rules_version = '2';
 *   service cloud.firestore {
 *     match /databases/{database}/documents {
 *       match /users/{userId}/{document=**} {
 *         allow read, write: if request.auth != null
 *                            && request.auth.uid == userId;
 *       }
 *     }
 *   }
 *
 * ──────────────────────────────────────────────────────────────────────────────
 *
 * ⚠️  Security note:
 *    Avoid committing real API keys to a public repository.
 *    For production deployments use environment variables, a CI/CD secret, or
 *    Firebase App Hosting's built-in secrets management.
 */

var FIREBASE_CONFIG = {
    apiKey:            'AIzaSyDda_Ns_ca4XqxD6e89hBaGAWz5vt1he8I',
    authDomain:        'lotto-management-system-26761.firebaseapp.com',
    projectId:         'lotto-management-system-26761',
    storageBucket:     'lotto-management-system-26761.firebasestorage.app',
    messagingSenderId: '986799310017',
    appId:             '1:986799310017:web:f65d7f237c26e8834d4040',
    measurementId:     'G-EPNKLK5B52'
};
