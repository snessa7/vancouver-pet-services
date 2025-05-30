#!/usr/bin/env python3
"""
Google Analytics 4 Installation Script for Vancouver Pet Services
This script adds GA4 tracking code to all HTML files
"""

import os
import re
from datetime import datetime

# IMPORTANT: Replace this with your actual GA4 Measurement ID
GA4_MEASUREMENT_ID = "G-4RSJ394H7V"  # <-- YOUR ACTUAL GA4 MEASUREMENT ID

def get_ga4_code(measurement_id):
    """Generate the complete GA4 tracking code"""
    return f'''<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{measurement_id}', {{
    page_title: document.title,
    page_location: window.location.href,
    page_path: window.location.pathname
  }});

  // Enhanced Ecommerce - Track business listing views
  function trackBusinessView(businessName, category) {{
    gtag('event', 'view_item', {{
      currency: 'USD',
      value: 0,
      items: [{{
        item_id: businessName.toLowerCase().replace(/\\s+/g, '-'),
        item_name: businessName,
        item_category: category,
        item_variant: 'free_listing',
        price: 0,
        quantity: 1
      }}]
    }});
  }}

  // Track phone clicks
  document.addEventListener('DOMContentLoaded', function() {{
    // Phone number click tracking
    const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
    phoneLinks.forEach(link => {{
      link.addEventListener('click', function() {{
        const phoneNumber = this.href.replace('tel:', '');
        const businessName = this.closest('.business-card')?.querySelector('h3')?.textContent || 'Unknown';
        
        gtag('event', 'phone_click', {{
          event_category: 'engagement',
          event_label: businessName,
          value: phoneNumber
        }});
      }});
    }});

    // Get Listed button tracking
    const ctaButtons = document.querySelectorAll('.cta-button, .hero-cta, button[onclick*="mailto"]');
    ctaButtons.forEach(button => {{
      button.addEventListener('click', function() {{
        gtag('event', 'get_listed_click', {{
          event_category: 'lead_generation',
          event_label: window.location.pathname,
          value: 1
        }});
      }});
    }});

    // Track search usage
    const searchInput = document.querySelector('.search-bar input, #searchBar');
    if (searchInput) {{
      let searchTimeout;
      searchInput.addEventListener('input', function() {{
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {{
          if (this.value.length > 2) {{
            gtag('event', 'search', {{
              search_term: this.value,
              event_category: 'engagement'
            }});
          }}
        }}, 1000);
      }});
    }}

    // Track category navigation
    const categoryLinks = document.querySelectorAll('.categories a, .category-card');
    categoryLinks.forEach(link => {{
      link.addEventListener('click', function() {{
        const category = this.textContent.trim();
        gtag('event', 'category_click', {{
          event_category: 'navigation',
          event_label: category
        }});
      }});
    }});
  }});

  // Track scroll depth
  let scrollDepths = [25, 50, 75, 90];
  let scrollsReached = [];
  
  window.addEventListener('scroll', function() {{
    let scrollPercent = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight * 100;
    
    scrollDepths.forEach(depth => {{
      if (scrollPercent >= depth && !scrollsReached.includes(depth)) {{
        scrollsReached.push(depth);
        gtag('event', 'scroll', {{
          event_category: 'engagement',
          event_label: `${{depth}}%`,
          value: depth
        }});
      }}
    }});
  }});
</script>

<!-- GDPR Privacy Notice Script -->
<script>
  // Simple privacy notice for GDPR compliance
  if (!localStorage.getItem('cookieConsent')) {{
    window.addEventListener('load', function() {{
      const notice = document.createElement('div');
      notice.innerHTML = `
        <div style="position: fixed; bottom: 0; left: 0; right: 0; background: #333; color: white; padding: 20px; text-align: center; z-index: 9999;">
          <p style="margin: 0 0 10px 0;">We use cookies to analyze site traffic and optimize your experience. By continuing, you agree to our use of cookies.</p>
          <button onclick="acceptCookies()" style="background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-right: 10px;">Accept</button>
          <a href="/privacy.html" style="color: #667eea;">Privacy Policy</a>
        </div>
      `;
      document.body.appendChild(notice);
    }});
  }}
  
  function acceptCookies() {{
    localStorage.setItem('cookieConsent', 'true');
    document.querySelector('div[style*="position: fixed"]').remove();
  }}
</script>'''

def add_ga4_to_html(file_path, ga4_code):
    """Add GA4 code to an HTML file before the closing </head> tag"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if GA4 is already installed
        if 'googletagmanager.com/gtag/js' in content:
            print(f"⚠️  GA4 already installed in {os.path.basename(file_path)}")
            return False
        
        # Find the </head> tag and insert GA4 code before it
        head_pattern = re.compile(r'(</head>)', re.IGNORECASE)
        
        if head_pattern.search(content):
            # Add GA4 code before </head>
            new_content = head_pattern.sub(f'{ga4_code}\n\\1', content)
            
            # Create backup
            backup_path = file_path + f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ GA4 added to {os.path.basename(file_path)} (backup created)")
            return True
        else:
            print(f"❌ No </head> tag found in {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {os.path.basename(file_path)}: {str(e)}")
        return False

def main():
    """Main function to install GA4 on all HTML files"""
    
    # Check if measurement ID has been updated
    if GA4_MEASUREMENT_ID == "G-XXXXXXXXXX":
        print("❌ ERROR: Please update GA4_MEASUREMENT_ID with your actual Measurement ID!")
        print("Edit this script and replace 'G-XXXXXXXXXX' with your real GA4 ID")
        return
    
    # HTML files to update
    html_files = [
        'index.html',
        'veterinary.html',
        'grooming.html',
        'boarding.html',
        'training.html',
        'pet-stores.html',
        'emergency.html',
        'privacy.html',
        'terms.html'
    ]
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"🚀 Installing Google Analytics 4 (ID: {GA4_MEASUREMENT_ID})")
    print(f"📁 Working directory: {current_dir}")
    print("-" * 50)
    
    # Generate GA4 code
    ga4_code = get_ga4_code(GA4_MEASUREMENT_ID)
    
    # Process each HTML file
    success_count = 0
    for html_file in html_files:
        file_path = os.path.join(current_dir, html_file)
        if os.path.exists(file_path):
            if add_ga4_to_html(file_path, ga4_code):
                success_count += 1
        else:
            print(f"⚠️  File not found: {html_file}")
    
    print("-" * 50)
    print(f"✅ Installation complete! {success_count}/{len(html_files)} files updated")
    print("\n📋 Next steps:")
    print("1. Commit and push changes to GitHub")
    print("2. Wait for Netlify auto-deploy (2-3 minutes)")
    print("3. Visit your site and check GA4 Realtime reports")
    print("4. Test phone clicks and button clicks")
    
    print("\n🔍 To verify installation:")
    print("1. Open https://analytics.google.com")
    print("2. Go to Reports → Realtime")
    print("3. Visit your website in another tab")
    print("4. You should see yourself as an active user")

if __name__ == "__main__":
    main()