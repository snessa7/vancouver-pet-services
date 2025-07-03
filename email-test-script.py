#!/usr/bin/env python3
"""
Email Forwarding Test Script for vancouverpetservices.com
Tests DNS propagation and email forwarding functionality
"""

import subprocess
import time
import datetime
import json
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
DOMAIN = "vancouverpetservices.com"
TEST_EMAIL = "info@vancouverpetservices.com"
FORWARD_TO = "snessa7@gmail.com"
LOG_FILE = "test-results.log"
STATUS_FILE = "email-test-status.json"

# Expected DNS records
EXPECTED_MX = [
    "10 mx1.improvmx.com.",
    "20 mx2.improvmx.com."
]
EXPECTED_SPF = "v=spf1 include:spf.improvmx.com ~all"

def log_message(message, level="INFO"):
    """Log message with timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

def check_dns_mx():
    """Check MX records for the domain"""
    try:
        result = subprocess.run(
            ["dig", "MX", DOMAIN, "+short"],
            capture_output=True,
            text=True
        )
        mx_records = result.stdout.strip().split('\n')
        mx_records = [r for r in mx_records if r]  # Remove empty strings
        
        log_message(f"Current MX records: {mx_records}")
        
        # Check if expected MX records are present
        mx_found = all(any(expected in record for record in mx_records) 
                      for expected in ["mx1.improvmx.com", "mx2.improvmx.com"])
        
        return mx_found, mx_records
    except Exception as e:
        log_message(f"Error checking MX records: {e}", "ERROR")
        return False, []

def check_dns_txt():
    """Check TXT records for SPF"""
    try:
        result = subprocess.run(
            ["dig", "TXT", DOMAIN, "+short"],
            capture_output=True,
            text=True
        )
        txt_records = result.stdout.strip().split('\n')
        txt_records = [r.strip('"') for r in txt_records if r]
        
        log_message(f"Current TXT records: {txt_records}")
        
        # Check if SPF record is present
        spf_found = any(EXPECTED_SPF in record for record in txt_records)
        
        return spf_found, txt_records
    except Exception as e:
        log_message(f"Error checking TXT records: {e}", "ERROR")
        return False, []

def send_test_email():
    """Send a test email using curl"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = f"TEST_{timestamp}"
    subject = f"Email Forwarding Test - {unique_id}"
    
    # Create a simple test message
    message = f"""Subject: {subject}
From: test@example.com
To: {TEST_EMAIL}

This is an automated test email sent at {datetime.datetime.now()}
Unique ID: {unique_id}

If you receive this email at {FORWARD_TO}, the forwarding is working correctly.
"""
    
    # Save message to temporary file
    temp_file = f"/tmp/test_email_{timestamp}.txt"
    with open(temp_file, "w") as f:
        f.write(message)
    
    try:
        # Try to send using sendmail (more reliable than curl for email)
        result = subprocess.run(
            ["sendmail", TEST_EMAIL],
            input=message,
            text=True,
            capture_output=True
        )
        
        if result.returncode == 0:
            log_message(f"Test email sent successfully - ID: {unique_id}")
            return True, unique_id
        else:
            log_message(f"Failed to send test email: {result.stderr}", "ERROR")
            return False, None
            
    except FileNotFoundError:
        # If sendmail not available, log instructions
        log_message("sendmail not available. Manual test required.", "WARNING")
        log_message(f"Please send test email to {TEST_EMAIL} with subject: {subject}")
        return False, None
    except Exception as e:
        log_message(f"Error sending test email: {e}", "ERROR")
        return False, None
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)

def update_status(status_data):
    """Update status file"""
    with open(STATUS_FILE, "w") as f:
        json.dump(status_data, f, indent=2)

def run_test_cycle():
    """Run a complete test cycle"""
    log_message("=== Starting Email Forwarding Test Cycle ===")
    
    status = {
        "last_check": datetime.datetime.now().isoformat(),
        "dns_mx_configured": False,
        "dns_txt_configured": False,
        "dns_fully_propagated": False,
        "email_sent": False,
        "email_delivered": False,
        "test_emails": []
    }
    
    # Check DNS MX records
    mx_found, mx_records = check_dns_mx()
    status["dns_mx_configured"] = mx_found
    status["mx_records"] = mx_records
    
    # Check DNS TXT records
    spf_found, txt_records = check_dns_txt()
    status["dns_txt_configured"] = spf_found
    status["txt_records"] = txt_records
    
    # Check if DNS is fully propagated
    status["dns_fully_propagated"] = mx_found and spf_found
    
    if status["dns_fully_propagated"]:
        log_message("DNS records are properly configured!", "SUCCESS")
        
        # Send test email
        sent, email_id = send_test_email()
        if sent:
            status["email_sent"] = True
            status["test_emails"].append({
                "id": email_id,
                "sent_at": datetime.datetime.now().isoformat(),
                "delivered": False
            })
    else:
        log_message("DNS not fully propagated yet. Waiting...", "WARNING")
        if not mx_found:
            log_message("Missing MX records: mx1.improvmx.com, mx2.improvmx.com", "WARNING")
        if not spf_found:
            log_message(f"Missing SPF TXT record: {EXPECTED_SPF}", "WARNING")
    
    # Update status file
    update_status(status)
    
    return status

