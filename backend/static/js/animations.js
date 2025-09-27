// Animation utilities
const animations = {
    // Fade in element
    fadeIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.display = 'block';
        element.style.transition = `opacity ${duration}ms ease`;
        requestAnimationFrame(() => {
            element.style.opacity = '1';
        });
    },

    // Fade out element
    fadeOut(element, duration = 300) {
        return new Promise(resolve => {
            element.style.opacity = '1';
            element.style.transition = `opacity ${duration}ms ease`;
            requestAnimationFrame(() => {
                element.style.opacity = '0';
            });
            setTimeout(() => {
                element.style.display = 'none';
                resolve();
            }, duration);
        });
    },

    // Slide down element
    slideDown(element, duration = 300) {
        element.style.display = 'block';
        const height = element.scrollHeight;
        element.style.height = '0';
        element.style.overflow = 'hidden';
        element.style.transition = `height ${duration}ms ease`;
        requestAnimationFrame(() => {
            element.style.height = height + 'px';
        });
        setTimeout(() => {
            element.style.height = '';
            element.style.overflow = '';
        }, duration);
    },

    // Slide up element
    slideUp(element, duration = 300) {
        const height = element.scrollHeight;
        element.style.height = height + 'px';
        element.style.overflow = 'hidden';
        element.style.transition = `height ${duration}ms ease`;
        requestAnimationFrame(() => {
            element.style.height = '0';
        });
        setTimeout(() => {
            element.style.display = 'none';
            element.style.height = '';
            element.style.overflow = '';
        }, duration);
    },

    // Show loading state
    showLoading(element) {
        element.classList.add('loading');
    },

    // Hide loading state
    hideLoading(element) {
        element.classList.remove('loading');
    },

    // Show spinner
    showSpinner(element) {
        const spinner = document.createElement('div');
        spinner.className = 'spinner';
        element.appendChild(spinner);
    },

    // Hide spinner
    hideSpinner(element) {
        const spinner = element.querySelector('.spinner');
        if (spinner) {
            spinner.remove();
        }
    },

    // Animate success checkmark
    showSuccess(element) {
        const checkmark = document.createElement('div');
        checkmark.className = 'success-checkmark';
        element.appendChild(checkmark);
        setTimeout(() => {
            checkmark.remove();
        }, 2000);
    },

    // Add ripple effect to buttons
    addRipple(event) {
        const button = event.currentTarget;
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.className = 'ripple';

        button.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    },

    // Show notification
    showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('hide');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, duration);
    },

    // Initialize skeleton loading
    initSkeletonLoading(container) {
        const items = container.children;
        Array.from(items).forEach(item => {
            item.style.opacity = '0';
            const skeleton = document.createElement('div');
            skeleton.className = 'skeleton';
            skeleton.style.height = item.offsetHeight + 'px';
            container.insertBefore(skeleton, item);
        });
    },

    // Remove skeleton loading
    removeSkeletonLoading(container) {
        const skeletons = container.querySelectorAll('.skeleton');
        const items = Array.from(container.children).filter(child => !child.classList.contains('skeleton'));
        
        skeletons.forEach(skeleton => {
            skeleton.remove();
        });

        items.forEach(item => {
            item.style.opacity = '1';
        });
    },

    // Initialize modal
    initModal(modal) {
        modal.querySelector('.modal-close')?.addEventListener('click', () => {
            this.closeModal(modal);
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeModal(modal);
            }
        });
    },

    // Open modal
    openModal(modal) {
        modal.style.display = 'flex';
        requestAnimationFrame(() => {
            modal.classList.add('show');
        });
    },

    // Close modal
    closeModal(modal) {
        modal.classList.remove('show');
        modal.classList.add('hide');
        setTimeout(() => {
            modal.style.display = 'none';
            modal.classList.remove('hide');
        }, 300);
    },

    // Initialize drop zone
    initDropZone(dropZone, onFilesDrop) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('drag-over');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('drag-over');
            });
        });

        dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (onFilesDrop) {
                onFilesDrop(files);
            }
        });
    },

    // Initialize tooltips
    initTooltips() {
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            element.classList.add('tooltip');
        });
    },

    // Update progress bar
    updateProgressBar(progressBar, percentage) {
        const fill = progressBar.querySelector('.progress-bar-fill');
        if (fill) {
            fill.style.width = percentage + '%';
        }
    },

    // Add page transition
    addPageTransition() {
        document.body.classList.add('page-transition');
        setTimeout(() => {
            document.body.classList.remove('page-transition');
        }, 500);
    },

    // Initialize animations on page load
    init() {
        // Add ripple effect to buttons
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('click', this.addRipple);
        });

        // Initialize tooltips
        this.initTooltips();

        // Add page transition on load
        this.addPageTransition();

        // Initialize modals
        document.querySelectorAll('.modal').forEach(modal => {
            this.initModal(modal);
        });
    }
};