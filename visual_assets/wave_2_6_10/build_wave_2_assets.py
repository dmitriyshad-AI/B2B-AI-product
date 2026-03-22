from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape


OUT = Path(__file__).resolve().parent
DATE = "21 марта 2026"

W = 1600
H = 900
BG = "#F6F1E8"
INK = "#10213B"
MUTED = "#5F6B7A"
ACCENT = "#C65A1E"
SAGE = "#5A7268"
INDIGO = "#6A56A5"
TEAL = "#2C6A7A"
PANEL = "#FFFDF8"
LINE = "#D7D0C1"
SOFT_ORANGE = "#FFF7EF"
SOFT_GREEN = "#EEF5F1"
SOFT_INDIGO = "#F7F5FD"
SOFT_SAND = "#F7F3EA"
FOOTER_TEXT = "Business-learning visual asset · Wave 2 production pack"


@dataclass
class Slide:
    filename: str
    unit: str
    title: str
    subtitle: str
    kind: str
    case_id: str
    purpose: str
    payload: dict
    copy_lines: list[str] = field(default_factory=list)


def wrap_lines(text: str, max_chars: int | None) -> list[str]:
    if max_chars is None:
        return [text]
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        lines.extend(wrap(paragraph, max_chars))
    return lines or [text]


def chars_for(width: int, size: int) -> int:
    return max(10, int(width / (size * 0.58)))


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
    anchor: str = "start",
) -> str:
    if line_height is None:
        line_height = int(size * 1.35)
    parts = wrap_lines(text, max_chars)
    tspans = []
    for idx, part in enumerate(parts):
        dy = "0" if idx == 0 else str(line_height)
        tspans.append(f'<tspan x="{x}" dy="{dy}">{escape(part)}</tspan>')
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
        f'font-family="{family}" font-weight="{weight}" fill="{fill}">'
        f'{"".join(tspans)}</text>'
    )


def rect(
    x: int,
    y: int,
    w: int,
    h: int,
    fill: str = PANEL,
    stroke: str = LINE,
    rx: int = 28,
    sw: int = 2,
) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def pill(x: int, y: int, w: int, h: int, text: str, fill: str, text_fill: str = "white") -> str:
    return rect(x, y, w, h, fill=fill, stroke=fill, rx=h // 2) + t(
        x + 22,
        y + h - 17,
        text,
        22,
        text_fill,
        "700",
        max_chars=chars_for(w - 40, 22),
        line_height=24,
    )


def tag(x: int, y: int, text: str, fill: str = "#E9E1D3", text_fill: str = INK) -> str:
    w = max(120, min(170, 28 + len(text) * 8))
    return rect(x, y, w, 34, fill=fill, stroke=fill, rx=17, sw=1) + t(
        x + 16,
        y + 23,
        text,
        16,
        text_fill,
        "700",
        max_chars=chars_for(w - 30, 16),
        line_height=18,
    )


def arrow(x1: int, y1: int, x2: int, y2: int, color: str = LINE, width: int = 3) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{width}" marker-end="url(#arrowhead)"/>'
    )


def title_block(slide: Slide) -> str:
    case_w = max(260, min(360, 60 + len(slide.case_id) * 14))
    case_x = 1510 - case_w
    return (
        t(90, 90, slide.unit, 24, ACCENT, "700")
        + t(90, 150, slide.title, 48, INK, "700", family="Georgia, serif", max_chars=38, line_height=56)
        + t(90, 220, slide.subtitle, 24, MUTED, "400", max_chars=84, line_height=34)
        + pill(case_x, 70, case_w, 54, slide.case_id, SAGE)
    )


def footer(slide: Slide) -> str:
    return (
        f'<line x1="90" y1="820" x2="1510" y2="820" stroke="{LINE}" stroke-width="2"/>'
        + t(90, 855, FOOTER_TEXT, 20, MUTED)
        + t(1130, 855, slide.filename.replace(".svg", ""), 20, MUTED, "700")
    )


def small_metric(x: int, y: int, w: int, title: str, body: str, accent: str = ACCENT) -> str:
    return (
        rect(x, y, w, 86)
        + t(x + 24, y + 34, title, 22, accent, "700")
        + t(
            x + 24,
            y + 64,
            body,
            19,
            INK,
            max_chars=chars_for(w - 48, 19),
            line_height=22,
        )
    )


def render_card(slide: Slide) -> str:
    body = slide.payload["body"]
    kicker = slide.payload.get("kicker", slide.unit)
    accent = slide.payload.get("accent", ACCENT)
    note = slide.payload.get("note", "")
    case_w = max(260, min(360, 60 + len(slide.case_id) * 14))
    case_x = 1480 - case_w
    out = [
        rect(90, 90, 1420, 720, fill="#FBF7EF", stroke=LINE, rx=40),
        pill(120, 120, 250, 52, kicker, accent),
        pill(case_x, 120, case_w, 52, slide.case_id, SAGE),
        t(120, 250, slide.title, 58, INK, "700", family="Georgia, serif", max_chars=32, line_height=66),
        t(120, 360, slide.subtitle, 28, MUTED, "400", max_chars=68, line_height=36),
        rect(120, 460, 1360, 170, fill="white", stroke=LINE),
        t(160, 530, body, 34, INK, "700", max_chars=48, line_height=42),
    ]
    if note:
        out.append(rect(120, 665, 1360, 78, fill=INK, stroke=INK, rx=24))
        out.append(t(154, 712, note, 24, "white", "400", max_chars=84, line_height=30))
    out.append(footer(slide))
    return "".join(out)


def render_grid(slide: Slide) -> str:
    cards = slide.payload["cards"]
    fills = [SOFT_ORANGE, SOFT_GREEN, SOFT_INDIGO, SOFT_SAND, "#EEF2F7", "#F7EEE6"]
    accents = [ACCENT, SAGE, INDIGO, INK, TEAL, ACCENT]
    positions = [
        (90, 280),
        (575, 280),
        (1060, 280),
        (90, 515),
        (575, 515),
        (1060, 515),
    ]
    out = [title_block(slide)]
    for idx, (x, y) in enumerate(positions[: len(cards)]):
        card = cards[idx]
        fill = card.get("fill", fills[idx % len(fills)])
        accent = card.get("accent", accents[idx % len(accents)])
        out.append(rect(x, y, 450, 180, fill=fill))
        out.append(t(x + 26, y + 46, card["title"], 28, accent, "700", max_chars=chars_for(398, 28), line_height=32))
        out.append(
            t(
                x + 26,
                y + 90,
                card["body"],
                21,
                INK,
                max_chars=chars_for(398, 21),
                line_height=26,
            )
        )
    note = slide.payload.get("note")
    if note:
        out.append(rect(90, 730, 1420, 70, fill=INK, stroke=INK))
        out.append(t(120, 774, note, 25, "white", "700", max_chars=88, line_height=30))
    out.append(footer(slide))
    return "".join(out)


