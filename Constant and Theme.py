

# ── Color Palette ─────────────────────────────────────────────────────────────
TEAL        = "#00BFA5"
TEAL_DARK   = "#00897B"
TEAL_LIGHT  = "#B2DFDB"
BG_OUTER    = "#DDE8E4"
BG_CARD     = "#EAF4F1"
BG_RESULT   = "#F5FAF9"
WHITE       = "#FFFFFF"
TEXT_DARK   = "#1A1A2E"
TEXT_GREY   = "#6B7280"

# ── Category Colors ───────────────────────────────────────────────────────────
CATEGORY_COLORS = {
    "Underweight": "#5C85D6",
    "Normal":      TEAL,
    "Overweight":  "#F59E0B",
    "Obese":       "#EF4444",
}

# ── File Paths ────────────────────────────────────────────────────────────────
HISTORY_FILE = "bmi_history.csv"

# ── Health Tips ───────────────────────────────────────────────────────────────
HEALTH_TIPS = {
    "Underweight": [
        "Eat calorie-dense nutritious foods like nuts, avocado, and whole grains.",
        "Add strength training to build healthy muscle mass.",
        "Eat 5-6 smaller meals throughout the day instead of 3 large ones.",
        "Consult a doctor or dietitian to rule out underlying conditions.",
        "Track your daily caloric intake to ensure you meet your needs.",
    ],
    "Normal": [
        "Maintain your healthy weight with balanced meals and regular exercise.",
        "Aim for at least 150 minutes of moderate activity per week.",
        "Stay hydrated — drink at least 8 glasses of water daily.",
        "Keep monitoring your BMI every 3-6 months.",
        "Prioritize sleep — 7-9 hours supports healthy weight maintenance.",
    ],
    "Overweight": [
        "Reduce processed and sugary foods from your daily diet.",
        "Aim for a 500 calorie daily deficit for safe, steady weight loss.",
        "Walk at least 30 minutes every day — even light activity helps.",
        "Replace sugary drinks with water, herbal teas, or black coffee.",
        "Consider speaking with a nutritionist for a personalized plan.",
    ],
    "Obese": [
        "Speak with your doctor before starting any new exercise program.",
        "Start with low-impact activities like walking or swimming.",
        "Focus on whole foods: vegetables, lean proteins, and complex carbs.",
        "Monitor blood pressure, cholesterol, and blood sugar regularly.",
        "Set small, achievable weekly goals rather than large targets.",
    ],
}

import tkinter as tk


_SEGMENT_COLORS = [
    "#5C85D6", "#4ABFB0", "#00BFA5",
    "#66BB6A", "#FFA726", "#EF6C00", "#E53935",
]

_CATEGORY_LABELS = [
    ("Underweight", 0.10),
    ("Normal",      0.38),
    ("Overweight",  0.63),
    ("Obese",       0.88),
]


def draw_slider_gauge(canvas: tk.Canvas, bmi: float) -> None:
    """Redraw the full gauge for *bmi* on *canvas*."""
    canvas.delete("all")
    cw = canvas.winfo_width()  or 400
    ch = canvas.winfo_height() or 80

    bar_x1, bar_x2 = 20, cw - 20
    bar_y1 = ch // 2 - 8
    bar_y2 = ch // 2 + 8
    bar_w  = bar_x2 - bar_x1

    # Colored segments
    seg_w = bar_w / len(_SEGMENT_COLORS)
    for i, color in enumerate(_SEGMENT_COLORS):
        canvas.create_rectangle(
            bar_x1 + i * seg_w, bar_y1,
            bar_x1 + (i + 1) * seg_w, bar_y2,
            fill=color, outline="",
        )

    # Rounded end caps
    r = (bar_y2 - bar_y1) // 2
    canvas.create_oval(bar_x1 - r, bar_y1, bar_x1 + r, bar_y2,
                       fill=_SEGMENT_COLORS[0], outline="")
    canvas.create_oval(bar_x2 - r, bar_y1, bar_x2 + r, bar_y2,
                       fill=_SEGMENT_COLORS[-1], outline="")

    # Labels above & below bar
    for label, frac in _CATEGORY_LABELS:
        x = bar_x1 + bar_w * frac
        canvas.create_text(x, bar_y1 - 14, text=label,
                           font=("Segoe UI", 8), fill="#6B7280", anchor="center")
        canvas.create_text(x, bar_y2 + 14, text=label,
                           font=("Segoe UI", 8), fill="#6B7280", anchor="center")

    # Indicator dot (BMI range 10–40)
    bmi_clamped = max(10.0, min(40.0, bmi))
    fraction    = (bmi_clamped - 10) / 30
    dot_x       = bar_x1 + fraction * bar_w
    dot_y       = ch // 2

    canvas.create_oval(dot_x - 12, dot_y - 12, dot_x + 12, dot_y + 12,
                       fill="#E0E0E0", outline="")
    canvas.create_oval(dot_x - 10, dot_y - 10, dot_x + 10, dot_y + 10,
                       fill="white", outline="#CCCCCC", width=1)
