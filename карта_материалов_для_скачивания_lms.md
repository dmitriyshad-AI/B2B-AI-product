# Карта материалов для скачивания LMS

Дата: 21 марта 2026
Статус: конкретная карта форм и материалов для скачивания базового модуля

## 1. Как читать карту

Статусы:

1. `form_ready`
- это встроенная форма LMS;
- отдельный файл не обязателен.

2. `copy_ready`
- текст и структура готовы;
- можно собирать PDF, DOCX или LMS handout без допридумывания.

3. `exported_html`
- есть реальный HTML-материал в репозитории;
- можно сразу загружать в LMS или печатать в PDF.

4. `linked_to_source`
- материал уже существует в исходном документе;
- достаточно выдать его как чистый материал для скачивания.

Ни один `downloadable_id` из manifest не должен оставаться без строки в этой карте.

Основной копибук для материалов:
- [копибук_материалов_для_скачивания_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/копибук_материалов_для_скачивания_базового_модуля.md)

## 2. Карта материалов

| ID материала для скачивания | Название в LMS | Имя файла по умолчанию | Единый источник истины | Используется в item | Формат выдачи | Что должно быть внутри | Статус |
|---|---|---|---|---|---|---|---|
| `form-diag-in` | Входная самодиагностика | `core-module-input-diagnostic` | [диагностические_формы_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/диагностические_формы_базового_модуля.md), форма 1 | `diag_in` | встроенная форма LMS | 7 вопросов про роль, текущий опыт, барьеры и 3 задачи на ускорение | `form_ready` |
| `dl-s00-baseline-compare` | Сравнение до / после: первая рабочая задача | `core-baseline-compare` | [диагностические_формы_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/диагностические_формы_базового_модуля.md), форма 2 | `baseline` | встроенная форма LMS или PDF-материал | исходная версия без AI, версия после улучшенного запроса, наблюдаемое улучшение, ручная проверка, первая практическая победа | `form_ready` |
| `dl-l01-first-win-card` | Карточка фиксации первой практической победы | `core-first-win-card` | [артефакты_результата_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/артефакты_результата_базового_модуля.md), раздел 3 | `s00`, `l01` | 1-page PDF или материал в LMS | название задачи, исходная версия, версия с AI, что стало лучше, что еще проверять | `exported_html` |
| `dl-hw01-task-map` | Шаблон HW1: карта задач для ускорения | `core-task-map-template` | [шаблоны_домашних_заданий_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/шаблоны_домашних_заданий_базового_модуля.md), HW1 | `l04`, `hw01` | DOCX, PDF или editable sheet | таблица 10 задач, оценка по частоте, времени, риску, пользе, shortlist 3-5 сценариев | `linked_to_source` |
| `dl-l06-prompt-formula-card` | Формула сильного запроса | `core-prompt-formula-card` | [шаблоны_домашних_заданий_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/шаблоны_домашних_заданий_базового_модуля.md), HW2 intro | `l05`, `l06` | 1-page PDF | цель, контекст, аудитория, формат, критерии, ограничения, пример слабого и улучшенного запроса | `exported_html` |
| `dl-hw02-prompt-library` | Шаблон HW2: библиотека рабочих запросов | `core-prompt-library-template` | [шаблоны_домашних_заданий_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/шаблоны_домашних_заданий_базового_модуля.md), HW2 | `l10`, `hw02` | DOCX или рабочий лист в LMS | 5 карточек с задачей, слабым запросом, улучшенным запросом, выводом и правилом повторения | `linked_to_source` |
| `dl-l12-quality-checklist` | Чек-лист проверки качества AI-ответа | `core-quality-checklist` | [шаблоны_домашних_заданий_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/шаблоны_домашних_заданий_базового_модуля.md), HW3 | `l12`, `hw03` | PDF-материал и текстовый блок LMS | 6 критериев: факты, логика, полнота, тон, применимость, риск | `exported_html` |
| `dl-l15-safe-use-rules` | Минимальные правила безопасного использования | `core-safe-use-rules` | [артефакты_результата_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/артефакты_результата_базового_модуля.md), раздел 4 и 5 | `l15` | 1-page PDF | что нельзя загружать, где обязательна проверка человеком, где нужны внутренние правила | `exported_html` |
| `dl-l16-follow-up-template` | Шаблон письма по итогам встречи | `core-follow-up-template` | [мини_проект_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/мини_проект_базового_модуля.md), сильный сценарий follow-up | `l16` | DOCX или PDF | входные факты встречи, запрос, чек-лист: следующий шаг, ответственный, срок, тон | `exported_html` |
| `dl-l17-summary-template` | Шаблон краткой выжимки из документа или заметок | `core-summary-template` | [пакет_b2b_отчетности_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/пакет_b2b_отчетности_базового_модуля.md), логика краткой выжимки | `l17` | DOCX или PDF | цель выжимки, факты, решения, риски, открытые вопросы, следующий шаг | `exported_html` |
| `dl-l18-meeting-prep-canvas` | Canvas подготовки к встрече | `core-meeting-prep-canvas` | [мини_проект_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/мини_проект_базового_модуля.md), формат сценария | `l18` | editable worksheet | цель встречи, участники, контекст, ключевые вопросы, риски, desired outcome | `exported_html` |
| `dl-l19-outline-canvas` | Canvas структуры и черновика | `core-outline-canvas` | [шаблоны_домашних_заданий_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/шаблоны_домашних_заданий_базового_модуля.md), LMS submission shape | `l19` | editable worksheet | задача, желаемая структура, блоки, тон, что проверять вручную | `exported_html` |
| `dl-l20-research-note-template` | Шаблон первичной исследовательской заметки | `core-research-note-template` | [пакет_b2b_отчетности_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/пакет_b2b_отчетности_базового_модуля.md), логика сравнения | `l20` | DOCX или таблица | гипотезы, вопросы, потенциальные источники, что уже подтверждено, что требует проверки источника | `exported_html` |
| `dl-l21-learning-guide` | Гайд: как учиться с AI без самообмана | `core-learning-with-ai-guide` | [система_оценки_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/система_оценки_базового_модуля.md), outcome 5 | `l21` | PDF-материал | как задавать вопросы, проверять понимание, не подменять источники ответами модели | `exported_html` |
| `dl-hw04-scenario-library` | Шаблон HW4: личная библиотека сценариев | `core-scenario-library-template` | [шаблоны_домашних_заданий_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/шаблоны_домашних_заданий_базового_модуля.md), HW4 | `hw04`, `l23` | DOCX или sheet | 5 сценариев с входом, шаблоном, шагом проверки и ожидаемым результатом | `linked_to_source` |
| `dl-l24-rollout-canvas` | Canvas плана внедрения на 14 дней | `core-rollout-canvas` | [артефакты_результата_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/артефакты_результата_базового_модуля.md), раздел 5 | `l24` | 1-page worksheet | 3 приоритетных сценария, owner, ожидаемая польза, способ измерения, дата review | `exported_html` |
| `dl-hw05-14-day-plan` | Шаблон HW5: личный план внедрения | `core-14-day-plan-template` | [шаблоны_домашних_заданий_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/шаблоны_домашних_заданий_базового_модуля.md), HW5 | `hw05` | DOCX или LMS worksheet | 3 сценария, где применяю, как часто, какую пользу жду, как измеряю, план по дням | `linked_to_source` |
| `dl-project-submission-template` | Шаблон итогового мини-проекта | `core-mini-project-template` | [мини_проект_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/мини_проект_базового_модуля.md), раздел 5 | `project` | DOCX или встроенный гид задания в LMS | исходная версия, рабочая последовательность, AI-черновик, чек-лист, ручные правки, финальная версия, правило повторения, следующий шаг на 14 дней | `linked_to_source` |
| `form-diag-out` | Выходная самодиагностика | `core-module-output-diagnostic` | [диагностические_формы_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/диагностические_формы_базового_модуля.md), форма 3 | `diag_out` | встроенная форма LMS | 3-5 сценариев, наблюдаемая польза, барьеры, лучший артефакт результата, что сохранится через 14 дней | `form_ready` |

## 3. Минимальный QA для материалов

1. Каждому required item из manifest соответствует ровно один `primary_downloadable_id`.
2. Материал для скачивания можно открыть из карточки без перехода в сторонний контекст.
3. Название в LMS совпадает с названием в карте или отличается только ради длины интерфейса.
4. У материалов первый экран сразу показывает поля, которые участник должен заполнить.
5. У forms нет лишних "опишите что-нибудь"; каждый вопрос собирает конкретные данные под assessment или pilot report.
