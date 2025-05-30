#!/bin/bash
# Vancouver Pet Services - GA4 Auto-Deploy Script
# Run this after updating your GA4 Measurement ID

echo "🚀 Vancouver Pet Services - GA4 Deployment"
echo "============================================"

# Check if we're in the right directory
if [ ! -f "install-ga4.py" ]; then
    echo "❌ Error: install-ga4.py not found"
    echo "   Run this from: /Users/sethpaonessa/Desktop/07_TEMP_WORKSPACE/Live_Websites/Vancouver_Pet_Services"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo "⏰ Starting deployment at $(date)"
echo ""

# Check if Measurement ID was updated
if grep -q "G-TEST123DEMO" install-ga4.py; then
    echo "⚠️  WARNING: Still using test Measurement ID"
    echo "   Please update install-ga4.py with your real GA4 Measurement ID first"
    echo "   Replace 'G-TEST123DEMO' with your actual ID (like G-ABC123DEF4)"
    echo ""
    echo "Quick fix command:"
    echo "sed -i '' 's/G-TEST123DEMO/YOUR_REAL_ID/' install-ga4.py"
    exit 1
fi

echo "✅ Measurement ID looks good"
echo ""

# Install GA4 tracking
echo "📊 Installing GA4 tracking code..."
python3 install-ga4.py
INSTALL_STATUS=$?

if [ $INSTALL_STATUS -eq 0 ]; then
    echo "✅ GA4 installation completed"
else
    echo "❌ GA4 installation failed"
    exit 1
fi

echo ""

# Git operations
echo "📦 Preparing Git deployment..."

# Check git status
if [ -d ".git" ]; then
    echo "✅ Git repository detected"
    
    # Add changes
    git add .
    
    # Commit
    git commit -m "Add Google Analytics 4 tracking to all pages

- Added GA4 tracking code to 9 HTML pages
- Configured phone click tracking
- Added business listing view tracking  
- Implemented search and navigation tracking
- Added GDPR-compliant cookie notice
- Ready for lead generation tracking"
    
    COMMIT_STATUS=$?
    
    if [ $COMMIT_STATUS -eq 0 ]; then
        echo "✅ Changes committed to Git"
        
        # Push to origin
        echo "🚀 Deploying to GitHub..."
        git push origin main
        PUSH_STATUS=$?
        
        if [ $PUSH_STATUS -eq 0 ]; then
            echo "✅ Successfully pushed to GitHub"
            echo "⏰ Netlify auto-deploy will take 2-3 minutes"
        else
            echo "❌ Git push failed"
            exit 1
        fi
    else
        echo "ℹ️  No changes to commit (maybe already committed)"
    fi
else
    echo "⚠️  No Git repository found"
    echo "   Manual deployment required"
fi

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo ""
echo "📋 Next Steps:"
echo "1. Wait 2-3 minutes for Netlify deployment"
echo "2. Visit: https://analytics.google.com"
echo "3. Go to: Reports → Realtime"
echo "4. Visit: https://vancouverpetservices.com" 
echo "5. You should see 1 active user (yourself) in GA4"
echo ""
echo "🔍 To verify installation:"
echo "python3 verify-ga4.py"
echo ""
echo "📊 Your analytics will track:"
echo "   • All page views and user sessions"
echo "   • Phone number clicks (lead generation)"
echo "   • Business listing views (enhanced ecommerce)"
echo "   • Search usage and category navigation"
echo "   • Scroll depth and engagement metrics"
echo ""
echo "🎯 Visit your live site now and check GA4 Realtime!"
