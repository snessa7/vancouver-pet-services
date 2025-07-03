# Fix Email Forwarding - Netlify DNS Setup

## Problem
Your email forwarding for info@vancouverpetservices.com isn't working because the required DNS records aren't configured in Netlify.

## Solution - Add These DNS Records in Netlify

### Step-by-Step Instructions

1. **Login to Netlify**
   - Go to https://app.netlify.com
   - Navigate to your Vancouver Pet Services site

2. **Access DNS Settings**
   - Click on "Domain settings"
   - Click on "DNS panel" or "Go to DNS panel"
   - You should see vancouverpetservices.com listed

3. **Add MX Records for Email Forwarding**
   
   Click "Add record" and create TWO MX records:
   
   **MX Record 1:**
   - Type: `MX`
   - Name: `@` (or leave blank - represents the root domain)
   - Priority: `10`
   - Value: `mx1.improvmx.com`
   - TTL: `3600` (or leave default)
   
   **MX Record 2:**
   - Type: `MX`
   - Name: `@` (or leave blank)
   - Priority: `20`
   - Value: `mx2.improvmx.com`
   - TTL: `3600` (or leave default)

4. **Add SPF Record for Email Authentication**
   
   Click "Add record" and create:
   
   - Type: `TXT`
   - Name: `@` (or leave blank)
   - Value: `v=spf1 include:spf.improvmx.com ~all`
   - TTL: `3600` (or leave default)

## After Adding Records

1. **Wait for DNS Propagation**
   - Changes can take 5 minutes to 48 hours to fully propagate
   - Usually works within 1-2 hours

2. **Test the Setup**
   Run this command in the terminal:
   ```bash
   cd /Users/sethpaonessa/Desktop/Live_Websites/Vancouver_Pet_Services
   bash quick-email-test.sh
   ```

3. **Expected Result**
   You should see:
   - ✅ MX records found
   - ✅ SPF record found
   - ✅ DNS fully configured

## Troubleshooting

- If records don't appear after 2 hours, double-check they were saved in Netlify
- Make sure there are no typos in the record values
- The @ symbol in the Name field represents the root domain (vancouverpetservices.com)

## What This Does

- **MX Records**: Tell email servers where to deliver mail for @vancouverpetservices.com
- **SPF Record**: Authorizes ImprovMX to send emails on behalf of your domain
- **ImprovMX**: Free service that forwards info@vancouverpetservices.com → snessa7@gmail.com

## Need Help?

If you're still having issues after 24 hours:
1. Check ImprovMX dashboard: https://improvmx.com
2. Verify the forwarding rule is active
3. Check spam folder in snessa7@gmail.com