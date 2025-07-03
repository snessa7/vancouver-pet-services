#!/bin/bash

# DNS Monitoring Script for vancouverpetservices.com
# Checks DNS propagation every 30 minutes and logs progress

DOMAIN="vancouverpetservices.com"
CHECK_INTERVAL=1800  # 30 minutes in seconds
MAX_DURATION=172800  # 48 hours in seconds
START_TIME=$(date +%s)
LOG_FILE="dns-propagation.log"

# Function to log with timestamp
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# Function to check DNS status
check_dns_status() {
    log_message "=== DNS Check Starting ==="
    
    # Check MX records
    local mx_records=$(dig MX $DOMAIN +short 2>/dev/null)
    local mx_status="NOT_FOUND"
    
    if [[ ! -z "$mx_records" ]]; then
        log_message "MX Records found: $mx_records"
        if echo "$mx_records" | grep -q "mx1.improvmx.com" && echo "$mx_records" | grep -q "mx2.improvmx.com"; then
            mx_status="CONFIGURED"
            log_message "✓ MX records correctly configured for ImprovMX"
        else
            mx_status="INCORRECT"
            log_message "⚠ MX records found but not pointing to ImprovMX"
        fi
    else
        log_message "✗ No MX records found"
    fi
    
    # Check TXT/SPF records
    local txt_records=$(dig TXT $DOMAIN +short 2>/dev/null)
    local spf_status="NOT_FOUND"
    
    if echo "$txt_records" | grep -q "spf.improvmx.com"; then
        spf_status="CONFIGURED"
        log_message "✓ SPF record correctly configured"
    else
        log_message "✗ SPF record not found"
    fi
    
    # Check A record (to verify domain exists)
    local a_record=$(dig A $DOMAIN +short 2>/dev/null)
    if [[ ! -z "$a_record" ]]; then
        log_message "A record found: $a_record (domain is active)"
    fi
    
    # Summary
    if [[ "$mx_status" == "CONFIGURED" ]] && [[ "$spf_status" == "CONFIGURED" ]]; then
        log_message "✅ DNS FULLY CONFIGURED AND READY!"
        return 0
    else
        log_message "❌ DNS not fully configured yet"
        log_message "   MX Status: $mx_status"
        log_message "   SPF Status: $spf_status"
        return 1
    fi
}

# Function to create status report
create_status_report() {
    local current_time=$(date '+%Y-%m-%d %H:%M:%S')
    local elapsed=$(($(date +%s) - START_TIME))
    local hours=$((elapsed / 3600))
    local minutes=$(((elapsed % 3600) / 60))
    
    cat > dns-status-report.md << EOF
# DNS Propagation Status Report

**Generated**: $current_time  
**Domain**: vancouverpetservices.com  
**Monitoring Duration**: ${hours}h ${minutes}m  

## Current Status

$(tail -n 20 "$LOG_FILE" | grep -E "(✓|✗|✅|❌|MX Status|SPF Status)" | tail -n 10)

## Required DNS Records

### MX Records (Email Receiving)
- \`@ 10 mx1.improvmx.com\`
- \`@ 20 mx2.improvmx.com\`

### TXT Record (Email Authentication)
- \`@ "v=spf1 include:spf.improvmx.com ~all"\`

## Next Check
$(date -d "+30 minutes" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date -v +30M '+%Y-%m-%d %H:%M:%S')

## Action Required
1. Log into Netlify
2. Navigate to Domains → vancouverpetservices.com → DNS settings
3. Add the missing DNS records listed above
4. Save changes and wait for propagation

---
*This report updates every 30 minutes*
EOF
    
    log_message "Status report updated: dns-status-report.md"
}

# Main monitoring loop
log_message "Starting DNS monitoring for $DOMAIN"
log_message "Will check every 30 minutes for up to 48 hours"
log_message "Press Ctrl+C to stop monitoring"

while true; do
    # Check DNS status
    if check_dns_status; then
        log_message "🎉 DNS is ready! Starting email tests..."
        
        # Run the Python test script
        if [[ -f "email-test-script.py" ]]; then
            python3 email-test-script.py --once
        fi
        
        # Create success report
        cat > dns-success-report.md << EOF
# DNS Configuration Success!

**Domain**: vancouverpetservices.com  
**Completed**: $(date '+%Y-%m-%d %H:%M:%S')  
**Status**: ✅ All DNS records properly configured  

## Next Steps

1. **Test Email Forwarding**
   - Send test email to info@vancouverpetservices.com
   - Check snessa7@gmail.com (including spam folder)

2. **Configure Gmail SMTP**
   - Follow the instructions in email-setup-guide.md
   - Set up sending from info@vancouverpetservices.com

3. **Verify Everything Works**
   - Run through email-testing-checklist.md
   - Perform all 6 test scenarios

The email forwarding system is now ready for use!
EOF
        
        log_message "Success report created: dns-success-report.md"
        break
    fi
    
    # Create/update status report
    create_status_report
    
    # Check if we've exceeded max duration
    elapsed=$(($(date +%s) - START_TIME))
    if [[ $elapsed -gt $MAX_DURATION ]]; then
        log_message "Maximum monitoring duration (48 hours) reached"
        log_message "DNS still not fully configured - manual intervention required"
        break
    fi
    
    # Wait for next check
    log_message "Next check in 30 minutes..."
    sleep $CHECK_INTERVAL
done

log_message "Monitoring completed"