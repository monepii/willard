// Configuración para Google Places API
// IMPORTANTE: Reemplaza 'YOUR_API_KEY' con tu clave real de Google Places API

const GOOGLE_PLACES_CONFIG = {
    // Reemplaza esta clave con tu API key real de Google Places
    API_KEY: 'AIzaSyBbGLLKAQssx1lApjJMAiFQInmIpcSSedU',
    
    // Configuración del autocompletado
    AUTOCOMPLETE_OPTIONS: {
        types: ['address'],
        componentRestrictions: { country: 'mx' }, // Restringir a México
        fields: ['address_components', 'formatted_address', 'geometry']
    },
    
    // Configuración de la región
    REGION: 'MX',
    
    // Idioma
    LANGUAGE: 'es'
};

// Función para obtener la URL de la API con la clave configurada
function getGooglePlacesAPIUrl() {
    return `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_PLACES_CONFIG.API_KEY}&libraries=places&callback=initAutocomplete&region=${GOOGLE_PLACES_CONFIG.REGION}&language=${GOOGLE_PLACES_CONFIG.LANGUAGE}`;
}

// Función para verificar si la API key está configurada
function isAPIKeyConfigured() {
    return GOOGLE_PLACES_CONFIG.API_KEY !== 'YOUR_API_KEY' && GOOGLE_PLACES_CONFIG.API_KEY.length > 0;
}

// Función para mostrar advertencia si la API key no está configurada
function showAPIKeyWarning() {
    if (!isAPIKeyConfigured()) {
        console.warn('⚠️ Google Places API Key no configurada. Por favor, configura tu API key en google-places-config.js');
        
        // Mostrar mensaje en la página
        const warningDiv = document.createElement('div');
        warningDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            z-index: 9999;
            max-width: 300px;
            font-size: 14px;
        `;
        warningDiv.innerHTML = `
            <strong>⚠️ Configuración requerida</strong><br>
            Para usar el autocompletado de direcciones, configura tu API key de Google Places en el archivo google-places-config.js
        `;
        document.body.appendChild(warningDiv);
        
        // Remover el mensaje después de 10 segundos
        setTimeout(() => {
            if (warningDiv.parentNode) {
                warningDiv.parentNode.removeChild(warningDiv);
            }
        }, 10000);
    }
}

// Verificar configuración cuando se carga el script
document.addEventListener('DOMContentLoaded', function() {
    showAPIKeyWarning();
});
