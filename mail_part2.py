import requests
import pdfplumber
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

url = "http://localhost:11434/api/chat"

def extract_text_from_pdf(pdf_path):
    print(f"Extracting text from PDF: {pdf_path}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        print(f"Text extraction successful. Extracted {len(text)} characters.")
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

pdf_path = "/Users/sampsamp/Desktop/BNHS/pdfs/SEPTEMBER-NEWSLETTER-BNHS-2024.pdf"

def get_summary(data):
    payload = {
        "model": "llama2:latest",
        "messages": [
            {
                "role" : "system",
                "content" : "You're BNHS AI assistant"
            },
            {
            "role": "user",
            "content": f"Can you summarize this {data} for me?"
            }
        ]
    }


    response = requests.post(url, json=payload)
    # import pdb;pdb.set_trace()
    if response.status_code == 200:
        return response.text

def send_email(subject, body, recipient_email):
    sender_email = "sustainathon06@gmail.com"
    sender_password = "klsnwqtxvhsqdjkp"
    
    print(f"Preparing to send email to {recipient_email}")
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Attach the body (summary of the newspaper)
        msg.attach(MIMEText(body, 'plain'))
        
        # Setup the SMTP server (use Gmail SMTP or any other service you prefer)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send the email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    text = extract_text_from_pdf(pdf_path)
    # response = requests.post(url, json={"message": text})
    # print(response.json())
    whole_dump = get_summary(text)
    contents = []
    for line in whole_dump.strip().split('\n'):
        try:
            data = json.loads(line)  # Parse JSON
            contents.append(data["message"]["content"])  # Extract the content
        except json.JSONDecodeError as e:
            print(f"❌ Error decoding JSON: {e}")
    final_content = "".join(contents)
    print(final_content)
    recipient_email = "ashwinihegde234@gmail.com"
    send_email("Newspaper Summary", final_content, recipient_email)