# Wave 2 Visual Pack

Дата: 21 марта 2026
Статус: рабочий пакет визуальных материалов для уроков 6-10

## Что внутри

- `build_wave_2_assets.py` - генератор пакета.
- `wave_2_slides_outline.md` - карта deck по урокам 6-10.
- `wave_2_slide_copy.md` - точная copy-опора по каждому экрану.
- `wave_2_diagrams.md` - Mermaid-схемы для workflow и process-логики.
- SVG-файлы - реальные assets для черновой монтаж, review и записи.

## Покрытие

- 25 SVG-assets: по 5 экранов на каждый урок с 6 по 10.
- Внутри пакета есть title cards, final cards, comparison screens, framework slides, tables и workflow diagrams.
- Все экраны привязаны к уже собранным case IDs: `L06-CASE-A`, `L07-CASE-A`, `L08-CASE-A`, `L09-CASE-A`, `L10-TEMPLATE-SET-A`.

## Как пересобрать

`python3 build_wave_2_assets.py`

## Карта SVG-файлов

- `l06_title_card.svg` - Урок 6: Формула хорошего запроса
- `l06_formula_4_plus_2.svg` - Урок 6: Формула 4+2 на одном экране
- `l06_weak_vs_strong_followup.svg` - Урок 6: Слабый запрос против рабочего запроса
- `l06_followup_build_flow.svg` - Урок 6: Как собираем follow-up по кейсу L06-CASE-A
- `l06_final_card.svg` - Урок 6: Действие после урока
- `l07_title_card.svg` - Урок 7: Роль, аудитория и уместность
- `l07_role_vs_audience.svg` - Урок 7: Роль ради роли против уместного результата
- `l07_audience_tone_structure.svg` - Урок 7: Аудитория -> Тон -> Структура
- `l07_three_versions_compare.svg` - Урок 7: Одна новость, три версии сообщения
- `l07_final_card.svg` - Урок 7: Действие после урока
- `l08_title_card.svg` - Урок 8: Как разбивать сложную задачу на шаги
- `l08_one_shot_vs_decomposition.svg` - Урок 8: Один большой запрос против декомпозиции
- `l08_decomposition_workflow.svg` - Урок 8: Пятишаговая декомпозиция кейса L08-CASE-A
- `l08_checkpoint_table.svg` - Урок 8: Checkpoint-вопросы по каждому этапу
- `l08_final_card.svg` - Урок 8: Действие после урока
- `l09_title_card.svg` - Урок 9: Почему не существует волшебного промпта
- `l09_myth_vs_iterations.svg` - Урок 9: Миф о волшебном промпте против нормальной работы
- `l09_iteration_cycle.svg` - Урок 9: Итерационный цикл на одном экране
- `l09_summary_iterations_compare.svg` - Урок 9: Три итерации одного weekly summary
- `l09_final_card.svg` - Урок 9: Действие после урока
- `l10_title_card.svg` - Урок 10: Как собирать свои рабочие шаблоны
- `l10_template_structure.svg` - Урок 10: Структура рабочего шаблона
- `l10_template_library_table.svg` - Урок 10: Три первых шаблона в личной библиотеке
- `l10_personal_to_team_bridge.svg` - Урок 10: Как личный шаблон превращается в командный
- `l10_final_card.svg` - Урок 10: Действие после урока

## Примечание

Пакет собран как isolated visual workspace для review и записи уроков 6-10 и не меняет файлы за пределами этой папки.
