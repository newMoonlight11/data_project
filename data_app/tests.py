from django.test import TestCase
from data_app.utils import data_fixed_width_file, map_row_to_fields
from data_app.utils import FIELD_SLICES
from data_app.models import Registro

class FileProcessingTest(TestCase):
    def test_file_parsing(self):
        rows = data_fixed_width_file('PRUEBA_20250129.txt')
        self.assertGreater(len(rows), 0)
    
    def test_map_row_to_fields(self):
        sample_line = '5         CC 1019300947     SEVILLA , YENIFER DURAN                                                                             30248422100    A36837815,1260         170999,999772         21063541      2025-01-07          -9   3015460261                                   Bogotá, D.C.                                      BOGOTÁ, D. C.                                     2025-01-071994-10-17AVIBENEFICIARIO DE LEY ,                                                                               FCentro                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          107 Hall Bancario                                                                                   14 Masivo                     jenniefersevil94@gmail.com                                                                          Linea telefonica-WhatsApp-Mensaje de texto-Correo electronico-Correspondencia fisica'
        fields = [sample_line[start:end].strip() for start, end in FIELD_SLICES]
        record = map_row_to_fields(fields, 'PRUEBA_20250129.txt')
        self.assertIn('nombre', record) 
    
    def test_registro_insertion(self):
        Registro.objects.create(
            documento='1234567890',
            nombre='Prueba Técnica',
            producto='PROD01',
            poliza='POL1234567890',
            periodo='A',
            valor_asegurado=100000.0,
            valor_prima=5000.0,
            doc_cobro='DOC001',
            dias=0,
            ciudad='Bogotá',
            departamento='Cundinamarca',
            fecha_venta='2025-01-07',
            fecha_nacimiento='1990-01-01',
            tipo_trans='AVI',
            beneficiarios='Beneficiario Ejemplo',
            genero='F',
            sucursal='Centro',
            ultimos_digitos_cuenta='1234',
            entidad_bancaria='Banco X',
            nombre_banco='Banco de Prueba',
            estado_debito='Aprobado',
            causal_rechazo='',
            codigo_canal='C01',
            descripcion_canal='Canal de prueba',
            codigo_estrategia='EST01',
            tipo_estrategia='Estrategia A',
            correo_electronico='prueba@example.com',
            mejor_canal='texto',
            contactar_al='3015460261'
        )
        self.assertEqual(Registro.objects.filter(documento='1234567890').count(), 1)