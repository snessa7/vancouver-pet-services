// UI Enhancement Script for Vancouver Pet Services Directory
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Add header scroll effect
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const header = document.querySelector('.header');
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        } else {
            header.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });

    // Enhance business cards with hover effects
    document.querySelectorAll('.business-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
            this.style.boxShadow = '0 10px 30px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        });
    });

    // Add loading animation to buttons
    document.querySelectorAll('.contact-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (this.href && this.href.includes('tel:')) {
                return; // Don't add loading to phone links
            }
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="loading"></span> Loading...';
            this.style.pointerEvents = 'none';
            
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.pointerEvents = 'auto';
            }, 1000);
        });
    });

    // Enhanced search functionality
    const searchBox = document.querySelector('.search-box, #searchBar, .search-input');
    if (searchBox) {
        searchBox.addEventListener('focus', function() {
            if (this.parentElement) {
                this.parentElement.style.transform = 'scale(1.05)';
            }
        });
        
        searchBox.addEventListener('blur', function() {
            if (this.parentElement) {
                this.parentElement.style.transform = 'scale(1)';
            }
        });

        // Add real-time search if not already implemented
        if (!window.searchBusinesses) {
            searchBox.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase().trim();
                const businessCards = document.querySelectorAll('.business-card');
                let hasResults = false;

                businessCards.forEach(card => {
                    const name = card.getAttribute('data-name') || '';
                    const services = card.getAttribute('data-services') || '';
                    const textContent = card.textContent.toLowerCase();
                    
                    const isMatch = searchTerm === '' || 
                                   name.includes(searchTerm) || 
                                   services.includes(searchTerm) || 
                                   textContent.includes(searchTerm);

                    if (isMatch) {
                        card.style.display = 'block';
                        hasResults = true;
                    } else {
                        card.style.display = 'none';
                    }
                });

                // Show/hide no results message
                const noResults = document.getElementById('noResults');
                if (noResults) {
                    noResults.style.display = hasResults ? 'none' : 'block';
                }
            });
        }
    }

    // Add fade-in animation to elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all business cards
    document.querySelectorAll('.business-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease-out';
        observer.observe(card);
    });
});

// Add modern CSS enhancements
const style = document.createElement('style');
style.textContent = `
    /* Modern UI Enhancements */
    :root {
        --primary: #2563eb;
        --primary-dark: #1e40af;
        --secondary: #7c3aed;
        --success: #10b981;
        --danger: #ef4444;
    }

    * {
        transition: all 0.3s ease;
    }

    body {
        background: #f8fafc;
    }

    .header {
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.95) !important;
        border-bottom: 1px solid #e5e7eb;
    }

    .logo {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    .nav-links a {
        position: relative;
        font-weight: 500;
    }

    .nav-links a::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 0;
        height: 2px;
        background: var(--primary);
        transition: width 0.3s;
    }

    .nav-links a:hover::after {
        width: 100%;
    }

    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        position: relative;
        overflow: hidden;
    }

    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        animation: float 20s linear infinite;
    }

    @keyframes float {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(-50px, -50px) rotate(10deg); }
    }

    .search-box {
        border: 2px solid transparent;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }

    .search-box:focus {
        border-color: var(--primary);
        box-shadow: 0 10px 40px rgba(37, 99, 235, 0.2);
    }

    .category-card {
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        background: white;
    }

    .category-card:hover {
        border-color: var(--primary);
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }

    .category-icon {
        animation: bounce 2s infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .business-card {
        border: 1px solid #e5e7eb;
        position: relative;
        overflow: hidden;
    }

    .business-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        transition: left 0.3s;
    }

    .business-card:hover::before {
        left: 0;
    }

    .contact-btn {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        font-weight: 600;
        border: none;
        position: relative;
        overflow: hidden;
    }

    .contact-btn::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .contact-btn:hover::before {
        width: 300px;
        height: 300px;
    }

    .contact-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    }

    .features {
        background: #f3f4f6;
        border-left: 3px solid var(--primary);
    }

    .emergency-badge {
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .business-card.emergency {
        border-color: var(--danger);
        border-width: 2px;
    }

    .loading {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Responsive improvements */
    @media (max-width: 768px) {
        .hero h1 {
            font-size: 2rem !important;
        }
        
        .business-grid {
            gap: 1rem;
        }
        
        .category-card {
            padding: 1.5rem;
        }
    }
`;

document.head.appendChild(style);