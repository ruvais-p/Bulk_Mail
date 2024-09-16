import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time
import random  # Import random module

# Function to send email with attachment
def send_email(to_email, subject, body, from_email, from_password, attachment_path=None):
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the email body to the message (HTML format)
        msg.attach(MIMEText(body, 'html'))

        # Attach file (if any)
        if attachment_path:
            filename = os.path.basename(attachment_path)
            try:
                with open(attachment_path, "rb") as attachment:
                    # Instance of MIMEBase and named as part
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())

                # Encode into base64
                encoders.encode_base64(part)

                part.add_header('Content-Disposition', f"attachment; filename= {filename}")

                # Attach the instance 'part' to the message
                msg.attach(part)
            except Exception as file_error:
                print(f"Failed to attach file {attachment_path}: {str(file_error)}")
                # Continue sending email without attachment if attachment fails

        # Connect to the server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use Gmail's SMTP server and port
        server.starttls()

        # Login to your email account
        server.login(from_email, from_password)

        # Send email
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        # Success message
        print(f"Email successfully sent to {to_email}")
        return True  # Return success status

    except smtplib.SMTPRecipientsRefused:
        print(f"Error: All recipients were refused. Failed to send email to {to_email}.")
    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Please check your email and password.")
    except smtplib.SMTPSenderRefused:
        print(f"Error: The server didn’t accept the sender address. Failed to send email to {to_email}.")
    except smtplib.SMTPDataError:
        print(f"Error: The server replied with an unexpected error code or message. Failed to send email to {to_email}.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}. Failed to send email to {to_email}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Failed to send email to {to_email}.")
    return False  # Return failure status

# Function to send email with retry logic
def send_email_with_retry(to_email, subject, body, from_email, from_password, attachment_path=None, retries=3):
    for attempt in range(retries):
        if send_email(to_email, subject, body, from_email, from_password, attachment_path):
            return True
        print(f"Retrying... ({attempt + 1}/{retries})")
        time.sleep(5)  # Wait 5 seconds before retrying
    return False

# Read the CSV file
csv_file = r'path of csv file'  # Replace with your CSV file path
df = pd.read_csv(csv_file, encoding='ISO-8859-1')  # or try 'cp1252'

# Email credentials
from_email = 'abc@gmail.com'  # Replace with your email
from_password = 'app password'  # Replace with your app password

# Email content with HTML formatting
subject = 'subject'
body = '''
    --body of mail 
'''

# List of attachments
attachments = []  # No attachments, or you can add paths if needed

# Initialize counters for total emails and successful emails
total_emails = 0
successful_emails = 0
batch_size = 15  # Number of emails per batch
batch_delay = random.randint(8, 20) * 60  # Delay in seconds (10 to 50 minutes)

# Iterate through the email list and send emails in batches
for index, row in df.iterrows():
    to_email = row['Email']  # Replace 'emails' with the correct column name in your CSV
    total_emails += 1  # Increment total emails counter
    
    # Send email with all attachments
    for attachment_path in attachments:
        if send_email_with_retry(to_email, subject, body, from_email, from_password, attachment_path):
            successful_emails += 1  # Increment successful emails counter

    # If no attachments, send email without any attachments
    if not attachments:
        if send_email_with_retry(to_email, subject, body, from_email, from_password):
            successful_emails += 1  # Increment successful emails counter

    # Check if the batch size has been reached
    if total_emails % batch_size == 0:
        print(f"Batch limit reached. Pausing for {batch_delay // 60} minutes...")
        time.sleep(batch_delay)  # Pause before sending the next batch

# Print the final count of emails sent
print(f"Total emails attempted: {total_emails}")
print(f"Total emails successfully sent: {successful_emails}")
