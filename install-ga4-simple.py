#!/usr/bin/env python3
"""
Simple GA4 Installation Script for Vancouver Pet Services
"""

import os
import re
from datetime import datetime

# Your actual GA4 Measurement ID
GA4_MEASUREMENT_ID = "G-4RSJ394H7V"

def get_simple_ga4_code(measurement_id):
    """Generate simple but complete GA4 tracking code"""
    return f'''<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{measurement_id}');

  // Track phone clicks for lead generation
  document.addEventListener('DOMContentLoaded', function() {{
    const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
    phoneLinks.forEach(link => {{
      link.addEventListener('click', function() {{
        gtag('event', 'phone_click', {{
          'event_category': 'engagement',
          'event_label': this.href.replace('tel:', ''),
          'value': 1
        }});
      }});
    }});

    // Track Get Listed button clicks
    const ctaButtons = document.querySelectorAll('.cta-button, .hero-cta');
    ctaButtons.forEach(button => {{
      button.addEventListener('click', function() {{
        gtag('event', 'get_listed_click', {{
          'event_category': 'lead_generation',
          'event_label': window.location.pathname,
          'value': 1
        }});
      }});
    }});
  }});
</script>'''

def add_ga4_to_file(file_path, ga4_code):
    """Add GA4 code to HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already installed
        if 'googletagmanager.com/gtag/js' in content:
            print(f"⚠️  GA4 already installed in {os.path.basename(file_path)}")
            return False
        
        # Find </head> and insert GA4 code before it
        if '</head>' in content:
            new_content = content.replace('</head>', f'{ga4_code}\\n</head>')
            
            # Create backup
            backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ GA4 added to {os.path.basename(file_path)}")
            return True
        else:
            print(f"❌ No </head> tag found in {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {os.path.basename(file_path)}: {str(e)}")
        return False

def main():
    """Install GA4 on all HTML files"""
    html_files = [
        'index.html', 'veterinary.html', 'grooming.html', 'boarding.html',
        'training.html', 'pet-stores.html', 'emergency.html', 'privacy.html', 'terms.html'
    ]
    
    print(f"🚀 Installing Google Analytics 4 (ID: {GA4_MEASUREMENT_ID})")
    print("-" * 50)
    
    ga4_code = get_simple_ga4_code(GA4_MEASUREMENT_ID)
    success_count = 0
    
    for html_file in html_files:
        if os.path.exists(html_file):
            if add_ga4_to_file(html_file, ga4_code):
                success_count += 1
        else:
            print(f"⚠️  File not found: {html_file}")
    
    print("-" * 50)
    print(f"✅ Installation complete! {success_count}/{len(html_files)} files updated")
    
    if success_count > 0:
        print("\\n🎉 GA4 tracking is now installed!")
        print("\\n📋 Next steps:")
        print("1. git add .")
        print("2. git commit -m 'Add GA4 tracking'")
        print("3. git push origin main")
        print("4. Wait 2-3 minutes for Netlify deploy")
        print("5. Visit your site and check GA4 Realtime reports")

if __name__ == "__main__":
    main()