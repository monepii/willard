// Funcionalidad JavaScript para el wishlist
document.addEventListener('DOMContentLoaded', function() {
    // Eliminar de wishlist
    document.querySelectorAll('.remove-from-wishlist-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const wishlistItem = this.closest('.wishlist-item');
            
            fetch(`/wishlist/remove/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    wishlistItem.remove();
                    updateWishlistCount();
                    
                    // Mostrar mensaje
                    showMessage(data.message, 'success');
                } else {
                    showMessage('Error al eliminar el producto', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Error al eliminar el producto', 'error');
            });
        });
    });

    // Agregar al carrito
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            
            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessage('Producto agregado al carrito', 'success');
                } else {
                    if (data.message && data.message.includes('logueado')) {
                        showMessage('Debes iniciar sesión para agregar productos al carrito', 'error');
                        // Opcional: redirigir al login después de un breve delay
                        setTimeout(() => {
                            window.location.href = '/account/login/';
                        }, 2000);
                    } else {
                        showMessage('Error al agregar al carrito', 'error');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Error al agregar al carrito', 'error');
            });
        });
    });

    // Limpiar wishlist
    const clearWishlistBtn = document.querySelector('.clear-wishlist-btn');
    if (clearWishlistBtn) {
        clearWishlistBtn.addEventListener('click', function() {
            if (confirm('¿Estás seguro de que quieres limpiar toda tu lista de deseos?')) {
                fetch('/wishlist/clear/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Limpiar la interfaz
                        const wishlistContent = document.querySelector('.wishlist-content');
                        if (wishlistContent) {
                            wishlistContent.innerHTML = `
                                <div class="empty-wishlist">
                                    <div class="empty-icon">♡</div>
                                    <h2>Tu lista de deseos está vacía</h2>
                                    <p>No tienes productos guardados en tu lista de deseos.</p>
                                    <a href="/shop/" class="btn-primary">Explorar Productos</a>
                                </div>
                            `;
                        }
                        showMessage(data.message, 'success');
                    } else {
                        showMessage('Error al limpiar la lista de deseos', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage('Error al limpiar la lista de deseos', 'error');
                });
            }
        });
    }

    function updateWishlistCount() {
        const items = document.querySelectorAll('.wishlist-item');
        const countElement = document.querySelector('.item-count');
        if (countElement) {
            countElement.textContent = `${items.length} producto${items.length !== 1 ? 's' : ''}`;
        }
        
        // Si no hay items, mostrar mensaje de lista vacía
        if (items.length === 0) {
            const wishlistContent = document.querySelector('.wishlist-content');
            if (wishlistContent) {
                wishlistContent.innerHTML = `
                    <div class="empty-wishlist">
                        <div class="empty-icon">♡</div>
                        <h2>Tu lista de deseos está vacía</h2>
                        <p>No tienes productos guardados en tu lista de deseos.</p>
                        <a href="/shop/" class="btn-primary">Explorar Productos</a>
                    </div>
                `;
            }
        }
    }

    function showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        const container = document.querySelector('.container');
        container.insertBefore(messageDiv, container.firstChild);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}); 