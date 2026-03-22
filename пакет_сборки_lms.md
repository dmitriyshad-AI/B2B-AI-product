# LMS Assembly Package

Дата: 21 марта 2026
Статус: максимально прикладной сборочный spec для базовый модуль в LMS

## 0. Главное правило

Этот файл — единственный `единый источник истины` для LMS build.

Остальные LMS-файлы используются как приложения:
- [манифест_lms_базового_модуля.csv](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/манифест_lms_базового_модуля.csv)
- [карточки_уроков_lms.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/карточки_уроков_lms.md)
- [карта_материалов_для_скачивания_lms.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/карта_материалов_для_скачивания_lms.md)
- [шаблоны_домашних_заданий_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/шаблоны_домашних_заданий_базового_модуля.md)
- [диагностические_формы_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/диагностические_формы_базового_модуля.md)

Если между LMS-документами есть расхождение, верить нужно этому файлу.

## 1. Назначение пакета

Этот пакет нужен, чтобы собрать базовый модуль в LMS как управляемый продукт:
- с понятным learner path;
- с явными unlock rules;
- с конкретными карточками уроков;
- с готовым mapping скачиваемых материалов;
- с publish-gates перед внешним пилотом.

Если по этому пакету нельзя собрать контур без устных пояснений, пакет считается недособранным.

## 2. Опорные приложения для сборки

1. [манифест_lms_базового_модуля.csv](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/манифест_lms_базового_модуля.csv)
2. [карточки_уроков_lms.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/карточки_уроков_lms.md)
3. [карта_материалов_для_скачивания_lms.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/карта_материалов_для_скачивания_lms.md)
4. [шаблоны_домашних_заданий_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/шаблоны_домашних_заданий_базового_модуля.md)
5. [артефакты_результата_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/артефакты_результата_базового_модуля.md)
6. [диагностические_формы_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/диагностические_формы_базового_модуля.md)
7. [система_оценки_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/система_оценки_базового_модуля.md)

## 3. Publish contour по разделам

| LMS-раздел | Что входит | Unlock rule | Что обязательно должно работать | Publish gate |
|---|---|---|---|---|
| Раздел 0. Старт | `diag_in`, `baseline`, `s00` | открывается при зачислении | участник без фасилитатора видит форму входной диагностики, сравнение до / после и первая практическая победа path | нельзя публиковать, если participant не понимает, что сдавать первым экраном |
| Модуль 1. Выбор задач | `l01-l05`, `hw01` | после `s00` и `baseline` | у уроков есть concrete action, у `hw01` есть таблица задач и критерии выбора | нельзя публиковать, если `hw01` нельзя проверить за 2 минуты |
| Модуль 2. Prompting | `l06-l10`, `hw02` | после принятия `hw01` | формула сильного запроса и library template выданы как материалы для скачивания | нельзя публиковать, если `hw02` не показывает weak vs improved prompt |
| Модуль 3. Проверка качества | `l11-l15`, `hw03` | после принятия `hw02` | quality checklist и safe-use rules доступны прямо из карточек | нельзя публиковать, если проверяющий не видит риск и ручную доработку |
| Модуль 4. Рабочие сценарии | `l16-l20`, `hw04` | после принятия `hw03` | минимум 5 прикладных кейсов имеют свои canvases или templates | `hw04` можно оставить optional, но сценарный слой должен быть собран |
| Модуль 5. Закрепление | `l21-l24`, `hw05`, `project`, `diag_out` | после `l20`; `project` открывается только после `hw05` | есть план внедрения, project submission shape и выходная диагностика | нельзя публиковать, если mini-project path непонятен без устных инструкций |

## 4. Обязательный состав карточки урока

Каждая lesson card в LMS должна содержать ровно эти поля:

1. Название урока.
2. Длительность в минутах.
3. Короткое описание на 180-260 знаков:
- не "вы узнаете про AI";
- а что участник сделает на своей рабочей задаче.
4. Блок `После урока вы сможете`:
- 2 конкретных результата;
- без общих формулировок.
5. `Главная мысль урока`:
- одна фраза;
- без теоретических абстракций.
6. `Сделайте сразу после урока`:
- один императив;
- одно наблюдаемое действие.
7. `Self-check`:
- 2 вопроса;
- каждый проверяет действие, а не мнение.
8. `Downloadable`:
- конкретный `downloadable_id`;
- либо `none`, если материал не нужен.
9. `Completion rule`:
- для lessons: просмотр + ответы на 2 self-check;
- для graded items: отправка шаблона в заданном submission shape.

Готовый copy для всех уроков находится в:
- [карточки_уроков_lms.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/карточки_уроков_lms.md)

## 5. Unlock rules и gating logic

