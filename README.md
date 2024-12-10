# ✨ Ditto : A Cross Platform Shared Clipboard Application.

Ditto is a real-time clipboard synchronization tool powered by Firebase Firestore. It enables seamless clipboard sharing between multiple devices securely and efficiently. With end-to-end encryption, Ditto ensures your clipboard content stays private while synchronizing across devices, eliminating the need for third-party servers.

## 🚀 Features

- 🔄 Real-Time Clipboard Sync: Automatically sync clipboard content across devices in real time.
- 🔐 End-to-End Encryption: AES-256 encryption ensures your clipboard data remains secure.
- ⚡ Cross-Platform: Compatible with any device that runs Python and supports Firebase.
- 🛠️ Lightweight: Minimal resource usage with no unnecessary bloat.

## 🛠️ How It Works

- Run Ditto on each device as a self-hosted Python application.
- Clipboard changes are encrypted and uploaded to Firebase Firestore.
- Other devices retrieve the encrypted data, decrypt it, and update their local clipboard in real time.
- Only authenticated devices can participate in the synchronization.

## 📋 Requirements

- Python 3.9+ installed on all devices.
- Firebase Firestore account.
- A valid firestore.json service account key file downloaded from the Firebase Console.

## ⚙️ Installation

## Step 1: Clone the Repository

```
git clone https://github.com/py-xis/Ditto.git
```
```
cd Ditto
```

## Step 2 : Ensure that you have the firebase config json file in the project's root directory. The directory must look like this with the firebase config json file.


<img width="521" alt="Screenshot 2024-12-10 at 6 43 00 PM" src="https://github.com/user-attachments/assets/ccfda95c-f90e-4272-a1c9-50476c066222">
<img width="951" alt="Screenshot 2024-12-10 at 6 43 18 PM" src="https://github.com/user-attachments/assets/9b62f803-79c7-4ce8-aa11-f7064e96e064">


## Step 3: Install Dependencies

Install the required Python libraries:

```
pip install -r requirements.txt
```

- Note the following,
- This project uses the pyperclip module. 
- If you are on windows, then you require no additional modules.
- If you are on macOS, you need pbcopy and pbpaste commands, which should come with the os.
- If you are on Linux, then pyperclip module makes use of the xclip or xsel commands, which should come with the os. Otherwise run ```sudo apt-get install xclip``` or ```sudo apt-get install xsel``` (Note: xsel does not always seem to work.)

## Step 4: Set Up Firebase Firestore
**(Not needed if, you already have a firebase config file)**
1. Create a Firebase project in the Firebase Console.
2. Enable the Firestore Database in the project.
3. Download the firestore.json file:
   - Go to Project Settings > Service Accounts.
   - Click Generate New Private Key and download the file.
   - Save the firestore.json file in the Ditto project directory.

### Step 4: Configure Firestore Rules
**(Not needed if, you already have a firebase config file)**

## Step 5: Run Ditto

Start Ditto using the following command:

```
python startScript.py
```

## 📖 Usage

1. On the first run, enter a unique username. This username will group your devices for synchronization.
2. Ditto will automatically add the current device to Firestore.
3. Clipboard changes will sync in real-time across all devices using the same username.


## 🔑 Key Features of the Code

## 📋 Clipboard Manager

- Manages local clipboard access using the Clipboard class.
- Implements the Singleton Pattern to ensure a single instance per process.

## 🔐 Encryption

- AES-256 encryption/decryption for ultimate security.
- Protects clipboard data from unauthorized access.

## 🔗 Firebase Integration

- Synchronizes clipboard content using Firestore.
- Automatically adds new devices to the user group.

## 🔄 Real-Time Updates

- Listener monitors Firestore for changes and updates the clipboard.
- Uploader detects local clipboard changes and uploads them to Firestore.
