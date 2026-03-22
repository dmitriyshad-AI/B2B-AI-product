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
        + pill(1280, 70, 230, 54, slide.case_id, SAGE)
    )


def footer(slide: Slide) -> str:
    return (
        f'<line x1="90" y1="820" x2="1510" y2="820" stroke="{LINE}" stroke-width="2"/>'
        + t(90, 855, "Business-learning visual asset · First wave production pack", 20, MUTED)
        + t(1110, 855, slide.filename.replace(".svg", ""), 20, MUTED, "700")
    )


def bullet_block(x: int, y: int, w: int, h: int, title: str, bullets: list[str], accent: str = INK) -> str:
    out = [rect(x, y, w, h), t(x + 28, y + 48, title, 28, accent, "700")]
    cy = y + 95
    for bullet in bullets:
        out.append(f'<circle cx="{x + 35}" cy="{cy - 8}" r="6" fill="{ACCENT}"/>')
        out.append(t(x + 55, cy, bullet, 24, INK, max_chars=34, line_height=30))
        cy += 70
    return "".join(out)


def small_metric(x: int, y: int, w: int, title: str, body: str, accent: str = ACCENT) -> str:
    return (
        rect(x, y, w, 120)
        + t(x + 24, y + 40, title, 24, accent, "700")
        + t(x + 24, y + 78, body, 22, INK, max_chars=28, line_height=28)
    )


