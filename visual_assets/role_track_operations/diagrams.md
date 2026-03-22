# Diagrams

## Общая система

- Все assets сделаны как standalone SVG экраны `1600 x 900`.
- На каждый модуль заложен один цветовой акцент и три типа экрана:
  - `title card`
  - `main screen`
  - `final card`
- Main screens несут конкретный рабочий объект из source: canvas, before/after, prep/follow-up board, option matrix, pipeline table.

## Title cards

Общая логика title cards:
- верхняя строка с номером модуля;
- крупный headline;
- под headline короткое обещание результата;
- внизу формула модуля;
- справа или снизу два чипа: `кейс` и `артефакт`.

Это дает единый сериализованный opening по всем пяти урокам.

## Final cards

Общая логика final cards:
- крупная closing phrase из ядра текста модуля;
- отдельный блок с домашним действием;
- маленький reminder, что AI не подменяет ответственность человека;
- визуальный мост к следующему шагу.

## `r1_launch_breakdown_screen.svg`

- Тип: `framework screen` с элементом `before -> after`.
- Layout:
  - слева карточка `сырой вход`;
  - по центру короткий мост пересборки;
  - справа сетка `task breakdown canvas` из 6 блоков.
- Concrete anchors из source:
  - пилот на `2 недели`;
  - группа `12 человек`;
  - `owner`, `kickoff`, `midpoint-check`, `final review`;
  - риск перегруза команды.

## `r2_status_update_before_after.svg`

- Тип: `before/after`.
- Layout:
  - слева перегруженный update;
  - справа короткий `signal-first update`;
  - внизу line о быстром чтении руководителем.
- Concrete anchors из source:
  - `4` направления работ;
  - `2` риска;
  - `1` сдвиг срока;
  - `3` next steps.

## `r3_meeting_prep_followup_screen.svg`

- Тип: `two-stage framework`.
- Layout:
  - левый блок `до встречи`;
  - центральный узел `созвон`;
  - правый блок `после встречи`.
- Concrete anchors из source:
  - несогласованность по срокам;
  - неясные owners двух блоков;
  - встреча должна закончиться решениями и next steps.

## `r4_options_risk_matrix.svg`

- Тип: `framework table`.
- Layout:
  - full-width matrix на `3` варианта;
  - шесть столбцов по формуле модуля;
  - внизу подпись про человеческое решение.
- Concrete anchors из source:
  - `больше синков`;
  - `база знаний и шаблоны`;
  - `короткий blended-подход`;
  - benefit, cost, risk, mitigation, fit.

## `r5_personal_ops_pipeline.svg`

- Тип: `system table`.
- Layout:
  - слева короткая проблема;
  - основная ширина занята pipeline-таблицей;
  - внизу мост от личной системы к team reuse.
- Concrete anchors из source:
  - `встречи`;
  - `статус-апдейты`;
  - `внутренние записки и summary`;
  - `input`, `prompt pattern`, `quality gate`, `output`, `storage`, `reuse`.

## Рекомендации по использованию

- Title cards держать на экране `2-4` секунды.
- Main screens можно разбирать с поэтапным zoom или pointer reveal.
- Final cards работают как чистое закрытие модуля и как стоп-кадр для homework.
