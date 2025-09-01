# Configuración de Google Places API para Autocompletado de Direcciones

## 📋 Pasos para configurar Google Places API

### 1. Obtener una API Key de Google

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la **Places API**:
   - Ve a "APIs & Services" > "Library"
   - Busca "Places API"
   - Haz clic en "Enable"

### 2. Crear una API Key

1. Ve a "APIs & Services" > "Credentials"
2. Haz clic en "Create Credentials" > "API Key"
3. Copia tu API Key

### 3. Configurar restricciones de seguridad (Recomendado)

1. Haz clic en tu API Key para editarla
2. En "Application restrictions", selecciona "HTTP referrers"
3. Agrega tu dominio (ej: `localhost:8000/*`, `tudominio.com/*`)
4. En "API restrictions", selecciona "Restrict key"
5. Selecciona solo "Places API"

### 4. Configurar en el proyecto

1. Abre el archivo `account/static/account/JS/google-places-config.js`
2. Reemplaza `YOUR_API_KEY` con tu API key real:

```javascript
const GOOGLE_PLACES_CONFIG = {
    API_KEY: 'TU_API_KEY_AQUI', // ← Reemplaza esto
    // ... resto de la configuración
};
```

### 5. Actualizar los templates

En los archivos de template, reemplaza `YOUR_API_KEY` con tu API key:

- `ferretetia/templates/ferretetia/main.html`
- `account/templates/account/agregar_direccion.html`
- `account/templates/account/editar_direccion.html`

Busca esta línea:
```html
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initAutocomplete" async defer></script>
```

Y reemplázala con:
```html
<script src="https://maps.googleapis.com/maps/api/js?key=TU_API_KEY_AQUI&libraries=places&callback=initAutocomplete" async defer></script>
```

## 🚀 Funcionalidades implementadas

### ✅ Autocompletado automático
- Escribe una dirección en el campo "Calle"
- Selecciona una opción del dropdown de Google
- Los campos se llenan automáticamente

### ✅ Campos que se autocompletan
- **Calle**: Nombre de la calle
- **Número exterior**: Número de la dirección
- **Colonia**: Colonia/barrio
- **Municipio**: Ciudad/municipio
- **Estado**: Estado
- **Código postal**: Código postal
- **País**: País (por defecto México)

### ✅ Botones de ayuda
- **Limpiar Dirección**: Limpia todos los campos
- **Validar Dirección**: Verifica que todos los campos estén llenos

### ✅ Mensajes informativos
- Mensaje de éxito cuando se autocompleta
- Mensaje de error si faltan campos
- Advertencia si la API key no está configurada

## 💰 Costos de Google Places API

- **Autocomplete (per session)**: $2.83 por 1000 sesiones
- **Place Details**: $17 por 1000 requests
- **Geocoding**: $5 por 1000 requests

### 💡 Consejos para reducir costos

1. **Configura restricciones** en tu API key
2. **Usa caché** para direcciones repetidas
3. **Implementa debounce** para evitar requests excesivos
4. **Monitorea el uso** en Google Cloud Console

## 🔧 Personalización

### Cambiar país de búsqueda
En `google-places-config.js`:
```javascript
componentRestrictions: { country: 'us' }, // Para Estados Unidos
componentRestrictions: { country: 'mx' }, // Para México
```

### Cambiar idioma
```javascript
LANGUAGE: 'en', // Inglés
LANGUAGE: 'es', // Español
```

### Cambiar tipos de lugares
```javascript
types: ['establishment'], // Solo establecimientos
types: ['geocode'], // Solo direcciones geográficas
types: ['address'], // Solo direcciones (recomendado)
```

## 🐛 Solución de problemas

### Error: "This API project is not authorized to use this API"
- Verifica que Places API esté habilitada
- Revisa las restricciones de tu API key

### Error: "RefererNotAllowedMapError"
- Agrega tu dominio a las restricciones HTTP referrers
- Para desarrollo local, agrega `localhost:8000/*`

### El autocompletado no aparece
- Verifica que la API key esté correctamente configurada
- Revisa la consola del navegador para errores
- Asegúrate de que el script se esté cargando

### Los campos no se llenan automáticamente
- Verifica que los IDs de los campos coincidan con el JavaScript
- Revisa que el callback `initAutocomplete` esté definido

## 📞 Soporte

Si tienes problemas con la implementación:
1. Revisa la consola del navegador para errores
2. Verifica que todos los archivos estén en su lugar
3. Confirma que la API key esté correctamente configurada
4. Consulta la [documentación oficial de Google Places API](https://developers.google.com/maps/documentation/places/web-service)
