// Enhanced main.js
document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    const navbar = document.getElementById('navbar');

    // Mobile menu toggle
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            const isExpanded = hamburger.getAttribute('aria-expanded') === 'true';
            hamburger.setAttribute('aria-expanded', !isExpanded);
            navLinks.classList.toggle('active');
            hamburger.innerHTML = isExpanded 
                ? '<i class="fas fa-bars"></i>' 
                : '<i class="fas fa-times"></i>';
        });

        // Close mobile menu when clicking a link
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                hamburger.innerHTML = '<i class="fas fa-bars"></i>';
                hamburger.setAttribute('aria-expanded', 'false');
            });
        });
    }

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (navbar) {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        }
    });

    // Form submission with better validation
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Validate required fields
            const requiredFields = [
                { id: 'name', message: 'Please enter your name' },
                { id: 'email', message: 'Please enter a valid email' },
                { id: 'phone', message: 'Please enter your phone number' },
                { id: 'date', message: 'Please select a date' },
                { id: 'time', message: 'Please select a time' },
                { id: 'package', message: 'Please select a package' },
                { id: 'location', message: 'Please select a location' }
            ];

            requiredFields.forEach(field => {
                const element = document.getElementById(field.id);
                if (element && !element.value.trim()) {
                    isValid = false;
                    element.focus();
                    alert(field.message);
                    return false;
                }
            });

            // Email validation
            const email = document.getElementById('email');
            if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
                isValid = false;
                email.focus();
                alert('Please enter a valid email address');
                return false;
            }

            if (!isValid) {
                e.preventDefault();
            }
        });
    }

    // Bubble animation
    function createBubbles() {
        const bubbles = document.getElementById('bubbles');
        if (!bubbles) return;
        
        // Clear existing bubbles
        bubbles.innerHTML = '';
        
        const bubbleCount = 20;
        
        for (let i = 0; i < bubbleCount; i++) {
            const bubble = document.createElement('div');
            bubble.classList.add('bubble');
            
            // Random properties
            const size = Math.random() * 40 + 10;
            bubble.style.width = `${size}px`;
            bubble.style.height = `${size}px`;
            bubble.style.left = `${Math.random() * 100}%`;
            bubble.style.animationDuration = `${Math.random() * 10 + 10}s`;
            bubble.style.animationDelay = `${Math.random() * 5}s`;
            
            bubbles.appendChild(bubble);
        }
    }

    // Wheel animation button (scroll to top)
    const wheelBtn = document.getElementById('wheelBtn');
    if (wheelBtn) {
        wheelBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // Show/hide based on scroll position
        window.addEventListener('scroll', () => {
            wheelBtn.style.display = window.scrollY > 300 ? 'flex' : 'none';
        });
    }

    // Initialize animations
    createBubbles();
    
    // Animate elements when they come into view
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.package, .gallery-item, .testimonial, .team-member, .value-item');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                element.classList.add('visible');
            }
        });
    };
    
    // Set initial state for animations
    const animatedElements = document.querySelectorAll('.package, .gallery-item, .testimonial, .team-member, .value-item');
    if (animatedElements.length > 0) {
        animatedElements.forEach(el => {
            el.classList.add('animate-on-scroll');
        });
        
        window.addEventListener('scroll', animateOnScroll);
        animateOnScroll(); // Run once on load
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
                
                // Update URL without jumping
                if (history.pushState) {
                    history.pushState(null, null, targetId);
                } else {
                    location.hash = targetId;
                }
            }
        });
    });
});
