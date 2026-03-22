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
PANEL = "#FFFDF8"
LINE = "#D7D0C1"


@dataclass(frozen=True)
class Lesson:
    key: str
    unit: str
    title: str
    case_id: str
    diagram: str


@dataclass(frozen=True)
class Slide:
    filename: str
    lesson_key: str
    unit: str
    title: str
    subtitle: str
    kind: str
    case_id: str
    purpose: str
    accent: str
    secondary: str
    copy: list[str]
    payload: dict


def hex_to_rgb(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#%02x%02x%02x" % rgb


def tint(color: str, ratio: float = 0.88) -> str:
    base = hex_to_rgb(color)
    white = (255, 255, 255)
    mixed = tuple(int(base[i] * (1 - ratio) + white[i] * ratio) for i in range(3))
    return rgb_to_hex(mixed)


def shade(color: str, ratio: float = 0.18) -> str:
    base = hex_to_rgb(color)
    black = (16, 24, 35)
    mixed = tuple(int(base[i] * (1 - ratio) + black[i] * ratio) for i in range(3))
    return rgb_to_hex(mixed)


def wrapped_lines(text: str, max_chars: int | None = None) -> list[str]:
    paragraphs = text.split("\n")
    out: list[str] = []
    for paragraph in paragraphs:
        if max_chars is None:
            out.append(paragraph)
            continue
        pieces = wrap(paragraph, max_chars) or [""]
        out.extend(pieces)
    return out


def t(
    x: int,
    y: int,
    text: str,
    size: int = 28,
    fill: str = INK,
    weight: str = "400",
    family: str = "'Trebuchet MS', 'Segoe UI', sans-serif",
    max_chars: int | None = None,
    line_height: int | None = None,
) -> str:
    if line_height is None:
        line_height = int(size * 1.35)
    parts = wrapped_lines(text, max_chars)
    tspans = []
    for idx, part in enumerate(parts):
        dy = "0" if idx == 0 else str(line_height)
        tspans.append(f'<tspan x="{x}" dy="{dy}">{escape(part)}</tspan>')
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-family="{family}" '
        f'font-weight="{weight}" fill="{fill}">{"".join(tspans)}</text>'
    )


