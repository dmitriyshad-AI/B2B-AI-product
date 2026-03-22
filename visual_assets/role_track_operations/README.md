# Visual Pack: Ролевой трек Operations / Project / Knowledge Work

Этот пакет собран только на базе двух source-файлов:
- `/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/ролевой_трек_операции_и_интеллектуальная_работа.md`
- `/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/ролевой_трек_операции_и_интеллектуальная_работа_прикладной_пакет.md`

## Что внутри

- `slides_outline.md` — покадровая структура по 5 модулям.
- `slide_copy.md` — готовый on-screen copy для title, framework/before-after и final screens.
- `diagrams.md` — описание логики диаграмм и layout notes.
- `15 SVG assets` — по 3 ассета на каждый модуль: `title card`, `main screen`, `final card`.

## Production logic

- Формат всех SVG: `1600 x 900`.
- Язык экранов: русский.
- В каждом модуле есть один главный one-screen visual:
  - `R1` — framework screen с переходом от сырого запроса к `task breakdown canvas`;
  - `R2` — before/after экран для `signal-first update`;
  - `R3` — screen для `prep note` и `follow-up`;
  - `R4` — option/risk matrix;
  - `R5` — personal ops AI pipeline table.
- Во всех модулях явно сохранен принцип из source: AI ускоряет мышление и черновики, но ответственность остается у человека.

## Asset map

| Модуль | Title card | Main screen | Final card |
| --- | --- | --- | --- |
| `R1` | `r1_title_card.svg` | `r1_launch_breakdown_screen.svg` | `r1_final_card.svg` |
| `R2` | `r2_title_card.svg` | `r2_status_update_before_after.svg` | `r2_final_card.svg` |
| `R3` | `r3_title_card.svg` | `r3_meeting_prep_followup_screen.svg` | `r3_final_card.svg` |
| `R4` | `r4_title_card.svg` | `r4_options_risk_matrix.svg` | `r4_final_card.svg` |
| `R5` | `r5_title_card.svg` | `r5_personal_ops_pipeline.svg` | `r5_final_card.svg` |

## Использование в монтаже

1. `A-roll hook` и `A-roll close` остаются в скрипте ведущего.
2. `Title card` открывает модуль и фиксирует главную формулу.
3. `Main screen` держит центральный demo beat и работает как опорная схема.
4. `Final card` закрывает урок, повторяет главный тезис и домашнее действие.

## Состав файлов

### Markdown

- `README.md`
- `slides_outline.md`
- `slide_copy.md`
- `diagrams.md`

### SVG

- `r1_title_card.svg`
- `r1_launch_breakdown_screen.svg`
- `r1_final_card.svg`
- `r2_title_card.svg`
- `r2_status_update_before_after.svg`
- `r2_final_card.svg`
- `r3_title_card.svg`
- `r3_meeting_prep_followup_screen.svg`
- `r3_final_card.svg`
- `r4_title_card.svg`
- `r4_options_risk_matrix.svg`
- `r4_final_card.svg`
- `r5_title_card.svg`
- `r5_personal_ops_pipeline.svg`
- `r5_final_card.svg`
