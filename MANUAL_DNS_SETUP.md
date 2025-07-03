# Manual DNS Setup for Vancouver Pet Services

Since the Netlify API is having issues, here's how to add the DNS records manually:

## Steps to Add DNS Records in Netlify Dashboard

1. **Go to Netlify Dashboard**
   - Visit: https://app.netlify.com
   - Login with your account (snessa7@gmail.com)

2. **Navigate to DNS Settings**
   - Click on "Domains" in the main navigation
   - Find "vancouverpetservices.com" and click on it
   - You'll see the DNS management page

3. **Add MX Records**
   
   Click "Add new record" and add:
   
   **First MX Record:**
   - Record type: `MX`
   - Name: Leave empty (this represents the root domain)
   - Priority: `10`
   - Value: `mx1.improvmx.com`
   - TTL: `3600` (or Auto)
   
   **Second MX Record:**
   - Record type: `MX`
   - Name: Leave empty
   - Priority: `20`
   - Value: `mx2.improvmx.com`
   - TTL: `3600` (or Auto)

4. **Add SPF TXT Record**
   
   Click "Add new record" and add:
   
   - Record type: `TXT`
   - Name: Leave empty
   - Value: `v=spf1 include:spf.improvmx.com ~all`
   - TTL: `3600` (or Auto)

## Direct Link to Your DNS Zone

Try this direct link:
https://app.netlify.com/teams/snessa7/dns/vancouverpetservices.com

## After Adding Records

1. Records should be visible immediately in the dashboard
2. DNS propagation takes 5 minutes to 48 hours
3. Test with: `bash /Users/sethpaonessa/Desktop/Live_Websites/Vancouver_Pet_Services/quick-email-test.sh`

## Alternative: Command Line with cURL

If you want to try the API directly with your Netlify token:

```bash
# First, get your Netlify access token from:
# https://app.netlify.com/user/applications#personal-access-tokens

# Then use these commands (replace YOUR_TOKEN):
NETLIFY_TOKEN="YOUR_TOKEN"
ZONE_ID="6838dcad734a1cec1e9c4ac7"

# Add MX record 1
curl -X POST "https://api.netlify.com/api/v1/dns_zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $NETLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "MX",
    "hostname": "vancouverpetservices.com",
    "value": "mx1.improvmx.com",
    "priority": 10,
    "ttl": 3600
  }'

# Add MX record 2
curl -X POST "https://api.netlify.com/api/v1/dns_zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $NETLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "MX",
    "hostname": "vancouverpetservices.com",
    "value": "mx2.improvmx.com",
    "priority": 20,
    "ttl": 3600
  }'

# Add SPF record
curl -X POST "https://api.netlify.com/api/v1/dns_zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $NETLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "TXT",
    "hostname": "vancouverpetservices.com",
    "value": "v=spf1 include:spf.improvmx.com ~all",
    "ttl": 3600
  }'
```