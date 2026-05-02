# Matriz de Evaluación de Calidad del Software - ISO/IEC 9126
## Proyecto: WILLARD - Sistema de E-commerce para Ferretería

---

## Metodología de Evaluación

**Escala de Calificación:**
- **Excelente (5)**: Cumple completamente el criterio, supera las expectativas
- **Muy Bueno (4)**: Cumple bien el criterio con mejoras menores posibles
- **Bueno (3)**: Cumple el criterio de manera aceptable
- **Regular (2)**: Cumple parcialmente, requiere mejoras significativas
- **Deficiente (1)**: No cumple el criterio o está ausente

**Peso de Características:**
- Funcionalidad: 25%
- Confiabilidad: 20%
- Usabilidad: 15%
- Eficiencia: 15%
- Mantenibilidad: 15%
- Portabilidad: 10%

---

## 1. FUNCIONALIDAD (Weight: 25%)

### 1.1 Adecuación (Suitability)
**Puntuación: 4/5**

**Justificación:**
- ✅ El sistema cumple con los requisitos funcionales principales (registro, login, carrito)
- ✅ Formularios adecuados para registro de usuarios con validación
- ✅ Sistema de carrito funcional con gestión de items
- ⚠️ Validación de datos básica pero podría ser más robusta
- ⚠️ Falta integración de algunos módulos secundarios

**Evidencia:**
- Formularios de registro con validación de contraseñas
- Sistema de autenticación completo
- Carrito con operaciones CRUD completas

---

### 1.2 Precisión (Accuracy)
**Puntuación: 3/5**

**Justificación:**
- ✅ Cálculos de precios del carrito son precisos
- ✅ Validación de stock antes de agregar productos
- ⚠️ No se observa validación exhaustiva de todos los campos
- ⚠️ Manejo de errores presente pero podría ser más detallado

**Evidencia:**
```python
# Cálculo preciso del total del carrito
@property
def total_precio(self):
    total = 0
    for item in self.items.all():
        total += item.cantidad * item.precio_unitario
    return total
```

---

### 1.3 Interoperabilidad (Interoperability)
**Puntuación: 3/5**

**Justificación:**
- ✅ Integración con Mercado Pago para pagos
- ✅ Uso de API estándar de Django
- ⚠️ Dependencia de servicios externos sin fallback claro
- ⚠️ Limitada interoperabilidad con otros sistemas

**Evidencia:**
- Integración con SDK de Mercado Pago
- Uso de estándares web (HTTP, JSON)
- Framework Django que facilita interoperabilidad

---

### 1.4 Seguridad (Security)
**Puntuación: 3/5**

**Justificación:**
- ✅ Protección CSRF habilitada en middleware
- ✅ Autenticación requerida para operaciones sensibles (@login_required)
- ✅ Validación de propiedad de recursos (usuario solo accede a su carrito)
- ❌ **CRÍTICO**: SECRET_KEY expuesta en código (DEBUG=True en producción)
- ⚠️ Falta validación de entrada más estricta en algunos endpoints
- ⚠️ No se observa protección contra SQL injection (aunque Django ORM lo previene)
- ⚠️ No hay rate limiting visible

**Evidencia:**
```python
# settings.py - PROBLEMA DE SEGURIDAD
SECRET_KEY = 'django-insecure-s6b3weaat)%8w()#*yid-0+u75gs-5xwyi=yqpi)n6=k=y6bcy'
DEBUG = True
```

**Mejoras necesarias:**
- Mover SECRET_KEY a variables de entorno
- Configurar DEBUG=False para producción
- Implementar rate limiting
- Agregar validación más estricta de entrada

---

### 1.5 Cumplimiento de Funcionalidad (Functionality Compliance)
**Puntuación: 3/5**

**Justificación:**
- ✅ Cumple con estándares básicos de aplicaciones web
- ⚠️ No se observa cumplimiento explícito de estándares específicos (WCAG, GDPR)
- ⚠️ Falta documentación de cumplimiento normativo