| Gate ID | Что проверяет | Что открывает | Если gate не пройден |
|---|---|---|---|
| `gate_start_block_complete` | `diag_in` + `baseline` + `s00` завершены | Модуль 1 | участник остается в стартовом блоке |
| `gate_hw01_pass` | `hw01` принят по шаблону | Модуль 2 | модуль 2 закрыт, пока нет карты задач |
| `gate_hw02_pass` | `hw02` показывает минимум 3 сильных prompt upgrade | Модуль 3 | участник не идет дальше без рабочего prompting layer |
| `gate_hw03_pass` | `hw03` показывает проверку и ручную доработку | Модуль 4 | путь блокируется, чтобы не тащить forward blind copy-paste |
| `gate_module4_complete` | `l16-l20` завершены | Модуль 5 | `hw04` optional, но lessons 16-20 обязательны |
| `gate_hw05_pass` | `hw05` сдан с 3 сценариями и 14-day plan | `project` | финальный проект не открывается без rollout logic |
| `gate_project_submitted` | `project` отправлен | `diag_out` | участник не завершает курс без финальной сдачи |

## 6. Downloadables pack для первого релиза

В первый релиз обязательно входят:

1. `form-diag-in`
2. `dl-s00-baseline-compare`
3. `dl-l01-first-win-card`
4. `dl-hw01-task-map`
5. `dl-l06-prompt-formula-card`
6. `dl-hw02-prompt-library`
7. `dl-l12-quality-checklist`
8. `dl-l15-safe-use-rules`
9. `dl-l16-follow-up-template`
10. `dl-l17-summary-template`
11. `dl-l18-meeting-prep-canvas`
12. `dl-l19-outline-canvas`
13. `dl-l20-research-note-template`
14. `dl-hw04-scenario-library`
15. `dl-l24-rollout-canvas`
16. `dl-hw05-14-day-plan`
17. `dl-project-submission-template`
18. `form-diag-out`

Полный build mapping, форматы и source sections перечислены в:
- [карта_материалов_для_скачивания_lms.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/карта_материалов_для_скачивания_lms.md)

## 7. Статусы сборки

Используем только эти статусы:

1. `copy_ready`
- текст карточки или формы готов;
- можно переносить в LMS без допридумывания.

2. `asset_mapped`
- есть понятный единый источник истины;
- есть конкретный материал для скачивания id и место использования.

3. `needs_media_link`
- copy готов;
- не хватает только рабочей ссылки на видео или файл.

4. `publish_ready`
- item прошел QA;
- participant path и материал для скачивания path работают.

5. `blocked`
- item нельзя выпускать наружу;
- есть разрыв в copy, форме, материал для скачивания или gating logic.

## 8. Порядок сборки в LMS

1. Создать разделы и порядок items строго по [манифест_lms_базового_модуля.csv](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/манифест_lms_базового_модуля.csv).
2. Перенести card copy из [карточки_уроков_lms.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/карточки_уроков_lms.md).
3. Собрать native LMS forms для `diag_in`, `baseline`, `diag_out`.
4. Подключить материалы для скачивания по [карта_материалов_для_скачивания_lms.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/карта_материалов_для_скачивания_lms.md).
5. Настроить unlock rules строго по gate table выше.
6. Пройти test-user path от зачисления до `hw01`.
7. Пройти second test-user path от `hw03` до `project`.
8. Перевести item в `publish_ready` только после двух проходов без устных пояснений.

## 9. QA-чеклист перед публикацией

1. У каждого item из manifest есть card copy, completion rule и материал для скачивания id или явное `none`.
2. Названия уроков в manifest, lesson cards и homework docs совпадают дословно.
3. У `hw01`, `hw02`, `hw03`, `hw05` и `project` первый экран показывает реальную рабочую задачу, а не общий текст.
4. Для `diag_in`, `baseline` и `diag_out` формы перенесены в native LMS fields.
5. У `s00`, `hw01`, `hw02`, `hw03`, `hw05` и `project` есть export-friendly submission shape.
6. Все required материалы для скачивания доступны из карточек без битых ссылок.
7. `hw04` помечена как optional и не ломает progression.
8. Participant может понять следующий шаг без сообщения от куратора.

## 10. Stop-rules перед внешним пилотом

Внешний пилот нельзя запускать, если выполняется хотя бы одно условие:

1. `diag_in -> baseline -> s00 -> hw01` нельзя пройти test-user'ом за один проход.
2. В manifest есть хотя бы один required item со статусом `blocked`.
3. У `hw01`, `hw02`, `hw03`, `hw05` или `project` нет ясного first-screen submission shape.
4. Хотя бы один обязательный материал для скачивания id есть в manifest, но отсутствует в `карта_материалов_для_скачивания_lms.md`.
5. Owner-side или participant-side briefing объясняет маршрут лучше, чем сам LMS.
