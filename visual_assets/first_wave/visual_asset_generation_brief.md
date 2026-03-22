# Visual Asset Generation Brief

Дата: 20 марта 2026
Статус: brief для генерации презентаций, схем и экранных assets

## Цель

Собрать первый полноценный пакет визуальных материалов для первой волны записи:
- сессия 0;
- урок 1;
- урок 5;
- урок 11;
- урок 16;
- урок 24.

## Главные источники

1. [1_программа_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/1_программа_базового_модуля.md)
2. [2_день_1_заморозка_продакшна_и_список_недостающих_материалов.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/2_день_1_заморозка_продакшна_и_список_недостающих_материалов.md)
3. [3_пакет_перед_записью.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/3_пакет_перед_записью.md)
4. [4_пакет_демо_кейсов_для_записи.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/4_пакет_демо_кейсов_для_записи.md)
5. [диагностические_формы_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/диагностические_формы_базового_модуля.md)
6. [сессия_0_съемочный_сценарий_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/сессия_0_съемочный_сценарий_базового_модуля.md)
7. [уроки_1_5_съемочные_сценарии_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/уроки_1_5_съемочные_сценарии_базового_модуля.md)
8. [уроки_11_15_съемочные_сценарии_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/уроки_11_15_съемочные_сценарии_базового_модуля.md)
9. [уроки_16_20_съемочные_сценарии_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/уроки_16_20_съемочные_сценарии_базового_модуля.md)
10. [уроки_21_24_съемочные_сценарии_базового_модуля.md](/Users/dmitrijfabarisov/Projects/Dmitriy+Arseniy AI corp course/уроки_21_24_съемочные_сценарии_базового_модуля.md)

## Что нужно собрать

### 1. Master deck outline

Файл:
- `visual_assets/first_wave/first_wave_slides_outline.md`

Содержимое:
- состав deck по 6 единицам;
- список слайдов по каждому уроку;
- назначение каждого слайда;
- source case ID для каждого слайда.

### 2. Готовые тексты слайдов

Файл:
- `visual_assets/first_wave/first_wave_slide_copy.md`

Содержимое:
- заголовок каждого слайда;
- body copy;
- callout;
- подписи;
- таблицы и списки в финальной форме.

### 3. Схемы и диаграммы

Файл:
- `visual_assets/first_wave/first_wave_diagrams.md`

Содержимое:
- схемы в Mermaid или другом plain-text-friendly формате;
- где именно используются;
- короткая инструкция, как экспортировать.

### 4. Реальные slide assets

Нужно создать набор файлов в `visual_assets/first_wave/`:
- `s00_*.svg`
- `l01_*.svg`
- `l05_*.svg`
- `l11_*.svg`
- `l16_*.svg`
- `l24_*.svg`

Предпочтительно:
- `SVG` для слайдов и схем;
- `Markdown` или `HTML` для deck notes;
- один `README.md` с картой файлов.

### 5. Картинки / иллюстрации

Если делаются картинки, то только в деловом, учебном стиле:
- без декоративного шума;
- без generic stock-like nonsense;
- без художественной фантазии ради красоты.

Лучший формат:
- инфографика;
- clean SVG;
- таблица;
- process diagram;
- comparison screen;
- metric block.

## Ограничения

1. Не переписывать архитектуру курса.
2. Не менять case IDs.
3. Не придумывать новые content-case без явной необходимости.
4. Не заменять деловые учебные материалы художественными картинками.
5. Не трогать чужие файлы вне `visual_assets/first_wave/`, кроме точечных необходимых ссылок или README.

## Критерий качества

Пакет считается сильным, если:
1. по каждой из 6 единиц есть хотя бы 3-5 реальных экранных assets;
2. по ним можно записывать урок без импровизации;
3. они выглядят как материалы для серьезного бизнес-курса, а не как черновые заметки;
4. они привязаны к уже собранным case IDs и сценариям;
5. владельцу проекта понятно, что ревьюить.