---

### **PUNTUACIÓN TOTAL FUNCIONALIDAD: 3.2/5 (64%)**

---

## 2. CONFIABILIDAD (Weight: 20%)

### 2.1 Madurez (Maturity)
**Puntuación: 2/5**

**Justificación:**
- ⚠️ Sistema en desarrollo, no se observan pruebas unitarias implementadas
- ⚠️ Archivos tests.py vacíos
- ⚠️ No hay evidencia de pruebas de integración
- ⚠️ Falta de documentación de bugs conocidos

**Evidencia:**
```python
# account/tests.py, cart/tests.py - VACÍOS
from django.test import TestCase
# Create your tests here.
```

---

### 2.2 Tolerancia a Fallos (Fault Tolerance)
**Puntuación: 3/5**

**Justificación:**
- ✅ Manejo de excepciones presente en operaciones críticas
- ✅ Validación de existencia de objetos antes de operar (get_object_or_404)
- ✅ Validación de autenticación antes de operaciones sensibles
- ⚠️ No hay manejo de errores para servicios externos (Mercado Pago)
- ⚠️ Falta recuperación automática de errores

**Evidencia:**
```python
# Manejo de excepciones en cart/views.py
try:
    producto = get_object_or_404(Producto, id=product_id, disponible=True)
    # ... código ...
except Producto.DoesNotExist:
    error_message = "Producto no encontrado o no disponible."
    messages.error(request, error_message)
except Exception as e:
    error_message = f"Error al agregar el producto: {str(e)}"
    messages.error(request, error_message)
```

---

### 2.3 Recuperabilidad (Recoverability)
**Puntuación: 2/5**

**Justificación:**
- ⚠️ No se observa sistema de backup automático
- ⚠️ No hay registro de transacciones para recuperación
- ⚠️ Falta mecanismo de rollback para operaciones críticas
- ✅ Mensajes de error informativos que ayudan al usuario
- ⚠️ No hay sistema de logs estructurado más allá de logging básico

**Evidencia:**
```python
# Logging básico presente
logger = logging.getLogger(__name__)
logger.info(f"MP Return - Full Path: {full_path}...")
logger.error(f"Error al consultar estado del pago en MP: {str(e)}")
```

---

### 2.4 Cumplimiento de Confiabilidad (Reliability Compliance)
**Puntuación: 2/5**

**Justificación:**
- ⚠️ Falta cumplimiento de estándares de disponibilidad (SLA)
- ⚠️ No hay documentación de políticas de recuperación
- ⚠️ Falta pruebas de estrés o carga

---

### **PUNTUACIÓN TOTAL CONFIABILIDAD: 2.25/5 (45%)**

---

## 3. USABILIDAD (Weight: 15%)

### 3.1 Comprensibilidad (Understandability)
**Puntuación: 4/5**

**Justificación:**
- ✅ Código bien estructurado con nombres descriptivos
- ✅ Docstrings en funciones principales
- ✅ Mensajes de usuario claros y en español
- ⚠️ Falta documentación técnica más extensa
- ✅ Nomenclatura consistente

**Evidencia:**
```python
def add_to_cart(request, product_id):
    """Agregar un producto al carrito"""
    # Código descriptivo y bien comentado
```

---

### 3.2 Aprendizaje (Learnability)
**Puntuación: 4/5**

**Justificación:**
- ✅ Interfaz intuitiva para registro y login
- ✅ Flujo de compra lógico y predecible
- ✅ Mensajes de error que guían al usuario
- ✅ Formularios con placeholders informativos
- ⚠️ Falta tutorial o ayuda contextual

**Evidencia:**
```python
# Placeholders informativos en formularios
'calle': forms.TextInput(attrs={
    'placeholder': 'Nombre de la calle'
})
```

---

### 3.3 Operabilidad (Operability)
**Puntuación: 4/5**