def render_compare(slide: Slide) -> str:
    cols = slide.payload["columns"]
    count = len(cols)
    out = [title_block(slide)]
    if count == 2:
        x_positions = [90, 820]
        width = 690
        height = 430
        top = 280
        title_size = 30
        body_size = 22
        fills = [SOFT_ORANGE, SOFT_GREEN]
        accents = [ACCENT, SAGE]
    else:
        x_positions = [90, 570, 1050]
        width = 390
        height = 420
        top = 280
        title_size = 27
        body_size = 20
        fills = [SOFT_ORANGE, SOFT_GREEN, SOFT_SAND]
        accents = [ACCENT, SAGE, INK]
    for idx, col in enumerate(cols):
        x = x_positions[idx]
        fill = col.get("fill", fills[idx % len(fills)])
        accent = col.get("accent", accents[idx % len(accents)])
        out.append(rect(x, top, width, height, fill=fill))
        out.append(
            t(
                x + 26,
                top + 44,
                col["title"],
                title_size,
                accent,
                "700",
                max_chars=chars_for(width - 52, title_size),
                line_height=32,
            )
        )
        out.append(
            t(
                x + 26,
                top + 92,
                col["body"],
                body_size,
                INK,
                max_chars=chars_for(width - 52, body_size),
                line_height=28 if count == 2 else 24,
            )
        )
    metrics = slide.payload.get("metrics", [])
    summary = slide.payload.get("summary")
    if metrics:
        metric_width = 430 if len(metrics) == 3 else 330
        gap = 60 if len(metrics) == 3 else 25
        start_x = 90 if len(metrics) == 3 else 90
        for idx, metric in enumerate(metrics):
            out.append(
                small_metric(
                    start_x + idx * (metric_width + gap),
                    730,
                    metric_width,
                    metric["title"],
                    metric["body"],
                    metric.get("accent", ACCENT),
                )
            )
    elif summary:
        out.append(rect(90, 730, 1420, 70, fill=INK, stroke=INK))
        out.append(t(120, 774, summary, 25, "white", "700", max_chars=90, line_height=30))
    out.append(footer(slide))
    return "".join(out)


