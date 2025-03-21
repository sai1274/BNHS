import requests
import os
import pdfplumber
import json
from datetime import datetime
from bs4 import BeautifulSoup

# Configuration
NEWSLETTER_URL = "https://bnhs.org/news-letter"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
TRACK_FILE = "downloaded_newsletters.txt"
SUMMARY_API_URL = "http://localhost:11434/api/chat"

# WhatsApp Configuration
ULTRAMSG_INSTANCE = "instance111020"
ULTRAMSG_TOKEN = "8ejwkcqv5vtnuwm1"
PHONE_NUMBERS = ["919640434636"]  # Add recipient numbers

# Function to track downloaded newsletters


def get_downloaded_newsletters():
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, "r") as f:
            return {line.split(" | ")[1].strip() for line in f.readlines()}
    return set()


def update_downloaded_newsletters(filename):
    with open(TRACK_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d')} | {filename}\n")


def get_latest_newsletter():
    response = requests.get(NEWSLETTER_URL, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a", href=True):
            if ".pdf" in link["href"] and "news_letter_pdf" in link["href"]:
                return link["href"]
    return None


def download_newsletter(pdf_link):
    filename = pdf_link.split("/")[-1]
    if filename in get_downloaded_newsletters():
        print(f"Newsletter {filename} already downloaded. Skipping.")
        return None

    response = requests.get(pdf_link, headers=HEADERS)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        update_downloaded_newsletters(filename)
        return filename
    return None


# def extract_text_from_pdf(pdf_path):
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             return "".join(page.extract_text() for page in pdf.pages if page.extract_text())
#     except Exception as e:
#         print(f"Error extracting text: {e}")
#         return None

import re

def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

            # Remove excessive whitespace and fix broken words
            text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
            text = re.sub(r"(?<=\w)-\s(?=\w)", "", text)  # Fix hyphenated words split across lines
            
            return text.strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None


# def get_summary(text):
#     payload = {"model": "llama2:latest", "messages": [{"role": "user", "content": f"Summarize this: {text}"}]}
#     response = requests.post(SUMMARY_API_URL, json=payload)
#     return response.json().get("message", {}).get("content", "Summary not available.") if response.status_code == 200 else None


def get_summary(text):
    payload = {
        "model": "llama2:latest",
        "messages": [{"role": "user", "content": f"Summarize this: {text}"}]
    }

    response = requests.post(SUMMARY_API_URL, json=payload)

    if response.status_code == 200:
        try:
            # Split response by lines in case of multiple JSON objects
            contents = []
            for line in response.text.strip().split("\n"):
                try:
                    data = json.loads(line)
                    contents.append(data.get("message", {}).get("content", ""))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
            return " ".join(contents).strip() if contents else "Summary not available."
        except Exception as e:
            print(f"Unexpected error processing summary response: {e}")
            return "Summary not available."
    return None


def send_whatsapp_message(message):
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE}/messages/chat"
    for phone in PHONE_NUMBERS:
        payload = {"token": ULTRAMSG_TOKEN, "to": phone, "body": message}
        response = requests.post(url, data=payload)
        print(response.json())


def main():
    print("Checking for new newsletters...")
    latest_newsletter = get_latest_newsletter()
    if latest_newsletter:
        pdf_filename = download_newsletter(latest_newsletter)
        if pdf_filename:
            text = extract_text_from_pdf(pdf_filename)
            if text:
                summary = get_summary(text)
                message = f"🌿 BNHS Newsletter Update 🌿\n\n📜 Summary: {summary}\n🔗 Read full newsletter: {NEWSLETTER_URL}\nKeep conserving! 🌎"
                send_whatsapp_message(message)
            else:
                print("Failed to extract text.")
    else:
        print("No new newsletter found.")


if __name__ == "__main__":
    main()
