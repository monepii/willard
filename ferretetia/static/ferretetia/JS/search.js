// Funcionalidad de búsqueda en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 Inicializando búsqueda en tiempo real...');
    
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');
    
    if (!searchInput) {
        console.error('❌ No se encontró el input de búsqueda');
        return;
    }
    
    console.log('✅ Input de búsqueda encontrado:', searchInput);
    
    // Crear contenedor de resultados
    const searchResults = document.createElement('div');
    searchResults.className = 'search-results';
    
    // Insertar el contenedor de resultados después del contenedor de búsqueda
    if (searchInput && searchInput.parentElement) {
        searchInput.parentElement.appendChild(searchResults);
        console.log('✅ Contenedor de resultados agregado');
    }
    
    let searchTimeout;
    
    // Función para obtener CSRF token
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
    
    // Función para realizar la búsqueda
    function performSearch(query) {
        console.log('🔍 Realizando búsqueda para:', query);
        
        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            return;
        }
        
        // Mostrar indicador de carga
        searchResults.innerHTML = '<div class="loading">Buscando...</div>';
        searchResults.style.display = 'block';
        
        fetch('/search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ query: query })
        })
        .then(response => {
            console.log('📡 Respuesta del servidor:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('📊 Datos recibidos:', data);
            if (data.success) {
                displaySearchResults(data.results, query);
            } else {
                console.error('❌ Error en búsqueda:', data.error);
                searchResults.innerHTML = '<div class="error">Error en la búsqueda</div>';
            }
        })
        .catch(error => {
            console.error('❌ Error de red:', error);
            searchResults.innerHTML = '<div class="error">Error de conexión</div>';
        });
    }
    
    // Función para mostrar resultados
    function displaySearchResults(results, query) {
        console.log('📋 Mostrando resultados:', results.length);
        
        if (results.length === 0) {
            searchResults.innerHTML = `
                <div class="no-results">
                    <p>No se encontraron productos para "${query}"</p>
                    <a href="/shop/" class="view-all-link">Ver todos los productos</a>
                </div>
            `;
        } else {
            let html = '<div class="search-results-list">';
            
            results.forEach(product => {
                const imageUrl = product.image || '/static/images/default.jpg';
                html += `
                                         <div class="search-result-item" onclick="window.location.href='/shop/?search=${encodeURIComponent(query)}'">
                        <div class="result-image">
                            <img src="${imageUrl}" alt="${product.name}" onerror="this.src='/static/images/default.jpg'">
                        </div>
                        <div class="result-info">
                            <h4>${product.name}</h4>
                            <p class="result-sku">SKU: ${product.sku}</p>
                            ${product.category ? `<p class="result-category">${product.category}</p>` : ''}
                            <p class="result-price">$${product.price.toFixed(2)}</p>
                        </div>
                    </div>
                `;
            });
            
            if (results.length >= 10) {
                html += `
                    <div class="view-all-results">
                        <a href="/shop/?search=${encodeURIComponent(query)}" class="view-all-link">
                            Ver todos los resultados (${results.length}+)
                        </a>
                    </div>
                `;
            }
            
            html += '</div>';
            searchResults.innerHTML = html;
        }
        
        searchResults.style.display = 'block';
    }
    
    // Event listeners
    // Búsqueda en tiempo real mientras se escribe
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        console.log('⌨️ Input cambiado:', query);
        
        // Limpiar timeout anterior
        clearTimeout(searchTimeout);
        
        // Establecer nuevo timeout para evitar demasiadas peticiones
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
    
    // Ocultar resultados cuando se hace clic fuera
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
    
    // Mostrar resultados cuando se hace focus en el input
    searchInput.addEventListener('focus', function() {
        const query = this.value.trim();
        if (query.length >= 2) {
            searchResults.style.display = 'block';
        }
    });
    
    // Manejar tecla Enter
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const query = this.value.trim();
            if (query) {
                console.log('🚀 Redirigiendo a búsqueda:', query);
                window.location.href = `/shop/?search=${encodeURIComponent(query)}`;
            }
        }
    });
    
    // Botón de búsqueda
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            const query = searchInput.value.trim();
            if (query) {
                console.log('🔍 Botón de búsqueda clickeado:', query);
                window.location.href = `/shop/?search=${encodeURIComponent(query)}`;
            }
        });
    }
    
    console.log('✅ Búsqueda en tiempo real inicializada correctamente');
});
