# WILLARD - Ferretería Online

Una moderna aplicación web de ferretería desarrollada con Django, con un diseño profesional y funcionalidades completas de e-commerce.

## 🚀 Características

- **Diseño Moderno**: Interfaz limpia inspirada en WILLARD con logo amarillo distintivo
- **Búsqueda en Tiempo Real**: Sistema de búsqueda funcional con resultados instantáneos
- **Carrito de Compras**: Funcionalidad completa de carrito persistente con localStorage
- **Navegación Intuitiva**: Menú superior e inferior con todas las secciones principales
- **Responsive Design**: Adaptable a dispositivos móviles y de escritorio
- **Gestión de Usuarios**: Secciones de cuenta, wishlist y comparación de productos

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.1
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Base de Datos**: SQLite (por defecto)
- **Estilos**: CSS custom con variables y diseño moderno

## 📁 Estructura del Proyecto

```
mysite/
├── mysite/                 # Configuración principal de Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── ferretetia/            # Aplicación principal
│   ├── templates/         # Plantillas HTML
│   ├── static/           # Archivos estáticos (CSS, JS)
│   ├── views.py          # Vistas del negocio
│   ├── urls.py           # URLs de la aplicación
│   └── ...
├── requirements.txt       # Dependencias del proyecto
└── README.md
```

## 🎯 Funcionalidades

### Navegación Superior
- **WISHLIST**: Lista de productos favoritos
- **COMPARE**: Comparación de productos
- **MY ACCOUNT**: Gestión de cuenta de usuario
- **CHECKOUT**: Proceso de finalización de compra
- **CART**: Carrito de compras funcional

### Navegación Inferior
- **POWER TOOLS**: Herramientas eléctricas
- **BLOG**: Artículos y guías
- **SHOP**: Categorías de productos
- **PAGES**: Páginas adicionales
- **ELEMENTS**: Elementos de diseño

### Características Técnicas
- Sistema de búsqueda con API REST
- Carrito persistente con localStorage
- Notificaciones en tiempo real
- Contador dinámico de productos
- Gestión completa de productos en el carrito

## 🚀 Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/willard-ferreteria.git
   cd willard-ferreteria
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Realizar migraciones**:
   ```bash
   python manage.py migrate
   ```

6. **Ejecutar el servidor**:
   ```bash
   python manage.py runserver
   ```

7. **Visitar la aplicación**:
   Abre tu navegador en `http://127.0.0.1:8000/ferreteria/`

## 📱 URLs Disponibles

| URL | Descripción |
|-----|-------------|
| `/` | Página principal |
| `/wishlist/` | Lista de deseos |
| `/compare/` | Comparar productos |
| `/account/` | Mi cuenta |
| `/checkout/` | Finalizar compra |
| `/cart/` | Carrito de compras |
| `/power-tools/` | Herramientas eléctricas |
| `/blog/` | Blog |
| `/shop/` | Tienda |
| `/pages/` | Páginas adicionales |
| `/elements/` | Elementos de diseño |
| `/api/search/` | API de búsqueda |

## 🎨 Diseño

El diseño está inspirado en una ferretería moderna con:
- **Colores**: Amarillo primario (#FDD835), negro, blanco y grises
- **Tipografía**: Sans-serif moderna y legible
- **Layout**: Grid responsive y flexbox
- **Iconos**: Emojis y símbolos Unicode
- **Efectos**: Hover, transiciones suaves y sombras

## 🔧 Desarrollo

### Estructura de Archivos Estáticos
- `ferretetia/static/ferretetia/CSS/styles.css` - Estilos principales
- `ferretetia/static/ferretetia/script.js` - JavaScript funcional

### Vistas Principales
- `index` - Página principal con productos destacados
- Vistas individuales para cada sección de navegación
- API REST para búsqueda de productos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## 👨‍💻 Autor

Desarrollado con ❤️ para crear una experiencia de ferretería online moderna y funcional.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

⭐ Si te gusta este proyecto, ¡dale una estrella!
