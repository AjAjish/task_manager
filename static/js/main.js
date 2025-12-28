// ============================================
// MOBILE MENU TOGGLE
// ============================================
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', function() {
        this.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = navMenu.contains(event.target);
        const isClickOnHamburger = hamburger.contains(event.target);

        if (!isClickInsideNav && !isClickOnHamburger && navMenu.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    });

    // Close menu when clicking on a nav link (mobile)
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    });
}

// ============================================
// THEME TOGGLE (Light/Dark Mode)
// ============================================
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

// Check for saved theme preference or default to 'light'
const currentTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', currentTheme);

if (themeToggle) {
    themeToggle.addEventListener('click', function() {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Add transition animation
        this.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            this.style.transform = 'rotate(0deg)';
        }, 300);
    });
}

// ============================================
// STICKY NAVBAR ON SCROLL
// ============================================
const navbar = document.getElementById('navbar');
let lastScrollTop = 0;

window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > 100) {
        navbar.style.boxShadow = 'var(--shadow-sm)';
    } else {
        navbar.style.boxShadow = 'none';
    }
    
    lastScrollTop = scrollTop;
});

// ============================================
// ACTIVE NAVIGATION LINK
// ============================================
function setActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        
        if (linkPath === currentPath) {
            link.style.color = 'var(--primary-color)';
            link.style.fontWeight = '500';
        }
    });
}

// Call on page load
document.addEventListener('DOMContentLoaded', setActiveNavLink);

// ============================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ============================================
// FORM INPUT ANIMATIONS
// ============================================
const formInputs = document.querySelectorAll('.form-input, .form-textarea, .form-select');

formInputs.forEach(input => {
    // Add focus effect
    input.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });
    
    // Remove focus effect
    input.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
        
        if (this.value.trim() !== '') {
            this.classList.add('filled');
        } else {
            this.classList.remove('filled');
        }
    });
    
    // Check if input has value on page load
    if (input.value.trim() !== '') {
        input.classList.add('filled');
    }
});

// ============================================
// INTERSECTION OBSERVER FOR ANIMATIONS
// ============================================
const observerOptions = {
    threshold:  0.1,
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

// Observe elements with animation classes
const animatedElements = document.querySelectorAll('.stat-card, .form-section, .activity-item');
animatedElements.forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(element);
});

// ============================================
// UTILITY FUNCTIONS
// ============================================

// Debounce function for performance optimization
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
                        func(... args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ============================================
// RESPONSIVE WINDOW RESIZE HANDLER
// ============================================
const handleResize = debounce(function() {
    // Close mobile menu if window is resized to desktop
    if (window.innerWidth > 768) {
        if (navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        }
    }
}, 250);

window.addEventListener('resize', handleResize);

// ============================================
// LOADING ANIMATION
// ============================================
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.3s ease-in';
        document.body.style.opacity = '1';
    }, 100);
});

// ============================================
// TOAST HANDLER - 5 Second Display
// ============================================

