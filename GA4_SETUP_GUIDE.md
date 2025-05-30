# Google Analytics 4 Setup Guide for Vancouver Pet Services

## 📊 Installation Instructions

### Step 1: Get Your GA4 Measurement ID

1. Go to [Google Analytics](https://analytics.google.com)
2. Create a new property for "Vancouver Pet Services Directory"
3. Set up a Web data stream for `vancouverpetservices.com`
4. Copy your Measurement ID (looks like `G-XXXXXXXXXX`)

### Step 2: Install GA4 Tracking Code

1. **Edit the installation script:**
   ```bash
   # Open install-ga4.py and replace G-XXXXXXXXXX with your actual ID
   nano install-ga4.py
   ```

2. **Run the installation script:**
   ```bash
   python3 install-ga4.py
   ```

3. **The script will:**
   - Add GA4 tracking to all 9 HTML files
   - Create backups of each file
   - Add event tracking for conversions
   - Include GDPR privacy notice

### Step 3: Deploy Changes

```bash
# Check what changed
git status

# Add all changes
git add .

# Commit with descriptive message
git commit -m "Add Google Analytics 4 tracking with enhanced ecommerce"

# Push to GitHub (triggers Netlify deploy)
git push origin main
```

## 🎯 Events Being Tracked

### 1. **Lead Generation Events**
- `get_listed_click` - When someone clicks "Get Listed" buttons
- `phone_click` - When someone clicks a phone number
- Form submissions (when contact form is added)

### 2. **Engagement Events**
- `search` - When users search for businesses
- `category_click` - When users navigate categories
- `scroll` - Tracks 25%, 50%, 75%, 90% scroll depth
- `view_item` - Business listing views (Enhanced Ecommerce)

### 3. **Navigation Events**
- Page views (automatic)
- Session duration (automatic)
- Bounce rate (automatic)

## ✅ Testing Checklist

### Immediate Tests (After Deployment)

1. **Verify Installation:**
   - [ ] Visit vancouverpetservices.com
   - [ ] Right-click → View Page Source
   - [ ] Search for "googletagmanager.com"
   - [ ] Confirm GA4 code is present

2. **Real-Time Testing:**
   - [ ] Open [GA4 Real-time Reports](https://analytics.google.com/analytics/web/)
   - [ ] Visit your website in another tab
   - [ ] Confirm you appear as active user
   - [ ] Navigate between pages
   - [ ] See page views updating

3. **Event Testing:**
   - [ ] Click a phone number → Check for `phone_click` event
   - [ ] Click "Get Listed" → Check for `get_listed_click` event
   - [ ] Use search bar → Check for `search` event
   - [ ] Click category → Check for `category_click` event
   - [ ] Scroll to bottom → Check for `scroll` events

4. **Mobile Testing:**
   - [ ] Test on mobile device
   - [ ] Verify all events fire correctly
   - [ ] Check page load speed

## 📈 Setting Up Reports & Goals

### 1. **Conversions Setup**
In GA4, go to Admin → Events → Mark as conversion:
- `get_listed_click` ✓
- `phone_click` ✓
- Future: `form_submit` ✓

### 2. **Custom Audiences**
Create audiences for:
- Vancouver, WA visitors
- Mobile vs Desktop users
- Engaged users (>2 min session)
- High-intent users (viewed 3+ categories)

### 3. **Reports to Monitor**

**Daily:**
- Real-time users
- Today's conversions
- Traffic sources

**Weekly:**
- User acquisition trends
- Top performing pages
- Geographic distribution
- Device breakdown

**Monthly:**
- Conversion rate trends
- User behavior flow
- Search terms used
- Revenue projections

## 🔗 Google Search Console Integration

1. Go to GA4 Admin → Product Links
2. Click "Link to Search Console"
3. Choose your Search Console property
4. Enable data sharing

This provides:
- Search queries bringing traffic
- Click-through rates
- Average position in search
- Pages getting most search traffic

## 🛡️ Privacy & Compliance

The installation includes:
- Cookie consent banner
- Link to privacy policy
- GDPR compliance
- User choice respected

To customize the privacy notice, edit the style and text in the GA4 tracking code.

## 🚨 Troubleshooting

**GA4 not showing data:**
- Wait 24-48 hours for initial data
- Check if ad blockers are interfering
- Verify Measurement ID is correct
- Check browser console for errors

**Events not firing:**
- Ensure JavaScript is enabled
- Check for conflicts with other scripts
- Verify selectors match your HTML
- Test in incognito mode

**Deployment issues:**
- Ensure Git is properly configured
- Check Netlify build logs
- Verify auto-deploy is enabled

## 📊 Expected Results

**Week 1:**
- 100-200 sessions
- 20-30% from Vancouver, WA
- 5-10 phone clicks
- 2-5 "Get Listed" clicks

**Month 1:**
- 500-1000 sessions
- Growing organic traffic
- 50+ conversions
- Clear user behavior patterns

## 🎯 Next Steps

1. **Set up Google Ads** (optional)
   - Link GA4 to Google Ads
   - Create remarketing audiences
   - Track ad conversions

2. **Enhanced Tracking**
   - Add form submission tracking
   - Track email clicks
   - Monitor 404 errors
   - Set up custom alerts

3. **Optimize Based on Data**
   - Improve low-performing pages
   - A/B test CTA buttons
   - Optimize for mobile
   - Focus on high-converting categories

---

**Need help?** 
- GA4 Documentation: https://support.google.com/analytics
- Netlify Support: https://docs.netlify.com
- Check browser console for errors

Remember: Good data leads to good decisions. Monitor regularly and optimize based on what you learn!