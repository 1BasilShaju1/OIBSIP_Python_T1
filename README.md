# 🧮 BMI Calculator

A feature-rich desktop BMI (Body Mass Index) calculator built with Python and Tkinter, featuring a polished teal-themed UI, history tracking, trend graphs, and PDF report export.

---

## ✨ Features

- **BMI Calculation** — Supports multiple weight and height units (kg, grams, lbs, oz / cm, m, feet, inches)
- **Visual Gauge** — Horizontal color-coded slider gauge showing your BMI position across categories
- **Category Classification** — Instantly shows Underweight / Normal / Overweight / Obese with color highlights
- **Personalised Health Tips** — Tailored advice based on your BMI category
- **History Tracking** — All results saved locally to a CSV file with timestamps
- **Trend Graph** — Interactive matplotlib chart showing BMI over time, filterable by name
- **PDF Report Export** — Generates a professional 2-page PDF report including measurements, classification table, health tips, and a BMI trend chart

---

## 📋 Requirements

- Python 3.8+
- [tkinter](https://docs.python.org/3/library/tkinter.html) *(included with standard Python on most platforms)*
- [matplotlib](https://matplotlib.org/)
- [reportlab](https://www.reportlab.com/)

---

## 🚀 Getting Started

1. **Clone or download** this repository.
2. **Install dependencies** (see above).
3. **Run the app:**


The application opens maximized and is ready to use.

---

## 🖥️ How to Use

### Calculator Tab
1. Enter your **Name**, **Height**, and **Weight**.
2. Select your preferred **units** from the dropdowns (or toggle Metric / Imperial).
3. Optionally enter your **Age** (displayed for reference).
4. Click **Calculate BMI** — your result, category, and gauge appear instantly.
5. Click **Reset** to clear all fields back to defaults.

### Export PDF
- After calculating, click **📄 Export PDF Report**.
- Choose a save location — the report is auto-named with your name and today's date.
- The PDF includes your measurements, BMI classification table, health tips, and a trend chart (if you have 2+ history entries).

### History Tab
- Automatically populated after each calculation.
- Rows are colour-coded by BMI category.
- Use **🗑 Clear All** to wipe the history (this is permanent).

### Trend Graph Tab
- Displays a line chart of your BMI over time.
- Use the **Filter by name** dropdown to view a specific user's trend.

---

## 📁 File Structure

```
bmi_calculator.py   # Main application fi
bmi_history.csv     # Auto-created history file (generated on first use)
```

> The `bmi_history.csv` file is created automatically in the same directory as the script when you first calculate a BMI.

---


## 📊 BMI Classification

| Category | BMI Range | Status |
|---|---|---|
| Underweight | < 18.5 | Below healthy range |
| Normal | 18.5 – 24.9 | Healthy range ✓ |
| Overweight | 25.0 – 29.9 | Above healthy range |
| Obese | ≥ 30.0 | High health risk |

---

## ⚠️ Disclaimer

This application is for **informational purposes only**. BMI is a general health indicator and does not account for muscle mass, age, gender, or ethnicity. Always consult a qualified healthcare professional before making any health decisions.

---

## 🛠️ Built With

- [Python](https://www.python.org/) — Core language
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — GUI framework
- [Matplotlib](https://matplotlib.org/) — Trend graphs and chart export
- [ReportLab](https://www.reportlab.com/) — PDF generation
