import json
import os
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from openai import OpenAI

from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, Image,
    BaseDocTemplate, Frame, PageTemplate, HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas

# ========================
# ENV + OPENAI
# ========================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ========================
# DESIGN TOKENS
# ========================
PRIMARY        = colors.HexColor("#1B5E20")   # deep green
PRIMARY_LIGHT  = colors.HexColor("#4CAF50")   # mid green
ACCENT         = colors.HexColor("#8BC34A")   # lime
DANGER         = colors.HexColor("#C62828")   # deep red
DANGER_LIGHT   = colors.HexColor("#FFCDD2")   # blush red bg
SUCCESS_LIGHT  = colors.HexColor("#E8F5E9")   # mint bg
TIP_BG         = colors.HexColor("#EDE7F6")   # lavender bg
TIP_TEXT       = colors.HexColor("#4527A0")   # deep purple
NEUTRAL_DARK   = colors.HexColor("#263238")   # charcoal
NEUTRAL_MID    = colors.HexColor("#546E7A")   # slate
NEUTRAL_LIGHT  = colors.HexColor("#ECEFF1")   # off-white
WHITE          = colors.white

PAGE_W, PAGE_H = A4
HEADER_H = 22 * mm
FOOTER_H = 14 * mm
MARGIN   = 18 * mm

CHART_PALETTE = ["#1B5E20", "#388E3C", "#66BB6A", "#A5D6A7",
                 "#C8E6C9", "#8BC34A"]

# ========================
# PAGE DECORATOR (header + footer)
# ========================
# ========================
# PAGE DECORATOR (HEADER ONLY — FOOTER REMOVED)
# ========================
def make_page_decorator(disease: str):
    def decorator(canv: rl_canvas.Canvas, doc):
        canv.saveState()
        w, h = PAGE_W, PAGE_H

        # Header band
        canv.setFillColor(PRIMARY)
        canv.rect(0, h - HEADER_H, w, HEADER_H, fill=1, stroke=0)

        # Accent stripe under header
        canv.setFillColor(ACCENT)
        canv.rect(0, h - HEADER_H - 3, w, 3, fill=1, stroke=0)

        canv.setFont("Helvetica-Bold", 13)
        canv.setFillColor(WHITE)
        canv.drawString(MARGIN, h - HEADER_H + 7 * mm,
                        f"Diet Plan Report  —  {disease.title()}")

        canv.setFont("Helvetica", 9)
        canv.setFillColor(colors.HexColor("#A5D6A7"))
        date_str = datetime.now().strftime("%B %d, %Y")
        canv.drawRightString(w - MARGIN, h - HEADER_H + 7 * mm, date_str)

        canv.restoreState()

    return decorator


# ========================
# CUSTOM PARAGRAPH STYLES
# ========================
def build_styles():
    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        "section_title": S("section_title",
            fontName="Helvetica-Bold", fontSize=11,
            textColor=WHITE, backColor=PRIMARY,
            spaceBefore=14, spaceAfter=6,
            borderPadding=(5, 8, 5, 8)),

        "body": S("body",
            fontName="Helvetica", fontSize=9.5,
            textColor=NEUTRAL_DARK, leading=14,
            spaceBefore=2, spaceAfter=2),

        "eat_item": S("eat_item",
            fontName="Helvetica", fontSize=9.5,
            textColor=colors.HexColor("#1B5E20"),
            backColor=SUCCESS_LIGHT,
            leading=14, spaceBefore=2, spaceAfter=2,
            leftIndent=6, borderPadding=(3, 6, 3, 6)),

        "avoid_item": S("avoid_item",
            fontName="Helvetica", fontSize=9.5,
            textColor=DANGER, backColor=DANGER_LIGHT,
            leading=14, spaceBefore=2, spaceAfter=2,
            leftIndent=6, borderPadding=(3, 6, 3, 6)),

        "tip_item": S("tip_item",
            fontName="Helvetica-Oblique", fontSize=9.5,
            textColor=TIP_TEXT, backColor=TIP_BG,
            leading=14, spaceBefore=2, spaceAfter=2,
            leftIndent=6, borderPadding=(3, 6, 3, 6)),

        "caption": S("caption",
            fontName="Helvetica-Oblique", fontSize=8,
            textColor=NEUTRAL_MID, alignment=TA_CENTER,
            spaceBefore=2, spaceAfter=6),

        "footer_note": S("footer_note",
            fontName="Helvetica-Oblique", fontSize=7.5,
            textColor=NEUTRAL_MID, alignment=TA_CENTER,
            spaceBefore=4),
    }


