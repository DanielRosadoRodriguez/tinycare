"""
Vista para descarga de datos personales del usuario.
Cumple con LFPDPPP (derecho de acceso) y NOM-024-SSA3-2012.
"""

import json
import csv
import io
import hashlib
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone

from accounts.models.profile_parent import ProfileParent
from accounts.models.profile_specialist import ProfileSpecialist
from babies.models import Baby
from vaccines.models.vaccine import Vaccine
from privacy.models import PrivacyAcceptance, Consentimiento
from core.encryption import decrypt_field


@login_required
def download_personal_data(request):
    """
    Genera un archivo ZIP con todos los datos personales del usuario.
    
    Contenido del ZIP:
    - datos_personales.json: datos estructurados en formato JSON
    - datos_personales.csv: datos tabulares en formato CSV
    - metadata.txt: checksums SHA-256 y conteo de registros
    
    Solo incluye datos del usuario autenticado.
    Los datos cifrados se descifran para la exportación.
    """
    user = request.user
    
    # Recolectar todos los datos del usuario
    data = collect_user_data(user)
    
    # Generar JSON
    json_content = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    json_bytes = json_content.encode('utf-8')
    
    # Generar CSV
    csv_content = generate_csv_from_data(data)
    csv_bytes = csv_content.encode('utf-8')
    
    # Calcular hashes SHA-256
    json_hash = hashlib.sha256(json_bytes).hexdigest()
    csv_hash = hashlib.sha256(csv_bytes).hexdigest()
    
    # Generar metadata
    metadata_content = generate_metadata(data, json_hash, csv_hash)
    metadata_bytes = metadata_content.encode('utf-8')
    
    # Crear archivo ZIP en memoria
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w', ZIP_DEFLATED) as zip_file:
        zip_file.writestr('datos_personales.json', json_bytes)
        zip_file.writestr('datos_personales.csv', csv_bytes)
        zip_file.writestr('metadata.txt', metadata_bytes)
    
    # Preparar respuesta HTTP
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'datos_personales_{user.id}_{timestamp}.zip'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def collect_user_data(user):
    """
    Recolecta todos los datos personales del usuario.
    
    Returns:
        dict: Diccionario con toda la información del usuario
    """
    data = {
        'usuario': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'fecha_registro': user.date_joined.isoformat(),
            'activo': user.is_active,
            'ultimo_login': user.last_login.isoformat() if user.last_login else None,
        },
        'perfil': None,
        'bebes': [],
        'vacunas': [],
        'consentimientos': {},
        'aceptaciones_privacidad': [],
    }
    
    # Intentar obtener perfil de padre
    try:
        parent_profile = ProfileParent.objects.get(user=user)
        data['perfil'] = {
            'tipo': 'Padre/Madre',
            'nombres': parent_profile.nombres,
            'apellido_paterno': parent_profile.apellido_paterno,
            'apellido_materno': parent_profile.apellido_materno,
        }
        
        # Obtener bebés del padre
        babies = Baby.objects.filter(parent=parent_profile)
        for baby in babies:
            baby_data = {
                'id': baby.id,
                'nombre': baby.nombre,
                'fecha_nacimiento': baby.fecha_nacimiento.isoformat(),
                'sexo': baby.get_sexo_display(),
                'peso': float(baby.peso) if baby.peso else None,
            }
            
            # Descifrar campos sensibles
            if baby.alergias:
                try:
                    baby_data['alergias'] = decrypt_field(baby.alergias)
                except Exception:
                    baby_data['alergias'] = '[Cifrado - no disponible]'
            else:
                baby_data['alergias'] = None
                
            if baby.condiciones_salud:
                try:
                    baby_data['condiciones_salud'] = decrypt_field(baby.condiciones_salud)
                except Exception:
                    baby_data['condiciones_salud'] = '[Cifrado - no disponible]'
            else:
                baby_data['condiciones_salud'] = None
            
            data['bebes'].append(baby_data)
            
            # Obtener vacunas del bebé
            vaccines = Vaccine.objects.filter(baby=baby)
            for vaccine in vaccines:
                data['vacunas'].append({
                    'id': vaccine.id,
                    'bebe_id': baby.id,
                    'bebe_nombre': baby.nombre,
                    'nombre_vacuna': vaccine.name,
                    'fecha_aplicacion': vaccine.applied_at.isoformat(),
                    'estado': vaccine.get_status_display(),
                    'fecha_registro': vaccine.created_at.isoformat(),
                })
    
    except ProfileParent.DoesNotExist:
        pass
    
    # Intentar obtener perfil de especialista
    try:
        specialist_profile = ProfileSpecialist.objects.get(user=user)
        data['perfil'] = {
            'tipo': 'Especialista',
            'nombres': specialist_profile.nombres,
            'apellido_paterno': specialist_profile.apellido_paterno,
            'apellido_materno': specialist_profile.apellido_materno,
            'cedula_profesional': specialist_profile.cedula_profesional,
        }
    except ProfileSpecialist.DoesNotExist:
        pass
    
    # Obtener consentimientos
    try:
        consentimiento = Consentimiento.objects.get(user=user)
        data['consentimientos'] = {
            'operacion': consentimiento.operacion,
            'analitica': consentimiento.analitica,
            'marketing': consentimiento.marketing,
            'personalizacion': consentimiento.personalizacion,
            'investigacion': consentimiento.investigacion,
            'ultima_actualizacion': consentimiento.actualizado_en.isoformat(),
        }
    except Consentimiento.DoesNotExist:
        pass
    
    # Obtener aceptaciones de avisos de privacidad
    acceptances = PrivacyAcceptance.objects.filter(user=user).select_related('privacy_notice')
    for acceptance in acceptances:
        data['aceptaciones_privacidad'].append({
            'aviso_id': acceptance.privacy_notice.id,
            'aviso_hash': acceptance.privacy_notice.content_hash,
            'fecha_aceptacion': acceptance.accepted_at.isoformat(),
        })
    
    return data


