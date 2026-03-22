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
SOFT_RED = "#FFF1EA"
SOFT_GREEN = "#EEF5F1"
SOFT_GOLD = "#FBF1D9"
SOFT_LILAC = "#F3F0FA"
RED = "#9B3D22"
GREEN = "#355E4B"
GOLD = "#9A6A10"
VIOLET = "#6A56A5"


@dataclass
class Slide:
    filename: str
    unit: str
    title: str
    subtitle: str
    kind: str
    case_id: str
    payload: dict


def wrap_lines(text: str, max_chars: int | None) -> list[str]:
    lines: list[str] = []
    for raw in text.split("\n"):
        if max_chars is None:
            lines.append(raw)
            continue
        parts = wrap(raw, max_chars) or [""]
        lines.extend(parts)
    return lines or [""]


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
    parts = wrap_lines(text, max_chars)
    tspans = []
    for idx, part in enumerate(parts):
        dy = "0" if idx == 0 else str(line_height)
        safe = escape(part) if part else " "
        tspans.append(f'<tspan x="{x}" dy="{dy}">{safe}</tspan>')
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-family="{family}" '
        f'font-weight="{weight}" fill="{fill}">{"".join(tspans)}</text>'
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
        x + 22, y + h - 18, text, 24, text_fill, "700"
    )


def arrow(x1: int, y1: int, x2: int, y2: int, stroke: str = LINE) -> str:
    if y1 == y2:
        tip = (
            f'<polygon points="{x2},{y2} {x2 - 14},{y2 - 8} {x2 - 14},{y2 + 8}" '
            f'fill="{stroke}"/>'
        )
        x2_line = x2 - 14
        return f'<line x1="{x1}" y1="{y1}" x2="{x2_line}" y2="{y2}" stroke="{stroke}" stroke-width="4"/>' + tip
    tip = (
        f'<polygon points="{x2},{y2} {x2 - 8},{y2 - 14} {x2 + 8},{y2 - 14}" '
        f'fill="{stroke}"/>'
    )
    y2_line = y2 - 14
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2_line}" stroke="{stroke}" stroke-width="4"/>' + tip


def case_pill(text: str) -> str:
    width = min(360, max(210, 80 + len(text) * 7))
    x = 1510 - width
    return pill(x, 70, width, 54, text, SAGE)


def title_block(slide: Slide) -> str:
    return (
        t(90, 90, slide.unit, 24, ACCENT, "700")
        + t(90, 150, slide.title, 48, INK, "700", family="Georgia, serif", max_chars=38, line_height=56)
        + t(90, 220, slide.subtitle, 24, MUTED, "400", max_chars=84, line_height=34)
        + case_pill(slide.case_id)
    )


def footer(slide: Slide) -> str:
    return (
        f'<line x1="90" y1="820" x2="1510" y2="820" stroke="{LINE}" stroke-width="2"/>'
        + t(90, 855, "Wave 2B visual asset · Lessons 11-15 production pack", 20, MUTED)
        + t(1115, 855, slide.filename.replace(".svg", ""), 20, MUTED, "700")
    )


def bullet_lines(
    x: int,
    y: int,
    bullets: list[str],
    body_size: int = 22,
    bullet_fill: str = ACCENT,
    max_chars: int = 34,
    step: int = 68,
) -> str:
    out: list[str] = []
    cy = y
    for bullet in bullets:
        out.append(f'<circle cx="{x}" cy="{cy - 10}" r="6" fill="{bullet_fill}"/>')
        out.append(t(x + 22, cy, bullet, body_size, INK, max_chars=max_chars, line_height=28))
        cy += step
    return "".join(out)


def small_metric(x: int, y: int, w: int, title: str, body: str, accent: str = ACCENT) -> str:
    return (
        rect(x, y, w, 104)
        + t(x + 24, y + 34, title, 24, accent, "700")
        + t(x + 24, y + 68, body, 20, INK, max_chars=28, line_height=24)
    )


def render_compare(slide: Slide) -> str:
    cols = slide.payload["columns"]
    out = [title_block(slide)]
    x_positions = [90, 570, 1050]
    fills = [slide.payload.get("fills", [SOFT_GOLD, SOFT_GREEN, SOFT_RED])[i] for i in range(3)]
    accents = slide.payload.get("accents", [GOLD, GREEN, RED])
    for idx, col in enumerate(cols):
        out.append(rect(x_positions[idx], 280, 390, 420, fill=fills[idx]))
        out.append(t(x_positions[idx] + 26, 325, col["title"], 28, accents[idx], "700", max_chars=20, line_height=34))
        out.append(t(x_positions[idx] + 26, 370, col["body"], 21, INK, max_chars=28, line_height=27))
    for i, metric in enumerate(slide.payload["metrics"]):
        out.append(small_metric(90 + i * 355, 700, 330, metric["title"], metric["body"], metric["accent"]))
    out.append(footer(slide))
    return "".join(out)


