document.addEventListener('DOMContentLoaded', () => {
    // Active navigation highlighting
    const navLinks = document.querySelectorAll('nav ul li a');
    const sections = document.querySelectorAll('.dashboard-section');
    
    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            window.scrollTo({
                top: targetSection.offsetTop - 20,
                behavior: 'smooth'
            });
            
            // Update active link
            document.querySelector('nav ul li.active').classList.remove('active');
            link.parentElement.classList.add('active');
        });
    });
    
    // Scroll spy for navigation
    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (pageYOffset >= sectionTop - 60) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.parentElement.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.parentElement.classList.add('active');
            }
        });
    });
    
    // Export report functionality
    const exportButton = document.querySelector('.btn-export');
    exportButton.addEventListener('click', () => {
        window.print();
    });
});