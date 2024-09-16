# Bulk_Mail
Bulk Email Sender
This Python script allows you to send bulk emails with attachments using Gmail's SMTP server. It is designed to send emails to a list of recipients provided in a CSV file, with support for retrying failed attempts and sending emails in batches to avoid overwhelming the server.

Features
Send emails to a list of recipients in a CSV file
Attach multiple files to each email
Supports retry logic for failed email attempts
Batch processing to avoid hitting Gmail rate limits
HTML-formatted email content
Requirements
Python 3.x
Libraries:
smtplib
pandas
email.mime for handling email MIME types
time for adding delays between retries and batches
Install Dependencies
You can install the required dependencies using the following command:

bash
Copy code
pip install pandas
Usage
1. Set Up Email Credentials
To send emails through Gmail's SMTP server, you'll need to enable App Passwords for your Gmail account. Follow these steps:

Go to your Google Account's Security settings.
Enable 2-Step Verification if you haven’t done so.
Create an App Password (for example, select "Mail" and "Windows Computer" as the app and device).
Copy the app password.
2. Configure the Script
Edit the script to include your Gmail email address and app password in the appropriate section.

python
Copy code
from_email = 'your-email@gmail.com'  # Your Gmail address
from_password = 'your-app-password'  # Your Gmail app password
3. Prepare the CSV File
Create a CSV file containing the list of recipient emails. The file should have a single column named emails.

Example CSV file (emails_mat.csv):

csv
Copy code
emails
recipient1@example.com
recipient2@example.com
recipient3@example.com
4. Run the Script
Place your email content in the subject and body variables. You can also specify any attachments in the attachments list.

Run the script:

bash
Copy code
python bulkmail.py
The script will read the emails from the CSV file, send the email to each recipient in batches, and include any specified attachments. Failed emails will be retried up to three times, and the script will pause between batches to avoid overwhelming the SMTP server.

5. Batch Sending and Retry Logic
The script is designed to send emails in batches (default is 10 emails per batch). You can adjust the batch_size and the batch_delay between batches. The delay is set in minutes to avoid sending too many emails too quickly.

Sample Email Body
You can format the body of the email using HTML tags for better styling.

python
Copy code
body = '''
We are excited to invite your students to Make-a-Ton 7.0, Kerala's largest hackathon organized by CITTIC, Cochin University of Science and Technology on October 19-20th, 2024. 
This event will bring together students from different colleges for 24 hours to innovate, network, and develop their skills. 
We’ve attached the brochure with all the event details. 

Best regards, <br>
Make-a-Ton 7.0 Team
'''
6. Logs and Feedback
The script will print out logs in the console, including how many emails were successfully sent and how many failed. In case of an error, it will retry sending up to 3 times, after which it will skip the email.

Important Notes
Gmail's SMTP server has limits for sending emails, especially if sending in bulk. Be sure to follow Gmail's sending limits (500 emails/day for free accounts) to avoid temporary suspension.
Ensure that you are not spamming recipients and that they have agreed to receive emails from you.
You might need to adjust your Gmail security settings to allow access for less secure apps.
Future Improvements
Support for other email providers such as Outlook or Yahoo.
Ability to send personalized email content to each recipient.
Advanced logging for tracking which emails failed and why.
