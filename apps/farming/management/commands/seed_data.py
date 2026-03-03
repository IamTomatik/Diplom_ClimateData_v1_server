from django.core.management.base import BaseCommand
from apps.farming.models import Crop, Variety

class Command(BaseCommand):
    help = 'Заполняет базу данных начальными культурами и сортами'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем заполнение данных...')
        
        # Словарь культур с категориями
        crops_data = {
            "Пшеница": {"category": "Зерновые"},
            "Кукуруза": {"category": "Зерновые"},
            "Ячмень": {"category": "Зерновые"},
            "Овес": {"category": "Зерновые"},
            "Морковь": {"category": "Корнеплоды"},
            "Свекла": {"category": "Корнеплоды"},
            "Картофель": {"category": "Клубнеплоды"},
            "Соя": {"category": "Бобовые"},
            "Горох": {"category": "Бобовые"},
            "Фасоль": {"category": "Бобовые"},
            "Подсолнечник": {"category": "Масличные"},
            "Огурцы": {"category": "Овощи"},
            "Помидоры": {"category": "Овощи"},
            "Лук": {"category": "Овощи"},
            "Чеснок": {"category": "Овощи"},
            "Капуста белокачанная": {"category": "Овощи"},
            "Капуста брокколи": {"category": "Овощи"},
            "Редис": {"category": "Овощи"},
            "Баклажан": {"category": "Овощи"},
            "Кабачок": {"category": "Овощи"},
            "Базилик": {"category": "Овощи"},
            "Шпинат": {"category": "Овощи"},
            "Капуста кольраби": {"category": "Овощи"},
            "Яблоня": {"category": "Фрукты"},
            "Груша": {"category": "Фрукты"},
            "Клубника": {"category": "Ягоды"},
            "Малина": {"category": "Ягоды"},
            "Гвоздика": {"category": "Цветы"},
            "Гортензия": {"category": "Цветы"},
            "Петуния": {"category": "Цветы"},
            "Роза": {"category": "Цветы"},
            "Лаванда": {"category": "Цветы"},
        }
        
        # Создаем культуры
        crops = {}
        created_crops = 0
        for name, data in crops_data.items():
            crop, created = Crop.objects.get_or_create(
                name=name,
                defaults={"category": data["category"]}
            )
            crops[name] = crop
            if created:
                created_crops += 1
                self.stdout.write(f'  Создана культура: {name}')
        
        self.stdout.write(self.style.SUCCESS(f'Создано {created_crops} культур'))
        
        # Данные для сортов
        varieties_data = []
        
        # Огурцы
        cucumbers = crops.get("Огурцы")
        if cucumbers:
            varieties_data.extend([
                {
                    "cropID": cucumbers.crop_ID,
                    "name": "Гибридный",
                    "optimal_temp_min": 18.0,
                    "optimal_temp_max": 28.0,
                    "optimal_humidity": 70.0,
                    "soil_humidity": 65.0,
                    "growth_days": 50,
                    "risk_factors": "Мучнистая роса, тля",
                    "description": "Раннеспелый гибрид, устойчивый к основным заболеваниям",
                    "recommended_seedling_time": "конец апреля — начало мая",
                    "recommended_open_ground_time": "конец мая — начало июня",
                    "recommended_greenhouse_time": "с середины апреля",
                    "seedling_age": "20–25 дней, 3–4 настоящих листа",
                    "soil_preparation": "Рыхлая, плодородная почва с pH 6.0-7.0",
                    "sowing_depth": "1.5-2 см",
                    "planting_scheme": "50x30 см",
                    "watering_after_planting": "Обильный полив, 2-3 л на растение",
                    "favorable_conditions": "Температура 22-26°C, влажность 70-80%",
                    "watering_recommendations": "Каждые 2-3 дня, утром или вечером",
                    "fertilizing_schedule": "Каждые 10-14 дней комплексным удобрением",
                    "loosening_and_mulching": "Рыхление после каждого полива, мульчирование торфом",
                    "disease_prevention": "Опрыскивание фитоспорином каждые 10-14 дней"
                },
                {
                    "cropID": cucumbers.crop_ID,
                    "name": "Апрельский",
                    "optimal_temp_min": 16.0,
                    "optimal_temp_max": 26.0,
                    "optimal_humidity": 75.0,
                    "soil_humidity": 70.0,
                    "growth_days": 45,
                    "risk_factors": "Бактериоз, паутинный клещ",
                    "description": "Ранний сорт для теплиц и открытого грунта",
                    "recommended_seedling_time": "середина апреля",
                    "recommended_open_ground_time": "конец мая",
                    "recommended_greenhouse_time": "начало апреля",
                    "seedling_age": "25-30 дней",
                    "soil_preparation": "Плодородная почва с высоким содержанием органики",
                    "sowing_depth": "1.5 см",
                    "planting_scheme": "50x40 см",
                    "watering_after_planting": "2-3 л на растение",
                    "favorable_conditions": "Температура 20-24°C",
                    "watering_recommendations": "Через день, 3-4 л/м²",
                    "fertilizing_schedule": "3 раза за сезон",
                    "loosening_and_mulching": "Рыхление 1 раз в неделю",
                    "disease_prevention": "Профилактическое опрыскивание"
                },
                {
                    "cropID": cucumbers.crop_ID,
                    "name": "Зозуля",
                    "optimal_temp_min": 20.0,
                    "optimal_temp_max": 30.0,
                    "optimal_humidity": 65.0,
                    "soil_humidity": 60.0,
                    "growth_days": 48,
                    "risk_factors": "Мучнистая роса, оливковая пятнистость",
                    "description": "Партенокарпический гибрид для теплиц",
                    "recommended_seedling_time": "начало мая",
                    "recommended_open_ground_time": "июнь",
                    "recommended_greenhouse_time": "апрель",
                    "seedling_age": "20-25 дней",
                    "soil_preparation": "Легкая, плодородная почва",
                    "sowing_depth": "2 см",
                    "planting_scheme": "60x30 см",
                    "watering_after_planting": "3 л на растение",
                    "favorable_conditions": "Температура 22-28°C",
                    "watering_recommendations": "Каждые 2 дня",
                    "fertilizing_schedule": "Каждые 2 недели",
                    "loosening_and_mulching": "Мульчирование соломой",
                    "disease_prevention": "Биопрепараты"
                },
                {
                    "cropID": cucumbers.crop_ID,
                    "name": "Конкурент",
                    "optimal_temp_min": 17.0,
                    "optimal_temp_max": 27.0,
                    "optimal_humidity": 72.0,
                    "soil_humidity": 68.0,
                    "growth_days": 52,
                    "risk_factors": "Антракноз, тля",
                    "description": "Пчелоопыляемый сорт для открытого грунта",
                    "recommended_seedling_time": "середина мая",
                    "recommended_open_ground_time": "начало июня",
                    "recommended_greenhouse_time": "середина апреля",
                    "seedling_age": "25-30 дней",
                    "soil_preparation": "Суглинистая почва с компостом",
                    "sowing_depth": "1.5-2 см",
                    "planting_scheme": "50x40 см",
                    "watering_after_planting": "2-3 л",
                    "favorable_conditions": "Температура 20-25°C",
                    "watering_recommendations": "Через 1-2 дня",
                    "fertilizing_schedule": "4 раза за сезон",
                    "loosening_and_mulching": "Регулярное рыхление",
                    "disease_prevention": "Севооборот"
                }
            ])

        # Помидоры
        tomatoes = crops.get("Помидоры")
        if tomatoes:
            varieties_data.extend([
                {
                    "cropID": tomatoes.crop_ID,
                    "name": "Бычье сердце",
                    "optimal_temp_min": 20.0,
                    "optimal_temp_max": 30.0,
                    "optimal_humidity": 65.0,
                    "soil_humidity": 60.0,
                    "growth_days": 90,
                    "risk_factors": "Фитофтора, тля",
                    "description": "Крупноплодный салатный сорт",
                    "recommended_seedling_time": "март",
                    "recommended_open_ground_time": "июнь",
                    "recommended_greenhouse_time": "май",
                    "seedling_age": "55-60 дней",
                    "soil_preparation": "Плодородная, рыхлая почва",
                    "sowing_depth": "1-1.5 см",
                    "planting_scheme": "70x50 см",
                    "watering_after_planting": "3-4 л",
                    "favorable_conditions": "Температура 22-26°C",
                    "watering_recommendations": "2 раза в неделю",
                    "fertilizing_schedule": "Каждые 2 недели",
                    "loosening_and_mulching": "Мульчирование",
                    "disease_prevention": "Фитоспорин"
                },
                {
                    "cropID": tomatoes.crop_ID,
                    "name": "Черри",
                    "optimal_temp_min": 22.0,
                    "optimal_temp_max": 32.0,
                    "optimal_humidity": 60.0,
                    "soil_humidity": 55.0,
                    "growth_days": 85,
                    "risk_factors": "Фитофтора, вершинная гниль",
                    "description": "Мелкоплодный сорт для свежего потребления",
                    "recommended_seedling_time": "апрель",
                    "recommended_open_ground_time": "июнь",
                    "recommended_greenhouse_time": "май",
                    "seedling_age": "50-55 дней",
                    "soil_preparation": "Легкая почва",
                    "sowing_depth": "1 см",
                    "planting_scheme": "50x40 см",
                    "watering_after_planting": "2 л",
                    "favorable_conditions": "Температура 24-28°C",
                    "watering_recommendations": "Частый, но умеренный",
                    "fertilizing_schedule": "Каждые 10 дней",
                    "loosening_and_mulching": "Рыхление",
                    "disease_prevention": "Кальциевая селитра"
                },
                {
                    "cropID": tomatoes.crop_ID,
                    "name": "Де Барао",
                    "optimal_temp_min": 18.0,
                    "optimal_temp_max": 28.0,
                    "optimal_humidity": 70.0,
                    "soil_humidity": 65.0,
                    "growth_days": 95,
                    "risk_factors": "Кладоспориоз, тля",
                    "description": "Высокорослый сорт для теплиц",
                    "recommended_seedling_time": "февраль-март",
                    "recommended_open_ground_time": "июнь",
                    "recommended_greenhouse_time": "апрель-май",
                    "seedling_age": "60-65 дней",
                    "soil_preparation": "Плодородная почва",
                    "sowing_depth": "1.5 см",
                    "planting_scheme": "80x60 см",
                    "watering_after_planting": "5 л",
                    "favorable_conditions": "Температура 20-24°C",
                    "watering_recommendations": "Обильный, редкий",
                    "fertilizing_schedule": "Каждые 3 недели",
                    "loosening_and_mulching": "Мульчирование",
                    "disease_prevention": "Проветривание"
                },
                {
                    "cropID": tomatoes.crop_ID,
                    "name": "Розовый гигант",
                    "optimal_temp_min": 19.0,
                    "optimal_temp_max": 29.0,
                    "optimal_humidity": 68.0,
                    "soil_humidity": 62.0,
                    "growth_days": 100,
                    "risk_factors": "Фитофтора, вертициллез",
                    "description": "Крупноплодный розовоплодный сорт",
                    "recommended_seedling_time": "март",
                    "recommended_open_ground_time": "июнь",
                    "recommended_greenhouse_time": "май",
                    "seedling_age": "60-70 дней",
                    "soil_preparation": "Богатая органикой",
                    "sowing_depth": "1-2 см",
                    "planting_scheme": "70x50 см",
                    "watering_after_planting": "4 л",
                    "favorable_conditions": "Температура 22-26°C",
                    "watering_recommendations": "2 раза в неделю",
                    "fertilizing_schedule": "Каждые 2 недели",
                    "loosening_and_mulching": "Рыхление",
                    "disease_prevention": "Медный купорос"
                },
                {
                    "cropID": tomatoes.crop_ID,
                    "name": "Санька",
                    "optimal_temp_min": 15.0,
                    "optimal_temp_max": 25.0,
                    "optimal_humidity": 65.0,
                    "soil_humidity": 60.0,
                    "growth_days": 80,
                    "risk_factors": "Фитофтора, фузариоз",
                    "description": "Ультраскороспелый сорт",
                    "recommended_seedling_time": "апрель",
                    "recommended_open_ground_time": "май-июнь",
                    "recommended_greenhouse_time": "апрель",
                    "seedling_age": "45-50 дней",
                    "soil_preparation": "Любая почва",
                    "sowing_depth": "1 см",
                    "planting_scheme": "50x40 см",
                    "watering_after_planting": "2 л",
                    "favorable_conditions": "Температура 18-22°C",
                    "watering_recommendations": "Умеренный",
                    "fertilizing_schedule": "3 раза",
                    "loosening_and_mulching": "Рыхление",
                    "disease_prevention": "Устойчив к фитофторе"
                }
            ])

        # Картофель
        potato = crops.get("Картофель")
        if potato:
            varieties_data.append({
                "cropID": potato.crop_ID,
                "name": "Невский",
                "optimal_temp_min": 12.0,
                "optimal_temp_max": 25.0,
                "optimal_humidity": 65.0,
                "soil_humidity": 70.0,
                "growth_days": 80,
                "risk_factors": "Колорадский жук, гниль",
                "description": "Среднеранний столовый сорт",
                "recommended_seedling_time": "май",
                "recommended_open_ground_time": "май-июнь",
                "recommended_greenhouse_time": "апрель",
                "seedling_age": "Пророщенные клубни",
                "soil_preparation": "Рыхлая, дренированная почва",
                "sowing_depth": "8-10 см",
                "planting_scheme": "70x30 см",
                "watering_after_planting": "2-3 л на куст",
                "favorable_conditions": "Температура 18-22°C",
                "watering_recommendations": "При засухе",
                "fertilizing_schedule": "3 раза за сезон",
                "loosening_and_mulching": "Окучивание",
                "disease_prevention": "Протравливание клубней"
            })

        # Капуста белокачанная
        cabbage = crops.get("Капуста белокачанная")
        if cabbage:
            varieties_data.append({
                "cropID": cabbage.crop_ID,
                "name": "Слава",
                "optimal_temp_min": 10.0,
                "optimal_temp_max": 20.0,
                "optimal_humidity": 70.0,
                "soil_humidity": 65.0,
                "growth_days": 90,
                "risk_factors": "Капустная муха, гниль",
                "description": "Среднеспелый сорт",
                "recommended_seedling_time": "апрель",
                "recommended_open_ground_time": "май-июнь",
                "recommended_greenhouse_time": "март-апрель",
                "seedling_age": "35-40 дней",
                "soil_preparation": "Плодородная, нейтральная",
                "sowing_depth": "1-2 см",
                "planting_scheme": "60x50 см",
                "watering_after_planting": "1-2 л",
                "favorable_conditions": "Температура 15-18°C",
                "watering_recommendations": "2 раза в неделю",
                "fertilizing_schedule": "3-4 раза",
                "loosening_and_mulching": "Рыхление",
                "disease_prevention": "Зола"
            })

        # Клубника
        strawberry = crops.get("Клубника")
        if strawberry:
            varieties_data.append({
                "cropID": strawberry.crop_ID,
                "name": "Гигантелла",
                "optimal_temp_min": 15.0,
                "optimal_temp_max": 25.0,
                "optimal_humidity": 70.0,
                "soil_humidity": 65.0,
                "growth_days": 90,
                "risk_factors": "Серая гниль, тля",
                "description": "Крупноплодный сорт",
                "recommended_seedling_time": "февраль-март",
                "recommended_open_ground_time": "май",
                "recommended_greenhouse_time": "апрель",
                "seedling_age": "рассада с 3-5 листьями",
                "soil_preparation": "Кислотность 5.0-6.5",
                "sowing_depth": "0.5 см",
                "planting_scheme": "30x30 см",
                "watering_after_planting": "0.5 л",
                "favorable_conditions": "Температура 20-22°C",
                "watering_recommendations": "Капельный полив",
                "fertilizing_schedule": "Каждые 2 недели",
                "loosening_and_mulching": "Мульчирование",
                "disease_prevention": "Мульчирование соломой"
            })

        # Создаем сорта
        created_varieties = 0
        for var_data in varieties_data:
            variety, created = Variety.objects.get_or_create(
                crop=var_data["crop"],
                name=var_data["name"],
                defaults=var_data
            )
            if created:
                created_varieties += 1
                self.stdout.write(f'  Создан сорт: {var_data["name"]} для {var_data["crop"].name}')
        
        self.stdout.write(self.style.SUCCESS(f'Создано {created_varieties} сортов'))
        self.stdout.write(self.style.SUCCESS('Заполнение данных завершено!'))