def render_table(slide: Slide) -> str:
    headers = slide.payload["headers"]
    rows = slide.payload["rows"]
    out = [title_block(slide), rect(90, 260, 1420, 500)]
    col_widths = slide.payload["widths"]
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
            out.append(t(x + 14, y + 36, cell, 18, INK, max_chars=max(10, width // 12), line_height=22))
            x += width
        y += 58
    note = slide.payload.get("note")
    if note:
        out.append(rect(90, 748, 1420, 52, fill=INK, stroke=INK, rx=18))
        out.append(t(118, 780, note, 19, "white", "700", max_chars=100, line_height=22))
    out.append(footer(slide))
    return "".join(out)


def render_split(slide: Slide) -> str:
    left = slide.payload["left"]
    right = slide.payload["right"]
    bottom = slide.payload.get("bottom")
    out = [
        title_block(slide),
        rect(90, 280, 650, 420, fill=slide.payload.get("left_fill", SOFT_RED)),
        rect(860, 280, 650, 420, fill=slide.payload.get("right_fill", SOFT_GREEN)),
        t(120, 330, left["title"], 30, slide.payload.get("left_accent", RED), "700", max_chars=28, line_height=36),
        t(890, 330, right["title"], 30, slide.payload.get("right_accent", GREEN), "700", max_chars=28, line_height=36),
        t(120, 380, left["body"], 22, INK, max_chars=40, line_height=28),
        t(890, 380, right["body"], 22, INK, max_chars=40, line_height=28),
    ]
    if bottom:
        out.append(rect(90, 730, 1420, 70, fill=INK, stroke=INK))
        out.append(t(120, 776, bottom, 26, "white", "700", max_chars=88, line_height=30))
    out.append(footer(slide))
    return "".join(out)


def render_checklist(slide: Slide) -> str:
    items = slide.payload["items"]
    out = [title_block(slide)]
    positions = [(90, 280), (820, 280), (90, 435), (820, 435), (90, 590), (820, 590)]
    fills = [SOFT_GOLD, SOFT_GREEN, SOFT_LILAC, "#F7F3EA", SOFT_RED, "#EEF0F6"]
    accents = [GOLD, GREEN, VIOLET, INK, RED, SAGE]
    for (x, y), item, fill, accent in zip(positions, items, fills, accents):
        out.append(rect(x, y, 690, 140, fill=fill))
        out.append(pill(x + 24, y + 20, 150, 40, item["title"], accent))
        out.append(t(x + 28, y + 86, item["body"], 20, INK, max_chars=48, line_height=24))
    note = slide.payload.get("note")
    if note:
        out.append(rect(90, 750, 1420, 50, fill=INK, stroke=INK))
        out.append(t(120, 780, note, 22, "white", "700", max_chars=98, line_height=26))
    out.append(footer(slide))
    return "".join(out)


def render_workflow(slide: Slide) -> str:
    steps = slide.payload["steps"]
    count = len(steps)
    out = [title_block(slide)]
    if count == 4:
        boxes = [(90, 340, 290, 220), (450, 340, 290, 220), (810, 340, 290, 220), (1170, 340, 290, 220)]
    else:
        boxes = [(90, 340, 240, 220), (370, 340, 240, 220), (650, 340, 240, 220), (930, 340, 240, 220), (1210, 340, 240, 220)]
    for idx, ((x, y, w, h), step) in enumerate(zip(boxes, steps)):
        accent = step["accent"]
        out.append(rect(x, y, w, h, fill=step.get("fill", PANEL)))
        out.append(pill(x + 20, y + 18, min(190, w - 40), 40, step["title"], accent))
        out.append(t(x + 22, y + 92, step["body"], 21, INK, max_chars=max(18, (w - 44) // 11), line_height=27))
        if idx < count - 1:
            right_edge = x + w
            next_x = boxes[idx + 1][0]
            center_y = y + h // 2
            out.append(arrow(right_edge + 10, center_y, next_x - 10, center_y, stroke=LINE))
    decision = slide.payload.get("decision")
    if decision:
        out.append(rect(90, 620, 1420, 130, fill="#FBF7EF"))
        out.append(t(118, 670, decision["title"], 28, ACCENT, "700"))
        out.append(t(118, 714, decision["body"], 22, INK, max_chars=90, line_height=28))
    note = slide.payload.get("note")
    if note:
        out.append(t(90, 792, note, 20, MUTED, "700", max_chars=110, line_height=24))
    out.append(footer(slide))
    return "".join(out)


def render_risk_map(slide: Slide) -> str:
    zones = slide.payload["zones"]
    xs = [90, 560, 1030]
    fills = [SOFT_GREEN, SOFT_GOLD, SOFT_RED]
    accents = [GREEN, GOLD, RED]
    out = [title_block(slide)]
    for x, zone, fill, accent in zip(xs, zones, fills, accents):
        out.append(rect(x, 280, 380, 460, fill=fill))
        out.append(pill(x + 24, 304, 170, 44, zone["title"], accent))
        out.append(t(x + 24, 392, zone["rule"], 23, INK, "700", max_chars=28, line_height=28))
        out.append(bullet_lines(x + 30, 460, zone["examples"], 21, accent, max_chars=24, step=62))
    note = slide.payload.get("note")
    if note:
        out.append(rect(90, 744, 1420, 56, fill=INK, stroke=INK, rx=18))
        out.append(t(118, 776, note, 19, "white", "700", max_chars=100, line_height=22))
    out.append(footer(slide))
    return "".join(out)


def render_before_after(slide: Slide) -> str:
    left = slide.payload["left"]
    right = slide.payload["right"]
    changes = slide.payload["changes"]
    out = [
        title_block(slide),
        rect(90, 280, 640, 420, fill=SOFT_RED),
        rect(870, 280, 640, 420, fill=SOFT_GREEN),
        t(118, 326, left["title"], 30, RED, "700", max_chars=28, line_height=36),
        t(898, 326, right["title"], 30, GREEN, "700", max_chars=28, line_height=36),
        t(118, 376, left["body"], 21, INK, max_chars=42, line_height=27),
        t(898, 376, right["body"], 21, INK, max_chars=40, line_height=27),
    ]
    for idx, change in enumerate(changes):
        out.append(small_metric(90 + idx * 355, 700, 330, change["title"], change["body"], change["accent"]))
    out.append(footer(slide))
    return "".join(out)


def render_do_dont(slide: Slide) -> str:
    do = slide.payload["do"]
    dont = slide.payload["dont"]
    out = [
        title_block(slide),
        rect(90, 280, 650, 430, fill=SOFT_GREEN),
        rect(860, 280, 650, 430, fill=SOFT_RED),
        t(120, 330, do["title"], 32, GREEN, "700"),
        t(890, 330, dont["title"], 32, RED, "700"),
        bullet_lines(126, 392, do["bullets"], 22, GREEN, max_chars=36, step=74),
        bullet_lines(896, 392, dont["bullets"], 22, RED, max_chars=36, step=74),
    ]
    bridge = slide.payload.get("bridge")
    if bridge:
        out.append(rect(90, 730, 1420, 70, fill=INK, stroke=INK))
        out.append(t(120, 776, bridge, 24, "white", "700", max_chars=92, line_height=28))
    out.append(footer(slide))
    return "".join(out)


def render_card(slide: Slide) -> str:
    body = slide.payload["body"]
    kicker = slide.payload.get("kicker", slide.unit)
    accent = slide.payload.get("accent", ACCENT)
    note = slide.payload.get("note", "")
    out = [
        rect(90, 90, 1420, 720, fill="#FBF7EF", stroke=LINE, rx=40),
        pill(120, 120, 240, 52, kicker, accent),
        t(120, 250, slide.title, 58, INK, "700", family="Georgia, serif", max_chars=32, line_height=66),
        t(120, 360, slide.subtitle, 28, MUTED, "400", max_chars=72, line_height=36),
        rect(120, 460, 1360, 180, fill="white", stroke=LINE),
        t(160, 530, body, 33, INK, "700", max_chars=52, line_height=42),
    ]
    if note:
        out.append(t(120, 705, note, 22, MUTED, "400", max_chars=88, line_height=28))
    out.append(footer(slide))
    return "".join(out)


def svg_wrap(body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f'<rect width="{W}" height="{H}" fill="{BG}"/>'
        f"{body}</svg>"
    )


slides = [
    Slide(
        "l11_title_card.svg",
        "Урок 11",
        "Почему AI выглядит уверенным даже когда ошибается",
        "Критически важный урок про доверие, проверку и ложную убедительность рабочего текста.",
        "card",
        "FW-L11-CASE-A",
        {
            "kicker": "Lesson 11",
            "body": "Гладкий язык не гарантирует надежный вывод.",
            "note": "Открывающий экран к кейсу с sales summary, где модель звучит уверенно и ошибается в фактах, выводах и контексте.",
        },
    ),
    Slide(
        "l11_sales_summary_compare.svg",
        "Урок 11",
        "Кейс: sales summary с ложной уверенностью",
        "Один кейс показывает, как уверенный tone of voice маскирует фактологическую и управленческую ошибку.",
        "compare",
        "FW-L11-CASE-A",
        {
            "columns": [
                {
                    "title": "Что было в заметках",
                    "body": "214 лидов против 182.\nДемо: 31% против 34% в январе.\n8 сделок на 6,4 млн руб.\nУзкие места: юристы и слабый follow-up.",
                },
                {
                    "title": "Что уверенно написал AI",
                    "body": "\"Конверсия поднялась до 31%. Юридический процесс ускорился. Узких мест почти нет. Можно увеличивать нагрузку на команду.\"",
                },
                {
                    "title": "Что должен понять руководитель",
                    "body": "Лидов стало больше, но конверсия в демо просела.\nРост выручки не отменяет два блокера.\nМасштабировать процесс рано.",
                },
            ],
            "metrics": [
                {"title": "Факт сдвинут", "body": "31% ниже 34%, а не рост.", "accent": RED},
                {"title": "Причина перевернута", "body": "Юристы и follow-up были проблемой.", "accent": ACCENT},
                {"title": "Контекст потерян", "body": "AI убрал узкие места из вывода.", "accent": VIOLET},
                {"title": "Решение опасно", "body": "Ложный позитив толкает к неверному действию.", "accent": SAGE},
            ],
        },
    ),
    Slide(
        "l11_false_confidence_breakdown.svg",
        "Урок 11",
        "Разбор ошибки по строкам",
        "Таблица нужна, чтобы в кадре было видно: проблема не в стиле текста, а в сдвиге смысла и решения.",
        "table",
        "FW-L11-CASE-A",
        {
            "headers": ["Ошибка", "Что не так", "Чем опасно"],
            "widths": [280, 540, 600],
            "rows": [
                ["Неверная динамика", "31% ниже 34%, но AI подает это как рост конверсии.", "Руководитель видит несуществующее улучшение воронки."],
                ["Искаженная причина", "Юристы и follow-up названы драйвером, хотя это явные проблемы.", "Команда закрепляет неправильное объяснение результата."],
                ["Завышение эффекта", "Рост выручки есть, но не подтверждает тезис о сильном масштабировании.", "Менеджмент получает ложное ощущение зрелости процесса."],
                ["Потеря узких мест", "Ответ пишет, что узких мест почти нет.", "Реальные точки провала не будут исправлены вовремя."],
            ],
            "note": "Опасность урока: чем правдоподобнее формулировка, тем легче пропустить ошибку до отправки.",
        },
    ),
    Slide(
        "l11_check_before_send.svg",
        "Урок 11",
        "Проверка перед отправкой: 4 вопроса к гладкому ответу",
        "Это не полный checklist урока 12, а аварийный фильтр, когда текст звучит слишком уверенно.",
        "workflow",
        "FW-L11-CASE-A",
        {
            "steps": [
                {"title": "1. Факт", "body": "Все числа, даты и сравнения совпадают с исходником?", "accent": ACCENT, "fill": "#FBF3E8"},
                {"title": "2. Вывод", "body": "Не сделал ли AI более широкий вывод, чем позволяют данные?", "accent": SAGE, "fill": SOFT_GREEN},
                {"title": "3. Контекст", "body": "Не пропал ли блокер, условие или ограничение?", "accent": VIOLET, "fill": SOFT_LILAC},
                {"title": "4. Цена ошибки", "body": "Что случится, если этот текст уйдет руководителю или клиенту?", "accent": RED, "fill": SOFT_RED},
            ],
            "decision": {
                "title": "Правило экрана",
                "body": "Если хотя бы на один вопрос ответ неочевиден, summary нельзя пересылать как есть. Сначала возвращаемся к источнику и правим.",
            },
            "note": "Этот экран закрывает урок действием: гладкий ответ сначала проверяем, потом используем.",
        },
    ),
    Slide(
        "l11_final_card.svg",
        "Урок 11",
        "Действие после урока",
        "Жесткое закрепление навыка проверки до использования.",
        "card",
        "FW-L11-CASE-A",
        {
            "kicker": "After Lesson 11",
            "body": "Откройте один старый AI-summary и проверьте в нем факт, вывод и потерянный контекст.",
            "note": "Не исправляйте все подряд. Найдите одну опасную ошибку, которую было бы легко отправить дальше из-за уверенного тона.",
            "accent": RED,
        },
    ),
    Slide(
        "l12_title_card.svg",
        "Урок 12",
        "Чек-лист проверки качества",
        "Проверка должна быть системной, а не интуитивной: короткий набор критериев вместо хаотичного сомнения.",
        "card",
        "CM-L12-CASE-A",
        {
            "kicker": "Lesson 12",
            "body": "За 90 секунд понять: использовать, править или стоп.",
            "note": "Урок строится на кейсе операционного синка по пилоту и превращает осторожность из урока 11 в рабочую систему.",
        },
    ),
    Slide(
        "l12_quality_checklist.svg",
        "Урок 12",
        "One-screen checklist: 6 критериев проверки",
        "Чек-лист нужен не для идеала, а чтобы быстро находить, где ответ надежный, а где уже опасен.",
        "checklist",
        "CM-L12-CASE-A",
        {
            "items": [
                {"title": "Факты", "body": "Даты, числа, условия и зависимости совпадают с исходником без домысливаний."},
                {"title": "Логика", "body": "Выводы реально следуют из исходных заметок, а не только красиво звучат."},
                {"title": "Полнота", "body": "Критичный контекст, блокеры и ограничения не выпали по дороге."},
                {"title": "Тон", "body": "Текст не создает ложного спокойствия там, где есть риск и неопределенность."},
                {"title": "Применимость", "body": "Ответ можно реально отправить, переслать или использовать в рабочем решении."},
                {"title": "Риск", "body": "Понятно, что сломается, если здесь останется ошибка или слишком широкий вывод."},
            ],
            "note": "Проходим сверху вниз. Если провалился любой из шести критериев, качество уже нельзя считать рабочим.",
        },
    ),
    Slide(
        "l12_pilot_review_scorecard.svg",
        "Урок 12",
        "CM-L12-CASE-A: где summary ломается",
        "Кейс операционного синка показывает, как чек-лист вытаскивает реальные блокеры за одну короткую проверку.",
        "table",
        "CM-L12-CASE-A",
        {
            "headers": ["Критерий", "Что проверяем", "Что сломалось в AI-summary"],
            "widths": [220, 420, 780],
            "rows": [
                ["Факты", "Сроки, числа, условия", "Потерян срок по списку 12 пользователей и условие про DPA до пятницы 17:00."],
                ["Логика", "Следует ли вывод из исходника", "Текст говорит, что запуск стабилен, хотя в исходнике есть блокеры и условия."],
                ["Полнота", "Сохранен ли критичный контекст", "Выпал риск по 2 магазинам и таблицам остатков."],
                ["Тон", "Не маскирует ли риск", "Summary звучит слишком успокаивающе для рискованной ситуации."],
                ["Применимость", "Можно ли переслать как есть", "Нет. Руководитель получит искаженный статус запуска."],
                ["Риск", "Цена ошибки при использовании", "Можно пообещать понедельничный запуск без фактической готовности."],
            ],
            "note": "Чек-лист не замедляет работу. Он быстро показывает, что именно надо чинить в ответе.",
        },
    ),
    Slide(
        "l12_summary_before_after.svg",
        "Урок 12",
        "До и после проверки: summary по пилоту",
        "Контраст нужен не ради красоты текста, а чтобы показать возврат сроков, условий и реального риска.",
        "split",
        "CM-L12-CASE-A",
        {
            "left": {
                "title": "AI-summary до проверки",
                "body": "Пилот стартует в понедельник.\nFAQ можно завершить после запуска.\nСписок пользователей желательно финализировать на следующей неделе.\nОсновной риск в нагрузке на support.",
            },
            "right": {
                "title": "Версия после проверки",
                "body": "Запуск в понедельник возможен только если DPA согласован до пятницы 17:00.\n12 пользователей нужны до четверга 16:00.\nFAQ готовим к пятнице 12:00.\n2 магазина без корректных остатков держат подключение под риском.",
            },
            "bottom": "Что именно вернули в текст: условие по DPA, срок по пользователям, дедлайн FAQ и риск по двум магазинам.",
            "left_fill": SOFT_RED,
            "right_fill": SOFT_GREEN,
        },
    ),
    Slide(
        "l12_final_card.svg",
        "Урок 12",
        "Действие после урока",
        "Чек-лист должен превратиться в привычку, а не остаться красивым списком.",
        "card",
        "CM-L12-CASE-A",
        {
            "kicker": "After Lesson 12",
            "body": "Прогоните один свой AI-ответ по 6 критериям и поставьте ему статус: use, fix или stop.",
            "note": "Если ответ попал в `fix`, исправьте только один самый рискованный провал. Задача урока не идеальность, а надежность.",
            "accent": SAGE,
        },
    ),
    Slide(
        "l13_title_card.svg",
        "Урок 13",
        "Когда нельзя копировать ответ как есть",
        "Урок про зоны риска: где AI можно использовать как черновик, а где нужен жесткий human review и policy gate.",
        "card",
        "CM-L13-RISK-MAP / CM-L13-CASE-A",
        {
            "kicker": "Lesson 13",
            "body": "Чем выше цена ошибки, тем меньше права на копипаст.",
            "note": "Фокус урока: внешние обещания, юридические формулировки, чувствительные данные и решения по непроверенным цифрам.",
        },
    ),
    Slide(
        "l13_risk_map.svg",
        "Урок 13",
        "Green / Yellow / Red map",
        "Экран нужен, чтобы ученик заранее понимал режим использования AI еще до того, как получил ответ.",
        "risk_map",
        "CM-L13-RISK-MAP",
        {
            "zones": [
                {
                    "title": "Зеленая зона",
                    "rule": "Быстрый черновик допустим.",
                    "examples": [
                        "Идеи заголовков",
                        "Черновик структуры",
                        "Summary публичной статьи",
                        "Внутренняя заметка без чувствительных данных",
                    ],
                },
                {
                    "title": "Желтая зона",
                    "rule": "Только после внимательной проверки.",
                    "examples": [
                        "Follow-up письмо клиенту",
                        "Summary рабочей встречи",
                        "Draft FAQ",
                        "Внутренняя status note",
                    ],
                },
                {
                    "title": "Красная зона",
                    "rule": "Без копипаста и без policy gate не используем.",
                    "examples": [
                        "Скидки и сроки запуска",
                        "Юридические формулировки",
                        "Чувствительные данные",
                        "Управленческий вывод по непроверенным цифрам",
                    ],
                },
            ],
            "note": "Режим работы определяют цена ошибки, внешний адресат и чувствительность данных, а не удобство пользователя.",
        },
    ),
    Slide(
        "l13_red_zone_client_promise.svg",
        "Урок 13",
        "Красная зона: обещание клиенту",
        "Один кейс показывает, почему гладкий ответ модели не равен праву его отправить.",
        "compare",
        "CM-L13-CASE-A",
        {
            "columns": [
                {
                    "title": "Что реально известно",
                    "body": "Скидка 15% не согласована.\nЮристы не подтвердили дату запуска.\nКлиент просит письменное подтверждение сроков.",
                },
                {
                    "title": "Небезопасный prompt",
                    "body": "\"Напиши клиенту, что дадим скидку 15% и запустимся до 1 апреля. Сделай письмо уверенным и спокойным.\"",
                },
                {
                    "title": "Опасный AI-ответ",
                    "body": "\"Подтверждаем скидку 15% и запуск до 1 апреля. Со своей стороны рисков не видим.\"",
                },
            ],
            "fills": [SOFT_GOLD, SOFT_RED, SOFT_RED],
            "accents": [GOLD, RED, RED],
            "metrics": [
                {"title": "Внешний адресат", "body": "Ошибка уходит сразу клиенту, а не остается внутри.", "accent": RED},
                {"title": "Деньги", "body": "Скидка превращает черновик в финансовое обещание.", "accent": ACCENT},
                {"title": "Срок не подтвержден", "body": "Дата запуска еще не согласована юридически.", "accent": VIOLET},
                {"title": "Репутационный риск", "body": "Письмо создает обязательство, которого бизнес не подтверждал.", "accent": SAGE},
            ],
        },
    ),
    Slide(
        "l13_zone_classifier.svg",
        "Урок 13",
        "Как быстро разметить задачу по зонам риска",
        "Вместо интуитивного ощущения используем короткую последовательность вопросов до запуска AI.",
        "workflow",
        "CM-L13-RISK-MAP / CM-L13-CASE-A",
        {
            "steps": [
                {"title": "1. Аудитория", "body": "Это внутренний черновик или внешний текст для клиента, партнера, руководителя?", "accent": ACCENT, "fill": "#FBF3E8"},
                {"title": "2. Обещание", "body": "Есть ли скидка, срок, юридическое условие или управленческий вывод?", "accent": RED, "fill": SOFT_RED},
                {"title": "3. Данные", "body": "Есть ли цифры, персональные данные или чувствительные детали?", "accent": VIOLET, "fill": SOFT_LILAC},
                {"title": "4. Цена ошибки", "body": "Что сломается, если в ответе останется ошибка или лишнее обещание?", "accent": GOLD, "fill": SOFT_GOLD},
                {"title": "5. Режим", "body": "Green = черновик. Yellow = проверка. Red = policy gate и human review.", "accent": SAGE, "fill": SOFT_GREEN},
            ],
            "decision": {
                "title": "Правило классификации",
                "body": "Если есть внешнее обещание и неподтвержденный факт, задача почти всегда уходит в красную зону, даже если текст выглядит безупречно.",
            },
            "note": "Экран переводит риск из абстракции в повторяемое решение до копипаста.",
        },
    ),
    Slide(
        "l13_final_card.svg",
        "Урок 13",
        "Действие после урока",
        "После урока ученик должен разметить свои реальные задачи, а не просто согласиться с теорией.",
        "card",
        "CM-L13-RISK-MAP / CM-L13-CASE-A",
        {
            "kicker": "After Lesson 13",
            "body": "Разметьте 5 своих рабочих задач по зонам: green, yellow, red, и запретите себе копипаст в red.",
            "note": "Если сомневаетесь между yellow и red, ставьте red. Цена лишней осторожности ниже цены ложного обещания.",
            "accent": RED,
        },
    ),
    Slide(
        "l14_title_card.svg",
        "Урок 14",
        "Как превращать сырой AI-черновик в рабочий результат",
        "Ценность появляется не в первом ответе, а в доработке: от воды и гладкости к фактам, рискам и формату задачи.",
        "card",
        "CM-L14-CASE-A",
        {
            "kicker": "Lesson 14",
            "body": "AI делает черновик. Специалист делает продукт.",
            "note": "Основной кейс: status update по первой неделе пилота с реальными блокерами, вопросами support и решением на пятницу.",
        },
    ),
    Slide(
        "l14_status_update_before_after.svg",
        "Урок 14",
        "Сырой AI-черновик против рабочего status update",
        "Контраст должен показать не литературное улучшение, а рост пригодности к рабочему использованию.",
        "before_after",
        "CM-L14-CASE-A",
        {
            "left": {
                "title": "Сырой AI-черновик",
                "body": "Хочу поделиться обновлением по пилоту. На первой неделе у нас уже есть хороший прогресс, команда активно отвечает на возникающие вопросы, а организационные моменты по таблицам остатков и юридическому согласованию дальнейшего расширения в целом не мешают позитивной динамике.",
            },
            "right": {
                "title": "Рабочая версия",
                "body": "Статус пилота за первую неделю:\n- подключены 3 магазина;\n- еще 2 не готовы: ждем корректные таблицы остатков;\n- support получил 14 вопросов, чаще всего по доступу;\n- расширение scope не подтверждено: ждем юристов;\n- в пятницу решаем, идем ли во вторую волну.",
            },
            "changes": [
                {"title": "Убрали воду", "body": "Позитивную динамику заменили на наблюдаемые факты.", "accent": RED},
                {"title": "Вернули цифры", "body": "3 магазина, 2 блокера, 14 вопросов.", "accent": ACCENT},
                {"title": "Выделили риски", "body": "Остатки и юристы вынесены как блокеры.", "accent": VIOLET},
                {"title": "Собрали формат", "body": "Руководитель считывает статус за 20 секунд.", "accent": SAGE},
            ],
        },
    ),
    Slide(
        "l14_edit_moves_workflow.svg",
        "Урок 14",
        "5 движений до рабочего результата",
        "Это не набор красивых советов, а короткий процесс редактуры, который можно повторять на каждом AI-черновике.",
        "workflow",
        "CM-L14-CASE-A",
        {
            "steps": [
                {"title": "1. Убрать воду", "body": "Снимаем общие слова, которые маскируют реальный статус.", "accent": RED, "fill": SOFT_RED},
                {"title": "2. Вернуть факты", "body": "Числа, сроки, условия и зависимости вставляем обратно.", "accent": ACCENT, "fill": "#FBF3E8"},
                {"title": "3. Выделить блокеры", "body": "Отдельно показываем, что тормозит решение и запуск.", "accent": VIOLET, "fill": SOFT_LILAC},
                {"title": "4. Подстроить адресата", "body": "Формулируем так, чтобы конкретный читатель быстро понял смысл.", "accent": GOLD, "fill": SOFT_GOLD},
                {"title": "5. Довести формат", "body": "Письмо, note, summary или status update должны выглядеть как рабочий артефакт.", "accent": SAGE, "fill": SOFT_GREEN},
            ],
            "decision": {
                "title": "Проверка готовности",
                "body": "Если адресат за 20 секунд понимает факты, риски и следующий шаг, черновик уже превратился в рабочий результат.",
            },
            "note": "Этот workflow закрывает главный тезис урока: не копировать, а доводить до стандарта задачи.",
        },
    ),
    Slide(
        "l14_edit_breakdown.svg",
        "Урок 14",
        "Что именно изменили и зачем",
        "Таблица помогает показать, что редактура нужна не ради стиля, а ради ясности решения.",
        "table",
        "CM-L14-CASE-A",
        {
            "headers": ["Шаг", "Что сделали", "Зачем"],
            "widths": [220, 480, 720],
            "rows": [
                ["Сократили воду", "Убрали слова про хороший прогресс и позитивную динамику.", "Текст перестал маскировать реальный статус за общими фразами."],
                ["Вернули факты", "Назвали 3 магазина, 2 неподключенные точки и 14 вопросов в support.", "Руководитель видит, что реально произошло за неделю пилота."],
                ["Показали блокеры", "Отдельно вынесли таблицы остатков и ожидание ответа юристов.", "Решение по следующей волне не принимается вслепую."],
                ["Собрали формат", "Сделали короткий список вместо рыхлого абзаца.", "Статус можно быстро читать, обсуждать и пересылать внутри команды."],
            ],
            "note": "Редактура сильного пользователя AI всегда улучшает пригодность к действию, а не только внешний вид текста.",
        },
    ),
    Slide(
        "l14_final_card.svg",
        "Урок 14",
        "Действие после урока",
        "Урок закрывается не принципом, а конкретной ручной доработкой своего черновика.",
        "card",
        "CM-L14-CASE-A",
        {
            "kicker": "After Lesson 14",
            "body": "Возьмите один свой AI-черновик и вручную проведите по нему 5 движений до рабочего стандарта.",
            "note": "Не просите модель исправить все самой. Сначала сами решите, какие факты, блокеры и формат должен увидеть адресат.",
            "accent": ACCENT,
        },
    ),
    Slide(
        "l15_title_card.svg",
        "Урок 15",
        "Минимальная цифровая гигиена и безопасность",
        "Базовый уровень профессионализма: думать не только о качестве ответа, но и о безопасности того, что вы отправляете в модель.",
        "card",
        "CM-L15-CASE-A / CM-L15-RULESET-A",
        {
            "kicker": "Lesson 15",
            "body": "Зрелая работа с AI = качество результата + безопасность входных данных.",
            "note": "Урок строится на контрасте двух prompt-сценариев и на пяти базовых правилах безопасной работы.",
        },
    ),
    Slide(
        "l15_safe_vs_unsafe_prompt.svg",
        "Урок 15",
        "Одна задача, два prompt-режима",
        "Контраст безопасной и небезопасной постановки показывает, что полезность можно сохранить без избыточных данных.",
        "split",
        "CM-L15-CASE-A",
        {
            "left": {
                "title": "Небезопасный prompt",
                "body": "Проанализируй обращение клиента Ивана Петрова.\nНомер договора: 54821.\nТелефон: +7 9XX XXX XX XX.\nСумма спорного возврата: 184 500 рублей.\nПодскажи, как ответить клиенту и кто виноват.",
            },
            "right": {
                "title": "Безопасная версия той же задачи",
                "body": "Проанализируй обезличенное обращение по спорному возврату.\nНужно:\n- назвать 2-3 вероятные причины;\n- предложить структуру ответа;\n- перечислить факты для ручной проверки до отправки.\nПерсональные и чувствительные детали убраны.",
            },
            "bottom": "Задача та же. Разница в том, что модель получает минимально достаточный контекст вместо полного чувствительного куска.",
            "left_fill": SOFT_RED,
            "right_fill": SOFT_GREEN,
        },
    ),
    Slide(
        "l15_safety_rules_checklist.svg",
        "Урок 15",
        "5 правил безопасной работы с AI",
        "Минимальный ruleset нужен каждому сотруднику, даже если до enterprise governance еще далеко.",
        "checklist",
        "CM-L15-RULESET-A",
        {
            "items": [
                {"title": "Правило 1", "body": "Не вставляйте персональные данные, если задачу можно решить без них."},
                {"title": "Правило 2", "body": "Не передавайте номера договоров, суммы и чувствительные условия без явной необходимости и понимания policy."},
                {"title": "Правило 3", "body": "Лучше кратко пересказать документ, чем загружать его целиком только ради удобства."},
                {"title": "Правило 4", "body": "Каждый раз спрашивайте себя: какой минимальный контекст действительно нужен модели?"},
                {"title": "Правило 5", "body": "Если цена утечки или ошибки высокая, сначала смотрите на корпоративные правила, а не на скорость."},
                {"title": "Итог", "body": "Безопасность не мешает полезности. Она убирает лишний риск из входа и оставляет рабочий смысл задачи."},
            ],
            "note": "Если задачу можно решить на обезличенном описании, нельзя тащить в prompt сырой чувствительный фрагмент.",
        },
    ),
    Slide(
        "l15_do_dont.svg",
        "Урок 15",
        "Do / Don't: цифровая гигиена на одном экране",
        "Один экран для записи и rough cut: что делаем всегда и что запрещаем себе по умолчанию.",
        "do_dont",
        "CM-L15-CASE-A / CM-L15-RULESET-A",
        {
            "do": {
                "title": "Делать",
                "bullets": [
                    "Обезличивать кейс, если это не ломает смысл задачи.",
                    "Передавать минимум контекста, достаточный для ответа.",
                    "Просить структуру, варианты и список ручных проверок.",
                    "Проверять чувствительные выводы до внешней отправки.",
                ],
            },
            "dont": {
                "title": "Не делать",
                "bullets": [
                    "Вставлять ФИО, телефоны, номера договоров и суммы без необходимости.",
                    "Грузить целый документ в модель только потому, что так быстрее.",
                    "Просить модель принять решение вместо вас в чувствительном кейсе.",
                    "Слепо копировать ответ в клиентскую или юридическую коммуникацию.",
                ],
            },
            "bridge": "Личная цифровая гигиена сотрудника потом превращается в правило команды, manager checklist и company policy.",
        },
    ),
    Slide(
        "l15_final_card.svg",
        "Урок 15",
        "Действие после урока",
        "Закрывающий экран должен перевести безопасность из абстрактной темы в конкретное правило следующего промпта.",
        "card",
        "CM-L15-CASE-A / CM-L15-RULESET-A",
        {
            "kicker": "After Lesson 15",
            "body": "Выпишите 5 правил безопасной работы и проверьте на них свой следующий prompt до отправки.",
            "note": "Если видите лишние персональные или чувствительные данные, сократите prompt до минимально достаточного описания задачи.",
            "accent": SAGE,
        },
    ),
]


RENDERERS = {
    "card": render_card,
    "compare": render_compare,
    "table": render_table,
    "split": render_split,
    "checklist": render_checklist,
    "workflow": render_workflow,
    "risk_map": render_risk_map,
    "before_after": render_before_after,
    "do_dont": render_do_dont,
}


def main() -> None:
    for slide in slides:
        renderer = RENDERERS[slide.kind]
        (OUT / slide.filename).write_text(svg_wrap(renderer(slide)), encoding="utf-8")
    print(f"Generated {len(slides)} SVG assets in {OUT}")


if __name__ == "__main__":
    main()
