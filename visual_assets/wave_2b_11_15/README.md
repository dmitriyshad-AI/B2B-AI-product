# Wave 2B Visual Assets

Дата: 21 марта 2026
Статус: рабочий пакет визуальных материалов для уроков 11-15

## Что внутри

- `build_wave_2b_assets.py` — генератор SVG в технике первой волны, но под пакет уроков 11-15.
- `wave_2b_slides_outline.md` — карта deck по 5 урокам.
- `wave_2b_slide_copy.md` — точный текст и роль каждого экрана.
- `wave_2b_diagrams.md` — Mermaid-схемы для process-логики.
- SVG-файлы — реальные slide assets для записи и черновой монтаж.

## Порядок работы

1. Открыть `wave_2b_slides_outline.md`.
2. Перейти к нужному SVG-asset.
3. При записи сверять смысл и формулировки с `wave_2b_slide_copy.md`.
4. Для process-мостов между экранами использовать `wave_2b_diagrams.md`.
5. При правках контента пересобрать SVG командой `python3 build_wave_2b_assets.py`.

## Карта SVG-файлов

- `l11_title_card.svg` — Урок 11: Почему AI выглядит уверенным даже когда ошибается
- `l11_sales_summary_compare.svg` — Урок 11: Кейс sales summary с ложной уверенностью
- `l11_false_confidence_breakdown.svg` — Урок 11: Разбор ошибки по строкам
- `l11_check_before_send.svg` — Урок 11: Проверка перед отправкой, 4 вопроса к гладкому ответу
- `l11_final_card.svg` — Урок 11: Действие после урока
- `l12_title_card.svg` — Урок 12: Чек-лист проверки качества
- `l12_quality_checklist.svg` — Урок 12: One-screen checklist из 6 критериев
- `l12_pilot_review_scorecard.svg` — Урок 12: Где summary ломается на кейсе пилота
- `l12_summary_before_after.svg` — Урок 12: До и после проверки
- `l12_final_card.svg` — Урок 12: Действие после урока
- `l13_title_card.svg` — Урок 13: Когда нельзя копировать ответ как есть
- `l13_risk_map.svg` — Урок 13: Green / Yellow / Red map
- `l13_red_zone_client_promise.svg` — Урок 13: Красная зона на кейсе обещания клиенту
- `l13_zone_classifier.svg` — Урок 13: Workflow разметки задач по зонам риска
- `l13_final_card.svg` — Урок 13: Действие после урока
- `l14_title_card.svg` — Урок 14: Как превращать сырой AI-черновик в рабочий результат
- `l14_status_update_before_after.svg` — Урок 14: Before / after status update
- `l14_edit_moves_workflow.svg` — Урок 14: 5 движений до рабочего результата
- `l14_edit_breakdown.svg` — Урок 14: Что изменили и зачем
- `l14_final_card.svg` — Урок 14: Действие после урока
- `l15_title_card.svg` — Урок 15: Минимальная цифровая гигиена и безопасность
- `l15_safe_vs_unsafe_prompt.svg` — Урок 15: Безопасный и небезопасный prompt
- `l15_safety_rules_checklist.svg` — Урок 15: 5 правил безопасной работы
- `l15_do_dont.svg` — Урок 15: Do / Don't экран
- `l15_final_card.svg` — Урок 15: Действие после урока

## Примечание

Пакет собран на конкретных case IDs для уроков 11-15 и намеренно опирается на реальные сценарии: risk maps, checklists, before / after, do / don't, workflow diagrams и final cards с жестким действием.
