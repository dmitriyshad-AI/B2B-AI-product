# ROI-пакет B2B

Дата: 22 марта 2026
Статус: concrete-first пакет для ROI-разговора, калькулятора и CFO-ready интерпретации

## 1. Что считаем ROI, а что нет

Считаем только то, что можно привязать к baseline и рабочему сценарию:
1. экономию времени на кейс;
2. снижение доли переделок;
3. снижение цены ошибки или числа инцидентов;
4. высвобождение управляемой мощности команды.

Не считаем в первой волне:
1. обещанный рост выручки без подтвержденного сценария;
2. полный ROI компании;
3. "скрытую магию AI" без baseline;
4. влияние на EBITDA без owner и без данных.

## 2. ROI baseline form

```text
Компания:
Функция / команда:
Shared scenario:
Business owner:
Сколько кейсов в неделю:
Какой baseline period:
Сколько минут уходит на кейс сейчас:
Сколько минут уходит на доработку:
Какой текущий quality pass rate:
Сколько стоит час роли:
Какой capture rate считаем реалистичным:
Какие риски считаем деньгами:
Сколько стоит пилот для клиента:
Какой горизонт annualization:
```

## 3. Структура ROI-калькулятора

Собирайте калькулятор в трех листах:

### Лист `inputs`

| Поле | Что вводим |
|---|---|
| Company | название компании |
| Team | функция или команда |
| Scenario | один shared scenario |
| Business owner | кто принимает решение |
| Participants | размер группы |
| Active weeks per year | обычно `40-46` |
| Contract cost | цена пакета |
| Internal enablement cost | внутренние часы клиента на запуск |
| Manager hours | часы руководителя на pilot governance |
| Manager hourly cost | стоимость часа руководителя |
| Capture rate | какая доля сэкономленного времени реально превращается в полезную мощность |
| Confidence factor | коэффициент доверия к денежному сигналу `0.3-1.0` |

### Лист `scenario_metrics`

| Поле | Описание |
|---|---|
| Cases per week | сколько кейсов проходит по shared scenario за неделю |
| Baseline minutes per case | сколько минут уходит на кейс до пилота |
| Pilot minutes per case | сколько минут уходит на кейс на пилоте |
| Adoption rate | доля участников, реально использующих новый сценарий |
| Rework before | доля кейсов с существенной переделкой до пилота |
| Rework after | доля кейсов с существенной переделкой после пилота |
| Rework minutes per case | среднее время на переделку одного кейса |
| First-pass quality before | доля кейсов, проходящих с первого раза до пилота |
| First-pass quality after | доля кейсов, проходящих с первого раза после пилота |
| Incidents before per month | число ошибок / инцидентов в месяц до пилота |
| Incidents after per month | число ошибок / инцидентов в месяц после пилота |
| Cost per incident | средняя цена одного инцидента в рублях |
| Loaded hour cost | стоимость часа исполнителя |

### Лист `summary`

| Выход | Что показывает |
|---|---|
| Weekly time value | недельная стоимость высвобожденного времени |
| Weekly quality value | недельная стоимость сокращенной переделки |
| Monthly risk value | месячная стоимость предотвращенных ошибок |
| Annual gross value | годовой валовый эффект |
| Total program cost | все затраты на пилот и запуск |
| Net value | чистая стоимость после вычета затрат |
| ROI % | `(Net value / Total program cost) * 100` |
| Payback weeks | срок окупаемости в неделях |

## 4. Формулы калькулятора

### 4.1. Экономия времени

```text
Minutes saved per case = max(0, Baseline minutes per case - Pilot minutes per case)

Weekly saved hours =
Cases per week * Minutes saved per case / 60 * Adoption rate

Weekly realized hours =
Weekly saved hours * Capture rate

Weekly time value =
Weekly realized hours * Loaded hour cost
```

### 4.2. Снижение переделки

```text
Rework delta =
max(0, Rework before - Rework after)

Weekly rework hours saved =
Cases per week * Rework delta * Rework minutes per case / 60 * Adoption rate

Weekly quality value =
Weekly rework hours saved * Loaded hour cost
```

