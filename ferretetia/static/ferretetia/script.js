// JavaScript para el sitio web de Willard
console.log('Sitio web cargado correctamente');

// Variables globales
let cart = [];
let cartCount = 0;

// Cargar carrito desde localStorage
function loadCart() {
    const savedCart = localStorage.getItem('willard_cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        cartCount = cart.reduce((total, item) => total + item.quantity, 0);
        updateCartUI();
    }
}

// Guardar carrito en localStorage
function saveCart() {
    localStorage.setItem('willard_cart', JSON.stringify(cart));
}

// Actualizar UI del carrito
function updateCartUI() {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = cartCount;
    }
}

// Agregar producto al carrito
function addToCart(productId, productName, price) {
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: productName,
            price: price,
            quantity: 1
        });
    }
    
    cartCount += 1;
    updateCartUI();
    saveCart();
    
    // Mostrar notificación
    showNotification(`${productName} agregado al carrito`);
}

// Mostrar notificación
function showNotification(message) {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #28a745;
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        z-index: 10000;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    `;
    
    document.body.appendChild(notification);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// Función de búsqueda
function performSearch(query) {
    if (!query.trim()) {
        hideSearchResults();
        return;
    }
    
    // Simular API call
    fetch('/api/search/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displaySearchResults(data.results);
        } else {
            console.error('Error en la búsqueda:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Mostrar resultados de ejemplo en caso de error
        const exampleResults = [
            { id: 1, name: `Martillo - ${query}`, price: 25.99 },
            { id: 2, name: `Destornillador - ${query}`, price: 15.50 },
            { id: 3, name: `Taladro - ${query}`, price: 89.99 }
        ];
        displaySearchResults(exampleResults);
    });
}

// Mostrar resultados de búsqueda
function displaySearchResults(results) {
    const searchResultsDiv = document.getElementById('search-results');
    const resultsContainer = document.getElementById('results-container');
    
    if (!searchResultsDiv || !resultsContainer) return;
    
    resultsContainer.innerHTML = '';
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>No se encontraron productos.</p>';
    } else {
        results.forEach(product => {
            const resultDiv = document.createElement('div');
            resultDiv.className = 'search-result-item';
            resultDiv.innerHTML = `
                <div>
                    <h4>${product.name}</h4>
                </div>
                <div>
                    <span class="price">$${product.price}</span>
                    <button class="add-to-cart" onclick="addToCart(${product.id}, '${product.name}', ${product.price})" style="margin-left: 10px; padding: 5px 10px; font-size: 12px;">Agregar</button>
                </div>
            `;
            resultsContainer.appendChild(resultDiv);
        });
    }
    
    searchResultsDiv.style.display = 'block';
}

// Ocultar resultados de búsqueda
function hideSearchResults() {
    const searchResultsDiv = document.getElementById('search-results');
    if (searchResultsDiv) {
        searchResultsDiv.style.display = 'none';
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM cargado completamente');
    
    // Cargar carrito
    loadCart();
    
    // Configurar búsqueda
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');
    
    if (searchInput && searchBtn) {
        searchBtn.addEventListener('click', function() {
            performSearch(searchInput.value);
        });
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(searchInput.value);
            }
        });
        
        // Ocultar resultados al hacer clic fuera
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.search-container') && !e.target.closest('.search-results')) {
                hideSearchResults();
            }
        });
    }
    
    // Configurar botones "Agregar al carrito"
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const productCard = this.closest('.product-card');
            const productName = productCard.querySelector('h3').textContent;
            const priceText = productCard.querySelector('.price').textContent;
            const price = parseFloat(priceText.replace('$', ''));
            
            addToCart(parseInt(productId), productName, price);
        });
    });
    
    // Efectos hover para las tarjetas de productos
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});
