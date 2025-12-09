"""
Email Sender Module
This module handles sending generated LinkedIn posts via email.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from src.config import get_secret
except ImportError:
    from config import get_secret

class EmailSender:
    """
    A class to send emails with LinkedIn posts.
    """
    
    def __init__(self):
        """Initialize the email sender with SMTP configuration."""
        self.sender_email = get_secret('EMAIL_SENDER')
        self.sender_password = get_secret('EMAIL_PASSWORD')
        self.recipient_email = get_secret('EMAIL_RECIPIENT')
        
        if not all([self.sender_email, self.sender_password]):
            raise ValueError("Email credentials not found. Please set EMAIL_SENDER and EMAIL_PASSWORD in .env file")
        
    
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Email Sender initialized successfully")
    
    def send_post(self, 
                      post: Dict[str, str], 
                      recipient: Optional[str] = None,
                      subject_prefix: str = "Generated LinkedIn Post") -> tuple:
        """
        Send a single post via email.
        
        Args:
            post (Dict[str, str]): The post data
            recipient (Optional[str]): Recipient email (uses default if not provided)
            subject_prefix (str): Prefix for email subject
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            recipient = recipient or self.recipient_email
            if not recipient:
                return False, "No recipient email specified"
            
            
            message = MIMEMultipart("alternative")
            message["Subject"] = f"{subject_prefix}: {post.get('title', 'Untitled')}"
            message["From"] = self.sender_email
            message["To"] = recipient
            
            
            email_body = self._create_email_body(post)
            
        
            text_part = MIMEText(email_body, "plain")
            html_part = MIMEText(self._create_html_body(post), "html")
            
            message.attach(text_part)
            message.attach(html_part)
            
            
            success, msg = self._send_email(message, recipient)
            if success:
                self.logger.info(f"Post email sent successfully to {recipient}")
                return True, f"Email sent successfully to {recipient}"
            else:
                self.logger.error(f"Email send failed: {msg}")
                return False, msg
            
        except Exception as e:
            error_msg = f"Error sending post email: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def send_to_multiple_recipients(self, 
                                   post: Dict[str, str], 
                                   recipients: List[str],
                                   subject_prefix: str = "Generated LinkedIn Post",
                                   personalized_subjects: Optional[Dict[str, str]] = None) -> Dict[str, tuple]:
        """
        Send a single post to multiple recipients.
        
        Args:
            post (Dict[str, str]): The post data
            recipients (List[str]): List of recipient email addresses
            subject_prefix (str): Default subject prefix
            personalized_subjects (Optional[Dict[str, str]]): Custom subjects per recipient
            
        Returns:
            Dict[str, tuple]: Results for each recipient (email -> (success, message))
        """
        results = {}
        
        for recipient in recipients:
            try:
                
                if personalized_subjects and recipient in personalized_subjects:
                    custom_subject = personalized_subjects[recipient]
                else:
                    custom_subject = f"{subject_prefix}: {post.get('title', 'Untitled')}"
                
                
                message = MIMEMultipart("alternative")
                message["Subject"] = custom_subject
                message["From"] = self.sender_email
                message["To"] = recipient
                
            
                email_body = self._create_email_body(post)
                
            
                text_part = MIMEText(email_body, "plain")
                html_part = MIMEText(self._create_html_body(post), "html")
                
                message.attach(text_part)
                message.attach(html_part)
                
                
                success, msg = self._send_email(message, recipient)
                results[recipient] = (success, msg)
                
                if success:
                    self.logger.info(f"Post email sent successfully to {recipient}")
                else:
                    self.logger.error(f"Failed to send email to {recipient}: {msg}")
                
            except Exception as e:
                error_msg = f"Failed to send email to {recipient}: {str(e)}"
                results[recipient] = (False, error_msg)
                self.logger.error(error_msg)
        
        return results
    
    def send_multiple_posts(self, 
                           posts: List[Dict[str, str]], 
                           recipient: Optional[str] = None,
                           send_separately: bool = True) -> Dict[str, bool]:
        """
        Send multiple posts via email.
        
        Args:
            posts (List[Dict[str, str]]): List of posts
            recipient (Optional[str]): Recipient email
            send_separately (bool): Whether to send each post as separate email
            
        Returns:
            Dict[str, bool]: Results of each email send attempt
        """
        results = {}
        
        if send_separately:
            
            for i, post in enumerate(posts):
                post_title = post.get('title', f'Post {i+1}')
                success = self.send_post(
                    post=post,
                    recipient=recipient,
                    subject_prefix=f"Blog Post {i+1}"
                )
                results[post_title] = success
        else:
            
            success = self._send_combined_posts(posts, recipient)
            results['Combined Posts'] = success
        
        return results
    
    def send_with_attachment(self, 
                           post: Dict[str, str], 
                           attachment_path: str,
                           recipient: Optional[str] = None) -> bool:
        """
        Send post email with file attachment.
        
        Args:
            post (Dict[str, str]): The post data
            attachment_path (str): Path to the attachment file
            recipient (Optional[str]): Recipient email
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            recipient = recipient or self.recipient_email
            if not recipient:
                raise ValueError("No recipient email specified")
            
    
            message = MIMEMultipart()
            message["Subject"] = f"LinkedIn Post (with attachment): {post.get('title', 'Untitled')}"
            message["From"] = self.sender_email
            message["To"] = recipient
            
    
            email_body = self._create_email_body(post)
            message.attach(MIMEText(email_body, "plain"))
            
            
            if os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                filename = os.path.basename(attachment_path)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}'
                )
                message.attach(part)
            
        
            self._send_email(message, recipient)
            
            self.logger.info(f"Post email with attachment sent successfully to {recipient}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending email with attachment: {str(e)}")
            return False
    
    def _create_email_body(self, post: Dict[str, str]) -> str:
        """
        Create the plain text email body.
        """
        body = f"""