def render_flow(slide: Slide) -> str:
    steps = slide.payload["steps"]
    gates = slide.payload.get("gates", [])
    note = slide.payload.get("note")
    count = len(steps)
    gap = 28 if count >= 5 else 36
    width = (1420 - gap * (count - 1)) // count
    height = 210 if count >= 5 else 230
    top = 320 if count >= 5 else 300
    title_size = 24 if count >= 5 else 26
    body_size = 19 if count >= 5 else 20
    fills = [SOFT_ORANGE, SOFT_GREEN, SOFT_INDIGO, SOFT_SAND, "#EEF2F7"]
    accents = [ACCENT, SAGE, INDIGO, INK, TEAL]
    x_positions = [90 + idx * (width + gap) for idx in range(count)]
    center_y = top + height // 2
    out = [title_block(slide)]
    for idx, step in enumerate(steps):
        x = x_positions[idx]
        fill = step.get("fill", fills[idx % len(fills)])
        accent = step.get("accent", accents[idx % len(accents)])
        out.append(rect(x, top, width, height, fill=fill))
        out.append(
            t(
                x + 22,
                top + 42,
                step["title"],
                title_size,
                accent,
                "700",
                max_chars=chars_for(width - 44, title_size),
                line_height=28,
            )
        )
        out.append(
            t(
                x + 22,
                top + 86,
                step["body"],
                body_size,
                INK,
                max_chars=chars_for(width - 44, body_size),
                line_height=24,
            )
        )
        if idx < count - 1:
            next_x = x_positions[idx + 1]
            out.append(arrow(x + width + 6, center_y, next_x - 10, center_y))
            if idx < len(gates):
                gate_x = x + width + (gap // 2) - 72
                out.append(tag(gate_x, top + height + 26, gates[idx], "#E9E1D3"))
    if note:
        out.append(rect(90, 730, 1420, 70, fill=INK, stroke=INK))
        out.append(t(120, 774, note, 25, "white", "700", max_chars=89, line_height=30))
    out.append(footer(slide))
    return "".join(out)


def render_table(slide: Slide) -> str:
    headers = slide.payload["headers"]
    widths = slide.payload["widths"]
    rows = slide.payload["rows"]
    header_h = 70
    base_row_h = slide.payload.get("row_height", 76)
    x0 = 90
    y0 = 260
    row_heights = []
    for row in rows:
        max_lines = 1
        for cell, width in zip(row, widths):
            max_lines = max(max_lines, len(wrap_lines(cell, chars_for(width - 28, 18))))
        row_heights.append(max(base_row_h, 20 + max_lines * 22 + 18))
    total_h = header_h + sum(row_heights)
    out = [title_block(slide), rect(x0, y0, 1420, total_h)]
    x = x0
    header_fills = ["#EFE7D8", "#E8F0EC", "#EFE7D8", "#E8F0EC"]
    for idx, (header, width) in enumerate(zip(headers, widths)):
        out.append(rect(x, y0, width, header_h, fill=header_fills[idx % len(header_fills)], stroke=LINE, rx=0))
        out.append(
            t(
                x + 16,
                y0 + 44,
                header,
                22,
                INK,
                "700",
                max_chars=chars_for(width - 32, 22),
                line_height=26,
            )
        )
        x += width
    y = y0 + header_h
    for ridx, (row, row_h) in enumerate(zip(rows, row_heights)):
        x = x0
        bg = PANEL if ridx % 2 == 0 else "#FCFAF4"
        for cell, width in zip(row, widths):
            out.append(rect(x, y, width, row_h, fill=bg, stroke=LINE, rx=0, sw=1))
            out.append(
                t(
                    x + 14,
                    y + 34,
                    cell,
                    18,
                    INK,
                    max_chars=chars_for(width - 28, 18),
                    line_height=22,
                )
            )
            x += width
        y += row_h
    note = slide.payload.get("note")
    if note:
        out.append(rect(90, 730, 1420, 70, fill=INK, stroke=INK))
        out.append(t(120, 774, note, 24, "white", "700", max_chars=88, line_height=30))
    out.append(footer(slide))
    return "".join(out)


def render_bridge(slide: Slide) -> str:
    left = slide.payload["left"]
    middle = slide.payload["middle"]
    right = slide.payload["right"]
    note = slide.payload.get("note")
    out = [
        title_block(slide),
        rect(90, 320, 420, 340, fill=SOFT_ORANGE),
        rect(590, 270, 420, 430, fill="white"),
        rect(1090, 320, 420, 340, fill=SOFT_GREEN),
        arrow(510, 490, 570, 490),
        arrow(1010, 490, 1070, 490),
        t(118, 370, left["title"], 30, ACCENT, "700", max_chars=chars_for(364, 30), line_height=34),
        t(118, 420, left["body"], 22, INK, max_chars=chars_for(364, 22), line_height=28),
        t(620, 320, middle["title"], 30, INDIGO, "700", max_chars=chars_for(360, 30), line_height=34),
        t(1118, 370, right["title"], 30, SAGE, "700", max_chars=chars_for(364, 30), line_height=34),
        t(1118, 420, right["body"], 22, INK, max_chars=chars_for(364, 22), line_height=28),
    ]
    cy = 382
    for item in middle["bullets"]:
        out.append(f'<circle cx="628" cy="{cy - 8}" r="6" fill="{INDIGO}"/>')
        out.append(t(646, cy, item, 22, INK, max_chars=chars_for(320, 22), line_height=28))
        cy += 72
    if note:
        out.append(rect(90, 730, 1420, 70, fill=INK, stroke=INK))
        out.append(t(120, 774, note, 24, "white", "700", max_chars=88, line_height=30))
    out.append(footer(slide))
    return "".join(out)


def svg_wrap(body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f'<defs><marker id="arrowhead" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto">'
        f'<polygon points="0,0 10,4 0,8" fill="{LINE}"/></marker></defs>'
        f'<rect width="{W}" height="{H}" fill="{BG}"/>'
        f'<circle cx="1480" cy="118" r="190" fill="#EEE5D4" opacity="0.45"/>'
        f'<circle cx="120" cy="804" r="170" fill="#EFE8DA" opacity="0.35"/>'
        f"{body}</svg>"
    )


TYPE_LABELS = {
    "card": "title/final card",
    "grid": "framework grid",
    "compare": "comparison screen",
    "flow": "workflow diagram",
    "table": "table screen",
    "bridge": "bridge / rollout screen",
}


slides = [
    Slide(
        "l06_title_card.svg",
        "Урок 6",
        "Формула хорошего запроса",
        "Сильный запрос обычно начинается с цели, контекста, формата и критериев.",
        "card",
        "L06-CASE-A",
        "Opening card для урока о формуле 4+2 и первом собранном рабочем запросе.",
        {
            "kicker": "Урок 6",
            "body": "Сильный запрос = цель + контекст + формат + критерии.",
            "note": "Дальше в уроке добавляем еще два слоя по ситуации: входные данные и ограничения.",
        },
        [
            "Экранная формула: сильный запрос = цель + контекст + формат + критерии.",
            "Мост в урок: базовый каркас дополняется входными данными и ограничениями.",
        ],
    ),
    Slide(
        "l06_formula_4_plus_2.svg",
        "Урок 6",
        "Формула 4+2 на одном экране",
        "Четыре обязательные части убирают хаос; входные данные и ограничения подключаются по ситуации.",
        "grid",
        "L06-CASE-A",
        "Главный framework-slide перед демонстрацией follow-up письма.",
        {
            "cards": [
                {
                    "title": "1. Цель",
                    "body": "Что должно случиться в конце: зафиксировать договоренности и следующий шаг.",
                },
                {
                    "title": "2. Контекст",
                    "body": "Кто участвует, что уже решено, какие сроки и условия важны именно здесь.",
                },
                {
                    "title": "3. Формат",
                    "body": "Письмо на 4-6 строк, short note, bullets или таблица - заранее задаем форму.",
                },
                {
                    "title": "4. Критерии качества",
                    "body": "Деловой тон, без канцелярита, один четкий next step, никакой воды.",
                },
                {
                    "title": "5. Входные данные",
                    "body": "Заметки встречи, факты, цифры и сроки, которые нельзя потерять.",
                },
                {
                    "title": "6. Ограничения",
                    "body": "Не обещать лишнего, не делать письмо слишком продающим и не придумывать факты.",
                },
            ],
            "note": "4 части обязательны почти всегда. Еще 2 подключаются по ситуации и страхуют от лишних обещаний.",
        },
        [
            "1. Цель: что должно получиться в конце.",
            "2. Контекст: кто участвует, что уже произошло, какие сроки важны.",
            "3. Формат: заранее задаем форму результата.",
            "4. Критерии качества: тон, ясность, next step.",
            "5. Входные данные: факты и заметки, которые нельзя потерять.",
            "6. Ограничения: не обещать лишнего и не придумывать факты.",
        ],
    ),
    Slide(
        "l06_weak_vs_strong_followup.svg",
        "Урок 6",
        "Слабый запрос против рабочего запроса",
        "Один и тот же кейс показывает, как формула 4+2 переводит письмо из случайного в управляемый черновик.",
        "compare",
        "L06-CASE-A",
        "Comparison screen для объяснения, почему модель перестает угадывать детали.",
        {
            "columns": [
                {
                    "title": "Слабый запрос",
                    "body": "Напиши письмо после встречи по пилоту. Неясно, кому пишем, что уже обещано и какой следующий шаг нужно зафиксировать.",
                },
                {
                    "title": "Рабочий запрос",
                    "body": "Цель: зафиксировать договоренности. Контекст: Мария, Илья, доступ до 18:00, 5 участников до четверга, старт в понедельник. Формат: 4-6 строк. Ограничения: без новых обещаний.",
                },
            ],
            "summary": "Сила не в секретном тексте, а в том, что модель перестает угадывать важные детали кейса.",
        },
        [
            "Слабый запрос: модель сама додумывает адресата, обещания и next step.",
            "Рабочий запрос: в него заранее внесены цель, контекст, формат и ограничения кейса.",
            "Нижняя линия: формула 4+2 убирает случайность и хаос.",
        ],
    ),
    Slide(
        "l06_followup_build_flow.svg",
        "Урок 6",
        "Как собираем follow-up по кейсу L06-CASE-A",
        "Экран показывает путь от сырых заметок до финального письма, которое не обещает лишнего.",
        "flow",
        "L06-CASE-A",
        "Workflow slide для screen demo по follow-up письму после kickoff-встречи.",
        {
            "steps": [
                {
                    "title": "Заметки встречи",
                    "body": "Мария, Илья, доступ до 18:00, список 5 участников до четверга, старт в понедельник.",
                },
                {
                    "title": "Промпт 4+2",
                    "body": "Цель, контекст, формат, критерии плюс входные данные и ограничения кейса.",
                },
                {
                    "title": "AI-черновик",
                    "body": "Сегодня до 18:00 отправлю доступ. До четверга пришлите 5 участников.",
                },
                {
                    "title": "Ручная проверка",
                    "body": "Подтверждаем сроки, tone и отсутствие новых обещаний перед отправкой письма.",
                },
            ],
            "gates": ["факты на месте", "есть next step", "ничего не придумано"],
            "note": "Ограничения нужны не для красоты: они не дают модели пообещать лишнее в follow-up письме.",
        },
        [
            "Шаг 1: берем реальные заметки встречи, а не абстрактный контекст.",
            "Шаг 2: собираем промпт через 4+2.",
            "Шаг 3: получаем черновик.",
            "Шаг 4: человек подтверждает сроки, тон и границы обещаний.",
        ],
    ),
    Slide(
        "l06_final_card.svg",
        "Урок 6",
        "Действие после урока",
        "Фиксация практики сразу после объяснения формулы.",
        "card",
        "L06-CASE-A",
        "Closing card с immediate action-copy по уроку 6.",
        {
            "kicker": "После урока 6",
            "body": "Соберите 1 рабочий запрос по формуле 4+2.",
            "note": "Лучше брать свою повторяющуюся задачу: follow-up, summary или короткий internal note.",
            "accent": SAGE,
        },
        [
            "Action-copy: соберите один рабочий запрос по формуле 4+2.",
            "Подсказка: берите реальную повторяющуюся задачу, а не абстрактный пример.",
        ],
    ),
    Slide(
        "l07_title_card.svg",
        "Урок 7",
        "Роль, аудитория и уместность",
        "Не роль ради роли, а результат, уместный для конкретного адресата.",
        "card",
        "L07-CASE-A",
        "Opening card для урока про адресата, тон и уместность результата.",
        {
            "kicker": "Урок 7",
            "body": "Сначала адресат и задача коммуникации, потом роль.",
            "note": "В кейсе ниже одна и та же новость адаптируется для коллеги, клиента и руководителя.",
        },
        [
            "Главная мысль: адресат и коммуникационная задача важнее красивого role prompting.",
            "Мост в демо: один базовый смысл будет разложен на три версии сообщения.",
        ],
    ),
    Slide(
        "l07_role_vs_audience.svg",
        "Урок 7",
        "Роль ради роли против уместного результата",
        "Красивый role prompting полезен редко; адресат и коммуникационная задача почти всегда важнее.",
        "compare",
        "L07-CASE-A",
        "Контрастный экран, который снимает культ магической роли.",
        {
            "columns": [
                {
                    "title": "Магическая роль",
                    "body": "Представь, что ты гениальный эксперт с двадцатью годами опыта. Звучит эффектно, но не отвечает на вопрос, кому и зачем мы пишем.",
                },
                {
                    "title": "Рабочий подход",
                    "body": "Сначала задаем адресата, tone и желаемое действие. Роль добавляем только тогда, когда она реально уточняет формат результата.",
                },
            ],
            "summary": "Не роль ради роли, а результат, который уместен для конкретного человека и ситуации.",
        },
        [
            "Левая колонка: role prompting без адресата почти не дает управляемой пользы.",
            "Правая колонка: сначала задаем аудиторию, тон и next step; роль вторична.",
            "Нижняя линия: полезна не роль сама по себе, а уместный результат.",
        ],
    ),
    Slide(
        "l07_audience_tone_structure.svg",
        "Урок 7",
        "Аудитория -> Тон -> Структура",
        "Один базовый смысл меняется не по волшебству, а через адресата, глубину и следующий шаг.",
        "table",
        "L07-CASE-A",
        "Framework-slide с тремя адресатами для одной и той же новости о переносе пилота.",
        {
            "headers": ["Адресат", "Тон", "Что подчеркиваем", "Следующий шаг"],
            "widths": [210, 240, 540, 430],
            "rows": [
                [
                    "Коллега",
                    "Прямо и операционно",
                    "Старт сдвигается на 2 дня; в понедельник просто потеряем время на ручных обходах.",
                    "До завтра фиксируем список участников и новый тайминг.",
                ],
                [
                    "Клиент",
                    "Спокойно и без обвинений",
                    "Перенос нужен, чтобы стартовать без технических накладок и сохранить надежность запуска.",
                    "Завтра до 15:00 отправляем подтвержденный тайминг запуска.",
                ],
                [
                    "Руководитель",
                    "Коротко, с риском и решением",
                    "Причина в доступах; риск управляемый, но важно не потерять доверие клиента.",
                    "До 15:00 даем обновленный статус и следующий управленческий шаг.",
                ],
            ],
        },
        [
            "Таблица: адресат, тон, что подчеркиваем, следующий шаг.",
            "Коллега: прямо и операционно.",
            "Клиент: спокойно, без обвинений, с акцентом на надежность.",
            "Руководитель: кратко, с риском, решением и управленческим next step.",
        ],
    ),
    Slide(
        "l07_three_versions_compare.svg",
        "Урок 7",
        "Одна новость, три версии сообщения",
        "Кейс L07-CASE-A показывает, как один базовый смысл адаптируется под коллегу, клиента и руководителя.",
        "compare",
        "L07-CASE-A",
        "Трехколоночный comparison screen для записи урока о корректной адаптации сообщения.",
        {
            "columns": [
                {
                    "title": "Для коллеги",
                    "body": "Коллеги, старт пилота переносим на среду. IT заканчивает доступы, поэтому в понедельник просто потеряем время на ручных обходах. До завтра фиксируем список участников и новый тайминг.",
                },
                {
                    "title": "Для клиента",
                    "body": "Мария, коротко обновлю статус по пилоту. Старт переносим на среду, потому что команда завершает настройку доступов. Это позволит начать без технических накладок. Завтра до 15:00 пришлю тайминг запуска.",
                },
                {
                    "title": "Для руководителя",
                    "body": "Старт пилота сдвигаем с понедельника на среду. Причина - доступы еще не готовы. Риск управляемый, но важно не потерять доверие клиента. До 15:00 отправлю обновленный статус и следующий шаг.",
                },
            ],
            "metrics": [
                {
                    "title": "Коллега",
                    "body": "операционно и без лишнего контекста",
                    "accent": ACCENT,
                },
                {
                    "title": "Клиент",
                    "body": "спокойно и с акцентом на надежность",
                    "accent": SAGE,
                },
                {
                    "title": "Руководитель",
                    "body": "риск, решение и короткий next step",
                    "accent": INK,
                },
            ],
        },
        [
            "Версия для коллеги: прямо и по делу.",
            "Версия для клиента: спокойно и без обвинительного tone.",
            "Версия для руководителя: кратко, с риском и решением.",
        ],
    ),
    Slide(
        "l07_final_card.svg",
        "Урок 7",
        "Действие после урока",
        "Closing screen для перевода наблюдения в реальную практику.",
        "card",
        "L07-CASE-A",
        "Closing card с действием по адаптации запроса под адресата.",
        {
            "kicker": "После урока 7",
            "body": "Перепишите 1 запрос под конкретную аудиторию.",
            "note": "Если не понятен адресат, роль почти ничего не спасает.",
            "accent": SAGE,
        },
        [
            "Action-copy: перепишите один свой запрос под конкретную аудиторию.",
            "Критерий: должен измениться tone, глубина и следующий шаг результата.",
        ],
    ),
    Slide(
        "l08_title_card.svg",
        "Урок 8",
        "Как разбивать сложную задачу на шаги",
        "Декомпозиция нужна не только для удобства, а для контроля качества.",
        "card",
        "L08-CASE-A",
        "Opening card для урока про управляемость больших задач через шаги и checkpoints.",
        {
            "kicker": "Урок 8",
            "body": "Сложную задачу не решают одним выстрелом. Ее ведут через этапы и checkpoints.",
            "note": "Дальше разбираем кейс внутренней презентации по итогам двухнедельного AI-пилота.",
        },
        [
            "Экранная формула: сложная задача идет через этапы и checkpoints.",
            "Кейс урока: презентация на 6 слайдов по итогам AI-пилота.",
        ],
    ),
    Slide(
        "l08_one_shot_vs_decomposition.svg",
        "Урок 8",
        "Один большой запрос против декомпозиции",
        "Кейс презентации показывает, почему один выстрел дает шум, а разбивка на шаги возвращает контроль.",
        "compare",
        "L08-CASE-A",
        "Comparison screen для контраста между one-shot запросом и пошаговой сборкой презентации.",
        {
            "columns": [
                {
                    "title": "Одним запросом",
                    "body": "Сделай презентацию по итогам AI-пилота для руководства. Модель смешивает цель, структуру, тезисы и управленческое решение в один шумный ответ.",
                },
                {
                    "title": "Через этапы",
                    "body": "Сначала цель и адресат. Потом структура на 6 слайдов. Затем тезисы, адаптация под руководителя и checkpoint по перегрузу и следующему шагу.",
                },
            ],
            "summary": "Декомпозиция нужна не только для удобства, а для того, чтобы держать качество результата под контролем.",
        },
        [
            "One-shot вариант смешивает цель, структуру и решение.",
            "Пошаговый вариант разделяет этапы: цель, структура, тезисы, адаптация, checkpoint.",
            "Нижняя линия: декомпозиция = контроль качества, а не лишняя бюрократия.",
        ],
    ),
    Slide(
        "l08_decomposition_workflow.svg",
        "Урок 8",
        "Пятишаговая декомпозиция кейса L08-CASE-A",
        "Шаги и checkpoints показывают, как довести сложную задачу до рабочего результата без потери управляемости.",
        "flow",
        "L08-CASE-A",
        "Основной workflow diagram урока о поэтапной сборке внутренней презентации.",
        {
            "steps": [
                {
                    "title": "1. Цель и адресат",
                    "body": "Какой один вывод должен услышать руководитель операционного блока?",
                },
                {
                    "title": "2. Структура",
                    "body": "Собираем 6 слайдов: цель, тест, что сработало, риски, next step.",
                },
                {
                    "title": "3. Наполнение",
                    "body": "Пишем черновые тезисы по каждому слайду без воды и общих слов.",
                },
                {
                    "title": "4. Адаптация",
                    "body": "Делаем текст короче, точнее и более decision-oriented для руководителя.",
                },
                {
                    "title": "5. Checkpoint",
                    "body": "Проверяем главный вывод, перегруз и ясность следующего шага.",
                },
            ],
            "gates": ["решение ясно?", "один смысл", "нет воды", "идем дальше?"],
            "note": "Шаг -> checkpoint -> следующий шаг. Так сложная задача остается управляемой и не разваливается в шум.",
        },
        [
            "Пять шагов: цель, структура, наполнение, адаптация, checkpoint.",
            "Между шагами стоят контрольные вопросы, а не слепое движение вперед.",
            "Главный эффект: сложная задача перестает быть шумной и становится управляемой.",
        ],
    ),
    Slide(
        "l08_checkpoint_table.svg",
        "Урок 8",
        "Checkpoint-вопросы по каждому этапу",
        "Эти проверки удерживают качество до того, как вы начнете собирать финальную презентацию.",
        "table",
        "L08-CASE-A",
        "Table slide с вопросами контроля качества для каждого этапа декомпозиции.",
        {
            "headers": ["Этап", "Что спрашиваем", "Зачем это нужно"],
            "widths": [250, 650, 520],
            "rows": [
                [
                    "Цель и адресат",
                    "Какое решение должен принять руководитель после презентации?",
                    "Отсекаем красивые, но бесполезные тезисы и держим управленческий фокус.",
                ],
                [
                    "Структура",
                    "Есть ли один смысл на слайд и отдельно ли показаны результаты, риски и next step?",
                    "Не даем материалу слипнуться в общий рассказ без архитектуры.",
                ],
                [
                    "Наполнение",
                    "Есть ли наблюдаемые факты вместо общих слов и самоуспокоения?",
                    "Слайды становятся decision-oriented, а не декларативными.",
                ],
                [
                    "Адаптация",
                    "Убраны ли детали, которые не нужны руководителю именно на этом уровне?",
                    "Сохраняем краткость и не перегружаем человека лишними подробностями.",
                ],
                [
                    "Checkpoint",
                    "Понятен ли вывод, нет ли перегруза и ясен ли следующий шаг?",
                    "Ловим слабые места до финальной сборки и переделки всего deck.",
                ],
            ],
        },
        [
            "Таблица удерживает один вопрос контроля на каждом этапе.",
            "Критичные проверки: решение, один смысл на слайд, наблюдаемые факты, отсутствие перегруза.",
            "Использовать как экран перед финальной сборкой презентации.",
        ],
    ),
    Slide(
        "l08_final_card.svg",
        "Урок 8",
        "Действие после урока",
        "Закрывающий экран для перевода принципа декомпозиции в реальную работу.",
        "card",
        "L08-CASE-A",
        "Closing card с заданием разбить реальную большую задачу на 4-5 шагов.",
        {
            "kicker": "После урока 8",
            "body": "Разбейте 1 большую задачу на 4-5 шагов.",
            "note": "И поставьте хотя бы один checkpoint между шагами, чтобы не тащить слабый результат дальше.",
            "accent": SAGE,
        },
        [
            "Action-copy: разбейте одну большую задачу на 4-5 шагов.",
            "Добавьте checkpoint между шагами, а не только список этапов.",
        ],
    ),
    Slide(
        "l09_title_card.svg",
        "Урок 9",
        "Почему не существует волшебного промпта",
        "Итерации не замедляют работу. Они экономят время на переделках.",
        "card",
        "L09-CASE-A",
        "Opening card для урока об итерациях вместо поиска секретного промпта.",
        {
            "kicker": "Урок 9",
            "body": "Сильный результат строится через цикл коротких улучшений, а не через магический текст.",
            "note": "Кейс урока - weekly summary для руководителя по итогам недели AI-пилота.",
        },
        [
            "Главная мысль: сильный результат строится через цикл коротких улучшений.",
            "Кейс урока: three-pass weekly summary для руководителя.",
        ],
    ),
    Slide(
        "l09_myth_vs_iterations.svg",
        "Урок 9",
        "Миф о волшебном промпте против нормальной работы",
        "Контрастный экран снимает культ секретного текста и возвращает взрослую рабочую механику.",
        "compare",
        "L09-CASE-A",
        "Comparison screen для проговаривания мифа о magical prompt и ценности итераций.",
        {
            "columns": [
                {
                    "title": "Миф о волшебном промпте",
                    "body": "Кажется, что где-то есть секретный текст, который сразу даст идеальный ответ. В реальной работе это почти всегда иллюзия и потеря времени.",
                },
                {
                    "title": "Нормальная работа",
                    "body": "Поставили задачу, посмотрели ответ, уточнили критерии, убрали шум и проверили итог. Так дешевле, чем потом переписывать слабый финал.",
                },
            ],
            "summary": "Итерации не замедляют работу. Они экономят время на переделках и делают результат предсказуемее.",
        },
        [
            "Левая колонка: иллюзия секретного промпта.",
            "Правая колонка: обычный рабочий цикл через уточнение и проверку.",
            "Нижняя линия: итерации экономят время на переделках.",
        ],
    ),
    Slide(
        "l09_iteration_cycle.svg",
        "Урок 9",
        "Итерационный цикл на одном экране",
        "Пятишаговый workflow показывает, как из слабого первого ответа сделать рабочий черновик без магии.",
        "flow",
        "L09-CASE-A",
        "Workflow diagram для основного цикла урока 9: запрос -> ответ -> оценка -> уточнение -> проверка.",
        {
            "steps": [
                {
                    "title": "Запрос",
                    "body": "Ставим задачу и заранее фиксируем адресата и цель summary.",
                },
                {
                    "title": "Ответ",
                    "body": "Получаем первый черновик, а не финальный verdict по кейсу.",
                },
                {
                    "title": "Оценка",
                    "body": "Ищем общие слова, шум, потерю фактов и слабый next step.",
                },
                {
                    "title": "Уточнение",
                    "body": "Добавляем критерии, формат, точность и ограничения по tone.",
                },
                {
                    "title": "Проверка",
                    "body": "Оставляем только наблюдаемые факты и рабочий управленческий вывод.",
                },
            ],
            "gates": ["что убрать?", "что неясно?", "что уточнить?", "можно отправлять?"],
            "note": "Цикл короткий. Его задача - не усложнить работу, а снять дорогую переделку в самом конце.",
        },
        [
            "Пять стадий: запрос, ответ, оценка, уточнение, проверка.",
            "Важный тезис: первый ответ - это черновик, а не повод останавливать работу.",
            "Цель цикла - убрать шум и довести результат до рабочего состояния.",
        ],
    ),
    Slide(
        "l09_summary_iterations_compare.svg",
        "Урок 9",
        "Три итерации одного weekly summary",
        "Кейс L09-CASE-A показывает, как ответ взрослеет: от общих слов к наблюдаемым фактам и управленческому next step.",
        "compare",
        "L09-CASE-A",
        "Трехколоночный comparison screen с эволюцией одного summary через три итерации.",
        {
            "columns": [
                {
                    "title": "Итерация 1",
                    "body": "Неделя пилота прошла успешно. Участники активно использовали AI и получили полезный опыт. Есть потенциал продолжить работу.",
                },
                {
                    "title": "Итерация 2",
                    "body": "9 из 12 участников использовали AI минимум 3 раза. Лучше всего сработали follow-up письма. Риск - summary длинных документов без проверки.",
                },
                {
                    "title": "Итерация 3",
                    "body": "9 из 12 участников использовали AI минимум 3 раза. Самый устойчивый сценарий - follow-up после встреч. Следующий шаг: закрепить 3 шаблона и ввести чек-лист проверки.",
                },
            ],
            "metrics": [
                {"title": "Итерация 1", "body": "слишком общо и без управленческой пользы", "accent": ACCENT},
                {"title": "Итерация 2", "body": "уже полезно, но критерии еще не дожаты", "accent": SAGE},
                {"title": "Итерация 3", "body": "рабочий черновик на основе наблюдаемых фактов", "accent": INK},
            ],
        },
        [
            "Итерация 1: общие слова и самоуспокоение.",
            "Итерация 2: появляются факты, адресат и главный риск.",
            "Итерация 3: остаются наблюдаемые факты и управленческий следующий шаг.",
        ],
    ),
    Slide(
        "l09_final_card.svg",
        "Урок 9",
        "Действие после урока",
        "Closing screen для закрепления привычки работать итерациями.",
        "card",
        "L09-CASE-A",
        "Closing card с практикой повторить одну задачу в 2-3 проходах.",
        {
            "kicker": "После урока 9",
            "body": "Повторите 1 задачу в 2-3 итерациях.",
            "note": "Оценивайте не красоту промпта, а качество финального черновика после уточнений.",
            "accent": SAGE,
        },
        [
            "Action-copy: повторите одну задачу в 2-3 итерациях.",
            "Фокус: не на секретном промпте, а на качестве финального результата.",
        ],
    ),
    Slide(
        "l10_title_card.svg",
        "Урок 10",
        "Как собирать свои рабочие шаблоны",
        "Ценность не в одном хорошем запросе, а в библиотеке повторяемых сценариев.",
        "card",
        "L10-TEMPLATE-SET-A",
        "Opening card для урока про переход от разовой удачи к системной библиотеке шаблонов.",
        {
            "kicker": "Урок 10",
            "body": "Зрелая работа с AI начинается там, где появляется библиотека повторяемых сценариев.",
            "note": "Дальше в pack: структура template, три базовых шаблона и мост в командную библиотеку.",
        },
        [
            "Главная мысль: ценность не в одном хорошем запросе, а в repeatable library.",
            "Дальше в уроке: структура template, три базовых сценария и переход в командный формат.",
        ],
    ),
    Slide(
        "l10_template_structure.svg",
        "Урок 10",
        "Структура рабочего шаблона",
        "Хороший template фиксирует не магию, а повторяемый сценарий от входа до обязательной проверки.",
        "flow",
        "L10-TEMPLATE-SET-A",
        "Framework workflow для объяснения, из каких частей собирается usable template.",
        {
            "steps": [
                {
                    "title": "Когда использовать",
                    "body": "Повторяющаяся задача: письмо, summary, подготовка к встрече.",
                },
                {
                    "title": "Что дать на вход",
                    "body": "Адресат, исходник, сроки, контекст и ограничения кейса.",
                },
                {
                    "title": "Логика запроса",
                    "body": "Какие шаги и формулировки стабильно работают в этом сценарии.",
                },
                {
                    "title": "Что должно выйти",
                    "body": "Формат, длина, action item, нужная структура и tone.",
                },
                {
                    "title": "Что проверить",
                    "body": "Факты, обещания, искажения, лишние выводы и уместность результата.",
                },
            ],
            "gates": ["повторяемость", "единый вход", "предсказуемый output", "обязательная проверка"],
            "note": "Хороший template не обещает чудо. Он делает повторяемым сценарий, который уже показал пользу в работе.",
        },
        [
            "Пять частей шаблона: когда использовать, вход, логика запроса, output, проверка.",
            "Template фиксирует repeatable workflow, а не случайную удачу.",
            "Обязательная проверка - часть шаблона, а не постфактум пожелание.",
        ],
    ),
    Slide(
        "l10_template_library_table.svg",
        "Урок 10",
        "Три первых шаблона в личной библиотеке",
        "L10-TEMPLATE-SET-A переводит разовые находки в repeatable assets: follow-up, summary документа и подготовку к встрече.",
        "table",
        "L10-TEMPLATE-SET-A",
        "Табличный экран с тремя готовыми шаблонами для повседневной практики.",
        {
            "headers": ["Шаблон", "Когда использовать", "Что даем на вход", "Что проверяем"],
            "widths": [210, 350, 470, 390],
            "rows": [
                [
                    "Follow-up после встречи",
                    "После клиентского или внутреннего созвона, когда нужно быстро зафиксировать договоренности.",
                    "Адресат, что обсуждали, что решили, следующий шаг, срок и нужный tone.",
                    "Сроки, конкретный next step и отсутствие новых обещаний.",
                ],
                [
                    "Summary документа",
                    "После чтения длинного документа, инструкции или заметок, когда нужно короткое summary.",
                    "Сам текст или выдержка, цель summary, адресат и нужный формат: тезисы, риски, actions.",
                    "Цифры, ограничения и отсутствие широких выводов сверх текста.",
                ],
                [
                    "Подготовка к встрече",
                    "Перед созвоном или встречей, когда нужно быстро собрать повестку и вопросы.",
                    "Тема, участники, цель, риски и желаемый результат встречи.",
                    "Нет ли лишних вопросов и соответствует ли глубина уровню участников.",
                ],
            ],
        },
        [
            "Шаблон 1: follow-up после встречи.",
            "Шаблон 2: summary документа.",
            "Шаблон 3: подготовка к встрече.",
            "У всех трех шаблонов есть входные данные и обязательная проверка.",
        ],
    ),
    Slide(
        "l10_personal_to_team_bridge.svg",
        "Урок 10",
        "Как личный шаблон превращается в командный",
        "Мост нужен, чтобы показать переход от случайной удачи к общей библиотеке сценариев.",
        "bridge",
        "L10-TEMPLATE-SET-A",
        "Bridge slide для объяснения, как personal template становится team-ready asset.",
        {
            "left": {
                "title": "Личный шаблон",
                "body": "Один удачный follow-up, который вы сохранили для себя. Полезен, но зависит от памяти, стиля и привычек одного человека.",
            },
            "middle": {
                "title": "Что добавляем",
                "bullets": [
                    "Owner и понятное место хранения",
                    "Единый формат входных данных",
                    "Блок обязательной проверки",
                    "Пример хорошего output",
                ],
            },
            "right": {
                "title": "Командный шаблон",
                "body": "Повторяемый сценарий для нескольких сотрудников: общий вход, предсказуемый output и меньше хаоса в ежедневной работе.",
            },
            "note": "Личная библиотека - первый слой. Командная библиотека начинается там, где сценарий становится общим стандартом.",
        },
        [
            "Левая зона: личный template зависит от памяти одного человека.",
            "Средняя зона: owner, единый вход, обязательная проверка, пример хорошего output.",
            "Правая зона: командный template делает сценарий повторяемым для нескольких сотрудников.",
        ],
    ),
    Slide(
        "l10_final_card.svg",
        "Урок 10",
        "Действие после урока",
        "Финальный экран для запуска личной библиотеки рабочих сценариев.",
        "card",
        "L10-TEMPLATE-SET-A",
        "Closing card с действием сохранить первые три шаблона в одном месте.",
        {
            "kicker": "После урока 10",
            "body": "Сохраните 3 первых рабочих шаблона.",
            "note": "Личный template today -> командная библиотека tomorrow.",
            "accent": SAGE,
        },
        [
            "Action-copy: сохраните три первых рабочих шаблона в одном месте.",
            "Мост вперед: личный template должен быть готов к будущей стандартизации в команде.",
        ],
    ),
]


LESSON_DIAGRAMS = {
    "Урок 6": """```mermaid
flowchart LR
    A["Заметки встречи"] --> B["Промпт 4+2"]
    B --> C["AI-черновик"]
    C --> D["Ручная проверка"]
    D --> E["Короткий follow-up без лишних обещаний"]
```""",
    "Урок 7": """```mermaid
flowchart LR
    A["Один базовый смысл"] --> B["Кто адресат?"]
    B --> C["Какой нужен тон?"]
    C --> D["Какая структура уместна?"]
    D --> E["Версия для коллеги / клиента / руководителя"]
```""",
    "Урок 8": """```mermaid
flowchart LR
    A["Цель и адресат"] --> B["Структура"]
    B --> C["Наполнение"]
    C --> D["Адаптация"]
    D --> E["Checkpoint"]
    E --> F["Финальный deck"]
```""",
    "Урок 9": """```mermaid
flowchart LR
    A["Запрос"] --> B["Ответ"]
    B --> C["Оценка"]
    C --> D["Уточнение"]
    D --> E["Проверка"]
    E --> F["Рабочий черновик"]
```""",
    "Урок 10": """```mermaid
flowchart LR
    A["Повторяющаяся задача"] --> B["Личный template"]
    B --> C["Единый вход + проверка"]
    C --> D["Личная библиотека"]
    D --> E["Командный стандарт"]
```""",
}


def group_slides() -> dict[str, list[Slide]]:
    grouped: dict[str, list[Slide]] = {}
    for slide in slides:
        grouped.setdefault(slide.unit, []).append(slide)
    return grouped


def build_outline() -> str:
    grouped = group_slides()
    lines = [
        "# Wave 2 Slides Outline",
        "",
        f"Дата: {DATE}",
        "Статус: outline реального visual deck для уроков 6-10",
        "",
        "## Порядок использования",
        "",
        "1. Сначала открыть `README.md` и нужный блок урока.",
        "2. Потом перейти к конкретному SVG-asset по имени файла.",
        "3. Для точной подачи в кадре сверяться с `wave_2_slide_copy.md`.",
        "4. Для process-слайдов и workflow объяснений брать опору из `wave_2_diagrams.md`.",
        "",
    ]
    for unit, unit_slides in grouped.items():
        lines.append(f"## {unit}")
        lines.append("")
        for slide in unit_slides:
            lines.append(f"- `{slide.filename}`")
            lines.append(f"  Роль: {TYPE_LABELS[slide.kind]}.")
            lines.append(f"  Назначение: {slide.purpose}")
            lines.append(f"  Source case ID: `{slide.case_id}`")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_copy() -> str:
    lines = [
        "# Wave 2 Slide Copy",
        "",
        f"Дата: {DATE}",
        "Статус: copy deck для уроков 6-10",
        "",
    ]
    for slide in slides:
        lines.append(f"## {slide.filename}")
        lines.append("")
        lines.append(f"Единица: {slide.unit}")
        lines.append(f"Case ID: `{slide.case_id}`")
        lines.append(f"Тип: {TYPE_LABELS[slide.kind]}")
        lines.append(f"Заголовок: {slide.title}")
        lines.append(f"Подзаголовок: {slide.subtitle}")
        lines.append(f"Назначение: {slide.purpose}")
        lines.append("")
        for line in slide.copy_lines:
            lines.append(f"- {line}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_diagrams() -> str:
    lines = [
        "# Wave 2 Diagrams",
        "",
        f"Дата: {DATE}",
        "Статус: mermaid-схемы для уроков 6-10",
        "",
        "Эти схемы можно использовать как:",
        "- основу для SVG-перерисовки;",
        "- быстрый visual appendix к урокам 6-10;",
        "- источник для workflow и bridge screens.",
        "",
    ]
    for unit, body in LESSON_DIAGRAMS.items():
        lines.append(f"## {unit}")
        lines.append("")
        lines.append(body)
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_readme() -> str:
    lines = [
        "# Wave 2 Visual Pack",
        "",
        f"Дата: {DATE}",
        "Статус: рабочий пакет визуальных материалов для уроков 6-10",
        "",
        "## Что внутри",
        "",
        "- `build_wave_2_assets.py` - генератор пакета.",
        "- `wave_2_slides_outline.md` - карта deck по урокам 6-10.",
        "- `wave_2_slide_copy.md` - точная copy-опора по каждому экрану.",
        "- `wave_2_diagrams.md` - Mermaid-схемы для workflow и process-логики.",
        "- SVG-файлы - реальные assets для rough cut, review и записи.",
        "",
        "## Покрытие",
        "",
        f"- {len(slides)} SVG-assets: по 5 экранов на каждый урок с 6 по 10.",
        "- Внутри пакета есть title cards, final cards, comparison screens, framework slides, tables и workflow diagrams.",
        "- Все экраны привязаны к уже собранным case IDs: `L06-CASE-A`, `L07-CASE-A`, `L08-CASE-A`, `L09-CASE-A`, `L10-TEMPLATE-SET-A`.",
        "",
        "## Как пересобрать",
        "",
        "`python3 build_wave_2_assets.py`",
        "",
        "## Карта SVG-файлов",
        "",
    ]
    for slide in slides:
        lines.append(f"- `{slide.filename}` - {slide.unit}: {slide.title}")
    lines.extend(
        [
            "",
            "## Примечание",
            "",
            "Пакет собран как isolated visual workspace для review и записи уроков 6-10 и не меняет файлы за пределами этой папки.",
            "",
        ]
    )
    return "\n".join(lines)


def slide_svg(slide: Slide) -> str:
    renderers = {
        "card": render_card,
        "grid": render_grid,
        "compare": render_compare,
        "flow": render_flow,
        "table": render_table,
        "bridge": render_bridge,
    }
    return svg_wrap(renderers[slide.kind](slide))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "wave_2_slides_outline.md").write_text(build_outline(), encoding="utf-8")
    (OUT / "wave_2_slide_copy.md").write_text(build_copy(), encoding="utf-8")
    (OUT / "wave_2_diagrams.md").write_text(build_diagrams(), encoding="utf-8")
    (OUT / "README.md").write_text(build_readme(), encoding="utf-8")
    for slide in slides:
        (OUT / slide.filename).write_text(slide_svg(slide), encoding="utf-8")


if __name__ == "__main__":
    main()
