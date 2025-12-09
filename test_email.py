#!/usr/bin/env python3
"""
Quick test script to verify email configuration and SMTP connectivity
"""
import sys
import logging
from src.email_sender import EmailSender

# Setup logging to see detailed output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_email_configuration():
    """Test if email sender can be initialized and send a test email"""
    print("\n" + "="*60)
    print("EMAIL CONFIGURATION TEST")
    print("="*60)
    
    try:
        print("\n[1/3] Initializing EmailSender...")
        sender = EmailSender()
        print(f"✓ EmailSender initialized successfully")
        print(f"  - Sender: {sender.sender_email}")
        print(f"  - SMTP Server: {sender.smtp_server}:{sender.smtp_port}")
        
        # Test email content
        test_post = {
            "post_content": "This is a test email from the LinkedIn Post Agent!",
            "hashtags": "#LinkedInAI #Test",
            "topic": "Testing",
            "tone": "professional",
            "title": "Test Post"
        }
        
        print("\n[2/3] Creating test email message...")
        print(f"  - Recipient: {sender.sender_email} (sending to self)")
        print(f"  - Topic: {test_post['topic']}")
        
        print("\n[3/3] Attempting to send test email...")
        success, message = sender.send_post(test_post, sender.sender_email)
        
        if success:
            print("\n" + "="*60)
            print("✓ EMAIL TEST PASSED!")
            print("="*60)
            print(f"\n{message}")
            print("Check your inbox for the test email.\n")
            return True
        else:
            print("\n" + "="*60)
            print("✗ EMAIL TEST FAILED")
            print("="*60)
            print(f"\nError: {message}\n")
            return False
            
    except ValueError as e:
        print(f"\n✗ Configuration Error: {e}")
        print("\nMake sure .env file has:")
        print("  - EMAIL_SENDER=your.email@gmail.com")
        print("  - EMAIL_PASSWORD=your_app_password")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nCommon issues:")
        print("  1. Gmail App Password may be invalid or expired")
        print("  2. 2-Factor Authentication not enabled on Gmail")
        print("  3. Network connectivity issues")
        print("  4. SMTP port 587 blocked by firewall")
        return False

if __name__ == "__main__":
    success = test_email_configuration()
    sys.exit(0 if success else 1)
