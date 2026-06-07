/**
 * Firebase Configuration for LottoCanvas Workstation
 *
 * Setup Instructions:
 * 1. Go to https://console.firebase.google.com/ and create (or select) a project.
 * 2. In Project Settings > General, click "Add app" and choose the Web (</>)  platform.
 *    Copy the firebaseConfig object that is shown and paste the values below.
 * 3. Enable Firestore Database under Build > Firestore Database (Native mode).
 * 4. Enable Email/Password Authentication under Build > Authentication > Sign-in method.
 * 5. Enable Phone Authentication under Build > Authentication > Sign-in method so that
 *    the phone OTP flow works.
 * 6. (Optional) Enable Anonymous Authentication as well if you want the guest mode
 *    button in the app to work.
 * 7. Enable Firebase App Check with a reCAPTCHA Enterprise provider, then copy your
 *    reCAPTCHA Enterprise site key for use below as appCheckEnterpriseKey.
 * 8. Apply the rules from firestore.rules and database.rules.json in your Firebase
 *    console (or deploy them with the Firebase CLI).
 * 9. Replace every "YOUR_…" placeholder below with your actual project values.
 *
 * See firestore.rules and database.rules.json in the repository root for the
 * checked-in Firebase security rules used by this app.
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
    appId:             '1:986799310017:web:3dd73e67ccc1654b4d4040',
    measurementId:     'G-9E7QXGCQW8',
    databaseURL:       'https://lotto-management-system-26761-default-rtdb.firebaseio.com',
    appCheckEnterpriseKey: ''
};
