// Add any interactive functionality here if needed
// Example: Toggle mobile menu
const navbar = document.querySelector('.navbar');
const navLinks = document.querySelector('.nav-links');

navbar.addEventListener('click', () => {
  navLinks.classList.toggle('active');
});