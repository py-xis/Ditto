# from multiprocessing import Process
# from uploader import Uploader
# from listener import Listener
# from clipboard import Clipboard
# from database import Firebase

# def run_uploader(clipboard, firebase):
#     """Runs the Uploader process."""
#     user = "pranav_kulkarni"  # Replace with your user identifier
#     uploader = Uploader(user, clipboard, firebase)
#     uploader.monitor_clipboard()

# def run_listener(clipboard, firebase):
#     """Runs the Listener process."""
#     user = "pranav_kulkarni"  # Replace with your user identifier
#     listener = Listener(user, clipboard, firebase)
#     listener.listen_for_updates()

# if __name__ == "__main__":
#     # Instantiate shared singletons
#     user = "pranav_kulkarni"  # Replace with your user identifier
#     clipboard = Clipboard()  # Singleton instance of Clipboard
#     firebase = Firebase(user)  # Singleton instance of Firebase

#     # Create processes for Uploader and Listener
#     uploader_process = Process(target=run_uploader, args=(clipboard, firebase))
#     listener_process = Process(target=run_listener, args=(clipboard, firebase))

#     # Start both processes
#     uploader_process.start()
#     listener_process.start()

#     print("Uploader and Listener processes started. Press Ctrl+C to stop.")

#     # Keep the main script alive to monitor both processes
#     try:
#         uploader_process.join()
#         listener_process.join()
#     except KeyboardInterrupt:
#         print("Stopping processes...")
#         uploader_process.terminate()
#         listener_process.terminate()
#         print("Processes stopped.")


from threading import Thread
from modules.uploader import Uploader
from modules.listener import Listener
from modules.clipboard import Clipboard
from modules.database import Firebase

def run_uploader(clipboard, firebase,userr):
    """Runs the Uploader thread."""
    user = userr  # Replace with your user identifier
    uploader = Uploader(user, clipboard, firebase)
    uploader.monitor_clipboard()

def run_listener(clipboard, firebase,userr):
    """Runs the Listener thread."""
    user = userr  # Replace with your user identifier
    listener = Listener(user, clipboard, firebase)
    listener.listen_for_updates()

if __name__ == "__main__":
    # Instantiate shared singletons
    print("Starting Ditto")
    userName = input("Enter username:  ")
    user = userName  # Replace with your user identifier
    clipboard = Clipboard()  # Shared Clipboard instance
    firebase = Firebase(user)  # Shared Firebase instance

    firebase.add_new_device()

    # Create threads for Uploader and Listener
    uploader_thread = Thread(target=run_uploader, args=(clipboard, firebase,user))
    listener_thread = Thread(target=run_listener, args=(clipboard, firebase,user))

    # Start both threads
    uploader_thread.start()
    listener_thread.start()

    print("Uploader and Listener threads started. Press Ctrl+C to stop.")

    # Keep the main script alive to monitor both threads
    try:
        uploader_thread.join()
        listener_thread.join()
    except KeyboardInterrupt:
        print("Stopping threads...")
        print("Threads stopped.")