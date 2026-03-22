from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape


OUT = Path(__file__).resolve().parent

W = 1600
H = 900
BG = "#F6F1E8"
INK = "#10213B"
MUTED = "#5F6B7A"
ACCENT = "#C65A1E"
SAGE = "#5A7268"
PANEL = "#FFFDF8"
LINE = "#D7D0C1"


@dataclass
class Slide:
    filename: str
    unit: str
    title: str
    subtitle: str
    kind: str
    case_id: str
    payload: dict


def t(x: int, y: int, text: str, size: int = 28, fill: str = INK, weight: str = "400",
      family: str = "'Trebuchet MS', 'Segoe UI', sans-serif", max_chars: int | None = None,
      line_height: int | None = None) -> str:
    if line_height is None:
        line_height = int(size * 1.35)
    parts = [text] if max_chars is None else wrap(text, max_chars)
    tspans = []
    for idx, part in enumerate(parts):
        dy = "0" if idx == 0 else str(line_height)
        tspans.append(f'<tspan x="{x}" dy="{dy}">{escape(part)}</tspan>')
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-family="{family}" '
        f'font-weight="{weight}" fill="{fill}">{"".join(tspans)}</text>'
    )


def rect(x: int, y: int, w: int, h: int, fill: str = PANEL, stroke: str = LINE,
         rx: int = 28, sw: int = 2) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def pill(x: int, y: int, w: int, h: int, text: str, fill: str, text_fill: str = "white") -> str:
    return rect(x, y, w, h, fill=fill, stroke=fill, rx=h // 2) + t(x + 24, y + h - 18, text, 24, text_fill, "700")


def title_block(slide: Slide) -> str:
    return (
        t(90, 90, slide.unit, 24, ACCENT, "700")
        + t(90, 150, slide.title, 48, INK, "700", family="Georgia, serif", max_chars=38, line_height=56)
        + t(90, 220, slide.subtitle, 24, MUTED, "400", max_chars=82, line_height=34)
        + pill(1270, 70, 240, 54, slide.case_id, SAGE)
    )


def footer(slide: Slide) -> str:
    return (
        f'<line x1="90" y1="820" x2="1510" y2="820" stroke="{LINE}" stroke-width="2"/>'
        + t(90, 855, "Business-learning visual asset · Wave 1B", 20, MUTED)
        + t(1140, 855, slide.filename.replace(".svg", ""), 20, MUTED, "700")
    )


def render_card(slide: Slide) -> str:
    body = slide.payload["body"]
    kicker = slide.payload.get("kicker", slide.unit)
    accent = slide.payload.get("accent", ACCENT)
    note = slide.payload.get("note", "")
    out = [
        rect(90, 90, 1420, 720, fill="#FBF7EF", stroke=LINE, rx=40),
        pill(120, 120, 260, 52, kicker, accent),
        t(120, 250, slide.title, 58, INK, "700", family="Georgia, serif", max_chars=32, line_height=66),
        t(120, 360, slide.subtitle, 28, MUTED, "400", max_chars=70, line_height=36),
        rect(120, 460, 1360, 180, fill="white", stroke=LINE),
        t(160, 530, body, 34, INK, "700", max_chars=50, line_height=42),
    ]
    if note:
        out.append(t(120, 705, note, 22, MUTED, "400", max_chars=88, line_height=28))
    out.append(footer(slide))
    return "".join(out)


def render_grid(slide: Slide) -> str:
    cards = slide.payload["cards"]
    out = [title_block(slide)]
    positions = [(90, 280), (820, 280), (90, 520), (820, 520)]
    fills = ["#FFF7EF", "#EEF5F1", "#F7F5FD", "#F7F3EA"]
    accents = [ACCENT, SAGE, "#6A56A5", INK]
    for (x, y), card, fill, accent in zip(positions, cards, fills, accents):
        out.append(rect(x, y, 690, 180, fill=fill))
        out.append(t(x + 28, y + 52, card["title"], 28, accent, "700"))
        out.append(t(x + 28, y + 92, card["body"], 22, INK, max_chars=42, line_height=28))
    out.append(footer(slide))
    return "".join(out)


def render_split(slide: Slide) -> str:
    left = slide.payload["left"]
    right = slide.payload["right"]
    bottom = slide.payload.get("bottom")
    out = [
        title_block(slide),
        rect(90, 280, 650, 420, fill="#FFF7EF"),
        rect(860, 280, 650, 420, fill="#EEF5F1"),
        t(120, 330, left["title"], 30, ACCENT, "700"),
        t(890, 330, right["title"], 30, SAGE, "700"),
        t(120, 380, left["body"], 23, INK, max_chars=38, line_height=30),
        t(890, 380, right["body"], 23, INK, max_chars=38, line_height=30),
    ]
    if bottom:
        out.append(rect(90, 730, 1420, 70, fill=INK, stroke=INK))
        out.append(t(120, 776, bottom, 26, "white", "700", max_chars=88, line_height=30))
    out.append(footer(slide))
    return "".join(out)


def render_table(slide: Slide) -> str:
    headers = slide.payload["headers"]
    rows = slide.payload["rows"]
    col_widths = slide.payload["widths"]
    out = [title_block(slide), rect(90, 260, 1420, 500)]
    x = 90
    for idx, (header, width) in enumerate(zip(headers, col_widths)):
        fill = "#EFE7D8" if idx % 2 == 0 else "#E8F0EC"
        out.append(rect(x, 260, width, 70, fill=fill, stroke=LINE, rx=0))
        out.append(t(x + 16, 304, header, 22, INK, "700", max_chars=max(12, width // 12)))
        x += width
    y = 330
    for ridx, row in enumerate(rows):
        x = 90
        bg = PANEL if ridx % 2 == 0 else "#FCFAF4"
        for cell, width in zip(row, col_widths):
            out.append(rect(x, y, width, 58, fill=bg, stroke=LINE, rx=0, sw=1))
            out.append(t(x + 14, y + 36, cell, 19, INK, max_chars=max(10, width // 12), line_height=22))
            x += width
        y += 58
    out.append(footer(slide))
    return "".join(out)


def render_compare(slide: Slide) -> str:
    cols = slide.payload["columns"]
    out = [title_block(slide)]
    x_positions = [90, 570, 1050]
    fills = ["#F8F1E8", "#EEF5F1", "#FFF7EF"]
    accents = [MUTED, SAGE, ACCENT]
    for idx, col in enumerate(cols):
        out.append(rect(x_positions[idx], 280, 390, 420, fill=fills[idx]))
        out.append(t(x_positions[idx] + 26, 325, col["title"], 28, accents[idx], "700"))
        out.append(t(x_positions[idx] + 26, 370, col["body"], 22, INK, max_chars=29, line_height=28))
    if slide.payload.get("bottom"):
        out.append(rect(90, 730, 1420, 70, fill=INK, stroke=INK))
        out.append(t(120, 776, slide.payload["bottom"], 26, "white", "700", max_chars=88, line_height=30))
    out.append(footer(slide))
    return "".join(out)


def svg_wrap(body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f'<rect width="{W}" height="{H}" fill="{BG}"/>'
        f'{body}</svg>'
    )


slides = [
    Slide(
        "l02_title_card.svg",
        "Урок 2",
        "Где AI помогает быстрее всего",
        "Карта повторяющихся классов задач, где польза появляется быстро и проверяется легко.",
        "card",
        "CM-L02-TASK-MAP-A",
        {
            "kicker": "Урок 2",
            "body": "Ищите не один волшебный кейс, а 6 повторяющихся классов задач.",
        },
    ),
    Slide(
        "l02_task_class_map.svg",
        "Урок 2",
        "Шесть стартовых классов задач",
        "Не обзор AI вообще, а конкретная карта типовых рабочих задач.",
        "table",
        "CM-L02-TASK-MAP-A",
        {
            "headers": ["Класс задачи", "Пример", "Что AI делает быстро", "Что проверяет человек"],
            "widths": [250, 340, 400, 430],
            "rows": [
                ["Переписка", "follow-up после kickoff", "собирает первый черновик", "тон, факт, обещания"],
                ["Summary", "заметки после синка", "выносит суть и action items", "сроки, риски, полноту"],
                ["Встречи", "weekly sync с IT", "повестка и вопросы", "релевантность и контекст"],
                ["Структура", "внутренняя записка", "собирает skeleton документа", "логика и адресат"],
                ["Research", "вход в тему RAG", "строит карту темы", "источники и границы"],
                ["Self-learning", "объяснение cohort analysis", "упрощает сложную тему", "корректность терминов"],
            ],
        },
    ),
    Slide(
        "l02_three_examples.svg",
        "Урок 2",
        "Три первых сценария без перегруза",
        "На старте нужно видеть не теорию, а три быстрых примера пользы.",
        "grid",
        "CM-L02-TASK-MAP-A",
        {
            "cards": [
                {"title": "Summary документа", "body": "AI быстро вытаскивает суть, риски и action items из длинных заметок."},
                {"title": "Структура документа", "body": "AI помогает перейти от пустого листа к рабочему skeleton для записки или презентации."},
                {"title": "Подготовка к встрече", "body": "AI собирает повестку, вопросы и следующий шаг для weekly sync."},
                {"title": "Стартовый фильтр", "body": "Берите только то, что повторяется, понятно проверяется и не несет высокой цены ошибки."},
            ]
        },
    ),
    Slide(
        "l02_start_filter.svg",
        "Урок 2",
        "Фильтр первой пользы",
        "Не каждая полезная задача подходит для старта. Важны повторяемость, понятность и управляемый риск.",
        "split",
        "CM-L02-TASK-MAP-A",
        {
            "left": {
                "title": "Подходит для старта",
                "body": "Повторяется. Результат понятен. Польза видна быстро. Ошибку легко заметить до отправки или решения.",
            },
            "right": {
                "title": "Не подходит для старта",
                "body": "Высокая цена ошибки. Внешние обещания. Юридические формулировки. Чувствительные данные. Непрозрачный результат.",
            },
            "bottom": "Стартуйте там, где AI ускоряет задачу, но не ломает вам работу при первой ошибке.",
        },
    ),
    Slide(
        "l02_final_card.svg",
        "Урок 2",
        "Действие после урока",
        "Курс должен быстро перевести карту задач в личное решение ученика.",
        "card",
        "CM-L02-TASK-MAP-A",
        {
            "kicker": "После урока 2",
            "body": "Выберите 3 класса задач, которые чаще всего встречаются именно у вас.",
            "accent": SAGE,
        },
    ),
    Slide(
        "l03_title_card.svg",
        "Урок 3",
        "Где AI слаб или опасен",
        "Взрослый курс должен рано показать не только пользу, но и границы доверия.",
        "card",
        "CM-L03-CASE-A",
        {
            "kicker": "Урок 3",
            "body": "AI полезен как инструмент. Опасен как авторитет без проверки.",
        },
    ),
    Slide(
        "l03_confident_wrong_case.svg",
        "Урок 3",
        "Гладкий ответ с высокой ценой ошибки",
        "Опасность начинается там, где модель звучит убедительно, но обещает то, что не подтверждено.",
        "split",
        "CM-L03-CASE-A",
        {
            "left": {
                "title": "Что реально известно",
                "body": "Запуск не подтвержден. DPA не согласован. Два магазина не передали таблицы. Клиент просит письменный статус.",
            },
            "right": {
                "title": "Что опасно пишет AI",
                "body": "“Запуск в понедельник подтвержден, критических рисков нет, можно спокойно идти в старт”. Гладко, но ложно.",
            },
            "bottom": "Чем убедительнее звучит ошибка, тем легче перенести ее в письмо, решение или обещание клиенту.",
        },
    ),
    Slide(
        "l03_risk_lens.svg",
        "Урок 3",
        "Четыре линзы риска",
        "Риск нужно объяснять не эмоциями, а повторяемой рамкой проверки.",
        "grid",
        "CM-L03-CASE-A",
        {
            "cards": [
                {"title": "Факты", "body": "Есть ли здесь даты, числа, статусы или условия, которые модель могла исказить?"},
                {"title": "Контекст", "body": "Модель реально знает бизнес-контекст или просто достраивает его правдоподобно?"},
                {"title": "Цена ошибки", "body": "Это внутренний черновик или внешнее сообщение, от которого зависит доверие и деньги?"},
                {"title": "Чувствительность", "body": "Не загрузили ли мы лишние данные, которые вообще не стоило отправлять в модель?"},
            ]
        },
    ),
    Slide(
        "l03_zone_map.svg",
        "Урок 3",
        "Green / Yellow / Red map",
        "Одна таблица должна быстро показывать, где AI можно использовать свободно, а где нужен жесткий контроль.",
        "table",
        "CM-L03-CASE-A",
        {
            "headers": ["Зона", "Тип задачи", "Правило использования"],
            "widths": [180, 690, 550],
            "rows": [
                ["Green", "идеи, внутренний черновик, структура документа, обезличенный summary", "использовать как быстрый черновик"],
                ["Yellow", "follow-up, summary важных заметок, prep к встрече, status note", "использовать только после проверки"],
                ["Red", "обещание срока, скидки, юридический текст, чувствительные данные", "не копировать как есть; нужен policy gate"],
            ],
        },
    ),
    Slide(
        "l03_final_card.svg",
        "Урок 3",
        "Действие после урока",
        "Ученик должен сразу разметить собственные задачи по зонам риска.",
        "card",
        "CM-L03-CASE-A",
        {
            "kicker": "После урока 3",
            "body": "Разметьте 5-7 своих задач по трем зонам: green, yellow, red.",
            "accent": SAGE,
        },
    ),
    Slide(
        "l04_title_card.svg",
        "Урок 4",
        "Как выбрать первые сценарии для AI",
        "Старт курса ломается не на отсутствии сценариев, а на выборе слишком сложного или опасного первого кейса.",
        "card",
        "CM-L04-MATRIX-A",
        {
            "kicker": "Урок 4",
            "body": "Первый сценарий должен пройти фильтр частоты, понятности, риска и пользы.",
        },
    ),
    Slide(
        "l04_filter_matrix.svg",
        "Урок 4",
        "Матрица выбора стартового сценария",
        "Не интуиция, а простой go / no-go фильтр для первых кейсов.",
        "table",
        "CM-L04-MATRIX-A",
        {
            "headers": ["Сценарий", "Частота", "Понятность результата", "Риск", "Польза", "Решение"],
            "widths": [340, 150, 230, 120, 150, 430],
            "rows": [
                ["Follow-up после встречи", "3", "3", "2", "3", "брать в старт"],
                ["Summary длинного документа", "3", "3", "2", "3", "брать в старт"],
                ["Подготовка к weekly sync", "3", "3", "2", "2", "брать в старт"],
                ["Внешнее письмо с обещанием срока", "2", "2", "1", "2", "не брать в старт"],
                ["Проверка юридического документа", "1", "1", "1", "2", "не брать в старт"],
            ],
        },
    ),
    Slide(
        "l04_good_vs_bad_start.svg",
        "Урок 4",
        "Хороший и плохой первый сценарий",
        "Нужно показать не просто матрицу, а контраст между разумным и опасным стартом.",
        "split",
        "CM-L04-MATRIX-A",
        {
            "left": {
                "title": "Хороший старт",
                "body": "Summary длинного документа: задача повторяется, хороший результат понятен, риск умеренный, польза ощущается сразу.",
            },
            "right": {
                "title": "Плохой старт",
                "body": "Письмо клиенту с обещанием скидки или срока: ошибка дорога, сценарий чувствительный, для старта это не учебный кейс.",
            },
            "bottom": "Стартуйте не с самой умной задачи, а с той, которая быстро дает пользу и не ломает вам работу.",
        },
    ),
    Slide(
        "l04_go_no_go.svg",
        "Урок 4",
        "Go / No-Go filter на одном экране",
        "У ученика должен остаться короткий экран, по которому он сможет отсеять плохие стартовые кейсы без наставника.",
        "grid",
        "CM-L04-MATRIX-A",
        {
            "cards": [
                {"title": "1. Повторяется", "body": "Если задача редкая, на ней трудно закрепить навык и увидеть системную пользу."},
                {"title": "2. Результат понятен", "body": "Вы должны быстро понимать, что считать хорошим выходом и что именно проверять."},
                {"title": "3. Риск умеренный", "body": "Ошибка не должна сразу бить по деньгам, репутации или чувствительным данным."},
                {"title": "4. Польза ощутима", "body": "Если ускорение не чувствуется, сценарий не даст ранней мотивации и first win."},
            ]
        },
    ),
    Slide(
        "l04_final_card.svg",
        "Урок 4",
        "Действие после урока",
        "После этого экрана ученик должен прийти в HW1 уже с отобранными стартовыми задачами.",
        "card",
        "CM-L04-MATRIX-A",
        {
            "kicker": "После урока 4",
            "body": "Выберите 3-5 стартовых сценариев и оцените каждый по 4 фильтрам.",
            "accent": SAGE,
        },
    ),
]


def slide_svg(slide: Slide) -> str:
    if slide.kind == "card":
        body = render_card(slide)
    elif slide.kind == "grid":
        body = render_grid(slide)
    elif slide.kind == "split":
        body = render_split(slide)
    elif slide.kind == "table":
        body = render_table(slide)
    elif slide.kind == "compare":
        body = render_compare(slide)
    else:
        raise ValueError(slide.kind)
    return svg_wrap(body)


def write_svg(slide: Slide) -> None:
    (OUT / slide.filename).write_text(slide_svg(slide), encoding="utf-8")


def build_outline() -> str:
    sections = [
        "# Wave 1B Slides Outline",
        "",
        "Дата: 21 марта 2026",
        "Статус: карта visual-pack для уроков 2-4",
        "",
        "## Урок 2",
        "1. `l02_title_card.svg`",
        "2. `l02_task_class_map.svg`",
        "3. `l02_three_examples.svg`",
        "4. `l02_start_filter.svg`",
        "5. `l02_final_card.svg`",
        "",
        "## Урок 3",
        "1. `l03_title_card.svg`",
        "2. `l03_confident_wrong_case.svg`",
        "3. `l03_risk_lens.svg`",
        "4. `l03_zone_map.svg`",
        "5. `l03_final_card.svg`",
        "",
        "## Урок 4",
        "1. `l04_title_card.svg`",
        "2. `l04_filter_matrix.svg`",
        "3. `l04_good_vs_bad_start.svg`",
        "4. `l04_go_no_go.svg`",
        "5. `l04_final_card.svg`",
        "",
    ]
    return "\n".join(sections)


def build_copy() -> str:
    parts = ["# Wave 1B Slide Copy", "", "Дата: 21 марта 2026", "Статус: copy deck для уроков 2-4", ""]
    for slide in slides:
        parts.append(f"## {slide.filename}")
        parts.append("")
        parts.append(f"Единица: {slide.unit}")
        parts.append(f"Case ID: `{slide.case_id}`")
        parts.append(f"Заголовок: {slide.title}")
        parts.append(f"Подзаголовок: {slide.subtitle}")
        if slide.kind == "card":
            parts.append(f"- Действие / тезис: {slide.payload['body']}")
        elif slide.kind == "grid":
            for card in slide.payload["cards"]:
                parts.append(f"- {card['title']}: {card['body']}")
        elif slide.kind == "split":
            parts.append(f"- Левая колонка: {slide.payload['left']['title']} — {slide.payload['left']['body']}")
            parts.append(f"- Правая колонка: {slide.payload['right']['title']} — {slide.payload['right']['body']}")
            parts.append(f"- Нижняя линия: {slide.payload['bottom']}")
        elif slide.kind == "table":
            parts.append(f"- Таблица: {' | '.join(slide.payload['headers'])}")
        elif slide.kind == "compare":
            for col in slide.payload["columns"]:
                parts.append(f"- {col['title']}: {col['body']}")
            parts.append(f"- Нижняя линия: {slide.payload['bottom']}")
        parts.append("")
    return "\n".join(parts)


def build_diagrams() -> str:
    return """# Wave 1B Diagrams

Дата: 21 марта 2026
Статус: Mermaid-схемы для уроков 2-4

## Урок 2. От карты задач к первым классам

```mermaid
flowchart LR
    A["Повторяющаяся работа"] --> B["Класс задачи"]
    B --> C["Быстрый сценарий"]
    C --> D["Проверяемый результат"]
```

## Урок 3. Линзы риска

```mermaid
flowchart TD
    A["AI-ответ"] --> B["Факты"]
    A --> C["Контекст"]
    A --> D["Цена ошибки"]
    A --> E["Чувствительность данных"]
```

## Урок 4. Go / No-Go filter

```mermaid
flowchart LR
    A["Сценарий"] --> B{"Повторяется?"}
    B -->|Да| C{"Результат понятен?"}
    B -->|Нет| X["No-Go"]
    C -->|Да| D{"Риск умеренный?"}
    C -->|Нет| X
    D -->|Да| E{"Польза ощутима?"}
    D -->|Нет| X
    E -->|Да| F["Go"]
    E -->|Нет| X
```
"""


def build_readme() -> str:
    lines = [
        "# Wave 1B Visual Assets",
        "",
        "Дата: 21 марта 2026",
        "Статус: рабочий пакет визуальных материалов для уроков 2-4",
        "",
        "## Что внутри",
        "",
        "- `build_wave_1b_assets.py` - генератор SVG-assets.",
        "- `wave_1b_slides_outline.md` - карта deck по урокам 2-4.",
        "- `wave_1b_slide_copy.md` - точный смысл каждого экрана.",
        "- `wave_1b_diagrams.md` - Mermaid-схемы для логики уроков.",
        "- SVG-файлы - реальные assets для записи и rough cut.",
        "",
        "## Покрытие",
        "",
        "- 15 SVG-assets: по 5 экранов на уроки 2, 3 и 4.",
        "- Урок 2 опирается на карту классов задач и реальные стартовые примеры.",
        "- Урок 3 опирается на confident-but-wrong risk case и green/yellow/red map.",
        "- Урок 4 опирается на матрицу выбора сценариев и go / no-go filter.",
        "",
        "## Как пересобрать",
        "",
        "`python3 build_wave_1b_assets.py`",
        "",
        "## Карта SVG-файлов",
        "",
    ]
    for slide in slides:
        lines.append(f"- `{slide.filename}` - {slide.unit}: {slide.title}")
    lines.extend([
        "",
        "## Примечание",
        "",
        "Пакет собран только внутри isolated-папки и опирается на канонический concrete pack для уроков 2-4.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    for slide in slides:
        write_svg(slide)
    (OUT / "wave_1b_slides_outline.md").write_text(build_outline(), encoding="utf-8")
    (OUT / "wave_1b_slide_copy.md").write_text(build_copy(), encoding="utf-8")
    (OUT / "wave_1b_diagrams.md").write_text(build_diagrams(), encoding="utf-8")
    (OUT / "README.md").write_text(build_readme(), encoding="utf-8")


if __name__ == "__main__":
    main()