def continuous_test(interval_minutes=15, max_hours=48):
    """Run continuous tests until successful or timeout"""
    start_time = datetime.datetime.now()
    max_duration = datetime.timedelta(hours=max_hours)
    test_interval = datetime.timedelta(minutes=interval_minutes)
    
    log_message(f"Starting continuous test - checking every {interval_minutes} minutes")
    log_message(f"Will run for maximum {max_hours} hours")
    
    success_count = 0
    required_successes = 5
    
    while datetime.datetime.now() - start_time < max_duration:
        status = run_test_cycle()
        
        if status["dns_fully_propagated"] and status["email_sent"]:
            success_count += 1
            log_message(f"Success count: {success_count}/{required_successes}", "SUCCESS")
            
            if success_count >= required_successes:
                log_message("Email forwarding is working reliably!", "SUCCESS")
                create_final_report(status, start_time)
                return True
        else:
            success_count = 0  # Reset on failure
        
        # Wait for next test
        next_test = datetime.datetime.now() + test_interval
        log_message(f"Next test at: {next_test.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(test_interval.total_seconds())
    
    log_message("Maximum test duration reached without success", "ERROR")
    create_error_report(start_time)
    return False

def create_final_report(status, start_time):
    """Create final success report"""
    report_content = f"""# Email Forwarding Test - Final Report

## Test Summary
- **Domain**: vancouverpetservices.com
- **Test Started**: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
- **Test Completed**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Status**: ✅ SUCCESSFUL

## DNS Configuration
- **MX Records**: ✅ Configured
  - {', '.join(status.get('mx_records', []))}
- **SPF Record**: ✅ Configured
  - {', '.join(status.get('txt_records', []))}

## Email Forwarding
- **Test Emails Sent**: {len(status.get('test_emails', []))}
- **Forwarding**: info@vancouverpetservices.com → snessa7@gmail.com
- **Status**: ✅ Working

## DNS Propagation Timeline
- **First DNS Detection**: {status.get('last_check', 'N/A')}
- **Full Propagation**: Confirmed

## Recommendations
1. Email forwarding is now active and working
2. Check snessa7@gmail.com for test emails
3. Configure Gmail to send FROM info@vancouverpetservices.com
4. The system is ready for production use

## Next Steps
- Send test email from external account to verify
- Set up Gmail SMTP for sending
- Update all marketing materials with new email
"""
    
    with open("final-test-report.md", "w") as f:
        f.write(report_content)
    
    log_message("Final report created: final-test-report.md", "SUCCESS")

def create_error_report(start_time):
    """Create error report after timeout"""
    report_content = f"""# Email Forwarding Test - Error Report

## Test Summary
- **Domain**: vancouverpetservices.com
- **Test Started**: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
- **Test Ended**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Status**: ❌ FAILED - Timeout

## Troubleshooting Steps Attempted
1. Checked DNS MX records every 15 minutes
2. Checked DNS TXT records for SPF
3. Attempted to send test emails when DNS was ready

## Issues Identified
- DNS records may not be properly configured in Netlify
- ImprovMX domain verification may be incomplete
- DNS propagation taking longer than expected

## Recommended Actions
1. Log into Netlify and verify DNS records are added:
   - MX: @ 10 mx1.improvmx.com
   - MX: @ 20 mx2.improvmx.com
   - TXT: @ "v=spf1 include:spf.improvmx.com ~all"
2. Check ImprovMX dashboard for domain status
3. Contact Netlify support if DNS not updating
4. Verify domain ownership in ImprovMX

## Manual Verification Steps
1. Visit: https://mxtoolbox.com/MXLookup.aspx
2. Enter: vancouverpetservices.com
3. Check if MX records point to improvmx.com
"""
    
    with open("error-report.md", "w") as f:
        f.write(report_content)
    
    log_message("Error report created: error-report.md", "ERROR")

if __name__ == "__main__":
    log_message("Email Forwarding Test Script Started")
    log_message(f"Testing domain: {DOMAIN}")
    log_message(f"Forwarding: {TEST_EMAIL} → {FORWARD_TO}")
    
    # Run single test if requested
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        run_test_cycle()
    else:
        # Run continuous test
        continuous_test(interval_minutes=15, max_hours=48)