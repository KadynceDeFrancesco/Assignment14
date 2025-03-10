from tkinter import *
from tkinter import messagebox
import requests
import sentimentAnalyzer  # Import your sentiment analysis module

class UserPostGUI:

    def __init__(self, root, user_handle, session_token):
        print("UserPostGUI opened")

        self.user_handle = user_handle
        self.session_token = session_token
        self.posts = []
        self.current_post_index = 0

        self.window = Toplevel(root)
        self.window.title("User Post GUI")
        self.window.geometry("500x450")
        self.window.configure(bg="#0088FF")

        ### Main Frame to Center Everything
        main_frame = Frame(self.window)
        main_frame.pack(expand=True, anchor="center")  # Expand ensures full centering

        # **Title**
        Label(main_frame, text="Bluesky Post Viewer", font=("Arial", 14)).pack(pady=10)

        # **Username input**
        Label(main_frame, text="Enter Bluesky Username:", font=("Arial", 10)).pack()
        self.user_input = Entry(main_frame, width=30)
        self.user_input.pack(pady=5)

        # **Post display area**
        self.post_display = Text(main_frame, wrap=WORD, width=50, height=5)
        self.post_display.pack(pady=10)


        nav_frame = Frame(main_frame)
        nav_frame.pack(fill=X, pady=10)  # Fill entire width for proper alignment

        # Left-aligned Previous Post button
        Button(nav_frame, text="Previous", command=self.show_previous_post).grid(row=0, column=0, padx=15, sticky=W)

        # Centered Sentiment Label
        self.sentiment_label = Label(nav_frame, text="Sentiment: N/A", font=("Arial", 12))
        self.sentiment_label.grid(row=0, column=1, padx=10)

        # Right-aligned Next Post button
        Button(nav_frame, text="  Next  ", command=self.show_next_post).grid(row=0, column=2, padx=15, sticky=E)

        Button(main_frame, text="Fetch Posts", command=self.fetch_and_display_posts).pack(pady=10)

        # **Clear & Exit Buttons (Below Fetch Button)**
        Button(main_frame, text="Clear", command=self.clear_fields).pack(pady=5)
        Button(main_frame, text="Exit", command=self.exit_application).pack(pady=5)

    def fetch_bluesky_posts(self, user_handle):
        """Fetch latest posts from a given Bluesky user."""
        if not self.session_token:
            return []

        if not user_handle:
            messagebox.showerror("Error", "⚠️ Error: user_handle is empty. Cannot fetch posts.")
            return []

        # Bluesky API request
        feed_url = f"https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed?actor={user_handle}"
        headers = {"Authorization": f"Bearer {self.session_token}"}
        response = requests.get(feed_url, headers=headers)

        if response.status_code == 200:
            posts = response.json().get("feed", [])
            return [post["post"]["record"]["text"] for post in posts if "post" in post and "record" in post["post"] and "text" in post["post"]["record"]]

        messagebox.showerror("Fetch Failed", f"❌ Failed to fetch posts: {response.text}")
        return []

    def fetch_and_display_posts(self):
        """Fetches posts from the provided username and displays them."""
        entered_user = self.user_input.get().strip()

        if entered_user:
            self.posts = self.fetch_bluesky_posts(entered_user)
            if self.posts:
                self.current_post_index = 0
                self.update_post_display()
            else:
                self.post_display.delete(1.0, END)
                self.post_display.insert(INSERT, "No posts found.")
                self.sentiment_label.config(text="Sentiment: N/A")

    def update_post_display(self):
        """Updates the displayed post and its sentiment analysis."""
        self.post_display.delete(1.0, END)
        self.post_display.insert(INSERT, self.posts[self.current_post_index])

        # Perform sentiment analysis
        sentiment = sentimentAnalyzer.analyze_sentiment(self.posts[self.current_post_index])
        self.sentiment_label.config(text=f"Sentiment: {sentiment}")

    def show_next_post(self):
        """Displays the next post."""
        if self.posts:
            self.current_post_index = (self.current_post_index + 1) % len(self.posts)
            self.update_post_display()

    def show_previous_post(self):
        """Displays the previous post."""
        if self.posts:
            self.current_post_index = (self.current_post_index - 1) % len(self.posts)
            self.update_post_display()

    def clear_fields(self):
        """Clears the username search bar and post display area."""
        self.user_input.delete(0, END)
        self.post_display.delete(1.0, END)
        self.sentiment_label.config(text="Sentiment: N/A")

    def exit_application(self):
        """Completely exits the software."""
        self.window.quit()  # Stops the Tkinter event loop
        self.window.destroy()  # Destroys all windows
        exit(0)  # Fully exits the program