**Justificación:**
- ✅ Operaciones comunes son rápidas y directas
- ✅ Validación inmediata de formularios
- ✅ Soporte para peticiones AJAX para mejor UX
- ✅ Redirecciones apropiadas después de acciones
- ⚠️ Podría beneficiarse de más feedback visual

**Evidencia:**
```python
# Soporte AJAX
if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    return JsonResponse({
        'success': True,
        'message': success_message,
        'cart_count': carrito.total_items
    })
```

---

### 3.4 Atractividad (Attractiveness)
**Puntuación: 3/5**

**Justificación:**
- ✅ Interfaz básica funcional
- ⚠️ No se puede evaluar completamente sin ver el frontend
- ⚠️ Depende de la implementación de CSS/JS

---

### 3.5 Cumplimiento de Usabilidad (Usability Compliance)
**Puntuación: 3/5**

**Justificación:**
- ⚠️ No se observa cumplimiento explícito de WCAG
- ✅ Idioma consistente (español)
- ⚠️ Falta validación de accesibilidad

---

### **PUNTUACIÓN TOTAL USABILIDAD: 3.6/5 (72%)**

---

## 4. EFICIENCIA (Weight: 15%)

### 4.1 Comportamiento Temporal (Time Behavior)
**Puntuación: 3/5**

**Justificación:**
- ✅ Uso de índices en modelos (presumiblemente por Django ORM)
- ⚠️ Consultas a base de datos podrían optimizarse (N+1 queries potenciales)
- ⚠️ No hay evidencia de caching implementado
- ✅ Operaciones de carrito son rápidas
- ⚠️ Integración con API externa (Mercado Pago) puede causar latencia

**Evidencia:**
```python
# Potencial problema N+1
for item in orden.items.all():  # Podría optimizarse con select_related
    items_mp.append({...})
```

**Mejoras sugeridas:**
- Implementar select_related/prefetch_related para optimizar queries
- Agregar caching para datos frecuentemente accedidos
- Implementar paginación para listas largas

---

### 4.2 Utilización de Recursos (Resource Utilization)
**Puntuación: 3/5**

**Justificación:**
- ✅ Uso eficiente del ORM de Django
- ⚠️ SQLite en desarrollo (limitado para producción)
- ⚠️ No se observa optimización de consultas complejas
- ✅ Uso adecuado de sesiones
- ⚠️ Falta configuración de recursos para producción

**Evidencia:**
```python
# Base de datos SQLite (no escalable para producción)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

### 4.3 Cumplimiento de Eficiencia (Efficiency Compliance)
**Puntuación: 3/5**

**Justificación:**
- ⚠️ No hay métricas de rendimiento definidas
- ⚠️ Falta documentación de requisitos de rendimiento
- ✅ Cumple con estándares básicos de aplicaciones web

---

### **PUNTUACIÓN TOTAL EFICIENCIA: 3.0/5 (60%)**

---

## 5. MANTENIBILIDAD (Weight: 15%)

### 5.1 Analizabilidad (Analyzability)
**Puntuación: 4/5**

**Justificación:**
- ✅ Código bien organizado en apps de Django
- ✅ Estructura de proyecto clara y estándar
- ✅ Logging implementado en partes críticas
- ✅ Mensajes de error descriptivos
- ⚠️ Falta documentación técnica más extensa
- ⚠️ No hay diagramas de arquitectura

**Evidencia:**
```python
# Estructura modular clara
account/
cart/
checkout/
ferretetia/
# Cada app con responsabilidad clara
```

---

### 5.2 Modificabilidad (Changeability)
**Puntuación: 4/5**

**Justificación:**
- ✅ Código modular bien separado en apps
- ✅ Uso de decoradores para funcionalidad común
- ✅ Separación de concerns (modelos, vistas, formularios)
- ✅ Uso de contexto processors para datos globales
- ⚠️ Algunas vistas podrían ser más pequeñas
- ✅ Fácil extensión mediante herencia de Django

**Evidencia:**
```python
# Uso de decoradores reutilizables
@login_required
@require_POST
def add_to_cart(request, product_id):
    # Funcionalidad encapsulada
