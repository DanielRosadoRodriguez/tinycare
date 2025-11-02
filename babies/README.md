# Babies App

App Django reutilizable para gestión de información de bebés (CRUD completo).

## Descripción

Esta app Django proporciona funcionalidad completa para registrar, visualizar, editar y eliminar información de bebés. Cada bebé está asociado a un perfil de padre/madre mediante una relación ForeignKey (1:N).

## Características

- ✅ CRUD completo de bebés (Create, Read, Update, Delete)
- ✅ Relación 1:N con ProfileParent (1 padre puede tener N hijos)
- ✅ Validación de permisos (solo el padre propietario puede ver/editar sus bebés)
- ✅ Campos obligatorios: nombre, fecha_nacimiento, sexo
- ✅ Campos opcionales: peso, alergias, condiciones_salud
- ✅ Cálculo automático de edad en meses
- ✅ Interfaz responsive con Bootstrap 5
- ✅ Admin de Django configurado
- ✅ Arquitectura modular siguiendo SOLID

## Estructura

```
babies/
├── models/
│   ├── __init__.py
│   └── baby_model.py          # Modelo Baby
├── forms/
│   ├── __init__.py
│   └── baby_form.py            # BabyForm (ModelForm)
├── views/
│   ├── __init__.py
│   └── baby_views.py           # Vistas CRUD (CBV)
├── permissions/
│   ├── __init__.py
│   └── owner_permission_mixin.py  # Mixin de permisos
├── templates/
│   └── babies/
│       ├── baby_list.html
│       ├── baby_detail.html
│       ├── baby_form.html
│       └── baby_confirm_delete.html
├── migrations/
├── admin.py                    # Registro en Django Admin
├── apps.py
├── urls.py                     # URL patterns
└── README.md
```

## Instalación en otro proyecto Django

### 1. Copiar la app

```bash
cp -r babies/ /ruta/a/tu/proyecto/
```

### 2. Registrar en `INSTALLED_APPS`

En `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'babies',
]
```

### 3. Incluir las URLs

En tu `urls.py` principal:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('bebes/', include('babies.urls')),
]
```

### 4. Dependencias

La app requiere:
- Django 5.x
- Una app que provea el modelo `ProfileParent` con la estructura:
  - `ProfileParent.user` (OneToOneField a User)
  - `ProfileParent.nombres`
  - `ProfileParent.apellido_paterno`

Si tu proyecto no tiene `ProfileParent`, puedes adaptar el modelo `Baby` cambiando:

```python
# En babies/models/baby_model.py
from django.contrib.auth import get_user_model

User = get_user_model()

class Baby(models.Model):
    # Cambiar de:
    # parent = models.ForeignKey(ProfileParent, ...)
    
    # A:
    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="babies",
        verbose_name="Padre/Madre"
    )
    # ... resto del modelo
```

Y actualizar las vistas en `babies/views/baby_views.py` para eliminar referencias a `ProfileParent`.

### 5. Aplicar migraciones

```bash
python manage.py makemigrations babies
python manage.py migrate
```

## Uso

### URLs disponibles

- `/bebes/` - Lista de bebés del usuario autenticado
- `/bebes/nuevo/` - Formulario para registrar un nuevo bebé
- `/bebes/<id>/` - Detalle de un bebé específico
- `/bebes/<id>/editar/` - Editar información de un bebé
- `/bebes/<id>/eliminar/` - Eliminar un bebé

### Permisos

- **BabyOwnerPermissionMixin**: Verifica que el usuario autenticado sea el padre/madre propietario del bebé antes de permitir acceso a vistas de detalle/edición/eliminación.
- Solo usuarios con `ProfileParent` pueden crear bebés.
- Los bebés solo son visibles para su padre/madre propietario.

## Modelo Baby

### Campos

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `parent` | ForeignKey | Sí | Relación con ProfileParent |
| `nombre` | CharField(100) | Sí | Nombre del bebé |
| `fecha_nacimiento` | DateField | Sí | Fecha de nacimiento |
| `sexo` | CharField(1) | Sí | M/F/O (Masculino/Femenino/Otro) |
| `peso` | DecimalField(5,2) | No | Peso en kilogramos |
| `alergias` | TextField | No | Alergias conocidas |
| `condiciones_salud` | TextField | No | Condiciones médicas |
| `created_at` | DateTimeField | Auto | Fecha de registro |
| `updated_at` | DateTimeField | Auto | Última actualización |

### Métodos

- `__str__()`: Retorna "{nombre} ({sexo})"
- `edad_en_meses()`: Calcula la edad del bebé en meses desde la fecha de nacimiento

## Integración con tu proyecto

### Agregar enlace en el menú

Si tienes un menú de navegación, agrega:

```django
<a href="{% url 'babies:baby_list' %}">Mis Bebés</a>
```

### Mostrar bebés de un usuario en otra vista

```python
from babies.models import Baby
from accounts.models import ProfileParent

# En tu vista
def my_view(request):
    try:
        parent = ProfileParent.objects.get(user=request.user)
        babies = Baby.objects.filter(parent=parent)
    except ProfileParent.DoesNotExist:
        babies = []
    
    return render(request, 'template.html', {'babies': babies})
```

## Personalización

### Estilos

Los templates usan Bootstrap 5. Puedes personalizar los estilos editando las etiquetas `<style>` en cada template o creando un archivo CSS externo.

### Campos adicionales

Para agregar nuevos campos al modelo:

1. Edita `babies/models/baby_model.py`
2. Agrega el campo al `BabyForm` en `babies/forms/baby_form.py`
3. Actualiza los templates si es necesario
4. Genera y aplica migraciones:
   ```bash
   python manage.py makemigrations babies
   python manage.py migrate
   ```

## Licencia

Esta app fue desarrollada como parte del proyecto TinyCare y puede ser reutilizada libremente.

## Autor

Equipo TinyCare - Innovatech Solutions
