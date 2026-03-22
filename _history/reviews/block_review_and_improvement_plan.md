# План проверки и доработки блоков

Дата: 20 марта 2026
Статус: рабочий план аудита и точечной доработки канонического контура

## Цель

Пройти по каноническим блокам проекта и довести их до состояния, в котором:
- ими можно реально пользоваться без устных пояснений;
- они поддерживают запись, LMS и пилот;
- в них нет лишней “черновиковости” и управленческой размытости.

## Принцип работы

Мы не переписываем проект заново.

Мы проходим по блокам и в каждом блоке ищем только такие правки, которые:
- снижают риск на production;
- упрощают сборку LMS;
- усиливают пилот и B2B-защиту результата;
- убирают двусмысленность в канонических документах.

## Блок 1. Архитектура продукта

Файлы:
- [program_architecture.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/program_architecture.md)
- [1_core_module_syllabus.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/1_core_module_syllabus.md)
- [role_track_operations_knowledge_work.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/role_track_operations_knowledge_work.md)
- [manager_layer_lite.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/manager_layer_lite.md)
- [company_layer_kit.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/company_layer_kit.md)

Критерии проверки:
- блоки сформулированы как продукты, а не идеи;
- есть границы между слоями;
- понятен MVP-контур;
- корпоративный слой не выглядит декларативным.

## Блок 2. Методика и оценивание

Файлы:
- [core_module_assessment_framework.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/core_module_assessment_framework.md)
- [core_module_proof_artifacts.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/core_module_proof_artifacts.md)
- [core_module_homework_templates.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/core_module_homework_templates.md)

Критерии проверки:
- домашки и assessment можно использовать в LMS и ручной проверке;
- proof artifacts собираются по умолчанию;
- у B2B есть понятный язык отчета и защиты результата.

## Блок 3. Production и LMS

Файлы:
- [3_pre_recording_package.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/3_pre_recording_package.md)
- [lms_assembly_package.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/lms_assembly_package.md)
- [launch_protocol_recording_and_lms.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/launch_protocol_recording_and_lms.md)
- [core_module_recording_board.csv](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/core_module_recording_board.csv)

Критерии проверки:
- различаются внутренний QA-контур и внешний pilot-ready контур;
- понятны go / no-go условия;
- документы помогают действовать, а не просто описывают желаемое состояние.

## Блок 4. Пилот и B2B-упаковка

Файлы:
- [pilot_package.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/pilot_package.md)
- [pilot_participant_brief.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/pilot_participant_brief.md)
- [pilot_company_owner_brief.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/pilot_company_owner_brief.md)
- [pilot_metrics_framework.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/pilot_metrics_framework.md)
- [pilot_report_template.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/pilot_report_template.md)

Критерии проверки:
- пилот можно реально запустить без импровизации;
- участник и owner понимают роли, сроки и выходы;
- по итогам пилота можно принять решение, а не просто собрать “обратную связь”.

## Порядок действий

1. Провести локальный аудит по всем 4 блокам.
2. Зафиксировать P0/P1 правки.
3. Внести правки в канонические файлы.
4. Прогнать обновленный контур через коллегию.
5. Сверить вывод коллегии с внешним review субагента.
6. Оставить только те правки, которые реально усиливают ближайший production sprint.

## Definition of done

Работа считается завершенной, если:
- по каждому блоку есть краткий audit verdict;
- все P0/P1 правки внесены в канонические файлы;
- коллегия считает обновленный контур пригодным для дальнейшего движения;
- не возник новый виток бесконечного переписывания.
