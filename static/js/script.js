const relatedSites = document.querySelector('.related-sites'); // Select the element

window.addEventListener('scroll', function() {
    const scrollPosition = window.scrollY; // Get scroll position
    relatedSites.style.top = scrollPosition + 'px'; // Set top position
});