def section_header(title: str, styles: dict):
    return Paragraph(f"&nbsp; {title}", styles["section_title"])


# ========================
# HEALTH SCORE CARD
# ========================
def health_score_card(score: int):
    if score > 80:
        bar_color = colors.HexColor("#43A047")
        label = "Excellent"
    elif score > 60:
        bar_color = colors.HexColor("#FB8C00")
        label = "Good"
    else:
        bar_color = colors.HexColor("#E53935")
        label = "Needs Improvement"

    hex_color = bar_color.hexval()

    score_p = Paragraph(
        f'<font size="26" color="{hex_color}"><b>{score}</b></font>'
        f'<font size="11" color="#546E7A">/100</font>',
        ParagraphStyle("sc", alignment=TA_CENTER, leading=32)
    )
    label_p = Paragraph(
        f'<font color="{hex_color}"><b>{label}</b></font>',
        ParagraphStyle("sl", alignment=TA_CENTER, fontSize=10)
    )
    desc_p = Paragraph(
        "Based on food variety, avoidance of harmful items, and nutrient coverage.",
        ParagraphStyle("sd", alignment=TA_CENTER, fontSize=8,
                       textColor=NEUTRAL_MID)
    )

    tbl = Table(
        [[score_p], [label_p], [desc_p]],
        colWidths=[PAGE_W - 2 * MARGIN]
    )
    tbl.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 1.2, bar_color),
        ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#F9FBE7")),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return tbl