def generate_csv_from_data(data):
    """
    Genera un archivo CSV plano con los datos del usuario.
    
    Estructura tabular con secciones separadas.
    
    Returns:
        str: Contenido del archivo CSV
    """
    output = io.StringIO()
    
    # Información del usuario
    output.write("=== DATOS DE USUARIO ===\n")
    writer = csv.writer(output)
    writer.writerow(['Campo', 'Valor'])
    writer.writerow(['ID', data['usuario']['id']])
    writer.writerow(['Email', data['usuario']['email']])
    writer.writerow(['Username', data['usuario']['username']])
    writer.writerow(['Fecha de registro', data['usuario']['fecha_registro']])
    writer.writerow(['Activo', 'Sí' if data['usuario']['activo'] else 'No'])
    writer.writerow(['Último login', data['usuario']['ultimo_login'] or 'Nunca'])
    output.write("\n")
    
    # Perfil
    if data['perfil']:
        output.write("=== PERFIL ===\n")
        writer.writerow(['Campo', 'Valor'])
        writer.writerow(['Tipo', data['perfil']['tipo']])
        writer.writerow(['Nombres', data['perfil']['nombres']])
        writer.writerow(['Apellido paterno', data['perfil']['apellido_paterno']])
        writer.writerow(['Apellido materno', data['perfil']['apellido_materno']])
        if 'cedula_profesional' in data['perfil']:
            writer.writerow(['Cédula profesional', data['perfil']['cedula_profesional']])
        output.write("\n")
    
    # Bebés
    if data['bebes']:
        output.write("=== BEBÉS ===\n")
        writer.writerow(['ID', 'Nombre', 'Fecha de nacimiento', 'Sexo', 'Peso (kg)', 'Alergias', 'Condiciones de salud'])
        for baby in data['bebes']:
            writer.writerow([
                baby['id'],
                baby['nombre'],
                baby['fecha_nacimiento'],
                baby['sexo'],
                baby['peso'] or '',
                baby['alergias'] or '',
                baby['condiciones_salud'] or '',
            ])
        output.write("\n")
    
    # Vacunas
    if data['vacunas']:
        output.write("=== VACUNAS ===\n")
        writer.writerow(['ID', 'Bebé ID', 'Bebé nombre', 'Vacuna', 'Fecha aplicación', 'Estado', 'Fecha registro'])
        for vaccine in data['vacunas']:
            writer.writerow([
                vaccine['id'],
                vaccine['bebe_id'],
                vaccine['bebe_nombre'],
                vaccine['nombre_vacuna'],
                vaccine['fecha_aplicacion'],
                vaccine['estado'],
                vaccine['fecha_registro'],
            ])
        output.write("\n")
    
    # Consentimientos
    if data['consentimientos']:
        output.write("=== CONSENTIMIENTOS ===\n")
        writer.writerow(['Finalidad', 'Consentimiento otorgado'])
        writer.writerow(['Operativas', 'Sí' if data['consentimientos']['operacion'] else 'No'])
        writer.writerow(['Analíticas', 'Sí' if data['consentimientos']['analitica'] else 'No'])
        writer.writerow(['Marketing', 'Sí' if data['consentimientos']['marketing'] else 'No'])
        writer.writerow(['Personalización', 'Sí' if data['consentimientos']['personalizacion'] else 'No'])
        writer.writerow(['Investigación', 'Sí' if data['consentimientos']['investigacion'] else 'No'])
        writer.writerow(['Última actualización', data['consentimientos']['ultima_actualizacion']])
        output.write("\n")
    
    # Aceptaciones de privacidad
    if data['aceptaciones_privacidad']:
        output.write("=== ACEPTACIONES DE AVISOS DE PRIVACIDAD ===\n")
        writer.writerow(['Aviso ID', 'Hash SHA-256', 'Fecha de aceptación'])
        for acceptance in data['aceptaciones_privacidad']:
            writer.writerow([
                acceptance['aviso_id'],
                acceptance['aviso_hash'],
                acceptance['fecha_aceptacion'],
            ])
    
    return output.getvalue()


