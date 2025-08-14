// Funcionalidad para botones de wishlist y carrito
document.addEventListener('DOMContentLoaded', function() {
    console.log('🛍️ Inicializando funcionalidad de productos...');
    
    // Manejar botones de wishlist
    document.querySelectorAll('.wishlist-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const wishlistIcon = this.querySelector('.wishlist-icon');
            
            console.log('Agregando producto al wishlist:', productId);
            
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
                    showPopupMessage('Debes iniciar sesión para agregar productos al wishlist', 'error');
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
                    
                    // Mostrar mensaje de éxito con popup
                    showPopupMessage(data.message, 'success');
                } else {
                    if (data.message && data.message.includes('logueado')) {
                        showPopupMessage('Debes iniciar sesión para agregar productos al wishlist', 'error');
                        setTimeout(() => {
                            window.location.href = '/account/login/';
                        }, 2000);
                    } else {
                        showPopupMessage(data.message || 'Error al agregar al wishlist', 'error');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showPopupMessage('Error al agregar al wishlist', 'error');
            });
        });
    });

    // Manejar botones de agregar al carrito
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
                    showPopupMessage(data.message, 'success');
                    // Actualizar contador del carrito si existe
                    const cartCountElement = document.querySelector('.cart-count');
                    if (cartCountElement && data.cart_count !== undefined) {
                        cartCountElement.textContent = data.cart_count;
                    }
                } else {
                    if (data.message && data.message.includes('logueado')) {
                        showPopupMessage('Debes iniciar sesión para agregar productos al carrito', 'error');
                        // Opcional: redirigir al login después de un breve delay
                        setTimeout(() => {
                            window.location.href = '/account/login/';
                        }, 2000);
                    } else {
                        showPopupMessage(data.message || 'Error al agregar al carrito', 'error');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showPopupMessage('Error al agregar al carrito', 'error');
            });
        });
    });

    console.log('✅ Funcionalidad de productos inicializada correctamente');
});

// Función para mostrar mensajes popup
function showPopupMessage(message, type) {
    // Remover mensajes existentes
    const existingMessages = document.querySelectorAll('.popup-message');
    existingMessages.forEach(msg => msg.remove());
    
    // Crear el elemento del mensaje
    const messageDiv = document.createElement('div');
    messageDiv.className = `popup-message popup-${type}`;
    
    // Agregar ícono según el tipo
    const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
    messageDiv.innerHTML = `
        <div class="popup-content">
            <span class="popup-icon">${icon}</span>
            <span class="popup-text">${message}</span>
        </div>
    `;
    
    // Agregar al body
    document.body.appendChild(messageDiv);
    
    // Mostrar con animación
    setTimeout(() => {
        messageDiv.classList.add('show');
    }, 100);
    
    // Ocultar después de 4 segundos
    setTimeout(() => {
        messageDiv.classList.remove('show');
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 300);
    }, 4000);
}

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

// Agregar estilos CSS para la animación y popup
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
    
    .popup-message {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        max-width: 400px;
        padding: 16px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateX(100%);
        opacity: 0;
        transition: all 0.3s ease;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .popup-message.show {
        transform: translateX(0);
        opacity: 1;
    }
    
    .popup-success {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        border-left: 4px solid #2E7D32;
    }
    
    .popup-error {
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
        border-left: 4px solid #c62828;
    }
    
    .popup-info {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        color: white;
        border-left: 4px solid #1565C0;
    }
    
    .popup-content {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .popup-icon {
        font-size: 20px;
        flex-shrink: 0;
    }
    
    .popup-text {
        font-size: 14px;
        font-weight: 500;
        line-height: 1.4;
    }
    
    @media (max-width: 768px) {
        .popup-message {
            top: 10px;
            right: 10px;
            left: 10px;
            max-width: none;
        }
    }
`;
document.head.appendChild(style);
