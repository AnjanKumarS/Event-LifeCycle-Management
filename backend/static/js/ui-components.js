// Advanced UI Components

class ParallaxEffect {
    constructor(elements, options = {}) {
        this.elements = document.querySelectorAll(elements);
        this.options = {
            speed: options.speed || 0.5,
            direction: options.direction || 'vertical'
        };
        this.init();
    }

    init() {
        window.addEventListener('scroll', () => this.animate());
    }

    animate() {
        const scrolled = window.pageYOffset;
        this.elements.forEach(element => {
            const elementOffset = element.offsetTop;
            const distance = elementOffset - scrolled;
            const translation = distance * this.options.speed;
            
            if (this.options.direction === 'vertical') {
                element.style.transform = `translateY(${translation}px)`;
            } else {
                element.style.transform = `translateX(${translation}px)`;
            }
        });
    }
}

class FloatingCards {
    constructor(selector) {
        this.cards = document.querySelectorAll(selector);
        this.init();
    }

    init() {
        this.cards.forEach(card => {
            card.addEventListener('mousemove', (e) => this.handleMouseMove(e, card));
            card.addEventListener('mouseleave', () => this.handleMouseLeave(card));
        });
    }

    handleMouseMove(e, card) {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 20;
        const rotateY = -(x - centerX) / 20;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        card.style.transition = 'transform 0.1s';
    }

    handleMouseLeave(card) {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
        card.style.transition = 'transform 0.5s';
    }
}

class TextScramble {
    constructor(element) {
        this.element = element;
        this.chars = '!<>-_\\/[]{}—=+*^?#________';
        this.queue = [];
        this.frame = 0;
        this.frameRequest = null;
        this.originalText = element.innerText;
        this.init();
    }

    init() {
        element.addEventListener('mouseenter', () => this.scramble());
    }

    scramble() {
        const text = this.originalText;
        const length = text.length;
        let counter = 0;
        
        const update = () => {
            let output = '';
            let complete = 0;
            for (let i = 0; i < length; i++) {
                if (i < counter) {
                    output += text[i];
                    complete++;
                } else {
                    output += this.chars[Math.floor(Math.random() * this.chars.length)];
                }
            }
            this.element.innerText = output;
            if (complete === length) {
                cancelAnimationFrame(this.frameRequest);
            } else {
                counter += 1 / 3;
                this.frameRequest = requestAnimationFrame(update);
            }
        };
        update();
    }
}

class GradientButton {
    constructor(selector) {
        this.buttons = document.querySelectorAll(selector);
        this.init();
    }

    init() {
        this.buttons.forEach(button => {
            button.addEventListener('mousemove', (e) => this.handleMouseMove(e, button));
            button.addEventListener('mouseleave', (e) => this.handleMouseLeave(e, button));
        });
    }

    handleMouseMove(e, button) {
        const rect = button.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        button.style.setProperty('--x', `${x}px`);
        button.style.setProperty('--y', `${y}px`);
        button.style.setProperty('--size', `${Math.max(rect.width, rect.height) * 2}px`);
    }

    handleMouseLeave(e, button) {
        button.style.setProperty('--size', '0px');
    }
}

class SmoothScroll {
    constructor(options = {}) {
        this.links = document.querySelectorAll('a[href^="#"]');
        this.options = {
            duration: options.duration || 800,
            easing: options.easing || this.easeInOutQuad
        };
        this.init();
    }

    init() {
        this.links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    this.scrollTo(target);
                }
            });
        });
    }

    scrollTo(target) {
        const start = window.pageYOffset;
        const end = target.getBoundingClientRect().top + start;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / this.options.duration, 1);
            
            window.scrollTo(0, start + (end - start) * this.options.easing(progress));
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }

    easeInOutQuad(t) {
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    }
}

// Initialize components when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize parallax effects
    new ParallaxEffect('.parallax-element', { speed: 0.5 });
    
    // Initialize floating cards
    new FloatingCards('.card-hover-effect');
    
    // Initialize gradient buttons
    new GradientButton('.btn-gradient');
    
    // Initialize smooth scroll
    new SmoothScroll({
        duration: 800
    });
    
    // Initialize text scramble effects
    document.querySelectorAll('.text-scramble').forEach(element => {
        new TextScramble(element);
    });
});

// Export components for use in other scripts
window.UI = {
    ParallaxEffect,
    FloatingCards,
    TextScramble,
    GradientButton,
    SmoothScroll
};