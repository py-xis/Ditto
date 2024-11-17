Ditto

Ditto is a self-hosted, real-time clipboard synchronization tool powered by Firebase Firestore. It enables seamless clipboard sharing between multiple devices securely and efficiently. Ditto ensures that your clipboard is always in sync across all your devices without relying on third-party servers for hosting.

Features

	•	🔄 Real-Time Clipboard Sync: Automatically synchronize clipboard content across multiple devices.
	•	🔐 End-to-End Encryption: Your clipboard content is encrypted using AES-256 for ultimate privacy and security.
	•	📂 Self-Hosted: Leverage Firebase Firestore to host and manage your clipboard data.
	•	⚡ Cross-Platform: Works across any devices that can run Python and support Firebase.
	•	🛠️ Lightweight: Minimal resource usage with no bloatware.

How It Works

	1.	Each device runs Ditto as a self-hosted Python application.
	2.	Clipboard changes are detected and uploaded to Firebase Firestore after encryption.
	3.	Other devices retrieve the encrypted data, decrypt it, and update their local clipboard in real time.
	4.	Only authenticated devices can participate in the synchronization.

Requirements

	1.	Python 3.9+ installed on all devices.
	2.	Firebase Firestore account.
	3.	A valid firestore.json service account key file downloaded from the Firebase Console.

Installation

Follow the steps below to get started:

Step 1: Clone the Repository

git clone https://github.com/your-username/Ditto.git
cd Ditto

Step 2: Install Dependencies

Install the required Python libraries:

pip install -r requirements.txt

Step 3: Set Up Firebase Firestore

	1.	Create a Firebase project in the Firebase Console.
	2.	Enable Firestore Database in the project.
	3.	Download the firestore.json file:
	•	Go to Project Settings > Service Accounts.
	•	Click Generate New Private Key and download the firestore.json file.
	•	Save the firestore.json file in the Ditto project directory.

Step 4: Configure Firestore Rules

Set up Firestore security rules to ensure that only authenticated devices can read/write data:

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /clipboard_data/{userId} {
      allow read, write: if request.auth != null;
    }
  }
}

Step 5: Run Ditto

Start Ditto by running the following command:

python startScript.py

Usage

	1.	On the first run, you’ll be asked to enter a unique username.
	•	This username will be used to group your devices for synchronization.
	2.	Ditto will automatically add the current device to Firestore.
	3.	Clipboard changes will sync in real-time between all devices using the same username.

Project Structure

Ditto/
│
├── clipboard.py         # Clipboard management (singleton implementation)
├── database.py          # Database interaction with Firebase Firestore
├── Encryption.py        # AES-256 encryption and decryption
├── uploader.py          # Monitors clipboard changes and uploads data
├── listener.py          # Listens for clipboard changes from Firestore
├── startScript.py       # Entry point to start the app
├── requirements.txt     # Python dependencies
├── firestore.json       # Firebase service account key file (add this manually)
└── README.md            # Project documentation

Key Features of the Code

	1.	Clipboard Manager:
	•	Manages local clipboard access using the Clipboard class.
	•	Implements the Singleton pattern to ensure only one instance per process.
	2.	Encryption:
	•	Encrypts and decrypts clipboard content with AES-256 for security.
	•	Prevents unauthorized access to clipboard data.
	3.	Firebase Integration:
	•	Synchronizes clipboard content between devices using Firestore.
	•	Automatically adds new devices to the user group.
	4.	Real-Time Updates:
	•	The Listener monitors Firestore for changes and updates the clipboard.
	•	The Uploader detects local clipboard changes and uploads them to Firestore.

Contributing

Contributions are welcome! If you’d like to improve Ditto, feel free to:
	1.	Fork the repository.
	2.	Create a new branch for your feature or bug fix.
	3.	Submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments

	•	Built using the Firebase Admin SDK.
	•	Secure encryption powered by the cryptography library.
