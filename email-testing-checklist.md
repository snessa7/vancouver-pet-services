# Email Forwarding Test Checklist

Use this checklist to verify your email forwarding is working correctly before the Tuesday launch.

## Pre-Test Requirements
- [ ] Domain vancouverpetservices.com is connected to Netlify
- [ ] DNS records have been added in Netlify (allow 1-48 hours for propagation)
- [ ] ImprovMX account is set up with domain verified
- [ ] Gmail is configured to send from info@vancouverpetservices.com

## DNS Propagation Check
1. [ ] Visit [MXToolbox](https://mxtoolbox.com/MXLookup.aspx)
2. [ ] Enter: `vancouverpetservices.com`
3. [ ] Verify you see:
   - mx1.improvmx.com (Priority 10)
   - mx2.improvmx.com (Priority 20)

## Test 1: Basic Email Forwarding
1. [ ] Send a test email from a personal email (not snessa7@gmail.com) to `info@vancouverpetservices.com`
2. [ ] Subject: "Test 1 - Basic Forwarding"
3. [ ] Wait 2-5 minutes
4. [ ] Check inbox at snessa7@gmail.com
5. [ ] Verify email arrived with original sender's address

## Test 2: Spam Folder Check
1. [ ] If Test 1 email didn't arrive in inbox, check spam folder
2. [ ] If found in spam, mark as "Not Spam"
3. [ ] Add sender to contacts

## Test 3: Sending FROM Professional Email
1. [ ] Open Gmail (snessa7@gmail.com)
2. [ ] Compose new email
3. [ ] Click "From" dropdown and select `info@vancouverpetservices.com`
4. [ ] Send to a different email you control
5. [ ] Verify it arrives showing sender as info@vancouverpetservices.com

## Test 4: Reply Test
1. [ ] Reply to the test email from Test 1
2. [ ] Make sure "From" is set to info@vancouverpetservices.com
3. [ ] Verify the reply is delivered successfully

## Test 5: Contact Form Integration
1. [ ] Submit a test entry through your website's contact form
2. [ ] Verify form submission arrives at snessa7@gmail.com
3. [ ] Check that reply-to address works correctly

## Test 6: Multiple Recipients
1. [ ] Have 2-3 friends/family send test emails to info@vancouverpetservices.com
2. [ ] Verify all emails arrive
3. [ ] Test replying to each with professional email

## Final Verification Checklist
- [ ] ✅ Receiving emails at info@ forwards to Gmail
- [ ] ✅ Can send emails FROM info@ via Gmail
- [ ] ✅ Replies show professional email address
- [ ] ✅ No emails landing in spam (after marking not spam)
- [ ] ✅ Contact forms working correctly

## Troubleshooting Quick Reference

### Emails Not Arriving?
1. Check spam folder first
2. Verify DNS records in Netlify
3. Check ImprovMX dashboard for domain status
4. Wait full 48 hours for DNS propagation

### Can't Send From Professional Email?
1. Re-verify SMTP settings in Gmail
2. Check verification email wasn't missed
3. Try regenerating SMTP password in ImprovMX

### Getting Bounce Backs?
1. Check recipient email is correct
2. Verify SPF record is properly set
3. Ensure not exceeding 25 emails/day limit

## Launch Day Checklist
- [ ] Send welcome email to your mailing list from info@
- [ ] Update email signature with professional address
- [ ] Test all website forms one final time
- [ ] Monitor inbox throughout the day
- [ ] Respond promptly to any inquiries

## Success Metrics
By end of launch day, you should have:
- Successfully received 5+ test emails
- Sent 5+ emails from professional address
- Zero delivery issues
- Professional email on all communications

---

**Remember**: Your free ImprovMX plan includes 25 emails per day. This is usually sufficient for small businesses, but monitor usage and upgrade if needed.

**Support**: If issues persist, contact ImprovMX support with your domain name and specific error messages.