def rect(x: int, y: int, w: int, h: int, fill: str = PANEL, stroke: str = LINE, rx: int = 28, sw: int = 2) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def pill(x: int, y: int, w: int, h: int, text: str, fill: str, text_fill: str = "white") -> str:
    return rect(x, y, w, h, fill=fill, stroke=fill, rx=h // 2) + t(x + 24, y + h - 18, text, 24, text_fill, "700")


def divider(x1: int, y1: int, x2: int, y2: int, color: str = LINE, width: int = 2, dash: str | None = None) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{dash_attr}/>'


def arrow(x1: int, y1: int, x2: int, y2: int, color: str, width: int = 4) -> str:
    head = ""
    if x2 > x1:
        head = (
            f'<polygon points="{x2},{y2} {x2 - 14},{y2 - 8} {x2 - 14},{y2 + 8}" '
            f'fill="{color}"/>'
        )
    elif x2 < x1:
        head = (
            f'<polygon points="{x2},{y2} {x2 + 14},{y2 - 8} {x2 + 14},{y2 + 8}" '
            f'fill="{color}"/>'
        )
    return divider(x1, y1, x2, y2, color=color, width=width) + head


def title_panel(slide: Slide) -> str:
    header_fill = slide.payload.get("header_fill", tint(slide.accent, 0.92))
    ribbon = tint(slide.secondary, 0.93)
    return (
        rect(60, 40, 1480, 210, fill=header_fill, stroke=LINE, rx=40)
        + rect(60, 40, 1480, 18, fill=ribbon, stroke=ribbon, rx=40)
        + pill(90, 70, 190, 48, slide.unit, slide.accent)
        + t(90, 158, slide.title, 50, INK, "700", family="Georgia, serif", max_chars=36, line_height=56)
        + t(90, 220, slide.subtitle, 24, MUTED, "400", max_chars=90, line_height=32)
        + pill(1230, 182, 280, 44, slide.case_id, shade(slide.secondary, 0.05))
    )


def footer(slide: Slide) -> str:
    return (
        divider(90, 824, 1510, 824)
        + t(90, 858, "Wave 3 visual pack · Lessons 17-24", 20, MUTED)
        + t(1150, 858, slide.filename.replace(".svg", ""), 20, MUTED, "700")
    )


def bullet_list(
    x: int,
    y: int,
    w: int,
    items: list[str],
    bullet_fill: str,
    size: int = 22,
    text_fill: str = INK,
) -> str:
    out = []
    cy = y
    max_chars = max(18, int((w - 50) / 11))
    line_height = int(size * 1.3)
    for item in items:
        lines = wrapped_lines(item, max_chars)
        out.append(f'<circle cx="{x + 10}" cy="{cy - 8}" r="5" fill="{bullet_fill}"/>')
        out.append(t(x + 28, cy, item, size, text_fill, "400", max_chars=max_chars, line_height=line_height))
        cy += len(lines) * line_height + 22
    return "".join(out)


def metric_card(x: int, y: int, w: int, h: int, title: str, body: str, accent: str) -> str:
    return (
        rect(x, y, w, h, fill="white", stroke=LINE)
        + t(x + 20, y + 40, title, 24, accent, "700", max_chars=max(12, w // 11))
        + t(x + 20, y + 78, body, 20, INK, max_chars=max(16, w // 11), line_height=24)
    )


def render_card(slide: Slide) -> str:
    fill = slide.payload.get("panel_fill", tint(slide.accent, 0.92))
    out = [
        rect(90, 90, 1420, 700, fill=fill, stroke=LINE, rx=42),
        rect(120, 120, 1360, 560, fill="white", stroke=LINE, rx=36),
        pill(140, 140, 210, 50, slide.payload.get("kicker", slide.unit), slide.accent),
        t(140, 285, slide.title, 60, INK, "700", family="Georgia, serif", max_chars=30, line_height=68),
        t(140, 390, slide.subtitle, 28, MUTED, "400", max_chars=66, line_height=36),
        rect(140, 470, 1320, 150, fill=tint(slide.secondary, 0.92), stroke=LINE),
        t(175, 530, slide.payload["body"], 34, INK, "700", max_chars=48, line_height=42),
    ]
    note = slide.payload.get("note")
    if note:
        out.append(t(140, 725, note, 22, MUTED, "400", max_chars=90, line_height=28))
    out.append(footer(slide))
    return "".join(out)


def render_columns(slide: Slide) -> str:
    columns = slide.payload["columns"]
    metrics = slide.payload.get("metrics", [])
    bottom = slide.payload.get("bottom")
    out = [title_panel(slide)]
    count = len(columns)
    gap = 20
    total_w = 1420 - gap * (count - 1)
    col_w = total_w // count
    fills = [tint(slide.accent, 0.92), tint(slide.secondary, 0.92), "#F4EEE3", "#EEF3F0", "#F4F0FA"]
    accents = [slide.accent, slide.secondary, shade(slide.accent, 0.12), INK, shade(slide.secondary, 0.12)]
    y = 290
    height = 420 if metrics else 470
    for idx, col in enumerate(columns):
        x = 90 + idx * (col_w + gap)
        out.append(rect(x, y, col_w, height, fill=fills[idx % len(fills)]))
        out.append(t(x + 24, y + 48, col["title"], 28, accents[idx % len(accents)], "700", max_chars=max(12, col_w // 12)))
        if "bullets" in col:
            out.append(bullet_list(x + 24, y + 98, col_w - 48, col["bullets"], slide.accent if idx % 2 == 0 else slide.secondary))
        else:
            out.append(t(x + 24, y + 98, col["body"], 22, INK, "400", max_chars=max(18, col_w // 11), line_height=28))
    if metrics:
        mx = 90
        card_w = 330
        for metric in metrics:
            out.append(metric_card(mx, 735, card_w, 74, metric["title"], metric["body"], metric["accent"]))
            mx += 360
    if bottom:
        out.append(rect(90, 724, 1420, 82, fill=shade(slide.accent, 0.2), stroke=shade(slide.accent, 0.2)))
        out.append(t(122, 772, bottom, 25, "white", "700", max_chars=92, line_height=30))
    out.append(footer(slide))
    return "".join(out)


def render_split(slide: Slide) -> str:
    left = slide.payload["left"]
    right = slide.payload["right"]
    bottom = slide.payload.get("bottom")
    out = [
        title_panel(slide),
        rect(90, 290, 680, 450, fill=tint(slide.accent, 0.93)),
        rect(830, 290, 680, 450, fill=tint(slide.secondary, 0.93)),
        t(120, 342, left["title"], 30, slide.accent, "700", max_chars=30),
        t(860, 342, right["title"], 30, slide.secondary, "700", max_chars=30),
    ]
    if "bullets" in left:
        out.append(bullet_list(120, 395, 610, left["bullets"], slide.accent))
    else:
        out.append(t(120, 395, left["body"], 23, INK, "400", max_chars=38, line_height=30))
    if "bullets" in right:
        out.append(bullet_list(860, 395, 610, right["bullets"], slide.secondary))
    else:
        out.append(t(860, 395, right["body"], 23, INK, "400", max_chars=38, line_height=30))
    if bottom:
        out.append(rect(90, 760, 1420, 50, fill=shade(slide.accent, 0.22), stroke=shade(slide.accent, 0.22), rx=24))
        out.append(t(120, 794, bottom, 24, "white", "700", max_chars=96, line_height=28))
    out.append(footer(slide))
    return "".join(out)


def render_table(slide: Slide) -> str:
    headers = slide.payload["headers"]
    widths = slide.payload["widths"]
    rows = slide.payload["rows"]
    row_height = slide.payload.get("row_height", 68)
    out = [title_panel(slide), rect(90, 274, 1420, 504)]
    x = 90
    header_fills = [tint(slide.accent, 0.9), tint(slide.secondary, 0.9), "#F0ECE3", "#EEF3F0", "#F7F2EA"]
    for idx, (header, width) in enumerate(zip(headers, widths)):
        fill = header_fills[idx % len(header_fills)]
        out.append(rect(x, 274, width, 72, fill=fill, stroke=LINE, rx=0))
        out.append(t(x + 14, 320, header, 21, INK, "700", max_chars=max(12, width // 11), line_height=24))
        x += width
    y = 346
    for ridx, row in enumerate(rows):
        bg = "white" if ridx % 2 == 0 else "#FCFAF4"
        x = 90
        for cell, width in zip(row, widths):
            out.append(rect(x, y, width, row_height, fill=bg, stroke=LINE, rx=0, sw=1))
            out.append(t(x + 14, y + 30, cell, 18, INK, "400", max_chars=max(10, width // 11), line_height=22))
            x += width
        y += row_height
    bottom = slide.payload.get("bottom")
    if bottom:
        out.append(t(90, 808, bottom, 22, MUTED, "400", max_chars=100, line_height=28))
    out.append(footer(slide))
    return "".join(out)


def render_workflow(slide: Slide) -> str:
    steps = slide.payload["steps"]
    note = slide.payload.get("bottom")
    metrics = slide.payload.get("metrics", [])
    out = [title_panel(slide)]
    gap = 18
    count = len(steps)
    step_w = int((1420 - gap * (count - 1)) / count)
    y = 340
    h = 240
    fills = [tint(slide.accent, 0.92), tint(slide.secondary, 0.92), "#F2EEE6", "#EFF4F1", "#F5F1FA", "#F1F4F8"]
    for idx, step in enumerate(steps):
        x = 90 + idx * (step_w + gap)
        fill = fills[idx % len(fills)]
        accent = slide.accent if idx % 2 == 0 else slide.secondary
        out.append(rect(x, y, step_w, h, fill=fill))
        out.append(pill(x + 20, y + 18, 72, 36, str(idx + 1), accent))
        out.append(t(x + 24, y + 86, step["title"], 24, accent, "700", max_chars=max(10, step_w // 11)))
        out.append(t(x + 24, y + 126, step["body"], 20, INK, "400", max_chars=max(14, step_w // 11), line_height=24))
        if idx < count - 1:
            x1 = x + step_w
            x2 = x + step_w + gap
            out.append(arrow(x1, y + 120, x2 - 6, y + 120, shade(slide.accent, 0.06), 4))
    if metrics:
        mx = 120
        for metric in metrics:
            out.append(metric_card(mx, 640, 380, 118, metric["title"], metric["body"], metric["accent"]))
            mx += 430
    if note:
        out.append(rect(90, 774, 1420, 36, fill=shade(slide.accent, 0.18), stroke=shade(slide.accent, 0.18), rx=18))
        out.append(t(116, 799, note, 22, "white", "700", max_chars=100, line_height=26))
    out.append(footer(slide))
    return "".join(out)


def render_grid(slide: Slide) -> str:
    cards = slide.payload["cards"]
    out = [title_panel(slide)]
    positions = [(90, 290), (820, 290), (90, 535), (820, 535)]
    fills = [tint(slide.accent, 0.93), tint(slide.secondary, 0.93), "#F3EFE7", "#EEF4F1"]
    accents = [slide.accent, slide.secondary, shade(slide.accent, 0.1), INK]
    for (x, y), card, fill, accent in zip(positions, cards, fills, accents):
        out.append(rect(x, y, 690, 190, fill=fill))
        out.append(t(x + 28, y + 50, card["title"], 27, accent, "700", max_chars=32))
        if "bullets" in card:
            out.append(bullet_list(x + 28, y + 98, 630, card["bullets"], accent, size=20))
        else:
            out.append(t(x + 28, y + 92, card["body"], 21, INK, "400", max_chars=42, line_height=27))
    note = slide.payload.get("bottom")
    if note:
        out.append(t(90, 792, note, 22, MUTED, "400", max_chars=100, line_height=28))
    out.append(footer(slide))
    return "".join(out)


def render_dashboard(slide: Slide) -> str:
    artifact = slide.payload["artifact"]
    metrics = slide.payload["metrics"]
    out = [
        title_panel(slide),
        rect(90, 290, 840, 470, fill=tint(slide.accent, 0.94)),
        t(120, 342, artifact["title"], 30, slide.accent, "700", max_chars=42),
    ]
    if "bullets" in artifact:
        out.append(bullet_list(120, 398, 770, artifact["bullets"], slide.accent, size=22))
    else:
        out.append(t(120, 398, artifact["body"], 22, INK, "400", max_chars=54, line_height=28))
    metric_positions = [(970, 290), (1245, 290), (970, 525), (1245, 525)]
    for (x, y), metric in zip(metric_positions, metrics):
        out.append(metric_card(x, y, 245, 200, metric["title"], metric["body"], metric["accent"]))
    note = slide.payload.get("bottom")
    if note:
        out.append(t(90, 790, note, 22, MUTED, "400", max_chars=100, line_height=28))
    out.append(footer(slide))
    return "".join(out)


def svg_wrap(body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f'<rect width="{W}" height="{H}" fill="{BG}"/>'
        f"{body}</svg>"
    )


LESSONS = [
    Lesson(
        "l17",
        "Урок 17",
        "Резюме документов и выделение сути",
        "FW-L17-CASE-A",
        """```mermaid
flowchart LR
    A["Внутренняя записка"] --> B["Суть"]
    A --> C["Риски"]
    A --> D["Action items"]
    B --> E["Ручная проверка"]
    C --> E
    D --> E
```""",
    ),
    Lesson(
        "l18",
        "Урок 18",
        "Подготовка к встречам и созвонам",
        "FW-L18-CASE-A / FW-L18-CASE-B",
        """```mermaid
flowchart LR
    A["Контекст встречи"] --> B["Agenda + вопросы"]
    B --> C["Решение на созвоне"]
    C --> D["Follow-up: owner + срок"]
    D --> E["Следующий статус"]
```""",
    ),
    Lesson(
        "l19",
        "Урок 19",
        "Идеи, структура и черновики",
        "FW-L19-CASE-A",
        """```mermaid
flowchart LR
    A["Проблема и ограничения"] --> B["5 вариантов"]
    B --> C["Отбор по критериям"]
    C --> D["Структура записки"]
    D --> E["Первый черновик"]
```""",
    ),
    Lesson(
        "l20",
        "Урок 20",
        "Первичное исследование темы",
        "FW-L20-CASE-A",
        """```mermaid
flowchart LR
    A["Новая тема"] --> B["Карта темы"]
    B --> C["Ключевые вопросы"]
    C --> D["Что проверить по источникам"]
    D --> E["Вывод человека"]
```""",
    ),
    Lesson(
        "l21",
        "Урок 21",
        "AI как инструмент самообучения",
        "L21-CASE-A",
        """```mermaid
flowchart LR
    A["Объясни просто"] --> B["Сравни с похожим"]
    B --> C["Задай вопросы"]
    C --> D["Проверь мой ответ"]
    D --> E["Что проверить отдельно"]
```""",
    ),
    Lesson(
        "l22",
        "Урок 22",
        "Как не превратить AI в лишнюю игрушку",
        "L22-CASE-A / L22-CASE-B",
        """```mermaid
flowchart LR
    A["Сценарий"] --> B["5 вопросов фильтра"]
    B --> C["Toy / Test / Tool"]
    C --> D["Измеримый эффект"]
```""",
    ),
    Lesson(
        "l23",
        "Урок 23",
        "Как строить личную систему использования AI",
        "L23-CASE-A / L23-BRIDGE-A",
        """```mermaid
flowchart LR
    A["Сценарии"] --> F["Личная AI-система"]
    B["Шаблоны"] --> F
    C["Чек-лист"] --> F
    D["Безопасность"] --> F
    E["Proof log"] --> F
    F --> G["Командный proof path"]
```""",
    ),
    Lesson(
        "l24",
        "Урок 24",
        "План внедрения на 14 дней",
        "FW-L24-CASE-A / FW-L24-CASE-B / L24-BRIDGE-A",
        """```mermaid
flowchart LR
    A["Личные сценарии"] --> B["14-дневный план"]
    C["Шаблоны и чек-лист"] --> B
    D["Proof log"] --> B
    B --> E["B2B proof pack"]
    E --> F["Следующий цикл внедрения"]
```""",
    ),
]


SLIDES = [
    Slide(
        "l17_title_card.svg",
        "l17",
        "Урок 17",
        "Резюме документов и выделение сути",
        "Полезно не любое summary, а summary под конкретное решение.",
        "card",
        "FW-L17-CASE-A",
        "Открывающий экран урока: один документ должен превращаться в суть, риски и действия, а не в нейтральный пересказ.",
        "#C65A1E",
        "#5A7268",
        [
            "Главная экранная фраза: summary нужен под конкретное решение, а не ради сокращения текста.",
            "Кейс урока: записка о двухнедельном пилоте AI-шаблонов в клиентском сервисе.",
        ],
        {
            "kicker": "Урок 17",
            "body": "Один документ должен дать три слоя пользы: суть, риски и action items.",
            "note": "Кейс: пилот на 2 недели, 6 специалистов первой линии, цель - быстрее собрать первый рабочий ответ.",
        },
    ),
    Slide(
        "l17_summary_modes.svg",
        "l17",
        "Урок 17",
        "Три режима summary из одного документа",
        "Один и тот же текст читается по-разному, если вы заранее знаете, какое решение готовите.",
        "columns",
        "FW-L17-CASE-A",
        "Главный framework урока: не просить абстрактный summary, а выбирать режим чтения под задачу.",
        "#C65A1E",
        "#5A7268",
        [
            "Суть: что команда тестирует, кто участвует и какой вопрос пилота главный.",
            "Риски: длинные и неестественные ответы, распад тона, устаревание библиотеки, риск утечки.",
            "Действия: owner шаблонов, список разрешенных сценариев, стандарт редактуры, review у тимлида.",
        ],
        {
            "columns": [
                {
                    "title": "1. Суть",
                    "bullets": [
                        "Цель пилота: сократить время от обращения до первого рабочего черновика ответа.",
                        "Участвуют 6 специалистов первой линии в течение 2 недель.",
                        "Тестируют greeting, follow-up и режим редактирования сырого ответа.",
                    ],
                },
                {
                    "title": "2. Риски",
                    "bullets": [
                        "Сотрудники могут копировать слишком длинные и неестественные тексты.",
                        "Может потеряться единый тон команды.",
                        "Без owner библиотека шаблонов быстро устареет.",
                        "Сырые диалоги в публичном AI повышают риск утечки.",
                    ],
                },
                {
                    "title": "3. Действия",
                    "bullets": [
                        "Назначить owner библиотеки шаблонов.",
                        "Зафиксировать разрешенные и запрещенные AI-сценарии.",
                        "Дать короткий стандарт ручной редактуры.",
                        "Определить, кто делает review шаблонов и спорных ответов.",
                    ],
                },
            ],
            "metrics": [
                {"title": "Пилот", "body": "2 недели и 6 специалистов первой линии", "accent": "#C65A1E"},
                {"title": "Цель", "body": "быстрее собрать первый рабочий ответ клиенту", "accent": "#5A7268"},
                {"title": "Режим", "body": "суть -> риски -> действия", "accent": "#10213B"},
            ],
        },
    ),
    Slide(
        "l17_pilot_outputs.svg",
        "l17",
        "Урок 17",
        "Один документ -> три разных экрана пользы",
        "Полезный summary меняется в зависимости от вопроса: что здесь главное, что опасно и что делать дальше.",
        "columns",
        "FW-L17-CASE-A",
        "Concrete compare screen: показать, как один текст превращается в три разные рабочие заготовки.",
        "#C65A1E",
        "#5A7268",
        [
            "Summary на 5 буллетов: короткая цель пилота, участники, что тестируют, какие ограничения уже зафиксированы.",
            "Риски и слабые точки: неестественные тексты, распад тона, устаревание библиотеки, утечка данных.",
            "Action items: назначить owner, зафиксировать правила, ввести стандарт редактуры и review.",
        ],
        {
            "columns": [
                {
                    "title": "Summary на 5 буллетов",
                    "bullets": [
                        "Двухнедельный пилот AI-шаблонов в клиентском сервисе.",
                        "6 специалистов первой линии.",
                        "Шаблоны приветствия, follow-up и edit mode.",
                        "Нельзя загружать полные диалоги и обещать сроки через AI.",
                        "По итогам проверяем скорость, reuse шаблонов и качество ответов.",
                    ],
                },
                {
                    "title": "Риски и спорные места",
                    "bullets": [
                        "Слишком длинные ответы выглядят искусственно.",
                        "Разные шаблоны размоют общий tone of voice.",
                        "Без owner библиотека быстро перестанет быть полезной.",
                        "Публичный AI для сырых диалогов = риск утечки.",
                    ],
                },
                {
                    "title": "Action items до старта",
                    "bullets": [
                        "Назначить owner библиотеки.",
                        "Разделить разрешенные и запрещенные сценарии.",
                        "Дать команде короткий стандарт ручной правки.",
                        "Определить, кто и как делает review спорных ответов.",
                    ],
                },
            ],
            "bottom": "Не просим 'summary вообще' - просим конкретный рабочий слой из текста.",
        },
    ),
    Slide(
        "l17_summary_quality_gate.svg",
        "l17",
        "Урок 17",
        "Quality gate для любого AI-summary",
        "Summary от AI - это рабочая версия извлечения смысла, а не окончательная истина.",
        "split",
        "FW-L17-CASE-A",
        "Экран на закрепление проверки: что именно нужно просмотреть человеком перед тем, как опираться на summary.",
        "#C65A1E",
        "#5A7268",
        [
            "Проверяем три вещи: AI не придумал факт, не выкинул критичный нюанс и не превратил спорное место в уверенный вывод.",
            "Красные флаги: пропали ограничения по данным, owner не назван, управленческий риск выглядит как решенный вопрос.",
        ],
        {
            "left": {
                "title": "Что проверяем руками",
                "bullets": [
                    "Не придумал ли AI факт, которого в записке не было.",
                    "Не исчез ли критичный нюанс: ограничения, сроки, ответственность.",
                    "Не превратился ли спорный пункт в уверенный вывод.",
                ],
            },
            "right": {
                "title": "Красные флаги слабого summary",
                "bullets": [
                    "Пропали ограничения по данным и ручной проверке.",
                    "Owner шаблонов не назван, хотя это ключевой риск пилота.",
                    "Проблема тона подана как уже решенная.",
                    "Управленческий вопрос масштабирования спрятан за гладким языком.",
                ],
            },
            "bottom": "Чем ближе документ к срокам, деньгам и обязательствам, тем обязательнее ручная проверка summary.",
        },
    ),
    Slide(
        "l17_final_card.svg",
        "l17",
        "Урок 17",
        "После урока: разберите один реальный документ",
        "Сохраните не только summary, но и выбранный режим чтения: суть, риски или action items.",
        "card",
        "FW-L17-CASE-A",
        "Финальная плашка урока: перевести навык из примера в рабочее действие сразу после просмотра.",
        "#C65A1E",
        "#5A7268",
        [
            "Действие после урока: взять один реальный документ и прогнать его через три режима summary.",
            "Сохранить лучший prompt как повторяемый шаблон чтения.",
        ],
        {
            "kicker": "После урока",
            "body": "Возьмите один рабочий документ и отдельно вытащите из него суть, риски и действия.",
            "note": "Сохраняйте не только хороший output, но и формулировку задачи чтения.",
            "panel_fill": tint("#C65A1E", 0.93),
        },
    ),
    Slide(
        "l18_title_card.svg",
        "l18",
        "Урок 18",
        "Подготовка к встречам и созвонам",
        "AI хорошо снижает хаос вокруг встречи, если вы заранее знаете цель и следующий шаг.",
        "card",
        "FW-L18-CASE-A / FW-L18-CASE-B",
        "Открывающий экран урока про meeting prep и follow-up без магии и без подмены ответственности.",
        "#2F6B83",
        "#5A7268",
        [
            "Главная экранная фраза: AI полезен как ускоритель структуры до и после встречи.",
            "Кейсы урока: статус-созвон по CRM-интеграции и follow-up после него.",
        ],
        {
            "kicker": "Урок 18",
            "body": "Встреча становится полезнее, когда AI собирает agenda, вопросы, follow-up и следующий шаг.",
            "note": "Кейс: интеграция уже сдвинулась на 8 рабочих дней, QA нашла 7 критичных дефектов, маркетинг готовит запуск по старой дате.",
        },
    ),
    Slide(
        "l18_meeting_window.svg",
        "l18",
        "Урок 18",
        "Три точки применения AI вокруг встречи",
        "До встречи нужна структура, после встречи нужна фиксация, между статусами нужен контекст.",
        "workflow",
        "FW-L18-CASE-A / FW-L18-CASE-B",
        "One-screen workflow для урока: до встречи, во время фиксации решения и после встречи.",
        "#2F6B83",
        "#5A7268",
        [
            "До встречи: agenda, вопросы, позиция и ключевые риски.",
            "На созвоне: держим фокус на решении по сроку, scope и owner коммуникации.",
            "После встречи: фиксируем решения, owner, сроки и следующий статус.",
            "Между статусами: восстанавливаем контекст, если задача тянется несколько дней.",
        ],
        {
            "steps": [
                {"title": "До встречи", "body": "Контекст, цель, 30-минутная agenda и список точных вопросов."},
                {"title": "Во время", "body": "Не уходим в детали: решаем срок запуска, cut scope и owner коммуникации."},
                {"title": "После встречи", "body": "Follow-up: решения, owner, сроки и подтвержденный следующий статус."},
                {"title": "Между статусами", "body": "Коротко восстанавливаем контекст, обязательства и открытые риски."},
            ],
            "metrics": [
                {"title": "Формат", "body": "30 минут на статус-созвон", "accent": "#2F6B83"},
                {"title": "Риск", "body": "сдвиг проекта на 8 рабочих дней", "accent": "#5A7268"},
                {"title": "Сигнал", "body": "7 критичных дефектов уже найдены QA", "accent": "#10213B"},
            ],
            "bottom": "AI здесь структурирует подготовку и фиксацию, но не принимает решение за команду.",
        },
    ),
    Slide(
        "l18_crm_status_prep.svg",
        "l18",
        "Урок 18",
        "Подготовка к статус-созвону по CRM-интеграции",
        "Хороший prep screen держит вместе контекст, agenda, вопросы и риски, чтобы встреча не расползлась.",
        "columns",
        "FW-L18-CASE-A",
        "Concrete prep board для 30-минутного звонка по проблемной интеграции.",
        "#2F6B83",
        "#5A7268",
        [
            "Контекст: интеграция сдвигается на 8 рабочих дней, 7 критичных дефектов, маркетинг уже готовит рассылку.",
            "Agenda: подтвердить статус, разобрать дефекты, решить по переносу и scope, закрепить owner коммуникации.",
            "Вопросы и риски: что блокирует запуск полностью, что можно выпустить безопасно, кому и когда сообщаем о переносе.",
        ],
        {
            "columns": [
                {
                    "title": "Контекст созвона",
                    "bullets": [
                        "Интеграция уже сдвигается на 8 рабочих дней.",
                        "QA нашла 7 критичных дефектов.",
                        "Маркетинг поставил рассылку о запуске на следующую неделю.",
                    ],
                },
                {
                    "title": "Agenda на 30 минут",
                    "bullets": [
                        "Подтвердить текущий статус и причины сдвига.",
                        "Разобрать 7 критичных дефектов и влияние на запуск.",
                        "Решить: переносим срок целиком или режем scope.",
                        "Зафиксировать владельца внешней коммуникации и следующий шаг.",
                    ],
                },
                {
                    "title": "Вопросы и риски",
                    "bullets": [
                        "Какие дефекты блокируют запуск полностью?",
                        "Какой минимальный scope можно выпустить безопасно?",
                        "Кто подтверждает новую дату и кто сообщает о переносе?",
                        "Риск: встреча уйдет в детали без решения по сроку.",
                    ],
                },
            ],
        },
    ),
    Slide(
        "l18_follow_up_actions.svg",
        "l18",
        "Урок 18",
        "Follow-up: решения, owner, сроки",
        "После встречи AI полезен там, где нужно быстро зафиксировать, что решено и кто что делает дальше.",
        "table",
        "FW-L18-CASE-B",
        "One-screen follow-up table из итоговых заметок по CRM-интеграции.",
        "#2F6B83",
        "#5A7268",
        [
            "Релиз переносим на 1 неделю и убираем из первого релиза автоматическое обновление дубликатов.",
            "Техлид подрядчика до четверга присылает новый график исправлений.",
            "Руководитель проекта до конца дня сообщает обновление продажам и маркетингу.",
            "Следующий статус назначен на пятницу, 15:00.",
        ],
        {
            "headers": ["Решение / шаг", "Owner", "Срок", "Почему это важно"],
            "widths": [430, 250, 220, 520],
            "rows": [
                ["Релиз переносим на 1 неделю", "руководитель проекта", "сразу после созвона", "снимаем ложный оптимизм и пересобираем коммуникацию"],
                ["В 1-й релиз не входит автообновление дубликатов", "команда проекта", "фиксируем в scope", "иначе обсуждение снова расползется"],
                ["Новый график исправлений", "техлид подрядчика", "до четверга", "без него нельзя подтвердить реалистичную дату"],
                ["Обновление продаж и маркетинга", "руководитель проекта", "до конца дня", "иначе внешняя рассылка уйдет по старой дате"],
                ["Следующий статус", "все участники", "пятница, 15:00", "новая точка контроля после переноса"],
            ],
            "row_height": 70,
            "bottom": "Перед отправкой follow-up вручную проверяем: решение не потерялось, owner не перепутан, срок понятен всем.",
        },
    ),
    Slide(
        "l18_final_card.svg",
        "l18",
        "Урок 18",
        "После урока: сохраните шаблон типовой встречи",
        "Сильный template для prep и follow-up снижает хаос не разово, а каждую неделю.",
        "card",
        "FW-L18-CASE-A / FW-L18-CASE-B",
        "Финальная плашка урока: перевести meeting workflow в повторяемый шаблон.",
        "#2F6B83",
        "#5A7268",
        [
            "Действие после урока: сохранить один template на prep и один template на follow-up.",
            "Для регулярных созвонов выделить, что можно сделать общим шаблоном команды.",
        ],
        {
            "kicker": "После урока",
            "body": "Сохраните один рабочий шаблон подготовки к встрече и один шаблон follow-up после нее.",
            "note": "Сильный сценарий вокруг встречи должен убирать хаос до разговора и после него.",
            "panel_fill": tint("#2F6B83", 0.93),
        },
    ),
    Slide(
        "l19_title_card.svg",
        "l19",
        "Урок 19",
        "Идеи, структура и черновики",
        "AI помогает быстро начать, но не должен думать за вас, что именно важно.",
        "card",
        "FW-L19-CASE-A",
        "Открывающий экран урока про выход из чистого листа через варианты, отбор и структуру.",
        "#B85B34",
        "#5A7268",
        [
            "Главная экранная фраза: AI полезен в старте интеллектуальной работы, но не подменяет позицию автора.",
            "Кейс урока: записка о сокращении времени адаптации новых сотрудников в операционной команде.",
        ],
        {
            "kicker": "Урок 19",
            "body": "Самая сильная польза AI в этом сценарии - быстро перевести пустой лист в отобранную структуру.",
            "note": "Контекст кейса: адаптация длится 5-6 недель, знания разбросаны, нужно показать результат за 30 дней без большого проекта.",
        },
    ),
    Slide(
        "l19_four_step_flow.svg",
        "l19",
        "Урок 19",
        "Из пустого листа в рабочий черновик: 4 шага",
        "Если перескочить сразу к финальному тексту, AI почти всегда даст гладкий, но слабый общий текст.",
        "workflow",
        "FW-L19-CASE-A",
        "Главный workflow урока: варианты -> отбор -> структура -> черновик.",
        "#B85B34",
        "#5A7268",
        [
            "Сначала генерируем 5 реалистичных вариантов подхода.",
            "Потом отбираем 1-2 лучших по эффекту за 30 дней, простоте запуска, owner и повторяемости.",
            "После отбора собираем структуру записки и только потом просим первый черновик.",
        ],
        {
            "steps": [
                {"title": "Варианты", "body": "Просим 5 реалистичных способов решить задачу в рамках ограничений."},
                {"title": "Отбор", "body": "Отбираем 1-2 лучших по эффекту за 30 дней, запуску и owner."},
                {"title": "Структура", "body": "Собираем план записки: проблема, решение, 30-дневный план, owner, метрики."},
                {"title": "Черновик", "body": "Только после структуры просим первый draft и редактируем его вручную."},
            ],
            "metrics": [
                {"title": "Ограничение", "body": "первые результаты нужны за 30 дней", "accent": "#B85B34"},
                {"title": "Старт", "body": "генерируем 5 вариантов, не 1", "accent": "#5A7268"},
                {"title": "Отбор", "body": "в shortlist попадают только 1-2 решения", "accent": "#10213B"},
            ],
            "bottom": "AI ускоряет старт. Критерии отбора и приоритеты все равно задает человек.",
        },
    ),
    Slide(
        "l19_option_matrix.svg",
        "l19",
        "Урок 19",
        "Матрица отбора: какие идеи реально брать в работу",
        "У варианта должна быть не только привлекательная формулировка, но и шанс дать эффект в первые 30 дней.",
        "table",
        "FW-L19-CASE-A",
        "Real compare screen с пятью вариантами решения задачи по адаптации сотрудников.",
        "#B85B34",
        "#5A7268",
        [
            "В shortlist попадают единая стартовая база знаний и набор типовых шаблонов по ежедневным задачам.",
            "Weekly review вопросов полезен как дополнительный слой, но не как главная ставка.",
            "Парные разборы кейсов и маршрут недели требуют больше согласования и зависят от сильных сотрудников.",
        ],
        {
            "headers": ["Идея", "Эффект за 30 дней", "Простой запуск", "Понятный owner", "Вердикт"],
            "widths": [430, 220, 220, 240, 310],
            "rows": [
                ["Единая стартовая база знаний", "да", "да", "да", "Берем в shortlist"],
                ["Типовые шаблоны ежедневных задач", "да", "да", "да", "Берем в shortlist"],
                ["Маршрут первой недели", "частично", "да", "да", "Нужна привязка к реальной работе"],
                ["Парные разборы типовых кейсов", "частично", "частично", "нет", "Сильно зависит от вовлечения сильных сотрудников"],
                ["Weekly review вопросов новичков", "да", "да", "частично", "Полезно как доп. слой, не как core-решение"],
            ],
            "row_height": 70,
            "bottom": "Ошибка новичка: считать первый список идей уже хорошим решением. Сильная работа начинается с отбора.",
        },
    ),
    Slide(
        "l19_memo_structure.svg",
        "l19",
        "Урок 19",
        "Структура записки на 1 страницу",
        "После отбора AI должен помочь собрать не красивый текст, а управленческий каркас решения.",
        "dashboard",
        "FW-L19-CASE-A",
        "Concrete memo screen: проблема, решение, 30-дневный план, owner и метрики.",
        "#B85B34",
        "#5A7268",
        [
            "Проблема: адаптация новых сотрудников длится 5-6 недель, руководители повторяют одно и то же вручную, знания разбросаны по чатам.",
            "Решение: короткая стартовая база знаний + набор типовых шаблонов по ежедневным задачам.",
            "Почему реалистично: материалы уже частично есть, а запуск не превращается в тяжелый проект.",
        ],
        {
            "artifact": {
                "title": "Что должно войти в записку",
                "bullets": [
                    "Проблема: долгий вход в работу и хаос в знаниях.",
                    "Решение: стартовая база знаний + шаблоны типовых задач.",
                    "Почему реалистично: часть материалов уже существует, запуск быстрый.",
                ],
            },
            "metrics": [
                {"title": "Первые 30 дней", "body": "собрать top-20 вопросов, 10 шаблонов и протестировать на 1-2 новичках", "accent": "#B85B34"},
                {"title": "Owner", "body": "руководитель операционной команды или куратор адаптации", "accent": "#5A7268"},
                {"title": "Метрики", "body": "время до самостоятельной задачи, число повторяющихся вопросов, reusable templates", "accent": "#10213B"},
                {"title": "Правило", "body": "не просим final text с нуля - сначала структура, потом draft", "accent": "#7A4B2A"},
            ],
            "bottom": "Перед первым черновиком отдельно фиксируем аудиторию, цель документа и критерии отбора.",
        },
    ),
    Slide(
        "l19_final_card.svg",
        "l19",
        "Урок 19",
        "После урока: соберите структуру одного документа",
        "Сильный результат урока - не красивый AI-текст, а понятная структура рабочего документа.",
        "card",
        "FW-L19-CASE-A",
        "Финальная плашка урока: закрепить схему варианты -> отбор -> структура.",
        "#B85B34",
        "#5A7268",
        [
            "Действие после урока: взять один давно откладываемый документ и собрать к нему структуру через 4 шага.",
            "Перед draft зафиксировать критерии отбора и приоритеты.",
        ],
        {
            "kicker": "После урока",
            "body": "Не просите AI сразу написать весь документ: сначала соберите варианты, shortlist и структуру.",
            "note": "Если критерии не названы, модель почти всегда выдаст уверенный, но слабый общий текст.",
            "panel_fill": tint("#B85B34", 0.93),
        },
    ),
    Slide(
        "l20_title_card.svg",
        "l20",
        "Урок 20",
        "Первичное исследование темы",
        "AI помогает быстро сориентироваться в теме, но не заменяет проверку источников.",
        "card",
        "FW-L20-CASE-A",
        "Открывающий экран урока про вход в новую тему без иллюзии точности.",
        "#496A8B",
        "#B67B32",
        [
            "Главная экранная фраза: AI полезен как карта местности, а не как окончательная истина.",
            "Кейс урока: быстрый вход в тему retrieval-augmented generation перед рабочим обсуждением AI-продукта.",
        ],
        {
            "kicker": "Урок 20",
            "body": "Хороший AI-исследователь сначала строит карту темы, потом список вопросов, и только затем отправляет вас к источникам.",
            "note": "Кейс: RAG, retrieval, embeddings, chunking, качество найденного контекста, стоимость поддержки.",
        },
    ),
    Slide(
        "l20_topic_entry_map.svg",
        "l20",
        "Урок 20",
        "Трехшаговый вход в новую тему",
        "Зрелое использование AI для исследования начинается с карты темы, а заканчивается списком того, что надо проверить отдельно.",
        "workflow",
        "FW-L20-CASE-A",
        "Main framework урока: карта темы -> ключевые вопросы -> внешняя проверка.",
        "#496A8B",
        "#B67B32",
        [
            "Шаг 1: получить карту темы простым рабочим языком.",
            "Шаг 2: выделить ключевые понятия, спорные места и типичные ошибки понимания.",
            "Шаг 3: сформировать список того, что нужно проверить по реальным источникам.",
        ],
        {
            "steps": [
                {"title": "Карта темы", "body": "Что такое RAG, из каких блоков состоит и где реально используется."},
                {"title": "Ключевые вопросы", "body": "Retrieval, embeddings, chunking, relevance, grounded answer и ошибки понимания."},
                {"title": "Проверка", "body": "Какие факты, цифры и ограничения нельзя брать на веру из красивого объяснения."},
            ],
            "metrics": [
                {"title": "Шаг 1", "body": "AI для ориентации", "accent": "#496A8B"},
                {"title": "Шаг 2", "body": "источники для проверки", "accent": "#B67B32"},
                {"title": "Шаг 3", "body": "человек для вывода и решения", "accent": "#10213B"},
            ],
            "bottom": "Не путайте карту темы с самой темой: AI снижает туман на старте, но не закрывает фактчек.",
        },
    ),
    Slide(
        "l20_rag_system_map.svg",
        "l20",
        "Урок 20",
        "RAG на одном экране",
        "Concrete screen для быстрого объяснения: модель отвечает не только из памяти, а с опорой на внешний найденный контекст.",
        "grid",
        "FW-L20-CASE-A",
        "One-screen system map по теме RAG.",
        "#496A8B",
        "#B67B32",
        [
            "RAG = пользовательский вопрос + поиск документов + передача контекста в модель + grounded answer.",
            "Сценарий полезен для баз знаний, политик, инструкций и ответов по внутренним документам.",
        ],
        {
            "cards": [
                {"title": "1. Пользовательский вопрос", "body": "Запрос формулирует, какую задачу система должна решить и по какому документному слою искать ответ."},
                {"title": "2. Retrieval", "body": "Система ищет релевантные куски документов, а не пытается отвечать только из внутренних знаний модели."},
                {"title": "3. Контекст в модель", "body": "Найденные фрагменты подаются в prompt, чтобы ответ опирался на конкретный материал."},
                {"title": "4. Grounded answer", "body": "Сильный ответ связан с найденным контекстом, а не просто звучит уверенно и красиво."},
            ],
            "bottom": "Типичная ошибка новичка: думать, что RAG автоматически решает hallucinations без настройки retrieval и оценки качества.",
        },
    ),
    Slide(
        "l20_rag_validation_table.svg",
        "l20",
        "Урок 20",
        "Что нельзя принимать на веру из AI-объяснения",
        "В исследовании темы важен не только красивый summary, но и список вопросов, которые обязаны уйти во внешнюю проверку.",
        "table",
        "FW-L20-CASE-A",
        "Validation table для темы RAG: что AI объясняет быстро, а что надо перепроверять по первичным источникам.",
        "#496A8B",
        "#B67B32",
        [
            "По AI-summary нельзя финально судить о качестве retrieval, доступах к данным и стоимости поддержки системы.",
            "Для важных решений нужны evaluation reports, security policy, архитектурные расчеты и реальные тестовые примеры.",
        ],
        {
            "headers": ["Что смотрим", "Что AI объясняет быстро", "Что надо проверить отдельно", "Тип источника"],
            "widths": [300, 360, 390, 370],
            "rows": [
                ["Качество retrieval", "общую механику поиска", "precision/recall, тестовые вопросы, провалы relevance", "evaluation reports / docs"],
                ["Доступы и данные", "верхнеуровневые ограничения", "какие документы индексируем и кто их видит", "security policy / architecture"],
                ["Стоимость и поддержка", "основные факторы системы", "обновление индекса, storage, ops-нагрузка", "архитектурные оценки"],
                ["Hallucination risk", "почему grounded answer лучше", "где ответ все равно может быть уверенным, но слабым", "реальные тестовые сценарии"],
            ],
            "row_height": 74,
            "bottom": "Формула урока: AI для ориентации. Источники для проверки. Человек для вывода и решения.",
        },
    ),
    Slide(
        "l20_final_card.svg",
        "l20",
        "Урок 20",
        "После урока: прогоните через AI одну незнакомую тему",
        "Сильный результат здесь - карта темы и список вопросов к источникам, а не ощущение, что тема уже освоена.",
        "card",
        "FW-L20-CASE-A",
        "Финальная плашка урока: закрепить трехшаговый вход в новую область знаний.",
        "#496A8B",
        "#B67B32",
        [
            "Действие после урока: выбрать одну тему, где пока есть туман, и пройти по схеме карта -> вопросы -> проверка.",
            "Отдельно выписать, какие реальные источники будете смотреть после AI-карты.",
        ],
        {
            "kicker": "После урока",
            "body": "Выберите одну незнакомую тему и отдельно выпишите, что после AI-объяснения нужно проверить по источникам.",
            "note": "Цель упражнения - сократить туман на старте, а не подменить исследование красивым summary.",
            "panel_fill": tint("#496A8B", 0.93),
        },
    ),
    Slide(
        "l21_title_card.svg",
        "l21",
        "Урок 21",
        "AI как инструмент самообучения",
        "AI полезен как тренер по объяснению и проверке понимания, а не как источник истины.",
        "card",
        "L21-CASE-A",
        "Открывающий экран финального блока: AI работает как learning partner, а не просто быстрый ответчик.",
        "#215B5D",
        "#B86A2B",
        [
            "Главная экранная фраза: AI особенно полезен, когда нужно не просто узнать ответ, а действительно разобраться.",
            "Кейс урока: когортный анализ против обычной помесячной статистики.",
        ],
        {
            "kicker": "Урок 21",
            "body": "Для взрослого обучения AI полезнее в роли объясняющего партнера, чем в роли автомата готовых ответов.",
            "note": "Режим урока: объясни простыми словами -> сравни -> задай вопросы -> проверь мой ответ -> скажи, что проверить отдельно.",
            "panel_fill": tint("#163E4A", 0.88),
            "header_fill": tint("#163E4A", 0.9),
        },
    ),
    Slide(
        "l21_learning_loop.svg",
        "l21",
        "Урок 21",
        "Learning loop: как учиться через диалог с AI",
        "Хорошее обучение активно: вы не только слушаете объяснение, но и проверяете себя на понимание.",
        "workflow",
        "L21-CASE-A",
        "Главная схема урока 21: объяснение, сравнение, вопросы, feedback и внешняя проверка.",
        "#215B5D",
        "#B86A2B",
        [
            "Шаг 1: объясни тему простым рабочим языком.",
            "Шаг 2: сравни с похожим понятием, чтобы убрать путаницу.",
            "Шаг 3: задай вопросы и заставь меня ответить.",
            "Шаг 4: проверь ответ и скажи, что я понял неполно.",
            "Шаг 5: выдели, что нужно проверить по надежным источникам.",
        ],
        {
            "steps": [
                {"title": "Объясни", "body": "Когортный анализ простыми словами для PM, без академического языка."},
                {"title": "Сравни", "body": "Против обычной помесячной статистики по одному набору вопросов."},
                {"title": "Спроси", "body": "5 коротких вопросов, которые проверяют реальное понимание, а не узнавание слов."},
                {"title": "Проверь", "body": "Что я понял верно, что понял неполно и где еще путаюсь."},
                {"title": "Проверь снаружи", "body": "Что нельзя принимать на веру и нужно сверить с надежными источниками."},
            ],
            "bottom": "Explanation mode полезен для обучения. Truth mode все равно требует внешней проверки.",
        },
    ),
    Slide(
        "l21_cohort_compare.svg",
        "l21",
        "Урок 21",
        "Когортный анализ vs обычная помесячная статистика",
        "Сильное объяснение не останавливается на определении: оно снимает типичную путаницу через прямое сравнение.",
        "table",
        "L21-CASE-A",
        "Concrete compare table для кейса про когортный анализ.",
        "#215B5D",
        "#B86A2B",
        [
            "Когортный анализ показывает поведение одной группы во времени, а месячная статистика - общее состояние периода.",
            "Типичная ошибка новичка: путать рост общего числа пользователей с хорошим удержанием.",
        ],
        {
            "headers": ["Вопрос", "Когортный анализ", "Обычная помесячная статистика"],
            "widths": [310, 555, 555],
            "rows": [
                ["Что показывает", "поведение одной группы во времени", "общее состояние за месяц"],
                ["Где полезен", "удержание, повторные действия, качество набора", "общий объем, динамика периода"],
                ["Ошибка новичка", "думать, что это просто еще одна сводка по месяцам", "делать вывод о качестве удержания без разбивки по группам"],
                ["Когда брать", "когда важно понять, что происходит с конкретной волной пользователей", "когда нужна общая картина периода"],
            ],
            "row_height": 84,
            "bottom": "Если после объяснения не стало проще различать похожие понятия, значит, learning loop не закончен.",
        },
    ),
    Slide(
        "l21_understanding_check.svg",
        "l21",
        "Урок 21",
        "Проверка понимания: что уже понял, что еще нет",
        "Самообучение становится рабочим только тогда, когда AI не просто объясняет, а дает вам обратную связь на ответ.",
        "dashboard",
        "L21-CASE-A",
        "Экран с примером student answer, AI feedback и списком внешних проверок.",
        "#215B5D",
        "#B86A2B",
        [
            "Пример ответа ученика: когорта - это группа пользователей с общим стартом; когортный анализ показывает их поведение во времени; месячная сводка не показывает качество удержания.",
            "Типовой AI-feedback: главное понято верно, но надо уточнить, что когорты нужны не только для retention, а также для повторных покупок, возвратов и активации.",
        ],
        {
            "artifact": {
                "title": "Пример ответа ученика",
                "bullets": [
                    "Когорта - это группа пользователей, которые пришли в одно время.",
                    "Когортный анализ показывает, как эта группа ведет себя дальше.",
                    "Обычная сводка по месяцу дает общие числа, но не качество удержания конкретной группы.",
                ],
            },
            "metrics": [
                {"title": "Что понял", "body": "когорта = группа с общим стартом; анализ = поведение во времени", "accent": "#215B5D"},
                {"title": "Что неполно", "body": "когорты нужны не только для retention, но и для повторных покупок и активации", "accent": "#B86A2B"},
                {"title": "5 вопросов", "body": "используем AI, чтобы проверить разницу, а не просто перечитать определение", "accent": "#10213B"},
                {"title": "Проверить отдельно", "body": "как компания считает retention, что считается возвратом и на каком интервале сравниваются когорты", "accent": "#6A4A24"},
            ],
            "bottom": "Зрелое самообучение = объяснение + сравнение + проверка себя + список того, что нельзя брать на веру.",
        },
    ),
    Slide(
        "l21_final_card.svg",
        "l21",
        "Урок 21",
        "После урока: используйте AI для объяснения одной новой темы",
        "Сильный результат урока - не просто понять термин, а пройти learning loop до обратной связи на свой ответ.",
        "card",
        "L21-CASE-A",
        "Финальная плашка урока: перевести AI из answer engine в learning engine.",
        "#215B5D",
        "#B86A2B",
        [
            "Действие после урока: взять одну новую тему и пройти цикл объясни -> сравни -> проверь меня.",
            "Отдельно сохранить список того, что надо проверить по надежным источникам.",
        ],
        {
            "kicker": "После урока",
            "body": "Возьмите одну новую тему и заставьте AI не только объяснить ее, но и проверить ваш ответ по ней.",
            "note": "Если вопрос важен для работы, финальный truth check всегда остается за внешними источниками.",
            "panel_fill": tint("#163E4A", 0.9),
        },
    ),
    Slide(
        "l22_title_card.svg",
        "l22",
        "Урок 22",
        "Как не превратить AI в лишнюю игрушку",
        "AI ценен не интересом, а измеримым эффектом в работе.",
        "card",
        "L22-CASE-A / L22-CASE-B",
        "Открывающий экран про полезность сценариев: от развлекательного интереса к repeatable value.",
        "#A04428",
        "#2F6B5C",
        [
            "Главная экранная фраза: ценность AI измеряется не восторгом, а повторяемым рабочим эффектом.",
            "Кейсы урока: креативные названия для встречи vs follow-up после клиентского созвона.",
        ],
        {
            "kicker": "Урок 22",
            "body": "Если AI не ускоряет, не улучшает и не облегчает повторяющуюся задачу, это пока не внедрение.",
            "note": "Контраст урока: названия для планерки не встраиваются в процесс; follow-up после созвона дает 8-10 минут -> 2-3 минуты на черновик.",
            "panel_fill": tint("#7B311A", 0.89),
            "header_fill": tint("#7B311A", 0.91),
        },
    ),
    Slide(
        "l22_toy_vs_tool_compare.svg",
        "l22",
        "Урок 22",
        "Игрушка vs инструмент",
        "Контрастный compare screen нужен, чтобы быстро отделять развлечение от сценария с repeatable value.",
        "table",
        "L22-CASE-A / L22-CASE-B",
        "Ключевая таблица урока 22: сравнение двух кейсов по пяти критериям.",
        "#A04428",
        "#2F6B5C",
        [
            "CASE-A: 20 названий для внутренней встречи - нет повторяемости, эффекта и встроенности в процесс.",
            "CASE-B: follow-up после созвона - высокий repeat rate, ясный результат, measurable effect и встраиваемость.",
        ],
        {
            "headers": ["Критерий", "CASE-A: названия для встречи", "CASE-B: follow-up после созвона"],
            "widths": [320, 550, 550],
            "rows": [
                ["Повторяемость", "низкая", "высокая"],
                ["Ясность результата", "низкая", "высокая"],
                ["Измеримый эффект", "нет", "да"],
                ["Встраиваемость в процесс", "нет", "да"],
                ["Стоит внедрять", "нет", "да"],
            ],
            "row_height": 78,
            "bottom": "Главный вопрос: если убрать AI из этого сценария, работа станет заметно медленнее, тяжелее или менее структурированной?",
        },
    ),
    Slide(
        "l22_practical_filter_scorecard.svg",
        "l22",
        "Урок 22",
        "Practical filter: стоит ли вообще внедрять этот сценарий",
        "Перед внедрением сценарий должен пройти короткий фильтр полезности, а не только показаться интересным.",
        "dashboard",
        "L22-CASE-A / L22-CASE-B",
        "Scorecard-слайд с 5 вопросами фильтра и decision rule.",
        "#A04428",
        "#2F6B5C",
        [
            "Фильтр: задача повторяется, результат понятен, эффект можно заметить, без AI работа реально тяжелее, сценарий можно повторить завтра.",
            "Decision rule: 4-5 'да' = кандидат на внедрение; 2-3 = на тест; 0-1 = пока игрушка.",
        ],
        {
            "artifact": {
                "title": "5 вопросов фильтра полезности",
                "bullets": [
                    "Это повторяется хотя бы несколько раз в неделю?",
                    "Результат можно быстро оценить?",
                    "Есть экономия времени или снижение трения?",
                    "Это можно встроить в реальный процесс?",
                    "Я готов повторить это завтра без героизма?",
                ],
            },
            "metrics": [
                {"title": "CASE-A", "body": "1-2 'да'. Интересно, но нет repeatable value и measurable effect.", "accent": "#A04428"},
                {"title": "CASE-B", "body": "4-5 'да'. Повторяемый сценарий с ясным результатом и рабочим SLA.", "accent": "#2F6B5C"},
                {"title": "Решение", "body": "4-5 = внедряем, 2-3 = тестируем, 0-1 = не тратим время на rollout", "accent": "#10213B"},
                {"title": "Смысл фильтра", "body": "AI должен стать частью процесса, а не разовым развлечением под впечатлением", "accent": "#6A4A24"},
            ],
            "bottom": "Самая частая ошибка - путать интерес к технологии с реальным изменением рабочего процесса.",
        },
    ),
    Slide(
        "l22_followup_impact_metrics.svg",
        "l22",
        "Урок 22",
        "Простой, но полезный сценарий: follow-up после созвона",
        "Взрослый B2C/B2B сценарий видно по конкретным метрикам: время, SLA и повторяемость.",
        "dashboard",
        "L22-CASE-B",
        "Metric block для сильного сценария из урока 22.",
        "#A04428",
        "#2F6B5C",
        [
            "Процесс: после каждого клиентского созвона менеджер просит AI собрать короткий черновик письма с 3 договоренностями и следующим шагом.",
            "Контроль: письмо уходит только после ручной правки, без несуществующих обещаний и без потери фактов встречи.",
        ],
        {
            "artifact": {
                "title": "Почему это уже инструмент, а не игрушка",
                "bullets": [
                    "Сценарий повторяется после каждого клиентского созвона.",
                    "Результат понятен: короткое follow-up письмо с договоренностями и следующим шагом.",
                    "Процесс легко встроить в ежедневную работу аккаунт-менеджера.",
                ],
            },
            "metrics": [
                {"title": "До AI", "body": "8-10 минут на письмо после звонка", "accent": "#A04428"},
                {"title": "С AI", "body": "2-3 минуты до первого черновика", "accent": "#2F6B5C"},
                {"title": "SLA", "body": "письма стабильно уходят в течение 30 минут после встречи", "accent": "#10213B"},
                {"title": "Контроль", "body": "ручная правка обязательна: AI не добавляет обещаний, которых не было", "accent": "#6A4A24"},
            ],
            "bottom": "Зрелый сценарий всегда можно описать как процесс, артефакт и measurable effect.",
        },
    ),
    Slide(
        "l22_final_card.svg",
        "l22",
        "Урок 22",
        "После урока: выберите 3 сценария с понятной пользой",
        "Сильный результат урока - shortlist сценариев, где AI даст measurable effect, а не просто интересный опыт.",
        "card",
        "L22-CASE-A / L22-CASE-B",
        "Финальная плашка урока: закрепить фильтр полезности на собственных задачах.",
        "#A04428",
        "#2F6B5C",
        [
            "Действие после урока: прогнать через фильтр три своих сценария и выбрать те, где эффект понятен уже завтра.",
            "Для командного пилота отметить один сценарий, который можно сделать общим стандартом.",
        ],
        {
            "kicker": "После урока",
            "body": "Выберите три сценария, где AI не развлекает, а дает измеримую экономию времени или снижение трения.",
            "note": "Если у сценария нет повторяемости и понятного результата, он пока не заслуживает rollout.",
            "panel_fill": tint("#7B311A", 0.9),
        },
    ),
    Slide(
        "l23_title_card.svg",
        "l23",
        "Урок 23",
        "Как строить личную систему использования AI",
        "Зрелое использование AI - это связка: задача, шаблон, проверка, хранение лучшей практики.",
        "card",
        "L23-CASE-A / L23-BRIDGE-A",
        "Открывающий экран предпоследнего урока: от разрозненных находок к системе, пригодной для личного и командного режима.",
        "#163E62",
        "#8A6A2B",
        [
            "Главная экранная фраза: если шаблоны, сценарии и проверка лежат врозь, системы еще нет.",
            "Кейс урока: личная AI-система из 5 блоков и мост в командный proof path.",
        ],
        {
            "kicker": "Урок 23",
            "body": "Сильная AI-система не выглядит красиво ради себя: она помогает повторять удачные сценарии без хаоса.",
            "note": "Минимальная форма хранения может быть очень простой: одна таблица, один документ, один Notion workspace или одна папка.",
            "panel_fill": tint("#163E62", 0.88),
            "header_fill": tint("#163E62", 0.9),
        },
    ),
    Slide(
        "l23_personal_system_stack.svg",
        "l23",
        "Урок 23",
        "Пять блоков личной AI-системы",
        "Система нужна не для красоты, а чтобы хороший сценарий можно было повторить через неделю и через месяц.",
        "workflow",
        "L23-CASE-A",
        "One-screen stack личной AI-системы.",
        "#163E62",
        "#8A6A2B",
        [
            "Блоки системы: сценарии, шаблоны, чек-лист проверки, правила безопасности и proof log.",
            "Минимальный критерий качества системы: удобно сохранять и повторять удачные сценарии, а не только собирать красивые папки.",
        ],
        {
            "steps": [
                {"title": "Сценарии", "body": "Список повторяющихся задач: follow-up, summary документа, внутренние сообщения."},
                {"title": "Шаблоны", "body": "Лучшие prompts и заготовки: followup_v2, summary_ops_v1, tone-edit."},
                {"title": "Проверка", "body": "Короткий quality checklist: факт, контекст, тон, следующий шаг, лишние обещания."},
                {"title": "Безопасность", "body": "Что нельзя отправлять в AI: персональные данные, конфиденциальные цифры, неанонимизированные договоры."},
                {"title": "Proof log", "body": "Что реально сработало: сценарий, дата, эффект, оставшийся риск."},
            ],
            "bottom": "Любой формат хранения подходит, если он помогает повторять лучшую практику, а не только выглядит организованно.",
        },
    ),
    Slide(
        "l23_system_table.svg",
        "l23",
        "Урок 23",
        "Как выглядит живая личная система",
        "Взрослый screen для финального блока: не философия, а конкретная структура хранения и заполненный пример.",
        "table",
        "L23-CASE-A",
        "Concrete table из урока 23: блок, что хранится, пример.",
        "#163E62",
        "#8A6A2B",
        [
            "Система хранит не только prompts, но и quality gate, правила безопасности и доказательства реальной пользы.",
            "Примеры сценариев: follow-up после встречи, summary внутренних документов, внутренние сообщения на согласование.",
        ],
        {
            "headers": ["Блок", "Что хранится", "Пример"],
            "widths": [250, 500, 670],
            "rows": [
                ["Сценарии", "список повторяющихся задач", "follow-up после встречи; summary документа; внутреннее сообщение"],
                ["Шаблоны", "лучшие prompts и заготовки", "followup_v2; summary_ops_v1; message_tone_fix_v1"],
                ["Проверка", "короткий quality checklist", "факт; контекст; тон; следующий шаг; лишние обещания"],
                ["Безопасность", "правила, что нельзя отправлять в AI", "персональные данные; конфиденциальные цифры; неанонимизированные договоры"],
                ["Proof log", "что реально сработало", "сценарий; дата; эффект; оставшийся риск"],
            ],
            "row_height": 76,
            "bottom": "Если в системе нет proof log, у вас нет доказательства пользы - только набор находок.",
        },
    ),
    Slide(
        "l23_team_proof_path.svg",
        "l23",
        "Урок 23",
        "Из личной системы в командный стандарт",
        "Финальный блок должен показывать путь в B2B: из личной практики рождается общий сценарий, шаблон и owner.",
        "workflow",
        "L23-BRIDGE-A",
        "Team proof path для моста из урока 23 в урок 24.",
        "#163E62",
        "#8A6A2B",
        [
            "Командный proof path: один общий сценарий, один общий шаблон, один общий чек-лист, один owner, 2-3 proof examples и одна метрика.",
            "Именно этот путь позволяет менеджеру увидеть первый наблюдаемый стандарт, а не ощущение, что команда просто что-то пробует.",
        ],
        {
            "steps": [
                {"title": "1 общий сценарий", "body": "Берем задачу, которая повторяется у нескольких людей в команде."},
                {"title": "1 общий шаблон", "body": "Фиксируем prompt или template, который реально помогает в этом сценарии."},
                {"title": "1 чек-лист", "body": "Определяем, как быстро проверить качество результата перед отправкой."},
                {"title": "1 owner", "body": "Нужен человек, который отвечает за шаблон, review и обновления."},
                {"title": "2-3 proof examples", "body": "Собираем реальные примеры использования, а не обещания будущей пользы."},
                {"title": "1 team metric", "body": "Выбираем простую метрику поведения или экономии времени."},
            ],
            "bottom": "Так личная система перестает быть личным лайфхаком и становится основой командного стандарта.",
        },
    ),
    Slide(
        "l23_final_card.svg",
        "l23",
        "Урок 23",
        "После урока: соберите свою AI-систему в одном месте",
        "Сильный результат урока - связать сценарии, шаблоны, проверку, безопасность и proof log в одну рабочую систему.",
        "card",
        "L23-CASE-A / L23-BRIDGE-A",
        "Финальная плашка урока: закрепить систему и обозначить shared scenario для команды.",
        "#163E62",
        "#8A6A2B",
        [
            "Действие после урока: собрать личную систему в одном месте, в любом удобном формате.",
            "Для корпоративного режима отдельно отметить один кандидат в shared team scenario.",
        ],
        {
            "kicker": "После урока",
            "body": "Соберите сценарии, шаблоны, quality checklist, правила безопасности и proof log в одном месте.",
            "note": "Если работаете в команде, сразу выделите один сценарий, который можно вынести в общий пилот.",
            "panel_fill": tint("#163E62", 0.9),
        },
    ),
    Slide(
        "l24_title_card.svg",
        "l24",
        "Урок 24",
        "План внедрения на 14 дней",
        "Внедрение AI начинается не с трансформации, а с 2 недель дисциплинированной практики.",
        "card",
        "FW-L24-CASE-A / FW-L24-CASE-B / L24-BRIDGE-A",
        "Открывающий экран финала Core: переход от обучения к rollout и B2B proof pack.",
        "#154E47",
        "#B86A2B",
        [
            "Главная экранная фраза: сильный финал курса = сценарии, шаблоны, проверка и короткий rollout, а не общие слова.",
            "Кейсы урока: личный 14-дневный план и B2B mini-rollout для команды из 5 аккаунт-менеджеров.",
        ],
        {
            "kicker": "Финал Core",
            "body": "Теперь у ученика должен появиться не только навык, но и короткий реалистичный план внедрения для себя и команды.",
            "note": "Блок 24 опирается на bridge из урока 23: личные сценарии, лучшие шаблоны, quality checklist и proof log превращаются в rollout.",
            "panel_fill": tint("#123B36", 0.87),
            "header_fill": tint("#123B36", 0.9),
        },
    ),
    Slide(
        "l24_14_day_rollout_plan.svg",
        "l24",
        "Урок 24",
        "Личный 14-дневный план внедрения",
        "Не идеальная автоматизация, а короткий и реалистичный rollout на 2-3 сценариях при нормальной занятости.",
        "table",
        "FW-L24-CASE-A",
        "Главный concrete screen финала: короткий rollout table на 14 дней.",
        "#154E47",
        "#B86A2B",
        [
            "Период 1-3: baseline по follow-up и первый prompt.",
            "Период 4-6: summary документов и quality notes по ошибкам.",
            "Период 7-8: внутренние сообщения и тон-редактура.",
            "Период 9-10: повтор лучшего сценария недели.",
            "Период 11-12: mini-library и self-report.",
            "Период 13-14: go / no-go и personal rollout note.",
        ],
        {
            "headers": ["Период", "Фокус", "Артефакт", "Что меряем"],
            "widths": [190, 350, 500, 380],
            "rows": [
                ["Дни 1-3", "Baseline и первый template", "baseline + prompt v1 + template 1", "стало ли быстрее начать follow-up"],
                ["Дни 4-6", "Summary документа и ошибки", "summary v1 + checklist notes + template 2", "где AI ошибается и где экономит время"],
                ["Дни 7-8", "Черновики внутренних сообщений", "draft v1 + final version", "сколько ручных правок остается"],
                ["Дни 9-10", "Повторяем лучший сценарий", "repeat result", "проверка повторяемости пользы"],
                ["Дни 11-12", "Mini-library и self-report", "3 шаблона + short report", "что хочется сохранить дальше"],
                ["Дни 13-14", "Go / no-go и следующий цикл", "personal rollout note", "есть ли дисциплина, а не хаос"],
            ],
            "row_height": 72,
            "bottom": "На этом экране rollout должен выглядеть выполнимым: 2-3 сценария, 3 шаблона, короткий proof, а не амбициозная трансформация.",
        },
    ),
    Slide(
        "l24_b2b_rollout_dashboard.svg",
        "l24",
        "Урок 24",
        "B2B mini-rollout: что показать ЛПР через 14 дней",
        "Сильный корпоративный финал выглядит как proof pack: общий сценарий, owner, 3 примера и одна простая метрика.",
        "dashboard",
        "FW-L24-CASE-B",
        "Executive-style dashboard для B2B mini-rollout артефакта.",
        "#154E47",
        "#B86A2B",
        [
            "Команда: 5 аккаунт-менеджеров. Общий сценарий: follow-up после клиентских созвонов. Owner: team lead.",
            "Expected proof через 14 дней: 1 общий шаблон, 3 реальных примера писем и короткий отчет team lead.",
        ],
        {
            "artifact": {
                "title": "Mini-rollout artifact",
                "bullets": [
                    "Shared scenario: follow-up после клиентских созвонов.",
                    "Owner: team lead клиентского направления.",
                    "Участники: 5 аккаунт-менеджеров.",
                    "Review date: через 14 дней после старта.",
                ],
            },
            "metrics": [
                {"title": "Метрика 1", "body": "доля follow-up писем, отправленных в течение 30 минут после встречи", "accent": "#154E47"},
                {"title": "Метрика 2", "body": "среднее время на подготовку первого черновика письма", "accent": "#B86A2B"},
                {"title": "Метрика 3", "body": "число писем, где менеджер использовал общий шаблон", "accent": "#10213B"},
                {"title": "Expected proof", "body": "1 template + 3 real examples + short team lead report", "accent": "#6A4A24"},
            ],
            "bottom": "Финал взрослого курса должен закрываться не словами про вдохновение, а формой доказательства внедрения.",
        },
    ),
    Slide(
        "l24_final_bridge.svg",
        "l24",
        "Урок 24",
        "Из уроков 21-23 в рабочий rollout",
        "Финал Core силен тогда, когда предыдущие уроки собираются в одну систему, а не остаются отдельными приемами.",
        "workflow",
        "L24-BRIDGE-A / FW-L24-CASE-A / FW-L24-CASE-B",
        "Bridge screen: learning loop, scenario filter, personal system и proof log становятся планом внедрения.",
        "#154E47",
        "#B86A2B",
        [
            "Из урока 21 берем learning loop: объяснить, сравнить, проверить понимание, сверить с источниками.",
            "Из урока 22 берем practical filter: какие сценарии вообще стоят rollout.",
            "Из урока 23 берем личную систему, templates, checklist и proof log.",
            "В уроке 24 все это превращается в 14-дневный план и B2B proof pack.",
        ],
        {
            "steps": [
                {"title": "Урок 21", "body": "Learning loop делает новое знание рабочим, а не пассивно просмотренным."},
                {"title": "Урок 22", "body": "Practical filter отсеивает игрушки и оставляет сценарии с measurable effect."},
                {"title": "Урок 23", "body": "Личная система сохраняет templates, checklist, safety rules и proof log."},
                {"title": "Урок 24", "body": "Все это становится rollout plan на 14 дней и proof pack для команды."},
            ],
            "metrics": [
                {"title": "Input", "body": "3 личных сценария + 2 лучших шаблона + 1 checklist", "accent": "#154E47"},
                {"title": "Output", "body": "14-дневный план + shared scenario + одна простая метрика", "accent": "#B86A2B"},
                {"title": "Финальный смысл", "body": "теперь у ученика есть система внедрения, а не просто набор знаний про AI", "accent": "#10213B"},
            ],
            "bottom": "Формула финала: не 'теперь вы много знаете про AI', а 'теперь у вас есть сценарии, шаблоны, проверка и короткий rollout'.",
        },
    ),
    Slide(
        "l24_final_card.svg",
        "l24",
        "Урок 24",
        "Финальное действие после Core",
        "Теперь задача модуля - стать рабочим стандартом: лично, в команде и, если нужно, в корпоративном внедрении.",
        "card",
        "FW-L24-CASE-A / FW-L24-CASE-B / L24-BRIDGE-A",
        "Закрывающий экран всего блока 17-24 и всего Core module.",
        "#154E47",
        "#B86A2B",
        [
            "После урока: заполнить личный 14-дневный план и выбрать 2-3 сценария для следующего цикла.",
            "Для команды: зафиксировать общий сценарий, owner, template, checklist и одну метрику proof.",
        ],
        {
            "kicker": "Финал Core",
            "body": "У вас уже есть сценарии, шаблоны, проверка, proof log и короткий rollout. Этого достаточно, чтобы начать взрослое внедрение.",
            "note": "Следующий шаг - не обсуждать AI еще раз, а провести 14 дней дисциплинированной практики и принести proof pack.",
            "panel_fill": tint("#123B36", 0.88),
        },
    ),
]


RENDERERS = {
    "card": render_card,
    "columns": render_columns,
    "split": render_split,
    "table": render_table,
    "workflow": render_workflow,
    "grid": render_grid,
    "dashboard": render_dashboard,
}


def write_outline() -> None:
    lesson_map = {lesson.key: lesson for lesson in LESSONS}
    slides_by_lesson: dict[str, list[Slide]] = {lesson.key: [] for lesson in LESSONS}
    for slide in SLIDES:
        slides_by_lesson[slide.lesson_key].append(slide)

    lines = [
        "# Wave 3 Slides Outline",
        "",
        "Дата: 21 марта 2026",
        "Статус: outline полноценного visual-pack для уроков 17-24",
        "",
        "## Порядок использования",
        "",
        "1. Сначала открыть нужный SVG-asset по уроку.",
        "2. Потом свериться с `wave_3_slide_copy.md` для точной формулировки в кадре.",
        "3. Для process-логики и монтажа использовать `wave_3_diagrams.md`.",
        "",
    ]
    for lesson in LESSONS:
        lines.extend([f"## {lesson.unit}", ""])
        for slide in slides_by_lesson[lesson.key]:
            lines.append(f"- `{slide.filename}`")
            lines.append(f"  Назначение: {slide.purpose}")
            lines.append(f"  Source case ID: `{slide.case_id}`")
        lines.append("")
    (OUT / "wave_3_slides_outline.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_slide_copy() -> None:
    lines = [
        "# Wave 3 Slide Copy",
        "",
        "Дата: 21 марта 2026",
        "Статус: copy deck для visual-pack уроков 17-24",
        "",
    ]
    for slide in SLIDES:
        lines.extend(
            [
                f"## {slide.filename}",
                "",
                f"Единица: {slide.unit}",
                f"Case ID: `{slide.case_id}`",
                f"Заголовок: {slide.title}",
                f"Подзаголовок: {slide.subtitle}",
                "",
            ]
        )
        for item in slide.copy:
            lines.append(f"- {item}")
        lines.append("")
    (OUT / "wave_3_slide_copy.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_diagrams() -> None:
    lines = [
        "# Wave 3 Diagrams",
        "",
        "Дата: 21 марта 2026",
        "Статус: Mermaid-схемы для уроков 17-24",
        "",
        "Эти схемы можно использовать как:",
        "- основу для SVG-перерисовки;",
        "- быстрый visual appendix к уроку;",
        "- источник для отдельных process-slides и rough cut.",
        "",
    ]
    for lesson in LESSONS:
        lines.extend([f"## {lesson.unit}", "", lesson.diagram, ""])
    (OUT / "wave_3_diagrams.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_readme() -> None:
    lines = [
        "# Wave 3 Visual Assets",
        "",
        "Дата: 21 марта 2026",
        "Статус: рабочий пакет визуальных материалов для уроков 17-24",
        "",
        "## Что внутри",
        "",
        "- `visual_asset_generation_brief.md` - brief текущей волны.",
        "- `build_wave_3_assets.py` - генератор markdown и SVG-assets.",
        "- `wave_3_slides_outline.md` - карта deck по урокам 17-24.",
        "- `wave_3_slide_copy.md` - точный смысл каждого слайда.",
        "- `wave_3_diagrams.md` - Mermaid-схемы по всем 8 урокам.",
        "- SVG-файлы - реальные assets для записи, rough cut и монтажных compare-сцен.",
        "",
        "## Порядок работы",
        "",
        "1. Открыть `wave_3_slides_outline.md`.",
        "2. Перейти к нужному SVG-asset по уроку.",
        "3. Во время записи сверять формулировки с `wave_3_slide_copy.md`.",
        "4. Для process-экранов и объяснения логики брать `wave_3_diagrams.md`.",
        "",
        "## Карта SVG-файлов",
        "",
    ]
    for slide in SLIDES:
        lines.append(f"- `{slide.filename}` - {slide.unit}: {slide.title}")
    lines.extend(
        [
            "",
            "## Примечание",
            "",
            "Материалы собраны только внутри этой isolated-папки и опираются на уже утвержденные concrete assets для уроков 17-24.",
            "",
        ]
    )
    (OUT / "README.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_svgs() -> None:
    for slide in SLIDES:
        renderer = RENDERERS[slide.kind]
        (OUT / slide.filename).write_text(svg_wrap(renderer(slide)), encoding="utf-8")


def main() -> None:
    write_outline()
    write_slide_copy()
    write_diagrams()
    write_readme()
    write_svgs()


if __name__ == "__main__":
    main()
