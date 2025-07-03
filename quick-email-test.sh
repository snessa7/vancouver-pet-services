#!/bin/bash

# Quick Email Test Script for vancouverpetservices.com
# Run this to quickly check DNS and attempt email sending

DOMAIN="vancouverpetservices.com"
TEST_EMAIL="info@vancouverpetservices.com"
LOG_FILE="test-results.log"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to log with timestamp
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

echo "========================================="
echo "Email Forwarding Test for $DOMAIN"
echo "========================================="
echo ""

# Check DNS MX Records
log_message "Checking MX records..."
MX_RECORDS=$(dig MX $DOMAIN +short)

if [[ -z "$MX_RECORDS" ]]; then
    echo -e "${RED}❌ No MX records found${NC}"
    log_message "ERROR: No MX records found for $DOMAIN"
else
    echo -e "${GREEN}✓ MX Records found:${NC}"
    echo "$MX_RECORDS"
    log_message "MX Records: $MX_RECORDS"
    
    # Check if ImprovMX records are present
    if echo "$MX_RECORDS" | grep -q "improvmx.com"; then
        echo -e "${GREEN}✓ ImprovMX MX records detected${NC}"
        MX_OK=true
    else
        echo -e "${YELLOW}⚠ MX records don't point to ImprovMX${NC}"
        MX_OK=false
    fi
fi

echo ""

# Check DNS TXT Records (SPF)
log_message "Checking TXT records for SPF..."
TXT_RECORDS=$(dig TXT $DOMAIN +short)

if echo "$TXT_RECORDS" | grep -q "spf.improvmx.com"; then
    echo -e "${GREEN}✓ SPF record found${NC}"
    echo "$TXT_RECORDS"
    SPF_OK=true
else
    echo -e "${RED}❌ SPF record not found${NC}"
    log_message "ERROR: SPF record not found"
    SPF_OK=false
fi

echo ""

# Check if we can proceed with email test
if [[ "$MX_OK" == true ]] && [[ "$SPF_OK" == true ]]; then
    echo -e "${GREEN}✓ DNS is properly configured!${NC}"
    log_message "SUCCESS: DNS is properly configured"
    
    # Create test email
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    SUBJECT="Test_${TIMESTAMP}"
    
    echo ""
    echo "Attempting to send test email..."
    echo "Subject: $SUBJECT"
    echo "To: $TEST_EMAIL"
    
    # Try using mail command if available
    if command -v mail &> /dev/null; then
        echo "Test email from vancouverpetservices.com - $TIMESTAMP" | mail -s "$SUBJECT" "$TEST_EMAIL"
        if [[ $? -eq 0 ]]; then
            echo -e "${GREEN}✓ Test email sent successfully${NC}"
            log_message "SUCCESS: Test email sent with subject: $SUBJECT"
        else
            echo -e "${RED}❌ Failed to send test email${NC}"
            log_message "ERROR: Failed to send test email"
        fi
    else
        echo -e "${YELLOW}⚠ 'mail' command not available${NC}"
        echo "Please send a manual test email to: $TEST_EMAIL"
        log_message "WARNING: mail command not available for automated testing"
    fi
else
    echo -e "${RED}❌ DNS not fully configured yet${NC}"
    echo ""
    echo "Required DNS records:"
    echo "1. MX Records:"
    echo "   - @ 10 mx1.improvmx.com"
    echo "   - @ 20 mx2.improvmx.com"
    echo "2. TXT Record:"
    echo "   - @ \"v=spf1 include:spf.improvmx.com ~all\""
    echo ""
    echo "Please add these records in Netlify DNS settings"
    log_message "ERROR: DNS not fully configured"
fi

echo ""
echo "========================================="
echo "Full log saved to: $LOG_FILE"
echo "========================================="

# Create a summary status file
cat > email-test-summary.txt << EOF
Email Test Summary - $(date)
================================
Domain: $DOMAIN
MX Records OK: ${MX_OK:-false}
SPF Record OK: ${SPF_OK:-false}
DNS Ready: $([[ "$MX_OK" == true ]] && [[ "$SPF_OK" == true ]] && echo "YES" || echo "NO")

Next Steps:
$(if [[ "$MX_OK" != true ]] || [[ "$SPF_OK" != true ]]; then
    echo "1. Add missing DNS records in Netlify"
    echo "2. Wait for DNS propagation (1-48 hours)"
    echo "3. Run this test again"
else
    echo "1. Check snessa7@gmail.com for test email"
    echo "2. If not received, check spam folder"
    echo "3. Configure Gmail SMTP for sending"
fi)
EOF

echo ""
echo "Summary saved to: email-test-summary.txt"