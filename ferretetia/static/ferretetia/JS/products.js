// Funcionalidad para botones de wishlist y carrito
document.addEventListener('DOMContentLoaded', function() {
    console.log('🛍️ Inicializando funcionalidad de productos...');
    
    // Manejar botones de wishlist
    document.querySelectorAll('.wishlist-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const wishlistIcon = this.querySelector('.wishlist-icon');
            
            console.log('💖 Agregando producto al wishlist:', productId);
            
            fetch(`/wishlist/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.status === 403) {
                    // Usuario no autenticado
                    showMessage('Debes iniciar sesión para agregar productos al wishlist', 'error');
                    setTimeout(() => {
                        window.location.href = '/account/login/';
                    }, 2000);
                    return null;
                }
                return response.json();
            })
            .then(data => {
                if (data === null) return; // Ya se manejó el error de autenticación
                
                if (data.success) {
                    // Cambiar el ícono para mostrar que está en el wishlist
                    wishlistIcon.textContent = '❤️';
                    this.title = 'Eliminar de favoritos';
                    
                    // Mostrar mensaje de éxito
                    showMessage(data.message, 'success');
                } else {
                    if (data.message && data.message.includes('logueado')) {
                        showMessage('Debes iniciar sesión para agregar productos al wishlist', 'error');
                        setTimeout(() => {
                            window.location.href = '/account/login/';
                        }, 2000);
                    } else {
                        showMessage(data.message || 'Error al agregar al wishlist', 'error');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Error al agregar al wishlist', 'error');
            });
        });
    });

    // Manejar botones de agregar al carrito
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            
            console.log('🛒 Agregando producto al carrito:', productId);
            
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
                    showMessage(data.message, 'success');
                    // Actualizar contador del carrito si existe
                    const cartCountElement = document.querySelector('.cart-count');
                    if (cartCountElement && data.cart_count !== undefined) {
                        cartCountElement.textContent = data.cart_count;
                    }
                } else {
                    if (data.message && data.message.includes('logueado')) {
                        showMessage('Debes iniciar sesión para agregar productos al carrito', 'error');
                        // Opcional: redirigir al login después de un breve delay
                        setTimeout(() => {
                            window.location.href = '/account/login/';
                        }, 2000);
                    } else {
                        showMessage(data.message || 'Error al agregar al carrito', 'error');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Error al agregar al carrito', 'error');
            });
        });
    });

    console.log('✅ Funcionalidad de productos inicializada correctamente');
});

// Función para obtener cookies
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

// Función para mostrar mensajes
function showMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem;
        border-radius: 5px;
        color: white;
        font-weight: 600;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    if (type === 'success') {
        messageDiv.style.backgroundColor = '#28a745';
    } else if (type === 'error') {
        messageDiv.style.backgroundColor = '#dc3545';
    }
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

// Agregar estilos CSS para la animación
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
