// Ferretetia JavaScript file
document.addEventListener('DOMContentLoaded', function() {
    console.log('Ferretetia script loaded');
    
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            console.log('Add to cart clicked for product:', productId);

        });
    });
    
    const searchButton = document.querySelector('.search-btn');
    const searchInput = document.querySelector('.search-input');
    
    if (searchButton && searchInput) {
        searchButton.addEventListener('click', function() {
            const query = searchInput.value.trim();
            if (query) {
                console.log('Search query:', query);
                // Add your search functionality here
            }
        });
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchButton.click();
            }
        });
    }
});
