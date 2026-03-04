import os
import pandas as pd
from django.core.management.base import BaseCommand
from apps.climate.models import City

class Command(BaseCommand):
    help = 'Загружает города из Excel файла ru.xlsx'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем загрузку городов из Excel...')
        
        # Путь к файлу
        current_dir = os.path.dirname(os.path.abspath(__file__))
        excel_file = os.path.join(current_dir, 'ru.xlsx')
        
        # Проверяем существование файла
        if not os.path.exists(excel_file):
            self.stdout.write(
                self.style.ERROR(f'Файл {excel_file} не найден!')
            )
            return
        
        self.stdout.write(self.style.SUCCESS(f'Найден файл: {excel_file}'))
        
        try:
            # Читаем
            df = pd.read_excel(excel_file)
            
            self.stdout.write(f'Найдено строк: {len(df)}')
            self.stdout.write(f'Колонки: {list(df.columns)}')
            
            created = 0
            updated = 0
            skipped = 0
            
            # Проходим по каждой строке
            for index, row in df.iterrows():
                # Получаем данные - обратите внимание: колонка называется 'region' в Excel
                city_name = str(row.get('city', '')).strip()
                lat = row.get('lat')
                lng = row.get('lng')
                region_name = str(row.get('region', '')).strip()  # Здесь 'region', а не 'admin_name'!
                
                # Пропускаем пустые строки
                if pd.isna(city_name) or city_name == 'nan' or not city_name:
                    skipped += 1
                    continue
                
                # Проверяем координаты
                if pd.isna(lat) or pd.isna(lng):
                    self.stdout.write(
                        self.style.WARNING(f'  Пропущен {city_name}: нет координат')
                    )
                    skipped += 1
                    continue
                
             
                if pd.isna(region_name) or region_name == 'nan':
                    region_name = ''
                

                try:
                    lat_clean = float(str(lat).strip().replace(',', '.'))
                    lng_clean = float(str(lng).strip().replace(',', '.'))
                except ValueError:
                    self.stdout.write(
                        self.style.ERROR(f'  Ошибка координат для {city_name}: {lat}, {lng}')
                    )
                    skipped += 1
                    continue
            
                city, is_new = City.objects.update_or_create(
                    name=city_name,
                    region=region_name, 
                    defaults={
                        'lat': lat_clean,
                        'lon': lng_clean,
                    }
                )
                
                if is_new:
                    created += 1
                    self.stdout.write(f'  + Создан: {city_name} ({region_name})')
                else:
                    updated += 1
                    self.stdout.write(f'  ~ Обновлен: {city_name} ({region_name})')
            
            # Итог
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nГотово! Создано: {created}, Обновлено: {updated}, Пропущено: {skipped}'
                )
            )
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            import traceback
            traceback.print_exc()