### 4.3. Снижение цены ошибки

```text
Monthly avoided incidents =
max(0, Incidents before per month - Incidents after per month)

Monthly risk value =
Monthly avoided incidents * Cost per incident * Confidence factor
```

### 4.4. Годовой эффект и ROI

```text
Annual gross value =
(Weekly time value + Weekly quality value) * Active weeks per year
+ Monthly risk value * 12

Total program cost =
Contract cost
+ Internal enablement cost
+ Manager hours * Manager hourly cost

Net value =
Annual gross value - Total program cost

ROI % =
Net value / Total program cost * 100

Payback weeks =
Total program cost / (Weekly time value + Weekly quality value + Monthly risk value / 4.33)
```

## 5. Консервативные правила расчета

1. `Capture rate` для первой волны ставим `0.35-0.60`, а не `1.00`.
2. Если adoption rate ниже `40%`, annualized ROI не показываем, только weekly signal.
3. Если нет baseline по времени, quality или incident cost, этот блок не монетизируем.
4. Если scenario volume плавает, берем худшую из двух последних недель.
5. Если эффект держится только на одном champion, считаем `confidence factor <= 0.5`.
6. Если есть red incident по безопасности, ROI не является аргументом к scale.

## 6. Пороговые зоны интерпретации

| Показатель | Green | Yellow | Red |
|---|---|---|---|
| Adoption rate | `>= 60%` | `40-59%` | `< 40%` |
| Weekly time value | устойчиво положительный | положительный, но сырой | около нуля |
| Weekly quality value | подтвержден выборкой | есть гипотеза, мало кейсов | нет сигнала |
| Payback weeks | `<= 26` | `27-52` | `> 52` |
| ROI % | `> 25%` | `0-25%` | `< 0%` |
| Confidence factor | `>= 0.7` | `0.5-0.69` | `< 0.5` |

## 7. Заполненный пример для коммерческой команды

### Входные данные

| Поле | Значение |
|---|---:|
| Cases per week | `120` |
| Baseline minutes per case | `35` |
| Pilot minutes per case | `20` |
| Adoption rate | `70%` |
| Capture rate | `50%` |
| Rework before | `35%` |
| Rework after | `20%` |
| Rework minutes per case | `10` |
| Incidents before per month | `2` |
| Incidents after per month | `1` |
| Cost per incident | `15 000 ₽` |
| Confidence factor | `0.5` |
| Loaded hour cost | `1 800 ₽` |
| Active weeks per year | `44` |
| Contract cost | `690 000 ₽` |
| Internal enablement cost | `35 000 ₽` |
| Manager hours | `22` |
| Manager hourly cost | `2 500 ₽` |

### Выход

| Метрика | Результат |
|---|---:|
| Weekly time value | `18 900 ₽` |
| Weekly quality value | `5 670 ₽` |
| Monthly risk value | `7 500 ₽` |
| Annual gross value | `1 171 080 ₽` |
| Total program cost | `780 000 ₽` |
| Net value | `391 080 ₽` |
| ROI % | `50.1%` |
| Payback weeks | `29.7` |

### Как интерпретировать пример

1. Это уже не "обещание роста выручки", а защищаемый operational ROI.
2. Основной вклад дает сокращение времени цикла, а не красивые revenue claims.
3. При payback `29.7` недель пилот еще требует дисциплины, но выглядит правдоподобно.
4. Если adoption упадет ниже `40%`, этот же расчет нельзя защищать перед CFO.

## 8. Что отдавать CFO / ЛПР из ROI-пакета

В финальный ROI-блок должны войти:
1. baseline table;
2. фактический summary по одному сценарию;
3. расчет `weekly value`, а не только annualized number;
4. допущения: capture rate, confidence factor, active weeks;
5. границы интерпретации: что еще не считаем деньгами.

Один обязательный вывод в конце:

`Мы не продаем гарантированный рост прибыли. Мы показываем, что на одном рабочем сценарии уже появился защищаемый экономический сигнал, который можно либо масштабировать, либо добрать второй волной.`