```

---

### 5.3 Estabilidad (Stability)
**Puntuación: 3/5**

**Justificación:**
- ✅ Uso de framework estable (Django 5.2)
- ✅ Migraciones de base de datos implementadas
- ⚠️ Falta de pruebas hace difícil evaluar estabilidad
- ⚠️ Cambios podrían romper funcionalidad sin detección temprana
- ✅ Manejo de versiones de dependencias

**Evidencia:**
```python
# Migraciones presentes
migrations/
  - 0001_initial.py
  - 0002_auto_20250806_1051.py
  # Sistema de versionado de esquema
```

---

### 5.4 Capacidad de Prueba (Testability)
**Puntuación: 2/5**

**Justificación:**
- ❌ **CRÍTICO**: No hay pruebas implementadas
- ⚠️ Archivos tests.py están vacíos
- ✅ Código es testeable (separación de concerns)
- ⚠️ Falta cobertura de código
- ⚠️ No hay pruebas de integración
- ⚠️ No hay pruebas de sistema

**Evidencia:**
```python
# Todos los archivos tests.py están vacíos
from django.test import TestCase
# Create your tests here.
```

---

### 5.5 Cumplimiento de Mantenibilidad (Maintainability Compliance)
**Puntuación: 3/5**

**Justificación:**
- ⚠️ Falta documentación técnica completa
- ✅ Código sigue convenciones de Django
- ⚠️ No hay guías de contribución o desarrollo

---

### **PUNTUACIÓN TOTAL MANTENIBILIDAD: 3.2/5 (64%)**

---

## 6. PORTABILIDAD (Weight: 10%)

### 6.1 Adaptabilidad (Adaptability)
**Puntuación: 4/5**

**Justificación:**
- ✅ Framework Django es multiplataforma
- ✅ Configuración mediante settings.py permite adaptación
- ✅ Uso de variables de entorno para configuración
- ⚠️ Algunas configuraciones hardcodeadas
- ✅ Base de datos abstraída por ORM

**Evidencia:**
```python
# Uso de variables de entorno
MP_ACCESS_TOKEN = os.environ.get('MP_ACCESS_TOKEN', ...)
# Permite configuración por ambiente
```

---

### 6.2 Instalabilidad (Installability)
**Puntuación: 4/5**

**Justificación:**
- ✅ Requirements.txt presente para dependencias
- ✅ Instrucciones estándar de Django
- ✅ Migraciones automatizadas
- ⚠️ Falta documentación de instalación específica
- ✅ Proceso de instalación estándar

**Evidencia:**
```
requirements.txt presente
Sistema de migraciones
```

---

### 6.3 Conformidad (Conformance)
**Puntuación: 4/5**

**Justificación:**
- ✅ Cumple con estándares de Django
- ✅ Sigue convenciones de Python (PEP 8 presumiblemente)
- ✅ Estructura estándar de proyecto Django
- ⚠️ No hay validación explícita de conformidad

---

### 6.4 Reemplazabilidad (Replaceability)
**Puntuación: 3/5**

**Justificación:**
- ✅ Componentes modulares
- ⚠️ Dependencia fuerte de Django (no es fácilmente reemplazable)
- ✅ Separación de apps permite reemplazo parcial
- ⚠️ Integración con servicios externos específicos (Mercado Pago)

---

### 6.5 Cumplimiento de Portabilidad (Portability Compliance)
**Puntuación: 3/5**

**Justificación:**
- ✅ Cumple con estándares de aplicaciones web
- ⚠️ Falta documentación de requisitos de portabilidad
- ✅ Compatible con múltiples plataformas (Windows, Linux, Mac)

---

### **PUNTUACIÓN TOTAL PORTABILIDAD: 3.6/5 (72%)**

---

## RESUMEN GENERAL

### Puntuaciones por Característica

| Característica | Puntuación | Porcentaje | Peso | Ponderado |
|----------------|------------|------------|------|-----------|
| **Funcionalidad** | 3.2/5 | 64% | 25% | 0.80 |
| **Confiabilidad** | 2.25/5 | 45% | 20% | 0.45 |
| **Usabilidad** | 3.6/5 | 72% | 15% | 0.54 |
| **Eficiencia** | 3.0/5 | 60% | 15% | 0.45 |
| **Mantenibilidad** | 3.2/5 | 64% | 15% | 0.48 |
| **Portabilidad** | 3.6/5 | 72% | 10% | 0.36 |

### **PUNTUACIÓN FINAL PONDERADA: 3.08/5 (61.6%)**

---

## ANÁLISIS DETALLADO

### Fortalezas Principales
1. ✅ **Arquitectura sólida**: Uso correcto de Django y separación modular
2. ✅ **Funcionalidad básica completa**: Login, registro y carrito funcionan
3. ✅ **Código legible**: Bien estructurado y comentado
4. ✅ **Seguridad básica**: Protección CSRF y autenticación
5. ✅ **Usabilidad**: Interfaz intuitiva y mensajes claros

### Áreas Críticas de Mejora

#### 🔴 **CRÍTICO - PRIORIDAD ALTA**
1. **Seguridad**
   - Mover SECRET_KEY a variables de entorno
   - Configurar DEBUG=False para producción
   - Implementar rate limiting

2. **Testing**
   - Implementar pruebas unitarias
   - Agregar pruebas de integración
   - Establecer cobertura de código mínima (70%+)

3. **Confiabilidad**
   - Implementar sistema de backup
   - Mejorar manejo de errores en servicios externos
   - Agregar logs estructurados

#### 🟡 **IMPORTANTE - PRIORIDAD MEDIA**
4. **Eficiencia**
   - Optimizar consultas a base de datos (select_related/prefetch_related)
   - Implementar caching
   - Considerar migración a PostgreSQL para producción

5. **Documentación**
   - Documentación técnica completa
   - Guías de instalación y despliegue
   - Documentación de API

6. **Mantenibilidad**
   - Refactorizar vistas muy largas
   - Mejorar manejo de excepciones
   - Establecer estándares de código

---

## RECOMENDACIONES PRIORITARIAS

### Corto Plazo (1-2 semanas)
1. Implementar pruebas unitarias básicas para módulos críticos (login, carrito)
2. Mover configuraciones sensibles a variables de entorno
3. Agregar validación más estricta de entrada
4. Implementar logging estructurado

### Mediano Plazo (1-2 meses)
1. Completar suite de pruebas (unidad, integración, sistema)
2. Optimizar consultas a base de datos
3. Implementar caching
4. Documentación técnica completa
5. Configurar ambiente de producción adecuado

### Largo Plazo (3+ meses)
1. Implementar CI/CD
2. Monitoreo y métricas de rendimiento
3. Mejoras de escalabilidad
4. Auditoría de seguridad completa
5. Cumplimiento de estándares (WCAG, GDPR si aplica)

---

## CONCLUSIÓN

El proyecto **WILLARD** muestra una **base sólida** con una arquitectura bien estructurada y funcionalidad core implementada. Sin embargo, presenta **deficiencias críticas** en aspectos de seguridad, testing y confiabilidad que deben abordarse antes de considerar el sistema listo para producción.

**Calificación General: 3.08/5 (61.6%) - APROBADO CON RESERVAS**

**Recomendación**: El sistema requiere mejoras significativas, especialmente en seguridad y testing, antes de ser desplegado en un ambiente de producción real.

---

**Fecha de Evaluación**: [Fecha actual]  
**Evaluador**: Análisis basado en ISO/IEC 9126  
**Versión del Software Evaluado**: Django 5.2.1