Hello!

I've generated a new LinkedIn post for you:

TITLE: {post.get('title', 'Untitled')}

CONTENT:
{post.get('content', 'No content available')}

"""
        
        if post.get('hashtags'):
            body += f"\nHASHTAGS: {post['hashtags']}\n"
        
        if post.get('call_to_action'):
            body += f"\nCALL TO ACTION: {post['call_to_action']}\n"
        
        body += f"""
---
Generated on: {post.get('generated_at', datetime.now().isoformat())}
Topic: {post.get('topic', 'Unknown')}
Tone: {post.get('tone', 'Unknown')}

Best regards,
LinkedIn Agent
"""
        
        return body
    
    def _create_html_body(self, post: Dict[str, str]) -> str:
        """
        Create the HTML email body for better formatting.
        """
        html = f"""
        <html>
        <head></head>
        <body>
            <h2>New LinkedIn Post Generated</h2>
            
            <h3 style="color: #0073b1;">{post.get('title', 'Untitled')}</h3>
            
            <div style="margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-left: 4px solid #0073b1;">
                <p style="white-space: pre-line; line-height: 1.6;">{post.get('content', 'No content available')}</p>
            </div>
        """
        
        if post.get('hashtags'):
            html += f"""
            <div style="margin: 15px 0;">
                <strong>Hashtags:</strong> <span style="color: #0073b1;">{post['hashtags']}</span>
            </div>
            """
        
        if post.get('call_to_action'):
            html += f"""
            <div style="margin: 15px 0; padding: 10px; background-color: #e7f3ff; border-radius: 5px;">
                <strong>Call to Action:</strong> {post['call_to_action']}
            </div>
            """
        
        html += f"""
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
            <small style="color: #666;">
                Generated on: {post.get('generated_at', datetime.now().isoformat())}<br>
                Topic: {post.get('topic', 'Unknown')}<br>
                Tone: {post.get('tone', 'Unknown')}
            </small>
            
            <p style="margin-top: 20px; color: #666;">
                Best regards,<br>
                <strong>LinkedIn Agent</strong>
            </p>
        </body>
        </html>
        """
        
        return html
    
    def _send_combined_posts(self, posts: List[Dict[str, str]], recipient: Optional[str] = None) -> bool:
        """
        Send multiple posts in a single email.
        """
        try:
            recipient = recipient or self.recipient_email
            if not recipient:
                raise ValueError("No recipient email specified")

            message = MIMEMultipart("alternative")
            message["Subject"] = f"Multiple LinkedIn Posts - {len(posts)} Posts Generated"
            message["From"] = self.sender_email
            message["To"] = recipient
            
            
            combined_body = f"Hello!\n\nI've generated {len(posts)} LinkedIn posts for you:\n\n"
            
            for i, post in enumerate(posts, 1):
                combined_body += f"=== BLOG POST {i} ===\n"
                combined_body += self._create_email_body(post)
                combined_body += "\n" + "="*50 + "\n\n"
            
            
            text_part = MIMEText(combined_body, "plain")
            message.attach(text_part)
            
            
            self._send_email(message, recipient)
            
            self.logger.info(f"Combined posts email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending combined posts email: {str(e)}")
            return False
    
    def _send_email(self, message, recipient: str) -> tuple:
        """
        Send the email using SMTP with proper error handling.
        Returns: (success: bool, message: str)
        """
        server = None
        try:
            self.logger.info(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)
            
            self.logger.info("SMTP connection established, starting TLS...")
            server.starttls()  # Enable security
            
            self.logger.info("Logging in with email credentials...")
            server.login(self.sender_email, self.sender_password)
            
            self.logger.info(f"Sending email to {recipient}...")
            text = message.as_string()
            server.sendmail(self.sender_email, recipient, text)
            
            self.logger.info("Email sent successfully, closing connection...")
            return True, "Email sent successfully"
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = "SMTP Authentication failed - Invalid EMAIL_PASSWORD or EMAIL_SENDER"
            self.logger.error(f"{error_msg}: {e}")
            return False, error_msg
        except smtplib.SMTPException as e:
            error_msg = f"SMTP error occurred: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
        except TimeoutError as e:
            error_msg = "Connection timeout - SMTP server took too long to respond"
            self.logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
        finally:
            if server:
                try:
                    server.quit()
                except Exception as e:
                    self.logger.warning(f"Error closing SMTP connection: {e}")
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if valid email format, False otherwise
        """
        import re
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_recipients(self, recipients: List[str]) -> Dict[str, bool]:
        """
        Validate multiple email addresses.
        
        Args:
            recipients (List[str]): List of email addresses to validate
            
        Returns:
            Dict[str, bool]: Validation results for each email
        """
        results = {}
        for email in recipients:
            results[email] = self.validate_email(email)
        return results
    
    def get_invalid_emails(self, recipients: List[str]) -> List[str]:
        """
        Get list of invalid email addresses from a list.
        
        Args:
            recipients (List[str]): List of email addresses to check
            
        Returns:
            List[str]: List of invalid email addresses
        """
        return [email for email in recipients if not self.validate_email(email)]
    
    def send_batch_with_validation(self, 
                                  post: Dict[str, str], 
                                  recipients: List[str],
                                  subject_prefix: str = "Generated LinkedIn Post",
                                  skip_invalid: bool = True) -> Dict[str, Any]:
        """
        Send post to multiple recipients with email validation.
        
        Args:
            post (Dict[str, str]): The post data
            recipients (List[str]): List of recipient email addresses
            subject_prefix (str): Subject prefix for emails
            skip_invalid (bool): Whether to skip invalid emails or fail entirely
            
        Returns:
            Dict[str, Any]: Detailed results including validation and sending status
        """
        results = {
            'validation': {},
            'sending': {},
            'summary': {
                'total_recipients': len(recipients),
                'valid_emails': 0,
                'invalid_emails': 0,
                'emails_sent': 0,
                'emails_failed': 0
            }
        }
        
        
        validation_results = self.validate_recipients(recipients)
        results['validation'] = validation_results
        
        valid_emails = [email for email, is_valid in validation_results.items() if is_valid]
        invalid_emails = [email for email, is_valid in validation_results.items() if not is_valid]
        
        results['summary']['valid_emails'] = len(valid_emails)
        results['summary']['invalid_emails'] = len(invalid_emails)
        
        
        if invalid_emails:
            self.logger.warning(f"Found {len(invalid_emails)} invalid emails: {invalid_emails}")
            if not skip_invalid and invalid_emails:
                results['error'] = f"Invalid emails found: {invalid_emails}"
                return results

        
        if valid_emails:
            sending_results = self.send_to_multiple_recipients(
                post=post,
                recipients=valid_emails,
                subject_prefix=subject_prefix
            )
            results['sending'] = sending_results
            
            
            results['summary']['emails_sent'] = sum(1 for success in sending_results.values() if success)
            results['summary']['emails_failed'] = len(sending_results) - results['summary']['emails_sent']
        
        return results

    def test_connection(self) -> bool:
        """
        Test the email connection without sending an email.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.quit()
            
            self.logger.info("Email connection test successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Email connection test failed: {str(e)}")
            return False


if __name__ == "__main__":
    
    try:
        
        email_sender = EmailSender()
        
        
        if email_sender.test_connection():
            print("Email connection successful!")

            sample_post = {
                'title': 'Test Blog Post',
                'content': 'This is a test post content.',
                'hashtags': '#LinkedIn #BlogPost #Test',
                'call_to_action': 'What do you think about this topic?',
                'generated_at': datetime.now().isoformat(),
                'topic': 'Test Topic',
                'tone': 'professional'
            }
            
            
            success = email_sender.send_post(sample_post)
            if success:
                print("Test email sent successfully!")
            else:
                print("Failed to send test email")
        else:
            print("Email connection failed. Please check your credentials.")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set your email credentials in the .env file")