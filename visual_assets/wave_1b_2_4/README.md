# Wave 1B Visual Assets

Дата: 21 марта 2026
Статус: рабочий пакет визуальных материалов для уроков 2-4

## Что внутри

- `build_wave_1b_assets.py` - генератор SVG-assets.
- `wave_1b_slides_outline.md` - карта deck по урокам 2-4.
- `wave_1b_slide_copy.md` - точный смысл каждого экрана.
- `wave_1b_diagrams.md` - Mermaid-схемы для логики уроков.
- SVG-файлы - реальные assets для записи и черновой монтаж.

## Покрытие

- 15 SVG-assets: по 5 экранов на уроки 2, 3 и 4.
- Урок 2 опирается на карту классов задач и реальные стартовые примеры.
- Урок 3 опирается на confident-but-wrong risk case и green/yellow/red map.
- Урок 4 опирается на матрицу выбора сценариев и go / no-go filter.

## Как пересобрать

`python3 build_wave_1b_assets.py`

## Карта SVG-файлов

- `l02_title_card.svg` - Урок 2: Где AI помогает быстрее всего
- `l02_task_class_map.svg` - Урок 2: Шесть стартовых классов задач
- `l02_three_examples.svg` - Урок 2: Три первых сценария без перегруза
- `l02_start_filter.svg` - Урок 2: Фильтр первой пользы
- `l02_final_card.svg` - Урок 2: Действие после урока
- `l03_title_card.svg` - Урок 3: Где AI слаб или опасен
- `l03_confident_wrong_case.svg` - Урок 3: Гладкий ответ с высокой ценой ошибки
- `l03_risk_lens.svg` - Урок 3: Четыре линзы риска
- `l03_zone_map.svg` - Урок 3: Green / Yellow / Red map
- `l03_final_card.svg` - Урок 3: Действие после урока
- `l04_title_card.svg` - Урок 4: Как выбрать первые сценарии для AI
- `l04_filter_matrix.svg` - Урок 4: Матрица выбора стартового сценария
- `l04_good_vs_bad_start.svg` - Урок 4: Хороший и плохой первый сценарий
- `l04_go_no_go.svg` - Урок 4: Go / No-Go filter на одном экране
- `l04_final_card.svg` - Урок 4: Действие после урока

## Примечание

Пакет собран только внутри isolated-папки и опирается на канонический concrete pack для уроков 2-4.
