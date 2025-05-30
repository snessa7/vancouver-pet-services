#!/bin/bash
# 🚀 Auto-Deploy Script for vancouver-pet-services
set -e
cd "/Users/sethpaonessa/Desktop/🌐 Live_Websites/Vancouver_Pet_Services"

if [[ -n $(git status --porcelain) ]]; then
    echo "📝 Changes detected, deploying..."
    git add .
    git commit -m "🚀 Auto-deploy: $(date)"
    git push origin main
    echo "✅ Deployed! Site will update in ~2 minutes"
else
    echo "ℹ️ No changes detected"
fi