(function() {
  'use strict';

  // ============================================
  // NAVBAR SCROLL EFFECT
  // ============================================
  function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    const handleScroll = () => {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    };

    // Throttle scroll event for performance
    let ticking = false;
    window.addEventListener('scroll', function() {
      if (!ticking) {
        window.requestAnimationFrame(function() {
          handleScroll();
          ticking = false;
        });
        ticking = true;
      }
    });

    // Check scroll position on load
    handleScroll();
  }

  // ============================================
  // TOAST NOTIFICATION FUNCTIONS
  // ============================================
  
  /**
   * Hide toast notification
   */
  window.hideToast = function() {
    const toast = document.getElementById('toast');
    if (toast) {
      toast.classList.remove('show');
      toast.classList.add('hide');
      
      // Remove from DOM after animation
      setTimeout(() => {
        if (toast.parentElement) {
          toast.style.display = 'none';
        }
      }, 400);
    }
  };

  /**
   * Show toast notification
   * @param {string} message - The message to display
   * @param {string} type - Type:  'success', 'error', 'warning', 'info'
   * @param {number} duration - Duration in milliseconds (default: 5000 = 5 seconds)
   */
  window.showToast = function(message, type = 'info', duration = 5000) {
    let toast = document.getElementById('toast');
    
    // Create toast if it doesn't exist
    if (! toast) {
      toast = document.createElement('div');
      toast.id = 'toast';
      toast.className = 'toast';
      document.body.appendChild(toast);
    }

    // Reset classes
    toast.className = 'toast';
    toast.style.display = 'flex';
    
    // Add type class
    if (type) {
      toast.classList.add(`toast-${type}`);
    }

    // Set icon based on type
    let icon = 'ℹ️';
    switch(type) {
      case 'success':
        icon = '✅';
        break;
      case 'error': 
        icon = '❌';
        break;
      case 'warning':
        icon = '⚠️';
        break;
      default:
        icon = 'ℹ️';
    }

    // Set content
    toast.innerHTML = `
      <div class="toast-content">
        <span class="toast-icon">${icon}</span>
        <div class="toast-message">${message}</div>
      </div>
      <button class="toast-close-btn" onclick="hideToast()" aria-label="Close">×</button>
    `;

    // Show toast
    setTimeout(() => {
      toast.classList.add('show');
    }, 10);

    // Auto-hide after 5 seconds (or custom duration)
    if (duration > 0) {
      setTimeout(() => {
        hideToast();
      }, duration);
    }
  };

  /**
   * Auto-show Django messages on page load
   * FIXED: Now shows for exactly 5 seconds
   */
  function initDjangoMessages() {
    const toast = document.getElementById('toast');
    if (toast) {
      // Show toast after 100ms delay
      setTimeout(() => {
        toast.classList.add('show');
      }, 100);

      // Auto-hide after exactly 5 seconds (5000ms)
      setTimeout(() => {
        hideToast();
      }, 5100); // 100ms delay + 5000ms display = 5100ms total
    }
  }

  // ============================================
  // PROFILE DROPDOWN
  // ============================================
  function initProfileDropdown() {
    const toggleBtn = document.getElementById('profileToggle');
    const menu = document.getElementById('profileMenu');
    const arrow = document.getElementById('arrow');

    if (!toggleBtn || !menu || !arrow) return;

    // Toggle dropdown
    toggleBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      const isVisible = menu.classList.contains('show');
      
      if (isVisible) {
        menu.classList.remove('show');
        arrow.style.transform = 'rotate(0deg)';
      } else {
        menu.classList.add('show');
        arrow.style.transform = 'rotate(180deg)';
      }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
      if (!toggleBtn.contains(e.target) && !menu.contains(e.target)) {
        menu.classList.remove('show');
        arrow.style.transform = 'rotate(0deg)';
      }
    });

    // Prevent dropdown from closing when clicking inside menu
    menu.addEventListener('click', function(e) {
      e.stopPropagation();
    });
  }

  // ============================================
  // INITIALIZATION
  // ============================================
  document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbarScroll();
    initDjangoMessages();
    initProfileDropdown();
  });

  // ============================================
  // HELPER FUNCTIONS
  // All helper functions default to 5 seconds
  // ============================================
  
  /**
   * Show success toast (5 seconds default)
   */
  window.toastSuccess = function(message, duration = 5000) {
    showToast(message, 'success', duration);
  };

  /**
   * Show error toast (5 seconds default)
   */
  window.toastError = function(message, duration = 5000) {
    showToast(message, 'error', duration);
  };

  /**
   * Show warning toast (5 seconds default)
   */
  window.toastWarning = function(message, duration = 5000) {
    showToast(message, 'warning', duration);
  };

  /**
   * Show info toast (5 seconds default)
   */
  window.toastInfo = function(message, duration = 5000) {
    showToast(message, 'info', duration);
  };

})();

// ============================================
// CONSOLE BRANDING (Optional)
// ============================================
console.log('%c TaskFlow ', 'background: #007AFF; color: white; font-size: 20px; padding: 10px; border-radius: 5px;');
console.log('%c Built with ❤️ using Django', 'color: #6E6E73; font-size: 12px;');