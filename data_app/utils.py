import os
from datetime import datetime
import re

# Definición correcta de los intervalos del archivo
FIELD_SLICES = [
    (0, 10),    # tipo_documento
    (10, 13),   # documento
    (13, 28),   # nombre
    (28, 128),  # producto + poliza
    (128, 143), # periodo + valor_asegurado
    (143, 165), # valor_prima
    (165, 187), # doc_cobro
    (187, 201), # fecha_ini
    (201, 221), # fecha_fin (vacío)
    (221, 226), # dias
    (226, 241), # telefono_1
    (241, 256), # telefono_2
    (256, 271), # telefono_3
    (271, 321), # ciudad
    (321, 371), # departamento
    (371, 494), # fecha_venta + fecha_nacimiento + tipo_trans + beneficiarios
    (494, 548), # genero + sucursal
    (548, 568), # tipo_cuenta (vacío) + ultimos_digitos_cuenta
    (568, 575), # entidad_bancaria
    (575, 615), # nombre_banco
    (615, 625), # estado_debito
    (625, 1615) # causal_rechazo + resto
]

def data_fixed_width_file(filepath: str) -> list[list[str]]:
    rows = []
    max_length = 1615  # Longitud máxima definida en FIELD_SLICES
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')  # Elimina saltos de línea
            if len(line) < max_length:
                line += ' ' * (max_length - len(line))  # Rellena con espacios
            fields = [line[start:end].strip() for start, end in FIELD_SLICES]
            rows.append(fields)
    return rows

