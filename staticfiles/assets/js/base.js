document.addEventListener('DOMContentLoaded', function() {
            const currentPath = window.location.pathname;
            const navLinks = document.querySelectorAll('nav ul li a');

            navLinks.forEach(link => {
                if (link.getAttribute('href') === '#') {
                    // Solo para demostración
                }
            });

            navLinks.forEach(link => {
                link.addEventListener('click', function(event) {
                    console.log('Navegando a: ' + this.textContent);
                });
            });
        });