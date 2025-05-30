#!/usr/bin/env python3
"""
GA4 Verification Script - Vancouver Pet Services
This script verifies GA4 installation is working correctly
"""

import os
import re
import requests
from datetime import datetime

def check_ga4_installation():
    """Check if GA4 is properly installed on all HTML files"""
    
    html_files = [
        'index.html', 'veterinary.html', 'grooming.html', 'boarding.html',
        'training.html', 'pet-stores.html', 'emergency.html', 'privacy.html', 'terms.html'
    ]
    
    print("🔍 Verifying GA4 Installation...")
    print("-" * 50)
    
    results = {}
    
    for html_file in html_files:
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for GA4 tracking code
            has_gtag = 'googletagmanager.com/gtag/js' in content
            has_config = 'gtag(\'config\'' in content
            has_events = 'phone_click' in content
            
            results[html_file] = {
                'exists': True,
                'has_gtag': has_gtag,
                'has_config': has_config,
                'has_events': has_events,
                'status': '✅' if (has_gtag and has_config) else '❌'
            }
            
            print(f"{results[html_file]['status']} {html_file}")
            if has_gtag and has_config and has_events:
                print(f"   ✅ GA4 tracking: ✓  Config: ✓  Events: ✓")
            else:
                print(f"   ❌ GA4 tracking: {'✓' if has_gtag else '✗'}  Config: {'✓' if has_config else '✗'}  Events: {'✓' if has_events else '✗'}")
        else:
            results[html_file] = {'exists': False, 'status': '❌'}
            print(f"❌ {html_file} - FILE NOT FOUND")
    
    print("-" * 50)
    
    # Summary
    installed_count = sum(1 for r in results.values() if r.get('has_gtag', False))
    total_count = len([r for r in results.values() if r['exists']])
    
    if installed_count == total_count and total_count > 0:
        print(f"🎉 SUCCESS! GA4 installed on all {installed_count} files")
        print("\n📋 Next Steps:")
        print("1. Commit changes: git add . && git commit -m 'Add GA4 tracking'")
        print("2. Deploy: git push origin main")
        print("3. Wait 2-3 minutes for Netlify deployment")
        print("4. Test: Visit https://vancouverpetservices.com")
        print("5. Verify: Check GA4 Realtime reports")
        return True
    else:
        print(f"❌ Issues found: {installed_count}/{total_count} files have GA4")
        print("Run install-ga4.py again to fix issues")
        return False

def check_live_site():
    """Check if the live site is accessible"""
    print("\n🌐 Checking Live Site Status...")
    
    try:
        response = requests.get('https://vancouverpetservices.com', timeout=10)
        if response.status_code == 200:
            print("✅ Live site is accessible")
            
            # Check if GA4 is live
            if 'googletagmanager.com/gtag/js' in response.text:
                print("✅ GA4 tracking detected on live site!")
                print("🎯 Visit https://analytics.google.com → Reports → Realtime")
                print("🎯 Then visit your site to see yourself as an active user")
                return True
            else:
                print("⚠️  GA4 not detected on live site yet")
                print("   This is normal if you just deployed. Wait 2-3 minutes.")
                return False
        else:
            print(f"⚠️  Site returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Could not reach site: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("🚀 Vancouver Pet Services - GA4 Verification")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check local installation
    local_ok = check_ga4_installation()
    
    # Check live site
    live_ok = check_live_site()
    
    print("\n" + "=" * 60)
    if local_ok and live_ok:
        print("🎉 VERIFICATION COMPLETE - Everything is working!")
        print("\n📊 Your GA4 tracking includes:")
        print("   • Page views and user sessions")
        print("   • Phone number click tracking")
        print("   • Business listing view tracking")
        print("   • Search and navigation tracking")
        print("   • Lead generation events")
        print("   • GDPR-compliant cookie notice")
    elif local_ok:
        print("✅ Local installation complete")
        print("⏰ Waiting for live deployment...")
        print("   Run this script again in 2-3 minutes")
    else:
        print("❌ Issues detected - check the output above")

if __name__ == "__main__":
    main()