// Google Places Autocomplete para direcciones
let autocomplete;
let place;

function initAutocomplete() {
    // Verificar si la API key está configurada
    if (typeof GOOGLE_PLACES_CONFIG !== 'undefined' && (!GOOGLE_PLACES_CONFIG.API_KEY || GOOGLE_PLACES_CONFIG.API_KEY === 'YOUR_API_KEY')) {
        console.warn(' Google Places API Key no configurada correctamente');
        return;
    }

    // Buscar el campo de dirección en la página
    const addressInput = document.getElementById('id_calle');
    
    if (addressInput) {
        // Crear el autocompletado con la configuración
        const options = typeof GOOGLE_PLACES_CONFIG !== 'undefined' ? 
            GOOGLE_PLACES_CONFIG.AUTOCOMPLETE_OPTIONS : {
                types: ['address'],
                componentRestrictions: { country: 'mx' },
                fields: ['address_components', 'formatted_address', 'geometry']
            };

        autocomplete = new google.maps.places.Autocomplete(addressInput, options);

        // Escuchar cuando se selecciona una dirección
        autocomplete.addListener('place_changed', fillInAddress);
        
        console.log('Google Places Autocomplete inicializado correctamente');
    }
}

function fillInAddress() {
    // Obtener el lugar seleccionado
    place = autocomplete.getPlace();
    
    if (!place.geometry || !place.geometry.location) {
        console.log("No se encontró información del lugar");
        return;
    }

    // Limpiar campos antes de llenar
    clearAddressFields();

    // Llenar campos con la información del lugar
    fillAddressComponents(place.address_components);
}

function clearAddressFields() {
    // Limpiar todos los campos de dirección
    const fields = [
        'id_numero_exterior',
        'id_numero_interior', 
        'id_colonia',
        'id_municipio',
        'id_estado',
        'id_codigo_postal',
        'id_pais'
    ];
    
    fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.value = '';
        }
    });
}

function fillAddressComponents(components) {
    // Mapear componentes de Google Places a nuestros campos
    const addressData = {
        street_number: '',
        route: '',
        sublocality_level_1: '', // Colonia
        locality: '', // Municipio/Ciudad
        administrative_area_level_1: '', // Estado
        postal_code: '',
        country: ''
    };

    // Extraer información de los componentes
    components.forEach(component => {
        const types = component.types;
        
        if (types.includes('street_number')) {
            addressData.street_number = component.long_name;
        } else if (types.includes('route')) {
            addressData.route = component.long_name;
        } else if (types.includes('sublocality_level_1')) {
            addressData.sublocality_level_1 = component.long_name;
        } else if (types.includes('locality')) {
            addressData.locality = component.long_name;
        } else if (types.includes('administrative_area_level_1')) {
            addressData.administrative_area_level_1 = component.long_name;
        } else if (types.includes('postal_code')) {
            addressData.postal_code = component.long_name;
        } else if (types.includes('country')) {
            addressData.country = component.long_name;
        }
    });

    // Llenar los campos del formulario
    fillFormFields(addressData);
}

function fillFormFields(data) {
    // Llenar calle (ya está lleno por el autocompletado)
    const calleField = document.getElementById('id_calle');
    if (calleField && data.route) {
        calleField.value = data.route;
    }

    // Llenar número exterior
    const numeroExteriorField = document.getElementById('id_numero_exterior');
    if (numeroExteriorField && data.street_number) {
        numeroExteriorField.value = data.street_number;
    }

    // Llenar colonia
    const coloniaField = document.getElementById('id_colonia');
    if (coloniaField && data.sublocality_level_1) {
        coloniaField.value = data.sublocality_level_1;
    }

    // Llenar municipio
    const municipioField = document.getElementById('id_municipio');
    if (municipioField && data.locality) {
        municipioField.value = data.locality;
    }

    // Llenar estado
    const estadoField = document.getElementById('id_estado');
    if (estadoField && data.administrative_area_level_1) {
        estadoField.value = data.administrative_area_level_1;
    }

    // Llenar código postal
    const codigoPostalField = document.getElementById('id_codigo_postal');
    if (codigoPostalField && data.postal_code) {
        codigoPostalField.value = data.postal_code;
    }

    // Llenar país
    const paisField = document.getElementById('id_pais');
    if (paisField && data.country) {
        paisField.value = data.country;
    }

    // Mostrar mensaje de éxito 
}

function showSuccessMessage(message) {
    // Crear o actualizar mensaje de éxito
    let successDiv = document.getElementById('address-success-message');
    
    if (!successDiv) {
        successDiv = document.createElement('div');
        successDiv.id = 'address-success-message';
        successDiv.className = 'address-success-message';
        
        // Insertar después del campo de calle
        const calleField = document.getElementById('id_calle');
        if (calleField && calleField.parentNode) {
            calleField.parentNode.insertAdjacentElement('afterend', successDiv);
        }
    }
    
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    
    // Ocultar mensaje después de 3 segundos
    setTimeout(() => {
        successDiv.style.display = 'none';
    }, 3000);
}

// Función para limpiar campos manualmente
function clearAddressForm() {
    clearAddressFields();
    const calleField = document.getElementById('id_calle');
    if (calleField) {
        calleField.value = '';
    }
    showSuccessMessage('Campos de dirección limpiados');
}

// Función para validar que todos los campos estén llenos
function validateAddressForm() {
    const requiredFields = [
        'id_calle',
        'id_numero_exterior',
        'id_colonia',
        'id_municipio',
        'id_estado',
        'id_codigo_postal'
    ];
    
    let isValid = true;
    const emptyFields = [];
    
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field && !field.value.trim()) {
            isValid = false;
            emptyFields.push(fieldId);
        }
    });
    
    if (!isValid) {
        showErrorMessage('Por favor, complete todos los campos obligatorios de la dirección');
        return false;
    }
    
    return true;
}

function showErrorMessage(message) {
    // Crear o actualizar mensaje de error
    let errorDiv = document.getElementById('address-error-message');
    
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'address-error-message';
        errorDiv.className = 'address-error-message';
        
        // Insertar después del campo de calle
        const calleField = document.getElementById('id_calle');
        if (calleField && calleField.parentNode) {
            calleField.parentNode.insertAdjacentElement('afterend', errorDiv);
        }
    }
    
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Ocultar mensaje después de 5 segundos
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Si Google Maps ya está cargado, inicializar inmediatamente
    if (typeof google !== 'undefined' && google.maps && google.maps.places) {
        initAutocomplete();
    }
});