def generate_metadata(data, json_hash, csv_hash):
    """
    Genera archivo de metadatos con checksums y conteo de registros.
    
    Returns:
        str: Contenido del archivo metadata.txt
    """
    lines = [
        "=" * 70,
        "METADATOS DE EXPORTACIÓN DE DATOS PERSONALES",
        "=" * 70,
        "",
        f"Fecha de generación: {timezone.now().isoformat()}",
        f"Usuario ID: {data['usuario']['id']}",
        f"Usuario email: {data['usuario']['email']}",
        "",
        "=" * 70,
        "CHECKSUMS SHA-256",
        "=" * 70,
        "",
        f"datos_personales.json: {json_hash}",
        f"datos_personales.csv:  {csv_hash}",
        "",
        "Estos checksums permiten verificar la integridad de los archivos.",
        "Puede calcularlos independientemente para confirmar que no han sido alterados.",
        "",
        "=" * 70,
        "CONTEO DE REGISTROS",
        "=" * 70,
        "",
        f"Bebés registrados: {len(data['bebes'])}",
        f"Vacunas registradas: {len(data['vacunas'])}",
        f"Aceptaciones de avisos de privacidad: {len(data['aceptaciones_privacidad'])}",
        f"Consentimientos registrados: {'Sí' if data['consentimientos'] else 'No'}",
        "",
        "=" * 70,
        "CUMPLIMIENTO NORMATIVO",
        "=" * 70,
        "",
        "Esta exportación cumple con:",
        "- Ley Federal de Protección de Datos Personales en Posesión de los Particulares",
        "  (LFPDPPP) - Derecho de Acceso",
        "- NOM-024-SSA3-2012 - Sistemas de información de registro electrónico para la salud",
        "",
        "Los datos sensibles (alergias, condiciones de salud) se exportan descifrados",
        "únicamente para el titular de los datos.",
        "",
        "=" * 70,
    ]
    
    return "\n".join(lines)
