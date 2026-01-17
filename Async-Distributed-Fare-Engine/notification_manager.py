# notification_manager.py
from twilio.rest import Client
import smtplib 

class NotificationManager:
    """
    Manages sending SMS and Email notifications.
    """
    def __init__(self, sid, auth_token, twilio_number, receiver_number, my_mail, my_pass, smtp_server):
        """
        Initializes the Twilio client and email credentials.
        """
        # Twilio setup 
        self.client = Client(sid, auth_token)
        self.twilio_number = twilio_number
        self.receiver_number = receiver_number
        
        # Email setup 
        self.my_mail = my_mail
        self.my_pass = my_pass
        self.smtp_server = smtp_server

    def send_sms(self, message_body: str):
        """
        Sends a text message with the specified body to the verified number.
        """
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=self.twilio_number,
                to=self.receiver_number
            )
            print(f"\n✅ SMS Status: {message.status}")
        except Exception as e:
            print(f"❌ Failed to send SMS: {e}")
            
    def send_individual_email(self, recipient_email: str, email_subject: str, email_body: str):
        """
        Sends a single email with the flight deal details.
        """
        try:
            with smtplib.SMTP(self.smtp_server, 587) as connection:
                connection.starttls()
                connection.login(self.my_mail, self.my_pass)
                
                # Construct the full message (subject and body)
                full_msg = f'Subject: {email_subject}\n\n{email_body}'
                
                connection.sendmail(
                    from_addr=self.my_mail, 
                    to_addrs=recipient_email,
                    msg=full_msg.encode('utf-8')
                )
            
            print(f"✅ Sent deal email to {recipient_email}")
        except Exception as e:
            print(f"❌ Failed to send email to {recipient_email}: {e}")