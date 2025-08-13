// Buscador global que funciona en todas las pestañas
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 Inicializando buscador global...');
    
    // Buscar el input de búsqueda en la página actual
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');
    
    if (!searchInput) {
        console.log('❌ No se encontró el input de búsqueda en esta página');
        return;
    }
    
    console.log('✅ Input de búsqueda encontrado:', searchInput);
    
    // Crear contenedor de resultados si no existe
    let searchResults = document.querySelector('.search-results');
    if (!searchResults) {
        searchResults = document.createElement('div');
        searchResults.className = 'search-results';
        searchResults.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 2px solid #007bff;
            border-top: none;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            max-height: 400px;
            overflow-y: auto;
            display: none;
        `;
        
        // Insertar después del contenedor de búsqueda
        const searchContainer = searchInput.closest('.search-container');
        if (searchContainer) {
            searchContainer.style.position = 'relative';
            searchContainer.appendChild(searchResults);
            console.log('✅ Contenedor de resultados agregado');
        }
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
        searchResults.innerHTML = '<div style="padding: 20px; text-align: center; color: #007bff; font-weight: 500;">Buscando...</div>';
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
                searchResults.innerHTML = '<div style="padding: 20px; text-align: center; color: #dc3545; font-weight: 500;">Error en la búsqueda</div>';
            }
        })
        .catch(error => {
            console.error('❌ Error de red:', error);
            searchResults.innerHTML = '<div style="padding: 20px; text-align: center; color: #dc3545; font-weight: 500;">Error de conexión</div>';
        });
    }
    
    // Función para mostrar resultados
    function displaySearchResults(results, query) {
        console.log('📋 Mostrando resultados:', results.length);
        
        if (results.length === 0) {
            searchResults.innerHTML = `
                <div style="padding: 20px; text-align: center; color: #6c757d;">
                    <p>No se encontraron productos para "${query}"</p>
                    <a href="/shop/" style="color: #007bff; text-decoration: none; font-weight: 600;">Ver todos los productos</a>
                </div>
            `;
        } else {
            let html = '<div style="padding: 0; margin: 0;">';
            
            results.forEach(product => {
                const imageUrl = product.image || '/static/images/default.jpg';
                html += `
                    <div class="search-result-item" onclick="window.location.href='/shop/?search=${encodeURIComponent(query)}'" style="display: flex; padding: 12px; border-bottom: 1px solid #e9ecef; cursor: pointer; transition: background-color 0.2s;">
                        <div style="width: 50px; height: 50px; margin-right: 12px; flex-shrink: 0;">
                            <img src="${imageUrl}" alt="${product.name}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 4px; border: 1px solid #dee2e6;" onerror="this.src='/static/images/default.jpg'">
                        </div>
                        <div style="flex: 1; min-width: 0;">
                            <h4 style="margin: 0 0 4px 0; font-size: 14px; font-weight: 600; color: #2c3e50; line-height: 1.2;">${product.name}</h4>
                            <p style="margin: 2px 0; font-size: 11px; color: #6c757d; font-weight: 500;">SKU: ${product.sku}</p>
                            ${product.category ? `<p style="margin: 2px 0; font-size: 11px; color: #007bff; font-weight: 500;">${product.category}</p>` : ''}
                            <p style="margin: 4px 0 0 0; font-size: 14px; font-weight: 700; color: #28a745;">$${product.price.toFixed(2)}</p>
                        </div>
                    </div>
                `;
            });
            
            if (results.length >= 10) {
                html += `
                    <div style="padding: 12px; text-align: center; background-color: #f8f9fa; border-top: 1px solid #e9ecef;">
                        <a href="/shop/?search=${encodeURIComponent(query)}" style="color: #007bff; text-decoration: none; font-weight: 600; font-size: 13px;">
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
    
    console.log('✅ Buscador global inicializado correctamente');
});
