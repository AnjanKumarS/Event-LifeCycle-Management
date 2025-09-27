// Main JavaScript file
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive elements
    initializeAnimations();
    initializeNavigation();
    initializeFlashMessages();
    initializeTooltips();
    initializeDropdowns();
});

function initializeAnimations() {
    // Add entrance animations to elements
    document.querySelectorAll('.animate-on-scroll').forEach(element => {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in-up');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        observer.observe(element);
    });
}

function initializeNavigation() {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            if (!mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('animate-fade-in-down');
            }
        });
    }

    // Add active state to current navigation item
    const currentPath = window.location.pathname;
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

function initializeFlashMessages() {
    // Auto-dismiss flash messages
    document.querySelectorAll('.alert').forEach(alert => {
        // Add close button functionality
        const closeButton = alert.querySelector('button');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                alert.classList.add('animate-fade-out');
                setTimeout(() => alert.remove(), 300);
            });
        }

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alert.isConnected) {
                alert.classList.add('animate-fade-out');
                setTimeout(() => alert.remove(), 300);
            }
        }, 5000);
    });
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeDropdowns() {
    // Initialize Bootstrap dropdowns
    const dropdownTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="dropdown"]'));
    dropdownTriggerList.map(function (dropdownTriggerEl) {
        return new bootstrap.Dropdown(dropdownTriggerEl);
    });
}

// Utility function to show loading state
function showLoading(element, text = 'Loading...') {
    const originalContent = element.innerHTML;
    element.disabled = true;
    element.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        <span class="ml-2">${text}</span>
    `;
    return () => {
        element.disabled = false;
        element.innerHTML = originalContent;
    };
}

// Utility function to show notifications
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} animate-fade-in-down fixed top-4 right-4 z-50 p-4 rounded-xl shadow-lg text-white ${
        type === 'success' ? 'bg-gradient-to-r from-green-500 to-emerald-500' : 'bg-gradient-to-r from-red-500 to-pink-500'
    }`;
    
    notification.innerHTML = `
        <div class="flex items-center space-x-3">
            <div class="flex-shrink-0">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} text-xl"></i>
            </div>
            <p class="flex-1">${message}</p>
            <button class="text-white hover:text-white/80">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="animate-progress h-1 bg-white/20 absolute bottom-0 left-0 right-0"></div>
    `;
    
    document.body.appendChild(notification);
    
    // Add click handler to close button
    notification.querySelector('button').addEventListener('click', () => {
        notification.classList.add('animate-fade-out');
        setTimeout(() => notification.remove(), 300);
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.isConnected) {
            notification.classList.add('animate-fade-out');
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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