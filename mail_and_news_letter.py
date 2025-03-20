import requests
from bs4 import BeautifulSoup
import os
import pdfplumber
import json
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# URL of the BNHS newsletter page
NEWSLETTER_URL = "https://bnhs.org/news-letter"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
TRACK_FILE = "downloaded_newsletters.txt"
SUMMARY_API_URL = "http://localhost:11434/api/chat"

SENDER_EMAIL = "sustainathon06@gmail.com"
SENDER_PASSWORD = "klsnwqtxvhsqdjkp"
RECIPIENT_EMAIL = ["ashwinihegde234@gmail.com", "neigant1274@gmail.com", "chethansaikumar9604@gmail.com"]


# Function to get downloaded newsletters
def get_downloaded_newsletters():
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, "r") as f:
            return {
                line.split(" | ")[1].strip() for line in f.readlines()
            }  # Extract filenames
    return set()


# Function to update the downloaded newsletter record
def update_downloaded_newsletters(filename):
    download_date = datetime.now().strftime("%Y-%m-%d")
    with open(TRACK_FILE, "a") as f:
        f.write(f"{download_date} | {filename}\n")


# Function to get the latest newsletter link
def get_latest_newsletter():
    response = requests.get(NEWSLETTER_URL, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a", href=True):
            if ".pdf" in link["href"] and "news_letter_pdf" in link["href"]:
                return link["href"]
    return None


# Function to download the newsletter
def download_newsletter(pdf_link):
    if not pdf_link.startswith("http"):
        pdf_link = os.path.join(NEWSLETTER_URL, pdf_link)

    filename = pdf_link.split("/")[-1]
    downloaded_newsletters = get_downloaded_newsletters()

    if filename in downloaded_newsletters:
        print(f"Newsletter {filename} already downloaded. Skipping.")
        return None

    print(f"Downloading: {filename}")
    pdf_response = requests.get(pdf_link, headers=HEADERS)
    if pdf_response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(pdf_response.content)
        print(f"Downloaded: {filename}")
        update_downloaded_newsletters(filename)
        return filename
    else:
        print("Failed to download.")
        return None


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "".join(
                page.extract_text() for page in pdf.pages if page.extract_text()
            )
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None


# Function to summarize text using AI
def get_summary(text):
    payload = {
        "model": "llama2:latest",
        "messages": [
            {"role": "system", "content": "You're BNHS AI assistant"},
            {"role": "user", "content": f"Can you summarize this {text} for me?"},
        ],
    }
    response = requests.post(SUMMARY_API_URL, json=payload)
    if response.status_code == 200:
        contents = []
        for line in response.text.strip().split("\n"):
            try:
                data = json.loads(line)
                contents.append(data["message"]["content"])
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        return "".join(contents)
    return None


# Function to send email
def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        # msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print(f"Email sent to {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"Email failed: {e}")


# Main execution
def main():
    print("Checking for new newsletters...")
    latest_newsletter = get_latest_newsletter()

    if latest_newsletter:
        pdf_filename = download_newsletter(latest_newsletter)
        if pdf_filename:
            text = extract_text_from_pdf(pdf_filename)
            if text:
                # summary = 'Hi Conservationist!!, \n '+' '+ get_summary(text) + ' \n' + 'Find the complete news letter on \n '+NEWSLETTER_URL+' \nRegards, \n BNHS'
                summary = f"""
🌿✨ Greetings, Conservationist!✨🌿  

Here's your latest BNHS Newsletter summary:  

📜 Summary:
{get_summary(text)}  

🔗 Read the complete newsletter here:
➡️ {NEWSLETTER_URL}  

🌎 Stay inspired. Keep conserving.  
Best Regards,  
BNHS Team 🦜🌱
"""

                if summary:
                    send_email("BNHS Newsletter Summary", summary)
                else:
                    print("Failed to generate summary.")
            else:
                print("Failed to extract text.")
    else:
        print("No new newsletter found.")


if __name__ == "__main__":
    main()
