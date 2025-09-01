// Funcionalidad JavaScript para el wishlist
document.addEventListener('DOMContentLoaded', function() {
    console.log('Wishlist JavaScript cargado');
    
    // Verificar elementos en la página
    const wishlistItems = document.querySelectorAll('.wishlist-item');
    console.log('Items de wishlist encontrados:', wishlistItems.length);
    
    // Eliminar de wishlist
    document.querySelectorAll('.remove-from-wishlist-btn').forEach(button => {
        console.log('Botón eliminar encontrado:', button);
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            console.log('Eliminando producto:', productId);
            
            if (confirm('¿Estás seguro de que quieres eliminar este producto de tu lista de deseos?')) {
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
                        this.closest('.wishlist-item').remove();
                        showMessage(data.message, 'success');
                        updateWishlistCount();
                    } else {
                        showMessage('Error al eliminar el producto', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage('Error al eliminar el producto', 'error');
                });
            }
        });
    });


    // Limpiar wishlist
    const clearWishlistBtn = document.querySelector('.clear-wishlist-btn');
    if (clearWishlistBtn) {
        console.log('Botón limpiar wishlist encontrado');
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
                        location.reload();
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
    }

    function showMessage(message, type) {
        console.log('Mostrando mensaje:', message, type);
        
        // Remover mensajes existentes
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(messageDiv, container.firstChild);
            
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.remove();
                }
            }, 3000);
        }
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
    
    console.log('Wishlist JavaScript inicializado completamente');
}); 