# Introducción del Proyecto - WILLARD

## Sistema de E-commerce para Ferretería

### Módulos Principales Presentados

---

## 🔐 1. Sistema de Autenticación

### **Registro de Usuarios**
- **Formulario dual**: Registro de usuario (Django User) + Perfil de usuario personalizado
- **Validación de datos**: Verificación de contraseñas y campos requeridos
- **Creación automática**: Al registrarse, se crea automáticamente:
  - Usuario en el sistema Django
  - Perfil de usuario con información personal (nombre, apellido, teléfono, email)
- **Inicio de sesión automático**: Tras el registro exitoso, el usuario queda autenticado
- **Redirección**: Los usuarios nuevos son dirigidos a su página de cuenta

### **Inicio de Sesión (Login)**
- **Autenticación segura**: Utiliza el sistema de autenticación nativo de Django
- **Validación de credenciales**: Verificación de usuario y contraseña
- **Mensajes de error**: Notificaciones claras cuando las credenciales son incorrectas
- **Redirección inteligente**: Después del login, redirige a la página de cuenta del usuario

### **Características Adicionales**
- **Gestión de sesiones**: Control de sesiones activas e inactivas
- **Protección de rutas**: Sistema de decoradores para proteger vistas que requieren autenticación
- **Cierre de sesión**: Función de logout que cierra la sesión y redirige al inicio

---

## 🛒 2. Sistema de Carrito de Compras

### **Funcionalidades Principales**

#### **Agregar Productos**
- **Verificación de autenticación**: Solo usuarios logueados pueden agregar productos
- **Control de stock**: Validación de disponibilidad antes de agregar
- **Gestión de cantidades**: Si el producto ya está en el carrito, aumenta la cantidad automáticamente
- **Precios inteligentes**: Detecta automáticamente si el producto tiene descuento y aplica el precio correspondiente
- **Actualización en tiempo real**: Soporte para peticiones AJAX para actualización sin recargar la página
- **Mensajes informativos**: Notificaciones claras sobre el estado de cada operación

#### **Visualización del Carrito**
- **Vista completa**: Muestra todos los productos agregados con sus detalles
- **Cálculo automático**: Total de items y precio total calculados automáticamente
- **Información detallada**: Cada item muestra:
  - Nombre del producto
  - Cantidad
  - Precio unitario
  - Precio total por item
  - Stock disponible

#### **Gestión de Items**
- **Modificar cantidades**: Permite aumentar o disminuir la cantidad de cada producto
- **Validación de stock**: No permite exceder el stock disponible
- **Eliminar productos**: Opción para remover items individuales del carrito
- **Limpiar carrito**: Función para vaciar completamente el carrito de compras

#### **Actualización de Precios**
- **Actualización automática**: Los precios se actualizan automáticamente si el producto cambia de precio o descuento
- **Cálculo dinámico**: El total del carrito se recalcula en tiempo real

### **Modelo de Datos**
- **Carrito**: Asociado a un usuario, mantiene estado activo/inactivo
- **ItemCarrito**: Relación entre carrito y producto, almacena:
  - Cantidad
  - Precio unitario (guardado al momento de agregar, preserva el precio histórico)
  - Fechas de creación y actualización

---

## 🔄 3. Integración entre Módulos

### **Flujo de Usuario**

1. **Registro/Login**
   - Usuario se registra o inicia sesión
   - Sistema valida credenciales
   - Usuario autenticado accede a la plataforma

2. **Navegación y Compra**
   - Usuario navega por productos
   - Agrega productos al carrito (requiere autenticación)
   - El carrito persiste durante toda la sesión

3. **Gestión del Carrito**
   - Usuario visualiza su carrito en `/cart/`
   - Modifica cantidades o elimina productos
   - Sistema valida stock en cada operación

4. **Proceso de Compra**
   - Cuando el usuario finaliza compra, el carrito se utiliza en el checkout
   - Después del pago exitoso, el carrito se limpia automáticamente

### **Seguridad**
- **Autenticación requerida**: Todas las operaciones del carrito requieren usuario autenticado
- **Validación de propiedad**: Los usuarios solo pueden acceder a su propio carrito
- **Protección CSRF**: Todas las operaciones están protegidas contra ataques CSRF

---

## 📊 Resumen Técnico

### **Tecnologías Utilizadas**
- **Framework**: Django 5.2
- **Autenticación**: Sistema nativo de Django (django.contrib.auth)
- **Base de datos**: ORM de Django con modelos relacionados
- **Interfaz**: Templates HTML con sistema de mensajes de Django

### **Modelos Principales**
- `User`: Modelo de usuario de Django (ampliado con PerfilUsuario)
- `PerfilUsuario`: Información adicional del usuario
- `Carrito`: Contenedor de compras del usuario
- `ItemCarrito`: Productos individuales dentro del carrito

### **Vistas Clave**
- `register_view`: Proceso de registro de nuevos usuarios
- `login_view`: Autenticación de usuarios existentes
- `cart_view`: Visualización del carrito
- `add_to_cart`: Agregar productos al carrito
- `update_cart`: Modificar cantidades en el carrito
- `remove_from_cart`: Eliminar productos del carrito

---

## ✅ Beneficios del Sistema

1. **Experiencia de Usuario Fluida**
   - Proceso de registro simple y rápido
   - Carrito intuitivo y fácil de usar
   - Mensajes claros en cada acción

2. **Seguridad**
   - Autenticación robusta
   - Protección de datos de usuario
   - Validación en cada operación

3. **Funcionalidad Completa**
   - Gestión completa del ciclo de compra
   - Control de stock en tiempo real
   - Manejo de precios y descuentos

4. **Escalabilidad**
   - Código modular y bien estructurado
   - Fácil mantenimiento y expansión
   - Preparado para futuras funcionalidades

---

**Proyecto desarrollado con Django para la tienda en línea WILLARD**


