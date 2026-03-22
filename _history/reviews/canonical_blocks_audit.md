# Аудит канонических блоков

Дата: 20 марта 2026
Статус: локальный аудит перед точечной доработкой

## Общий вывод

Канонический контур уже достаточно сильный, чтобы на нем работать дальше.

Главные слабые места сейчас лежат не в содержании уроков, а в четырех зонах:
- документы местами все еще написаны как “черновики”;
- assessment и proof artifacts недостаточно операционализированы;
- LMS и production-документы не везде жестко разводят внутренний QA и внешний pilot-ready контур;
- B2B-слой и pilot briefs еще можно сделать более прикладными для owner и ЛПР.

## P0-правки

### P0. Сделать assessment framework более операционным

Файл:
- [core_module_assessment_framework.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/core_module_assessment_framework.md)

Что не хватает:
- уровней оценки;
- быстрого стандарта для ручной проверки;
- формы вывода для B2B-отчета.

### P0. Усилить proof artifacts как обязательный pipeline, а не описание идей

Файл:
- [core_module_proof_artifacts.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/core_module_proof_artifacts.md)

Что не хватает:
- owner каждого артефакта;
- точки появления;
- обязательного минимального формата;
- экспортируемости в пилот и продажу.

### P0. Развести внутренний LMS QA-контур и внешний pilot-ready контур

Файлы:
- [lms_assembly_package.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/lms_assembly_package.md)
- [launch_protocol_recording_and_lms.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/launch_protocol_recording_and_lms.md)

Что не хватает:
- ясного разграничения состояний готовности;
- stop-rules перед внешним пилотом;
- минимального набора, который уже можно показывать участникам.

## P1-правки

### P1. Довести syllabus до состояния канонического backbone, а не черновика

Файл:
- [1_core_module_syllabus.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/1_core_module_syllabus.md)

Что не хватает:
- статуса канонического документа;
- связи с MVP- и pilot-safe контуром;
- финального definition of done по модулю.

### P1. Усилить pilot package и briefs под реальный запуск

Файлы:
- [pilot_package.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/pilot_package.md)
- [pilot_participant_brief.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/pilot_participant_brief.md)
- [pilot_company_owner_brief.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/pilot_company_owner_brief.md)

Что не хватает:
- четкого launch gate;
- фиксированного таймлайна;
- ролей и обязательств;
- ясного финального решения по итогам пилота.

### P1. Усилить корпоративный слой до более продаваемого и управляемого состояния

Файлы:
- [company_layer_kit.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/company_layer_kit.md)
- [manager_layer_lite.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/manager_layer_lite.md)
- [role_track_operations_knowledge_work.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/role_track_operations_knowledge_work.md)

Что не хватает:
- канонического статуса;
- более четкого результата для заказчика;
- минимального набора файлов и артефактов для продажи и пилота.

## Что не требует правок сейчас

1. Основная логика Core lesson packs.
2. Production-пакет для записи как таковой.
3. Общая архитектура продукта в [program_architecture.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/program_architecture.md).
4. 10-дневный action list.

## Практический вывод

Правильный ход сейчас:
1. внести P0 в assessment, proof artifacts и LMS / launch docs;
2. затем закрыть P1 в syllabus, pilot docs и B2B-слое;
3. после этого прогнать обновленный контур через коллегию и внешний review.
