# SentimentAnalyzer

## Overview
**SentimentAnalyzer** is a **Graphical User Interface (GUI)** application that allows users to pull posts from any **Bluesky** account and analyze the **sentiment** of each post using **NLTK's VADER sentiment analysis**.

The application starts with a **login screen**, where users enter their **Bluesky credentials** to authenticate with the **Bluesky API**. After logging in, users can enter any **Bluesky username** to retrieve posts from that account. The GUI provides **navigation buttons** to browse through posts, and a **status bar** displays the sentiment analysis result of each post.

---

## Features
- **Login Authentication** – Users must log in with their Bluesky credentials to access the API.  
- **Fetch Posts from Any User** – Enter any Bluesky username to pull their latest posts.  
- **Sentiment Analysis** – Uses **NLTK’s VADER** to classify posts as **Positive, Negative, or Neutral**.  
- **Post Navigation** – Use **Next and Previous buttons** to browse through posts.  
- **Graphical User Interface (GUI)** – Built using **Tkinter** for an interactive experience.  

---

## Installation
### Prerequisites
Ensure you have **Python 3.8+** installed. Then, install the required dependencies:

```bash
pip install nltk requests tkinter
