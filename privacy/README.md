# Funcionalidad de Aviso de Privacidad

## Descripción

Sistema completo para gestionar avisos de privacidad en formato Markdown con las siguientes características:

- ✅ Solo superusuarios pueden subir avisos
- ✅ Los avisos no pueden editarse una vez subidos
- ✅ Se pueden reemplazar por nuevos avisos
- ✅ Se mantiene el historial de versiones con hash SHA-256
- ✅ Solo un aviso puede estar activo a la vez
- ✅ Los usuarios deben aceptar el aviso al registrarse
- ✅ Se registra qué versión aceptó cada usuario con timestamp
- ✅ No se permite registro sin aceptar el aviso

## Estructura

### Modelos (`privacy/models.py`)

1. **PrivacyNotice**
   - `content`: Contenido del aviso en formato Markdown
   - `content_hash`: Hash SHA-256 del contenido (único)
   - `is_active`: Indica si es el aviso activo
   - `uploaded_by`: Usuario que subió el aviso
   - `created_at`: Fecha de creación

2. **PrivacyAcceptance**
   - `user`: Usuario que aceptó el aviso
   - `privacy_notice`: Versión del aviso aceptada
   - `accepted_at`: Timestamp de aceptación
   - Restricción: Un usuario solo puede aceptar la misma versión una vez

### Admin (`privacy/admin.py`)

- Solo superusuarios pueden:
  - Agregar nuevos avisos mediante archivo .md (drag & drop)
  - Eliminar avisos
- No se permite editar avisos una vez creados
- Vista de solo lectura para las aceptaciones

### Formularios de Registro

Se agregó campo `accept_privacy` en `accounts/forms/registration_base.py`:
- Campo booleano requerido
- Mensaje de error personalizado si no se acepta

### Vistas de Registro

Actualizadas `register_parent_view` y `register_specialist_view`:
- Obtienen el aviso activo
- Lo pasan al template
- Registran la aceptación después de crear el usuario

### Templates

Actualizados `register_parent.html` y `register_specialist.html`:
- Muestran el aviso en una tarjeta con scroll
- Checkbox de aceptación requerido
- Validación de errores

## Uso

### 1. Subir un aviso de privacidad (Superusuario)

1. Acceder al admin: `/admin/`
2. Ir a "Privacy" → "Avisos de privacidad"
3. Clic en "Agregar aviso de privacidad"
4. Seleccionar archivo .md o arrastrarlo
5. Marcar "Activo" si quieres que sea el aviso activo
6. Guardar

### 2. Registro de usuarios

Los usuarios (padres/especialistas) verán:
- El contenido del aviso de privacidad activo
- Un checkbox para aceptarlo
- No podrán registrarse sin aceptar

### 3. Ver historial de aceptaciones

En el admin:
- "Privacy" → "Aceptaciones de avisos de privacidad"
- Ver quién aceptó qué versión y cuándo

## Ejemplo

Se incluye un archivo `ejemplo_aviso_privacidad.md` que puedes usar para probar.

## Características técnicas

- Hash SHA-256 calculado automáticamente
- Solo un aviso activo a la vez (se desactivan los demás automáticamente)
- Validación de formato .md en el admin
- Restricción de unicidad en aceptaciones (user + notice)
- Timestamps automáticos

## Archivos modificados/creados

### Nuevos archivos:
- `privacy/models.py`
- `privacy/admin.py`
- `privacy/views.py`
- `privacy/urls.py`
- `privacy/templates/privacy/privacy_notice.html`
- `ejemplo_aviso_privacidad.md`

### Modificados:
- `accounts/forms/registration_base.py`
- `accounts/views/register_parent.py`
- `accounts/views/register_specialist.py`
- `accounts/templates/accounts/register_parent.html`
- `accounts/templates/accounts/register_specialist.html`
- `tinycare/settings.py` (agregada app 'privacy')

### Migraciones:
- `privacy/migrations/0001_initial.py`
