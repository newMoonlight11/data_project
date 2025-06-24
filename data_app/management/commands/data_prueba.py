from django.core.management.base import BaseCommand
from data_app.utils import data_fixed_width_file, map_row_to_fields
from data_app.models import Registro

class Command(BaseCommand):
    help = 'Importa datos desde un archivo de texto plano a la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        filepath = options['filepath']
        rows = data_fixed_width_file(filepath)
        registros = [Registro(**map_row_to_fields(r, filepath)) for r in rows]
        Registro.objects.bulk_create(registros)
        self.stdout.write(self.style.SUCCESS(f'{len(registros)} registros importados'))