# ========================
# PIE CHART
# ========================
def generate_pie_chart(nutrition: dict):
    try:
        values = [
            int(nutrition["protein"].split()[0]),
            int(nutrition["carbs"].split()[0]),
            int(nutrition["fat"].split()[0]),
        ]
        labels = ["Protein", "Carbs", "Fat"]
        palette = [CHART_PALETTE[0], CHART_PALETTE[2], CHART_PALETTE[3]]

        fig, ax = plt.subplots(figsize=(4.2, 3.5),
                               facecolor="#F9FBE7")
        ax.set_facecolor("#F9FBE7")

        wedges, texts, autotexts = ax.pie(
            values, labels=labels, autopct="%1.1f%%",
            colors=palette, startangle=140,
            wedgeprops=dict(width=0.65, edgecolor="white", linewidth=1.5),
            pctdistance=0.75,
        )
        for t in texts:
            t.set_fontsize(9); t.set_color("#263238")
        for at in autotexts:
            at.set_fontsize(8); at.set_color("white"); at.set_fontweight("bold")

        ax.set_title("Macro Distribution", fontsize=11,
                     fontweight="bold", color="#1B5E20", pad=10)
        fig.tight_layout()

        path = "outputs/pie_chart.png"
        fig.savefig(path, dpi=150, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        plt.close(fig)
        return path
    except Exception as e:
        print(f"Pie chart error: {e}")
        return None


# ========================
# BAR CHART (real meal_split data)
# ========================
def generate_bar_chart(nutrition: dict):
    try:
        meal_split = nutrition.get("meal_split", {})
        if not meal_split:
            return None

        labels = [k.title() for k in meal_split.keys()]
        values = list(meal_split.values())
        palette = (CHART_PALETTE * 4)[: len(labels)]

        fig, ax = plt.subplots(figsize=(5, 3.2), facecolor="#F9FBE7")
        ax.set_facecolor("#F9FBE7")

        bars = ax.bar(labels, values, color=palette,
                      edgecolor="white", linewidth=1.2, width=0.52, zorder=3)
        ax.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel("Calories (kcal)", fontsize=8.5, color="#546E7A")
        ax.set_title("Estimated Calories per Meal", fontsize=11,
                     fontweight="bold", color="#1B5E20", pad=10)
        ax.tick_params(colors="#546E7A", labelsize=8.5)

        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(values) * 0.02,
                    str(val), ha="center", va="bottom",
                    fontsize=8, fontweight="bold", color="#1B5E20")
        ax.set_ylim(0, max(values) * 1.25)
        fig.tight_layout()

        path = "outputs/bar_chart.png"
        fig.savefig(path, dpi=150, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        plt.close(fig)
        return path
    except Exception as e:
        print(f"Bar chart error: {e}")
        return None


# ========================
# HEALTH SCORE LOGIC
# ========================
def calculate_health_score(diet: dict, nutrition: dict) -> int:
    score = 70
    if len(diet.get("eat", [])) > 5:
        score += 10
    if len(diet.get("avoid", [])) > 2:
        score += 10
    if "protein" in nutrition:
        score += 10
    return min(score, 100)


# ========================
# OPENAI EXPLANATION
# ========================
FOOD_ICONS = {
    "spinach": "🥬", "oats": "🌾", "fish": "🐟", "banana": "🍌",
    "broccoli": "🥦", "lentils": "🫘", "egg": "🥚", "rice": "🍚",
    "chicken": "🍗", "milk": "🥛", "apple": "🍎", "carrot": "🥕",
}

def get_icon(food: str) -> str:
    for k, v in FOOD_ICONS.items():
        if k in food.lower():
            return v
    return "🥗"

def explain_food(food: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You are a nutrition expert. Give exactly 1 concise sentence (max 12 words)."},
                {"role": "user",
                 "content": f"Why is {food} beneficial for health?"}
            ],
            max_tokens=40,
            timeout=5,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Provides essential vitamins and minerals."


# ========================
# MAIN: SAVE FILES
# ========================
def save_files(data: dict):
    os.makedirs("outputs", exist_ok=True)

    ts = datetime.now().strftime("%H%M%S")
    json_path = f"outputs/diet_{ts}.json"
    pdf_path  = f"outputs/diet_{ts}.pdf"

    # JSON
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

    # PDF setup
    styles  = build_styles()
    disease = data["disease"]

    doc = BaseDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=HEADER_H + 8 * mm,
        bottomMargin=FOOTER_H + 8 * mm,
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        PAGE_W - 2 * MARGIN,
        PAGE_H - HEADER_H - FOOTER_H - 16 * mm,
        id="main",
    )
    doc.addPageTemplates([
        PageTemplate(id="main", frames=[frame],
                     onPage=make_page_decorator(disease))
    ])

    story = []

    # ── Title ────────────────────────────────────────────────────────
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<font size="20" color="#1B5E20"><b>Personalised Diet Plan</b></font>',
        ParagraphStyle("big_title", alignment=TA_CENTER, leading=28)
    ))
    story.append(Paragraph(
        f'<font size="12" color="#546E7A">Condition: <b>{disease.title()}</b></font>',
        ParagraphStyle("subtitle", alignment=TA_CENTER, leading=18)
    ))
    story.append(HRFlowable(width="100%", thickness=1.5,
                             color=PRIMARY_LIGHT, spaceAfter=10))

    # ── Health Score ─────────────────────────────────────────────────
    story.append(section_header("Health Score", styles))
    story.append(Spacer(1, 6))
    score = calculate_health_score(data["diet"], data["nutrition"])
    story.append(health_score_card(score))
    story.append(Spacer(1, 10))

    # ── Recommended Foods ────────────────────────────────────────────
    story.append(section_header("Recommended Foods", styles))
    story.append(Spacer(1, 4))
    for food in data["diet"]["eat"]:
        icon = get_icon(food)
        note = explain_food(food)
        story.append(Paragraph(
            f'<b>{icon} {food.title()}</b>  '
            f'<font color="#546E7A">— {note}</font>',
            styles["eat_item"]
        ))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 8))

    # ── Foods to Avoid ───────────────────────────────────────────────
    story.append(section_header("Foods to Avoid", styles))
    story.append(Spacer(1, 4))
    for food in data["diet"]["avoid"]:
        story.append(Paragraph(f"&#10006;  {food.title()}", styles["avoid_item"]))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 8))

    # ── Meal Plan Table ──────────────────────────────────────────────
    story.append(section_header("Daily Meal Plan", styles))
    story.append(Spacer(1, 6))

    col_w = PAGE_W - 2 * MARGIN
    header_row = [
        Paragraph("<b>Meal</b>",
                  ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=10,
                                 textColor=WHITE, alignment=TA_CENTER)),
        Paragraph("<b>Recommended Options</b>",
                  ParagraphStyle("th2", fontName="Helvetica-Bold", fontSize=10,
                                 textColor=WHITE)),
    ]
    rows = [header_row]
    even = colors.HexColor("#F1F8E9")

    for i, (meal, opts) in enumerate(data["diet"]["meals"].items()):
        formatted = "<br/>".join(
            [f'<font color="#1B5E20">&#9679;</font>  {o}' for o in opts]
        )
        rows.append([
            Paragraph(f"<b>{meal.title()}</b>",
                      ParagraphStyle("mc", fontName="Helvetica-Bold",
                                     fontSize=9.5, alignment=TA_CENTER,
                                     textColor=PRIMARY)),
            Paragraph(formatted,
                      ParagraphStyle("mo", fontName="Helvetica",
                                     fontSize=9.5, leading=14,
                                     textColor=NEUTRAL_DARK)),
        ])

    tbl = Table(rows, colWidths=[col_w * 0.22, col_w * 0.78])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  PRIMARY),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [even, WHITE]),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#C8E6C9")),
        ("BOX",           (0, 0), (-1, -1), 1,   PRIMARY_LIGHT),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 12))

    # ── Charts ───────────────────────────────────────────────────────
    pie = generate_pie_chart(data["nutrition"])
    bar = generate_bar_chart(data["nutrition"])

    charts = [(img, cap) for img, cap in [
        (pie, "Macro Distribution"),
        (bar, "Meal Calories"),
    ] if img]

    if charts:
        story.append(section_header("Nutritional Analysis", styles))
        story.append(Spacer(1, 6))

        if len(charts) == 2:
            half = col_w / 2
            chart_tbl = Table(
                [[Image(charts[0][0], width=5.8*cm, height=4.9*cm),
                  Image(charts[1][0], width=7.0*cm, height=4.9*cm)],
                 [Paragraph(charts[0][1], styles["caption"]),
                  Paragraph(charts[1][1], styles["caption"])]],
                colWidths=[half, half]
            )
        else:
            chart_tbl = Table(
                [[Image(charts[0][0], width=8*cm, height=5.5*cm)],
                 [Paragraph(charts[0][1], styles["caption"])]],
                colWidths=[col_w]
            )

        chart_tbl.setStyle(TableStyle([
            ("ALIGN",  (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(chart_tbl)
        story.append(Spacer(1, 10))

    # ── Tips ─────────────────────────────────────────────────────────
    if data["diet"].get("tips"):
        story.append(section_header("Wellness Tips", styles))
        story.append(Spacer(1, 4))
        tip_icons = ["💧", "🕐", "🚶", "🛌", "🧘"]
        for i, tip in enumerate(data["diet"]["tips"]):
            icon = tip_icons[i % len(tip_icons)]
            story.append(Paragraph(f"{icon}  {tip}", styles["tip_item"]))
            story.append(Spacer(1, 3))
        story.append(Spacer(1, 10))

    # ── Footer note ──────────────────────────────────────────────────
    #story.append(HRFlowable(width="100%", thickness=0.8,
     #                        color=NEUTRAL_LIGHT, spaceBefore=4))
    #story.append(Paragraph(
    #    "Generated by AI Diet Planner &nbsp;|&nbsp; "
   #     "Always consult a qualified nutritionist before making dietary changes.",
    #    styles["footer_note"]
    #))

    doc.build(story)
    return json_path, pdf_path


# ========================
# DEMO
# ========================
if __name__ == "__main__":
    sample = {
        "disease": "diabetes",
        "nutrition": {
            "protein": "80 g",
            "carbs": "200 g",
            "fat": "55 g",
            "meal_split": {
                "breakfast": 350,
                "lunch": 620,
                "snack": 230,
                "dinner": 480,
            },
        },
        "diet": {
            "eat": ["spinach", "oats", "fish", "banana", "broccoli", "lentils"],
            "avoid": ["fried food", "white bread", "sugary drinks", "processed meat"],
            "meals": {
                "breakfast": ["Oats porridge with nuts", "Boiled eggs with whole wheat toast"],
                "lunch":     ["Grilled fish with brown rice", "Lentil soup with salad"],
                "snack":     ["Mixed fruit bowl", "Roasted chickpeas"],
                "dinner":    ["Steamed vegetables with tofu", "Spinach dal with roti"],
            },
            "tips": [
                "Drink 8-10 glasses of water daily",
                "Eat small meals every 3-4 hours",
                "30 minutes of walking each morning",
                "Get 7-8 hours of sleep for metabolic health",
                "Practice mindful eating and chew slowly",
            ],
        },
    }

    j, p = save_files(sample)
    print(f"JSON: {j}")
    print(f"PDF : {p}")