def render_form(slide: Slide) -> str:
    left = slide.payload["left"]
    right = slide.payload["right"]
    return (
        title_block(slide)
        + bullet_block(90, 280, 650, 470, left["title"], left["bullets"], SAGE)
        + bullet_block(860, 280, 650, 470, right["title"], right["bullets"], ACCENT)
        + footer(slide)
    )


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
    for i, metric in enumerate(slide.payload["metrics"]):
        out.append(small_metric(90 + i * 355, 730, 330, metric["title"], metric["body"], metric["accent"]))
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
            out.append(t(x + 14, y + 36, cell, 19, INK, max_chars=max(10, width // 12), line_height=22))
            x += width
        y += 58
    out.append(footer(slide))
    return "".join(out)


def render_metrics(slide: Slide) -> str:
    artifact = slide.payload["artifact"]
    metrics = slide.payload["metrics"]
    out = [
        title_block(slide),
        rect(90, 270, 850, 460, fill="#FFF7EF"),
        rect(980, 270, 530, 460, fill="#EEF5F1"),
        t(120, 320, artifact["title"], 30, ACCENT, "700"),
        t(120, 370, artifact["body"], 22, INK, max_chars=52, line_height=28),
        t(1010, 320, "Что показываем ЛПР", 30, SAGE, "700"),
    ]
    cy = 370
    for metric in metrics:
        out.append(rect(1010, cy - 18, 470, 88, fill="white", stroke=LINE))
        out.append(t(1034, cy + 14, metric["title"], 24, SAGE, "700"))
        out.append(t(1034, cy + 46, metric["body"], 20, INK, max_chars=36, line_height=24))
        cy += 104
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
        t(120, 360, slide.subtitle, 28, MUTED, "400", max_chars=70, line_height=36),
        rect(120, 460, 1360, 180, fill="white", stroke=LINE),
        t(160, 530, body, 34, INK, "700", max_chars=50, line_height=42),
    ]
    if note:
        out.append(t(120, 705, note, 22, MUTED, "400", max_chars=88, line_height=28))
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
        "s00_title_card.svg",
        "Сессия 0",
        "Диагностика и первая практическая победа",
        "Старт курса должен сразу дать пользу, baseline и первый рабочий артефакт.",
        "card",
        "FW-S00-L01-CASE-A",
        {
            "kicker": "Старт",
            "body": "Первая польза от AI должна появиться сразу.",
            "note": "Использовать как opening card перед входной формой и baseline compare.",
        },
    ),
    Slide(
        "s00_diagnostic_form.svg",
        "Сессия 0",
        "Входная самодиагностика",
        "Один экран для старта: роль, частота использования AI, рабочие задачи и критерий успеха на 14 дней.",
        "form",
        "FW-S00-L01-CASE-A",
        {
            "left": {
                "title": "Что спрашиваем до старта",
                "bullets": [
                    "Роль и текущий уровень использования AI.",
                    "Какие задачи уже пробовали ускорять.",
                    "Где чувствуется уверенность.",
                    "Где есть риск, барьер или недоверие.",
                ],
            },
            "right": {
                "title": "Что фиксируем как стартовую точку",
                "bullets": [
                    "Три задачи, которые хочется ускорить в первую очередь.",
                    "Ожидаемый результат через 14 дней.",
                    "Где человек теряет время прямо сейчас.",
                    "С каким страхом или сомнением идет в курс.",
                ],
            },
        },
    ),
    Slide(
        "s00_first_win_compare.svg",
        "Сессия 0",
        "First Win: от baseline к рабочему черновику",
        "Один и тот же кейс показывает не магию, а ускорение старта и рост ясности уже в первые 10 минут.",
        "compare",
        "FW-S00-L01-CASE-A",
        {
            "columns": [
                {"title": "Baseline без AI", "body": "Спасибо за встречу. Пришлем доступ и потом созвонимся. Направьте список участников."},
                {"title": "AI-черновик", "body": "Сегодня до 18:00 отправлю демо. Пришлите 3 email участников до пятницы. Созвон подтверждаю: вторник, 11:00."},
                {"title": "Финальная версия", "body": "Короткое письмо с четким сроком, понятным действием и спокойным деловым тоном."},
            ],
            "metrics": [
                {"title": "Польза", "body": "быстрее начать и не забыть следующий шаг", "accent": SAGE},
                {"title": "Проверка", "body": "тон и факт встречи все равно подтверждает человек", "accent": ACCENT},
                {"title": "Артефакт", "body": "baseline, AI-draft и final draft сохраняются в LMS", "accent": INK},
                {"title": "Первый win", "body": "курс дает пользу сразу, до длинной теории", "accent": SAGE},
            ],
        },
    ),
    Slide(
        "s00_final_card.svg",
        "Сессия 0",
        "Что сохранить после сессии",
        "Закрывающий экран после первого quick win.",
        "card",
        "FW-S00-L01-CASE-A",
        {
            "kicker": "После сессии 0",
            "body": "Сохраните baseline, AI-черновик и свой first win.",
            "note": "Этот экран должен закрывать сессию 0 и мостить переход к уроку 1.",
            "accent": SAGE,
        },
    ),
    Slide(
        "l01_title_card.svg",
        "Урок 1",
        "AI в работе: инструмент, а не магия",
        "Главная рамка всего курса: AI помогает быстрее начать, но не снимает ответственность.",
        "card",
        "FW-S00-L01-CASE-A",
        {
            "kicker": "Урок 1",
            "body": "AI не заменяет специалиста. Он ускоряет часть его работы.",
        },
    ),
    Slide(
        "l01_two_extremes.svg",
        "Урок 1",
        "Две ложные крайности на старте",
        "Взрослая рамка курса начинается не с хайпа и не со скепсиса, а с трезвой рабочей позиции.",
        "split",
        "FW-S00-L01-CASE-A",
        {
            "left": {
                "title": "Крайность 1",
                "body": "“AI все сделает за меня”. В этой позиции человек снимает с себя ответственность и ждет чудо вместо осмысленной работы.",
            },
            "right": {
                "title": "Крайность 2",
                "body": "“AI бесполезен”. В этой позиции человек не доходит даже до первого полезного сценария и путает плохой старт с отсутствием пользы.",
            },
            "bottom": "Рабочая позиция: AI не заменяет специалиста. Он ускоряет часть его работы и помогает быстрее собрать первый полезный черновик.",
        },
    ),
    Slide(
        "l01_ai_vs_human.svg",
        "Урок 1",
        "Где роль AI, а где роль человека",
        "Этот экран удерживает главный принцип курса: AI полезен как ускоритель старта, но не как автопилот ответственности.",
        "split",
        "FW-S00-L01-CASE-A",
        {
            "left": {
                "title": "Что делает AI",
                "body": "Помогает быстрее начать. Предлагает структуру. Ускоряет первый черновик. Снижает хаос на входе в задачу.",
            },
            "right": {
                "title": "Что остается за человеком",
                "body": "Проверка фактов. Учет контекста компании. Решение, уместность и ответственность за итоговый результат.",
            },
            "bottom": "Формула урока: AI = черновик, структура, ускорение. Человек = проверка, контекст, решение.",
        },
    ),
    Slide(
        "l01_final_card.svg",
        "Урок 1",
        "Действие после урока",
        "Экран для жесткой фиксации early-value contour.",
        "card",
        "FW-S00-L01-CASE-A",
        {
            "kicker": "После урока 1",
            "body": "Зафиксируйте first win и выпишите 3 повторяющиеся задачи.",
            "note": "Использовать как action-screen перед переходом к уроку 2.",
            "accent": SAGE,
        },
    ),
    Slide(
        "l05_title_card.svg",
        "Урок 5",
        "Почему слабый запрос дает слабый результат",
        "Контрастный урок про постановку задачи, а не про магию модели.",
        "card",
        "FW-L05-CASE-A",
        {
            "kicker": "Урок 5",
            "body": "Качество ответа начинается с качества постановки задачи.",
        },
    ),
    Slide(
        "l05_prompt_compare.svg",
        "Урок 5",
        "Слабый запрос против сильного запроса",
        "Один и тот же кейс показывает: проблема часто не в модели, а в расплывчатой постановке задачи.",
        "split",
        "FW-L05-CASE-A",
        {
            "left": {
                "title": "Слабый запрос",
                "body": "“Напиши хорошее письмо клиенту после встречи”. Нет цели, нет контекста, нет формата и нет критериев качества.",
            },
            "right": {
                "title": "Сильный запрос",
                "body": "Есть адресат, сценарий, сроки, ожидаемое действие и ограничение по тону. Модель работает внутри понятной рамки.",
            },
            "bottom": "Качество ответа начинается с качества постановки задачи.",
        },
    ),
    Slide(
        "l05_prompt_formula.svg",
        "Урок 5",
        "Формула хорошего запроса на одном экране",
        "Четыре опоры нужны не для красоты, а чтобы AI перестал угадывать вслепую.",
        "grid",
        "FW-L05-CASE-A",
        {
            "cards": [
                {"title": "1. Цель", "body": "Что должно получиться в конце: письмо, summary, note, список решений."},
                {"title": "2. Контекст", "body": "Кто адресат, что уже произошло, какие сроки и ограничения важны именно здесь."},
                {"title": "3. Формат", "body": "Сколько строк, какой тип ответа, какая структура, нужен ли список или письмо."},
                {"title": "4. Критерий качества", "body": "Что делает ответ пригодным: краткость, тон, следующий шаг, ясность, отсутствие лишнего."},
            ]
        },
    ),
    Slide(
        "l05_final_card.svg",
        "Урок 5",
        "Действие после урока",
        "Экран для перевода наблюдения в практику.",
        "card",
        "FW-L05-CASE-A",
        {
            "kicker": "После урока 5",
            "body": "Перепишите один свой слабый запрос через цель, контекст, формат и критерий.",
            "accent": SAGE,
        },
    ),
    Slide(
        "l11_title_card.svg",
        "Урок 11",
        "Почему AI выглядит уверенным даже когда ошибается",
        "Критически важный урок про доверие, проверку и ложную уверенность.",
        "card",
        "FW-L11-CASE-A",
        {
            "kicker": "Урок 11",
            "body": "Уверенный тон не равен качеству результата.",
        },
    ),
    Slide(
        "l11_false_confidence_summary.svg",
        "Урок 11",
        "Когда гладкий язык маскирует ошибку",
        "Этот экран нужен, чтобы на видео было видно: опасность рождается не из явной ерунды, а из правдоподобного и уверенного тона.",
        "split",
        "FW-L11-CASE-A",
        {
            "left": {
                "title": "Что говорят исходные заметки",
                "body": "214 лидов против 182. Конверсия в демо снизилась с 34% до 31%. Узкие места: юристы и слабый follow-up.",
            },
            "right": {
                "title": "Что уверенно выдает AI",
                "body": "“Конверсия выросла до 31%, главным драйвером стал быстрый юридический процесс, узких мест почти нет”. Тон гладкий, выводы ошибочны.",
            },
            "bottom": "Ловушка урока: чем убедительнее звучит ошибка, тем выше риск перенести ее в письмо, записку или презентацию.",
        },
    ),
    Slide(
        "l11_error_breakdown.svg",
        "Урок 11",
        "Разбор ошибки по слоям",
        "Один экран для проговаривания трех типов ложной уверенности: сдвиг факта, лишний вывод и потеря контекста.",
        "table",
        "FW-L11-CASE-A",
        {
            "headers": ["Тип ошибки", "Что произошло", "Чем это опасно"],
            "widths": [310, 560, 550],
            "rows": [
                ["Сдвиг факта", "31% ниже 34%, но AI подает это как рост конверсии.", "Руководитель видит несуществующее улучшение воронки."],
                ["Лишний вывод", "Юристы и follow-up были проблемой, а модель называет их драйвером роста.", "Команда может закрепить неверное решение."],
                ["Потеря контекста", "AI пишет, что узких мест почти нет.", "Реальные провалы останутся без внимания и исправления."],
                ["Завышение результата", "Рост выручки подается как «резкий скачок» без достаточных оснований.", "Менеджмент получает искаженную картину эффективности."],
            ],
        },
    ),
    Slide(
        "l11_final_card.svg",
        "Урок 11",
        "Действие после урока",
        "Экран для закрепления навыка проверки.",
        "card",
        "FW-L11-CASE-A",
        {
            "kicker": "После урока 11",
            "body": "Проверьте один старый AI-ответ: факт, вывод, контекст.",
            "accent": SAGE,
        },
    ),
    Slide(
        "l16_title_card.svg",
        "Урок 16",
        "Деловая переписка и сообщения",
        "Прикладной урок про реальную рабочую переписку без канцелярита и неловкой автоматизации.",
        "card",
        "FW-L16-CASE-A / FW-L16-CASE-B",
        {
            "kicker": "Урок 16",
            "body": "AI ускоряет первый черновик, но ответственность за сообщение остается у человека.",
        },
    ),
    Slide(
        "l16_four_anchors.svg",
        "Урок 16",
        "Четыре опоры качественной переписки",
        "Этот экран должен стоять в начале блока, чтобы потом все демо читались через одну рабочую рамку.",
        "grid",
        "FW-L16-CASE-A",
        {
            "cards": [
                {"title": "Кому пишем", "body": "Роль адресата и уровень близости: клиент, коллега, руководитель, партнер."},
                {"title": "Зачем пишем", "body": "Подтвердить договоренности, напомнить о действии, согласовать решение, попросить данные."},
                {"title": "Какое действие ждем", "body": "Прислать email, подтвердить слот, отправить документы, дать комментарий, согласовать текст."},
                {"title": "Какой тон допустим", "body": "Короткий, деловой, спокойный, без канцелярита и без искусственной идеальности."},
            ]
        },
    ),
    Slide(
        "l16_message_workflow.svg",
        "Урок 16",
        "AI как черновик и как редактор",
        "Два режима на одном экране: кейс A показывает письмо с нуля, кейс B — улучшение уже написанного сообщения.",
        "compare",
        "FW-L16-CASE-A / FW-L16-CASE-B",
        {
            "columns": [
                {"title": "Кейс A · с нуля", "body": "Follow-up после встречи: AI собирает первый черновик, человек сокращает и делает следующий шаг конкретным."},
                {"title": "Кейс B · из сырого текста", "body": "Напоминание о документах: AI не пишет «лучше человека», а помогает сделать текст яснее и спокойнее."},
                {"title": "Главное правило", "body": "AI полезен как черновик и редактор. Ответственность за тон, уместность и точность остается у человека."},
            ],
            "metrics": [
                {"title": "Режим 1", "body": "сбор письма после встречи", "accent": SAGE},
                {"title": "Режим 2", "body": "редактура слабого сообщения", "accent": ACCENT},
                {"title": "Проверяем", "body": "ясность действия и естественность тона", "accent": INK},
                {"title": "Результат", "body": "2 шаблона для типовой переписки", "accent": SAGE},
            ],
        },
    ),
    Slide(
        "l16_final_card.svg",
        "Урок 16",
        "Действие после урока",
        "Экран для фиксации двух повторяемых шаблонов переписки.",
        "card",
        "FW-L16-CASE-A / FW-L16-CASE-B",
        {
            "kicker": "После урока 16",
            "body": "Соберите 2 шаблона для типовой переписки: с нуля и из сырого текста.",
            "accent": SAGE,
        },
    ),
    Slide(
        "l24_title_card.svg",
        "Урок 24",
        "План внедрения на 14 дней",
        "Финальный урок Core: переход от понимания к дисциплинированной практике.",
        "card",
        "FW-L24-CASE-A / FW-L24-CASE-B",
        {
            "kicker": "Урок 24",
            "body": "Внедрение AI начинается не с трансформации, а с 2 недель дисциплинированной практики.",
        },
    ),
    Slide(
        "l24_14_day_plan.svg",
        "Урок 24",
        "Личный план внедрения на 14 дней",
        "Не трансформация ради презентации, а короткий и реалистичный цикл практики на 2-3 сценариях.",
        "table",
        "FW-L24-CASE-A",
        {
            "headers": ["Период", "Фокус", "Артефакт", "Что измеряем"],
            "widths": [180, 420, 380, 440],
            "rows": [
                ["Дни 1-3", "Baseline и первый шаблон follow-up", "baseline + prompt v1 + template 1", "стало ли быстрее начать"],
                ["Дни 4-6", "Summary документа и проверка ошибок", "summary v1 + checklist notes + template 2", "где AI ошибается и где экономит время"],
                ["Дни 7-8", "Черновики внутренних сообщений", "draft v1 + final version", "сколько ручных правок остается"],
                ["Дни 9-10", "Повторяем лучший сценарий", "repeat result", "проверка повторяемости пользы"],
                ["Дни 11-12", "Mini-library и self-report", "3 шаблона + short report", "что хочется сохранить дальше"],
                ["Дни 13-14", "Go / no-go и personal rollout note", "решение о внедрении", "есть ли дисциплина, а не хаос"],
            ],
        },
    ),
    Slide(
        "l24_b2b_rollout_metrics.svg",
        "Урок 24",
        "B2B mini-rollout и три метрики",
        "Этот экран нужен для разговора с ЛПР: что именно показывать через 14 дней, чтобы обучение не осталось ощущением.",
        "metrics",
        "FW-L24-CASE-B",
        {
            "artifact": {
                "title": "Mini-rollout artifact",
                "body": "Команда из 5 аккаунт-менеджеров берет один общий сценарий: follow-up после клиентских созвонов. Owner — team lead. Через 14 дней команда приносит 1 общий шаблон, 3 реальных примера писем и короткий отчет по применению.",
            },
            "metrics": [
                {"title": "Метрика 1", "body": "доля follow-up писем, отправленных в течение 30 минут после встречи"},
                {"title": "Метрика 2", "body": "среднее время на подготовку первого черновика"},
                {"title": "Метрика 3", "body": "число писем, где команда использовала общий шаблон"},
            ],
        },
    ),
    Slide(
        "l24_final_card.svg",
        "Урок 24",
        "Финальное действие после Core",
        "Закрывающий экран всего Core module.",
        "card",
        "FW-L24-CASE-A / FW-L24-CASE-B",
        {
            "kicker": "После Core module",
            "body": "Заполните личный 14-дневный план и выберите 2-3 сценария для следующего цикла.",
            "accent": SAGE,
        },
    ),
]


