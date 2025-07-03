# Email Forwarding Setup Guide for vancouverpetservices.com

This guide will help you set up professional email forwarding from info@vancouverpetservices.com to snessa7@gmail.com using ImprovMX (free) and Netlify.

## Prerequisites
- Domain vancouverpetservices.com must be connected to Netlify
- Access to Netlify DNS settings
- Gmail account (snessa7@gmail.com)

## Step 1: Configure DNS Records in Netlify

1. Log in to your Netlify account
2. Go to **Domains** section
3. Click on **vancouverpetservices.com**
4. Navigate to **DNS settings**
5. Add the following DNS records:

### MX Records (for receiving emails)
| Type | Name | Priority | Value |
|------|------|----------|--------|
| MX | @ | 10 | mx1.improvmx.com |
| MX | @ | 20 | mx2.improvmx.com |

### TXT Record (for email authentication)
| Type | Name | Value |
|------|------|--------|
| TXT | @ | v=spf1 include:spf.improvmx.com ~all |

**Important:** After adding these records, it may take 1-48 hours for DNS propagation.

## Step 2: Set Up ImprovMX Account

1. Go to [https://improvmx.com](https://improvmx.com)
2. Click **Sign Up** (free plan is sufficient)
3. Create an account using:
   - Email: snessa7@gmail.com
   - Choose a secure password

### Add Your Domain

1. After login, click **Add Domain**
2. Enter: `vancouverpetservices.com`
3. ImprovMX will check your DNS records
4. Once verified (green checkmarks), proceed to next step

### Create Email Alias

1. In your domain dashboard, click **Add Alias**
2. Set up forwarding:
   - **Alias**: `info` (this creates info@vancouverpetservices.com)
   - **Forward to**: `snessa7@gmail.com`
3. Click **Save**

## Step 3: Configure Gmail to Send FROM info@vancouverpetservices.com

### Get SMTP Credentials from ImprovMX

1. In ImprovMX dashboard, go to your domain
2. Click **SMTP** tab
3. Generate SMTP credentials:
   - Username: `info@vancouverpetservices.com`
   - Password: (ImprovMX will generate this - save it!)
   - SMTP Server: `smtp.improvmx.com`
   - Port: `587`
   - Encryption: `STARTTLS`

### Add to Gmail

1. Open Gmail (snessa7@gmail.com)
2. Click ⚙️ Settings → **See all settings**
3. Go to **Accounts and Import** tab
4. In "Send mail as" section, click **Add another email address**
5. Enter:
   - Name: `Vancouver Pet Services`
   - Email: `info@vancouverpetservices.com`
   - Uncheck "Treat as an alias"
6. Click **Next Step**
7. Enter SMTP settings:
   - SMTP Server: `smtp.improvmx.com`
   - Port: `587`
   - Username: `info@vancouverpetservices.com`
   - Password: (from ImprovMX)
   - Select "Secured connection using TLS"
8. Click **Add Account**
9. Gmail will send a verification code to info@vancouverpetservices.com
10. Check your Gmail inbox for the code and enter it

## Step 4: Set as Default (Optional)

1. In Gmail Settings → Accounts and Import
2. Under "Send mail as", click **make default** next to info@vancouverpetservices.com
3. Now all emails will be sent from your professional address by default

## Troubleshooting

### DNS Not Verified
- Wait up to 48 hours for DNS propagation
- Check records are exactly as shown above
- Use [MXToolbox](https://mxtoolbox.com) to verify MX records

### Emails Not Forwarding
- Check spam folder in Gmail
- Verify alias is active in ImprovMX dashboard
- Test with a different sender email

### Can't Send Emails
- Double-check SMTP credentials
- Ensure port 587 is not blocked
- Try regenerating SMTP password in ImprovMX

## Important Notes

- **Free Limit**: ImprovMX free plan allows 25 emails/day
- **Upgrade**: For more emails or features, consider their paid plans
- **Security**: Never share your SMTP password
- **Backup**: Keep a copy of all credentials in a secure password manager

## Support Resources

- ImprovMX Help: [help.improvmx.com](https://help.improvmx.com)
- Netlify Support: [docs.netlify.com](https://docs.netlify.com)
- Gmail Help: [support.google.com/mail](https://support.google.com/mail)