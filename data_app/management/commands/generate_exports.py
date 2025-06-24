from django.core.management.base import BaseCommand
import os
import pandas as pd
from data_app.utils import data_fixed_width_file, map_row_to_fields

class Command(BaseCommand):
    help = 'Procesa un archivo y genera CSV/JSON'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        filepath = options['filepath']
        output_dir = 'exports'
        os.makedirs(output_dir, exist_ok=True)

        rows = data_fixed_width_file(filepath)
        records = [map_row_to_fields(r, filepath) for r in rows]
        df = pd.DataFrame(records)
        df.to_csv(os.path.join(output_dir, 'output.csv'), index=False)
        df.to_json(os.path.join(output_dir, 'output.json'), orient='records', force_ascii=False)

        self.stdout.write(self.style.SUCCESS(f'Archivos generados en {output_dir}'))