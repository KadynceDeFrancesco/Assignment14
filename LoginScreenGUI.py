from tkinter import *
from tkinter import messagebox
import tkinter as tk
import requests
from UserPostGUI import UserPostGUI

class LoginScreenGUI:
    """Login screen for Bluesky authentication"""

    def __init__(self, root):
        self.root = root
        self.root.title("Bluesky Login")
        self.root.geometry("350x250")
        self.root.configure(bg="white")

        Label(root, text="Sign in", font=("InterVariable", 18), bg="white").pack(pady=5)

        # Username input
        Label(root, text="Account Name:", font=("InterVariable", 12), bg="white").pack(pady=5)
        self.username_entry = Entry(root, width=30)
        self.username_entry.pack(pady=5)

        # Password input (masked)
        Label(root, text="Password:", font=("InterVariable", 12), bg="white").pack(pady=5)
        self.password_entry = Entry(root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        tk.Button(text="Login",
                  highlightbackground="blue",
                  font=("InterVariable", 12),
                  activebackground="blue",
                  bg="#0088ff",
                  fg="black",
                  borderwidth=0, highlightthickness=0,
                  command=self.login).pack(pady=10)


    def authenticate_bluesky(self, username, password):
        """Authenticate with Bluesky API and return session token."""
        login_url = "https://bsky.social/xrpc/com.atproto.server.createSession"
        payload = {"identifier": username, "password": password}

        try:
            session_response = requests.post(login_url, json=payload)

            if session_response.status_code == 200:
                return session_response.json()["accessJwt"]
            else:
                messagebox.showerror("Login Failed", "❌ Authentication Failed! Check credentials.")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Network error: {e}")
            return None

    def login(self):
        """Handles login validation and opens the UserPost GUI."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password.")
            return

        # Authenticate with Bluesky
        session_token = self.authenticate_bluesky(username, password)

        if session_token:
            messagebox.showinfo("Login Success", "Welcome," + username)
            self.root.withdraw()
            UserPostGUI(self.root, username, session_token)  # Open UserPostGUI


if __name__ == "__main__":
    root = Tk()
    app = LoginScreenGUI(root)
    root.mainloop()