def map_row_to_fields(fields: list[str], filepath: str = '') -> dict:
    record = {}
    record['tipo_documento'] = fields[0].strip() if len(fields) > 0 else ''
    record['documento'] = fields[1].strip() if len(fields) > 1 else ''
    record['nombre'] = fields[2].strip() if len(fields) > 2 else ''

    # Producto y póliza (extraídos de fields[3])
    producto_poliza = fields[3].strip() if len(fields) > 3 else ''
    record['producto'] = producto_poliza[:5]  # Primeros 5 caracteres
    record['poliza'] = producto_poliza[5:]     # Resto de caracteres

    # Periodo (primer caracter de fields[4])
    periodo_str = fields[4][0] if len(fields) > 4 and len(fields[4]) > 0 else ''
    record['periodo'] = periodo_str

    
    # Validación y limpieza para valor_asegurado
    valor_asegurado_str = fields[4][1:].strip() if len(fields) > 4 else '0'
    valor_asegurado_str = re.sub(r'[^\d.]', '', valor_asegurado_str.replace(',', '.'))
    record['valor_asegurado'] = float(valor_asegurado_str or '0')

    # Validación y limpieza para valor_prima
    valor_prima_str = fields[5].strip() if len(fields) > 5 else '0'
    valor_prima_str = re.sub(r'[^\d.]', '', valor_prima_str.replace(',', '.'))
    record['valor_prima'] = float(valor_prima_str or '0')
    
    record['doc_cobro'] = fields[6].strip() if len(fields) > 6 else ''
    
    # Validación para fechas
    fecha_ini_str = fields[7].strip() if len(fields) > 7 else ''
    if fecha_ini_str and len(fecha_ini_str) == 10:
        try:
            record['fecha_ini'] = datetime.strptime(fecha_ini_str, '%Y-%m-%d').date()
        except ValueError:
            record['fecha_ini'] = None
    else:
        record['fecha_ini'] = None
    
    record['fecha_fin'] = None
    
    dias_str = fields[9].strip() if len(fields) > 9 else ''
    dias_str = dias_str.replace(' ', '')  # Elimina espacios
    try:
        dias = int(dias_str)
        record['dias'] = dias if dias >= 0 else 0  # Reemplaza valores negativos con 0
    except ValueError:
        record['dias'] = 0 
        
    # Teléfonos
    record['telefono_1'] = fields[10].strip() if len(fields) > 10 else ''
    record['telefono_2'] = fields[11].strip() if len(fields) > 11 else ''
    record['telefono_3'] = fields[12].strip() if len(fields) > 12 else ''
    
    # Ubicación
    record['ciudad'] = fields[13].strip() if len(fields) > 13 else ''
    record['departamento'] = fields[14].strip() if len(fields) > 14 else ''
    
    # Fecha de venta y nacimiento
    if len(fields) > 15:
        venta = fields[15]
        fecha_venta_str = venta[:10].strip()
        try:
            record['fecha_venta'] = datetime.strptime(fecha_venta_str, '%Y-%m-%d').date() if fecha_venta_str else None
        except ValueError:
            record['fecha_venta'] = None
        
        fecha_nacimiento_str = venta[10:20].strip()
        try:
            record['fecha_nacimiento'] = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date() if fecha_nacimiento_str else None
        except ValueError:
            record['fecha_nacimiento'] = None
        
        record['tipo_trans'] = venta[20:23].strip() if len(venta) > 23 else ''
        record['beneficiarios'] = venta[23:].strip()
    else:
        record['fecha_venta'] = None
        record['fecha_nacimiento'] = None
        record['tipo_trans'] = ''
        record['beneficiarios'] = ''
    
    # Género y sucursal
    genero_sucursal = fields[16] if len(fields) > 16 else ''
    record['genero'] = genero_sucursal[0].strip() if genero_sucursal else ''
    record['sucursal'] = genero_sucursal[1:].strip() if genero_sucursal else ''
    
    # Cuenta bancaria
    record['tipo_cuenta'] = ''
    record['ultimos_digitos_cuenta'] = fields[17].strip() if len(fields) > 17 else ''
    record['entidad_bancaria'] = fields[18].strip() if len(fields) > 18 else ''
    record['nombre_banco'] = fields[19].strip() if len(fields) > 19 else ''
    
    # Estado de débito y causal de rechazo
    record['estado_debito'] = fields[20].strip() if len(fields) > 20 else ''
    record['causal_rechazo'] = fields[21].strip() if len(fields) > 21 else ''
    
    # Canal y estrategia
    canal = fields[22] if len(fields) > 22 else ''
    record['codigo_canal'] = canal[:3].strip() if canal else ''
    record['descripcion_canal'] = canal[3:].strip() if canal else ''
    
    record['codigo_estrategia'] = fields[23].strip() if len(fields) > 23 else ''
    record['tipo_estrategia'] = fields[24].strip() if len(fields) > 24 else ''
    record['correo_electronico'] = fields[25].strip() if len(fields) > 25 else ''
    
    # Fecha de entrega y mes
    if filepath:
        fname = os.path.basename(filepath)
        date_str = fname.replace('PRUEBA_', '').replace('.txt', '')
        try:
            entrega = datetime.strptime(date_str, '%Y%m%d').date()
        except ValueError:
            entrega = datetime.now().date()
    else:
        entrega = datetime.now().date()
    
    record['fecha_entrega_colmena'] = entrega
    record['mes_a_trabajar'] = entrega.month
    record['nombre_db'] = fname if filepath else ''
    
    # Canales de contacto
    notes = fields[28].lower() if len(fields) > 28 else ''
    record['telefono'] = 1 if 'linea telefonica' in notes else 0
    record['whatsapp'] = 1 if 'whatsapp' in notes else 0
    record['texto'] = 1 if 'mensaje de texto' in notes else 0
    record['email'] = 1 if 'correo electronico' in notes else 0
    record['fisica'] = 1 if 'correspondencia fisica' in notes else 0
    
    # Determinar mejor canal
    channels = ['texto', 'email', 'telefono', 'whatsapp', 'fisica']
    record['mejor_canal'] = 'texto'  # Valor por defecto
    
    for ch in channels:
        if record.get(ch):
            record['mejor_canal'] = ch
            break
    
    # Contactar_al según mejor canal
    contact_number = ''
    if record['mejor_canal'] in ['texto', 'telefono', 'whatsapp']:
        for t in ['telefono_1', 'telefono_2', 'telefono_3']:
            if record[t]:
                contact_number = record[t]
                break
        record['contactar_al'] = contact_number or record['correo_electronico'] or ''
    elif record['mejor_canal'] == 'email':
        record['contactar_al'] = record['correo_electronico'] or ''
    else:
        record['contactar_al'] = ''
    
    return record