def slide_svg(slide: Slide) -> str:
    if slide.kind == "form":
        body = render_form(slide)
    elif slide.kind == "compare":
        body = render_compare(slide)
    elif slide.kind == "split":
        body = render_split(slide)
    elif slide.kind == "grid":
        body = render_grid(slide)
    elif slide.kind == "table":
        body = render_table(slide)
    elif slide.kind == "metrics":
        body = render_metrics(slide)
    elif slide.kind == "card":
        body = render_card(slide)
    else:
        raise ValueError(slide.kind)
    return svg_wrap(body)


def build_outline() -> str:
    sections = {
        "Сессия 0": ["s00_diagnostic_form.svg", "s00_first_win_compare.svg"],
        "Урок 1": ["l01_two_extremes.svg", "l01_ai_vs_human.svg"],
        "Урок 5": ["l05_prompt_compare.svg", "l05_prompt_formula.svg"],
        "Урок 11": ["l11_false_confidence_summary.svg", "l11_error_breakdown.svg"],
        "Урок 16": ["l16_four_anchors.svg", "l16_message_workflow.svg"],
        "Урок 24": ["l24_14_day_plan.svg", "l24_b2b_rollout_metrics.svg"],
    }
    lines = [
        "# First Wave Slides Outline",
        "",
        "Дата: 20 марта 2026",
        "Статус: outline реального visual deck для первой волны записи",
        "",
        "## Порядок использования",
        "",
        "1. Сначала открыть SVG-asset по нужной единице.",
        "2. Потом свериться с `first_wave_slide_copy.md` для точной формулировки в кадре.",
        "3. При необходимости использовать `first_wave_diagrams.md` как источник process-схем.",
        "",
    ]
    for unit, files in sections.items():
        lines.append(f"## {unit}")
        lines.append("")
        for name in files:
            slide = next(s for s in slides if s.filename == name)
            lines.append(f"- `{name}`")
            lines.append(f"  Назначение: {slide.subtitle}")
            lines.append(f"  Source case ID: `{slide.case_id}`")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_copy() -> str:
    lines = [
        "# First Wave Slide Copy",
        "",
        "Дата: 20 марта 2026",
        "Статус: copy deck для первой волны",
        "",
    ]
    for slide in slides:
        lines.extend([
            f"## {slide.filename}",
            "",
            f"Единица: {slide.unit}",
            f"Case ID: `{slide.case_id}`",
            f"Заголовок: {slide.title}",
            f"Подзаголовок: {slide.subtitle}",
            "",
        ])
        if slide.kind == "compare":
            for col in slide.payload["columns"]:
                lines.append(f"- {col['title']}: {col['body']}")
            lines.append("")
        elif slide.kind == "split":
            lines.append(f"- {slide.payload['left']['title']}: {slide.payload['left']['body']}")
            lines.append(f"- {slide.payload['right']['title']}: {slide.payload['right']['body']}")
            lines.append(f"- Нижняя линия: {slide.payload['bottom']}")
            lines.append("")
        elif slide.kind == "grid":
            for card in slide.payload["cards"]:
                lines.append(f"- {card['title']}: {card['body']}")
            lines.append("")
        elif slide.kind == "table":
            lines.append(f"- Таблица: {' | '.join(slide.payload['headers'])}")
            for row in slide.payload["rows"]:
                lines.append(f"  - {' | '.join(row)}")
            lines.append("")
        elif slide.kind == "metrics":
            lines.append(f"- Артефакт: {slide.payload['artifact']['body']}")
            for metric in slide.payload["metrics"]:
                lines.append(f"- {metric['title']}: {metric['body']}")
            lines.append("")
        elif slide.kind == "form":
            lines.append(f"- {slide.payload['left']['title']}: {'; '.join(slide.payload['left']['bullets'])}")
            lines.append(f"- {slide.payload['right']['title']}: {'; '.join(slide.payload['right']['bullets'])}")
            lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_diagrams() -> str:
    diagrams = {
        "Сессия 0": """```mermaid
flowchart LR
    A["Baseline без AI"] --> B["Guided prompt"]
    B --> C["AI-черновик"]
    C --> D["Ручная доработка"]
    D --> E["First win + compare"]
```""",
        "Урок 1": """```mermaid
flowchart TD
    A["Крайность: AI все сделает"] --> C["Рабочая рамка"]
    B["Крайность: AI бесполезен"] --> C["Рабочая рамка"]
    C --> D["AI = черновик, структура, ускорение"]
    C --> E["Человек = проверка, контекст, решение"]
```""",
        "Урок 5": """```mermaid
flowchart LR
    A["Слабый запрос"] --> B["Слабый ответ"]
    C["Цель + контекст + формат + критерий"] --> D["Более сильный черновик"]
    D --> E["Ручная проверка"]
```""",
        "Урок 11": """```mermaid
flowchart TD
    A["Исходные заметки"] --> B["AI-summary"]
    B --> C["Сдвиг факта"]
    B --> D["Лишний вывод"]
    B --> E["Потеря контекста"]
    C --> F["Проверка человеком"]
    D --> F
    E --> F
```""",
        "Урок 16": """```mermaid
flowchart LR
    A["Кому пишем"] --> E["Промпт / исходник"]
    B["Зачем пишем"] --> E
    C["Какое действие ждем"] --> E
    D["Какой тон допустим"] --> E
    E --> F["AI-черновик"]
    F --> G["Ручная редактура"]
```""",
        "Урок 24": """```mermaid
flowchart LR
    A["Выбрать 2-3 сценария"] --> B["Протестировать шаблоны"]
    B --> C["Измерить эффект"]
    C --> D["Закрепить рабочее"]
    D --> E["Следующий цикл внедрения"]
```""",
    }
    lines = [
        "# First Wave Diagrams",
        "",
        "Дата: 20 марта 2026",
        "Статус: мермайд-схемы для первой волны",
        "",
        "Эти схемы можно использовать как:",
        "- основу для SVG-перерисовки;",
        "- быстрый visual appendix к уроку;",
        "- источник для отдельных process-slides.",
        "",
    ]
    for unit, body in diagrams.items():
        lines.append(f"## {unit}")
        lines.append("")
        lines.append(body)
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_readme() -> str:
    lines = [
        "# First Wave Visual Assets",
        "",
        "Дата: 20 марта 2026",
        "Статус: рабочий пакет визуальных материалов для первой волны записи",
        "",
        "## Что внутри",
        "",
        "- `first_wave_slides_outline.md` — карта deck по 6 единицам.",
        "- `first_wave_slide_copy.md` — точный текст и смысл каждого слайда.",
        "- `first_wave_diagrams.md` — Mermaid-схемы по 6 единицам.",
        "- SVG-файлы — реальные slide assets для записи и rough cut.",
        "",
        "## Порядок работы",
        "",
        "1. Открыть `first_wave_slides_outline.md`.",
        "2. Перейти к нужному SVG-asset.",
        "3. При записи сверять подачу с `first_wave_slide_copy.md`.",
        "4. Для process-diagrams брать схемы из `first_wave_diagrams.md`.",
        "",
        "## Карта SVG-файлов",
        "",
    ]
    for slide in slides:
        lines.append(f"- `{slide.filename}` — {slide.unit}: {slide.title}")
    lines.append("")
    lines.append("## Примечание")
    lines.append("")
    lines.append("Все материалы собраны на базе уже утвержденных case IDs и не переписывают архитектуру курса.")
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "first_wave_slides_outline.md").write_text(build_outline(), encoding="utf-8")
    (OUT / "first_wave_slide_copy.md").write_text(build_copy(), encoding="utf-8")
    (OUT / "first_wave_diagrams.md").write_text(build_diagrams(), encoding="utf-8")
    (OUT / "README.md").write_text(build_readme(), encoding="utf-8")
    for slide in slides:
        (OUT / slide.filename).write_text(slide_svg(slide), encoding="utf-8")


if __name__ == "__main__":
    main()
