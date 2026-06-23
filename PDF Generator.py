import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Table, TableStyle, HRFlowable, Image, PageBreak)

from core.constants import TEAL, CATEGORY_COLORS, HEALTH_TIPS, BG_RESULT

_TEMP_CHART = "_bmi_chart_temp.png"


def _make_style(name, **kwargs) -> ParagraphStyle:
    return ParagraphStyle(name, **kwargs)


def generate_pdf(name: str, bmi: float, category: str, color_hex: str,
                 weight_val: float, weight_unit: str,
                 height_val: float, height_unit: str,
                 history_rows: list[dict], save_path: str) -> None:

    doc = SimpleDocTemplate(save_path, pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)

    teal_c  = colors.HexColor(TEAL)
    accent  = colors.HexColor(CATEGORY_COLORS.get(category, TEAL))

    # ── Styles ────────────────────────────────────────────────
    title_s = _make_style("T",  fontSize=26, fontName="Helvetica-Bold",
                           textColor=colors.white, alignment=TA_CENTER, spaceAfter=4)
    sub_s   = _make_style("S",  fontSize=11, fontName="Helvetica",
                           textColor=colors.HexColor("#E0F7F4"), alignment=TA_CENTER)
    sec_s   = _make_style("H",  fontSize=13, fontName="Helvetica-Bold",
                           textColor=colors.HexColor("#111827"),
                           spaceBefore=14, spaceAfter=6)
    body_s  = _make_style("B",  fontSize=10, fontName="Helvetica",
                           textColor=colors.HexColor("#374151"),
                           spaceAfter=4, leading=15)
    tip_s   = _make_style("Tip", fontSize=10, fontName="Helvetica",
                           textColor=colors.HexColor("#374151"),
                           leftIndent=10, spaceAfter=5, leading=14)
    meta_s  = _make_style("M",  fontSize=9, fontName="Helvetica",
                           textColor=colors.HexColor("#6B7280"), alignment=TA_CENTER)

    story = []

    # ── Page 1

    # Header banner
    hdr = Table([[Paragraph("BMI HEALTH REPORT", title_s)],
                 [Paragraph("Body Mass Index Assessment", sub_s)]],
                colWidths=[170*mm])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), teal_c),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    story += [hdr, Spacer(1, 5*mm)]

    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y  %I:%M %p')}  |  "
        f"Prepared for: <b>{name}</b>", meta_s))
    story += [Spacer(1, 4*mm),
              HRFlowable(width="100%", thickness=1,
                         color=colors.HexColor("#E5E7EB")),
              Spacer(1, 4*mm)]

    # BMI result card
    bmi_card = Table([
        [Paragraph("YOUR BMI RESULT",
                   _make_style("CH", fontSize=11, fontName="Helvetica-Bold",
                               textColor=colors.white, alignment=TA_CENTER))],
        [Paragraph(str(bmi),
                   _make_style("BN", fontSize=52, fontName="Helvetica-Bold",
                               textColor=colors.white, alignment=TA_CENTER, leading=58))],
        [Paragraph(category,
                   _make_style("CL", fontSize=16, fontName="Helvetica-Bold",
                               textColor=colors.white, alignment=TA_CENTER))],
    ], colWidths=[170*mm])
    bmi_card.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), accent),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story += [bmi_card, Spacer(1, 5*mm)]

    # Measurements table
    story.append(Paragraph("Your Measurements", sec_s))
    mdata = [
        ["Field",    "Value",                              "Unit"],
        ["Name",     name,                                 "—"],
        ["Weight",   str(weight_val),                      weight_unit],
        ["Height",   str(height_val),                      height_unit],
        ["BMI",      str(bmi),                             "kg/m²"],
        ["Category", category,                             "—"],
        ["Date",     datetime.now().strftime("%Y-%m-%d"),  "—"],
    ]
    mt = Table(mdata, colWidths=[50*mm, 70*mm, 50*mm])
    mt.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  teal_c),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 10),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("TEXTCOLOR",     (0, 1), (-1, -1), colors.HexColor("#374151")),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F0FDF4")]),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("BACKGROUND",    (0, 4), (-1, 4),  accent),
        ("TEXTCOLOR",     (0, 4), (-1, 4),  colors.white),
        ("FONTNAME",      (0, 4), (-1, 4),  "Helvetica-Bold"),
    ]))
    story += [mt, Spacer(1, 5*mm)]

    # Classification table
    story.append(Paragraph("BMI Classification", sec_s))
    cdata = [
        ["Category",    "BMI Range",    "Status"],
        ["Underweight", "< 18.5",       "Below healthy range"],
        ["Normal",      "18.5 – 24.9",  "Healthy range ✓"],
        ["Overweight",  "25.0 – 29.9",  "Above healthy range"],
        ["Obese",       "≥ 30.0",       "High health risk"],
    ]
    cbg = {
        "Underweight": colors.HexColor("#DBEAFE"),
        "Normal":      colors.HexColor("#DCFCE7"),
        "Overweight":  colors.HexColor("#FEF3C7"),
        "Obese":       colors.HexColor("#FEE2E2"),
    }
    ct_style = [
        ("BACKGROUND",    (0, 0), (-1, 0),  teal_c),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 10),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("TEXTCOLOR",     (0, 1), (-1, -1), colors.HexColor("#374151")),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ]
    for i, row in enumerate(cdata[1:], 1):
        ct_style.append(("BACKGROUND", (0, i), (-1, i), cbg.get(row[0], colors.white)))
        if row[0] == category:
            ct_style.append(("FONTNAME", (0, i), (-1, i), "Helvetica-Bold"))
    ct = Table(cdata, colWidths=[55*mm, 55*mm, 60*mm])
    ct.setStyle(TableStyle(ct_style))
    story.append(ct)

    # ── Page 2: Tips + Chart ──────────────────────────────────
    story.append(PageBreak())

    story.append(Paragraph("Personalised Health Tips", sec_s))
    story.append(Paragraph(f"Based on your <b>{category}</b> BMI:", body_s))
    story.append(Spacer(1, 3*mm))
    for i, tip in enumerate(HEALTH_TIPS.get(category, []), 1):
        story.append(Paragraph(f"{i}.  {tip}", tip_s))

    story += [Spacer(1, 5*mm),
              HRFlowable(width="100%", thickness=1,
                         color=colors.HexColor("#E5E7EB")),
              Spacer(1, 5*mm)]

    # BMI Trend chart
    story.append(Paragraph("Your BMI Trend", sec_s))
    user_rows = [r for r in history_rows if r["Name"] == name]

    if len(user_rows) >= 2:
        dates = [datetime.strptime(r["Date"], "%Y-%m-%d %H:%M") for r in user_rows]
        bmis  = [float(r["BMI"]) for r in user_rows]
        fig, ax = plt.subplots(figsize=(7, 3), dpi=120)
        fig.patch.set_facecolor(BG_RESULT)
        ax.set_facecolor(BG_RESULT)
        ax.plot(dates, bmis, color=TEAL, linewidth=2.5, marker="o", markersize=7,
                markerfacecolor="white", markeredgecolor=TEAL,
                markeredgewidth=2, zorder=3)
        ax.axhspan(0,    18.5, alpha=0.08, color="#5C85D6")
        ax.axhspan(18.5, 25.0, alpha=0.08, color=TEAL)
        ax.axhspan(25.0, 30.0, alpha=0.08, color="#F59E0B")
        ax.axhspan(30.0, 50.0, alpha=0.08, color="#EF4444")
        for y, c in [(18.5, "#5C85D6"), (25.0, TEAL), (30.0, "#EF4444")]:
            ax.axhline(y=y, color=c, linewidth=1, linestyle="--", alpha=0.5)
        for d, b in zip(dates, bmis):
            ax.annotate(str(b), xy=(d, b), xytext=(0, 10),
                        textcoords="offset points", ha="center",
                        fontsize=8, color=TEAL, fontweight="bold")
        ax.set_title(f"BMI History — {name}", fontsize=11,
                     fontweight="bold", color="#111827")
        ax.set_ylabel("BMI", fontsize=9, color="#6B7280")
        ax.tick_params(colors="#6B7280", labelsize=8)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.set_ylim(max(0, min(bmis) - 4), max(bmis) + 4)
        fig.autofmt_xdate(rotation=25)
        fig.tight_layout()
        fig.savefig(_TEMP_CHART, dpi=120, bbox_inches="tight",
                    facecolor=BG_RESULT)
        plt.close(fig)
        story.append(Image(_TEMP_CHART, width=160*mm, height=65*mm))
        story.append(Spacer(1, 3*mm))
    else:
        story.append(Paragraph(
            "Not enough history to show trend. "
            "Calculate BMI multiple times to track your progress.", body_s))

    story += [Spacer(1, 6*mm),
              HRFlowable(width="100%", thickness=1,
                         color=colors.HexColor("#E5E7EB")),
              Spacer(1, 4*mm)]

    # Disclaimer
    story.append(Paragraph(
        "Disclaimer: This report is for informational purposes only. BMI is a general "
        "health indicator and does not account for muscle mass, age, gender, or ethnicity. "
        "Always consult a qualified healthcare professional before making any health decisions.",
        _make_style("Disc", fontSize=7.5, fontName="Helvetica",
                    textColor=colors.HexColor("#9CA3AF"),
                    alignment=TA_CENTER, leading=11)))

    doc.build(story)

    if os.path.isfile(_TEMP_CHART):
        os.remove(_TEMP_CHART)
