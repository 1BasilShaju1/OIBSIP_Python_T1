

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from core.constants import (TEAL, TEAL_DARK, BG_CARD, BG_RESULT,
                             BG_OUTER, WHITE, TEXT_DARK, TEXT_GREY,
                             CATEGORY_COLORS)
from core.bmi import (convert_weight_to_kg, convert_height_to_meters,
                      calculate_bmi, get_category, validate_inputs)
from ui.gauge import draw_slider_gauge
from utils.history import save_result, load_history
from utils.pdf_report import generate_pdf

import os


class CalculatorTab(tk.Frame):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=BG_OUTER, **kwargs)

        self.weight_unit_var = tk.StringVar(value="kg")
        self.height_unit_var = tk.StringVar(value="cm")
        self.mode            = tk.StringVar(value="Metric")

        # Last computed result (needed for PDF export)
        self._last: dict | None = None

        self._build()

    # ── Layout ────────────────────────────────────────────────

    def _build(self):
        card = tk.Frame(self, bg=BG_CARD)
        card.place(relx=0.5, rely=0.5, anchor="center",
                   relwidth=0.88, relheight=0.92)

        left  = tk.Frame(card, bg=BG_CARD,   padx=40, pady=36)
        right = tk.Frame(card, bg=BG_RESULT,  padx=36, pady=36)
        left.place( relx=0,   rely=0, relwidth=0.48, relheight=1.0)
        right.place(relx=0.5, rely=0, relwidth=0.50, relheight=1.0)

        self._build_left(left)
        self._build_right(right)

    # ── Left panel (inputs) ───────────────────────────────────

    def _build_left(self, p):
        tk.Label(p, text="BMI Calculator",
                 font=("Segoe UI", 24, "bold"),
                 fg=TEXT_DARK, bg=BG_CARD).pack(anchor="w")
        tk.Label(p, text="Track your body mass index",
                 font=("Segoe UI", 11),
                 fg=TEXT_GREY, bg=BG_CARD).pack(anchor="w", pady=(2, 20))

        # Name
        tk.Label(p, text="Name", font=("Segoe UI", 12, "bold"),
                 fg=TEXT_DARK, bg=BG_CARD).pack(anchor="w")
        self.name_entry = self._entry(p)
        self.name_entry.pack(fill="x", pady=(6, 16), ipady=9)
        self.name_entry.insert(0, "User")

        # Height
        tk.Label(p, text="Height", font=("Segoe UI", 12, "bold"),
                 fg=TEXT_DARK, bg=BG_CARD).pack(anchor="w")
        self.height_entry = self._entry(p)
        self.height_entry.pack(fill="x", pady=(6, 4), ipady=9)
        self.height_entry.insert(0, "170")
        self.height_unit_menu = ttk.Combobox(
            p, textvariable=self.height_unit_var,
            values=["cm", "m", "feet", "inches"],
            width=8, state="readonly", font=("Segoe UI", 11))
        self.height_unit_menu.pack(anchor="w", pady=(0, 16), ipady=5)

        # Weight
        tk.Label(p, text="Weight", font=("Segoe UI", 12, "bold"),
                 fg=TEXT_DARK, bg=BG_CARD).pack(anchor="w")
        self.weight_entry = self._entry(p)
        self.weight_entry.pack(fill="x", pady=(6, 4), ipady=9)
        self.weight_entry.insert(0, "65")
        self.weight_unit_menu = ttk.Combobox(
            p, textvariable=self.weight_unit_var,
            values=["kg", "grams", "lbs", "oz"],
            width=8, state="readonly", font=("Segoe UI", 11))
        self.weight_unit_menu.pack(anchor="w", pady=(0, 16), ipady=5)

        # Age
        tk.Label(p, text="Age", font=("Segoe UI", 12, "bold"),
                 fg=TEXT_DARK, bg=BG_CARD).pack(anchor="w")
        self.age_entry = self._entry(p)
        self.age_entry.pack(fill="x", pady=(6, 4), ipady=9)
        self.age_entry.insert(0, "25")
        tk.Label(p, text="Age in years", font=("Segoe UI", 9),
                 fg=TEXT_GREY, bg=BG_CARD).pack(anchor="w", pady=(0, 4))

        # Unit toggle
        tog = tk.Frame(p, bg=BG_CARD)
        tog.pack(fill="x", pady=(4, 24))
        tk.Label(tog, text="Units:", font=("Segoe UI", 10),
                 fg=TEXT_GREY, bg=BG_CARD).pack(side="left")
        tk.Label(tog, text="Metric (cm / kg)", font=("Segoe UI", 9),
                 fg=TEXT_GREY, bg=BG_CARD).pack(side="left", padx=(4, 8))

        self.imperial_btn = tk.Button(
            tog, text="Imperial",
            command=lambda: self.set_mode("Imperial"),
            font=("Segoe UI", 10, "bold"),
            fg="white", bg=TEAL, relief="flat", cursor="hand2",
            padx=12, pady=4, bd=0)
        self.imperial_btn.pack(side="left")

        self.metric_btn = tk.Button(
            tog, text="(ft / lbs)",
            command=lambda: self.set_mode("Metric"),
            font=("Segoe UI", 10),
            fg=TEXT_GREY, bg="#D8EDE9", relief="flat", cursor="hand2",
            padx=12, pady=4, bd=0)
        self.metric_btn.pack(side="left", padx=(4, 0))

        # Action buttons
        btn_row = tk.Frame(p, bg=BG_CARD)
        btn_row.pack(fill="x")

        calc_btn = tk.Button(btn_row, text="Calculate BMI",
                             command=self._calculate,
                             font=("Segoe UI", 13, "bold"),
                             fg="white", bg=TEAL, relief="flat",
                             cursor="hand2", pady=12, padx=24, bd=0)
        calc_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        calc_btn.bind("<Enter>", lambda e: calc_btn.config(bg=TEAL_DARK))
        calc_btn.bind("<Leave>", lambda e: calc_btn.config(bg=TEAL))

        reset_btn = tk.Button(btn_row, text="Reset",
                              command=self._reset,
                              font=("Segoe UI", 13),
                              fg=TEXT_DARK, bg=WHITE, relief="solid",
                              cursor="hand2", pady=12, padx=24, bd=1)
        reset_btn.pack(side="left", fill="x", expand=True)

        pdf_btn = tk.Button(p, text="📄  Export PDF Report",
                            command=self._export_pdf,
                            font=("Segoe UI", 11, "bold"),
                            fg="white", bg="#5C6BC0",
                            relief="flat", cursor="hand2", pady=10, bd=0)
        pdf_btn.pack(fill="x", pady=(12, 0))
        pdf_btn.bind("<Enter>", lambda e: pdf_btn.config(bg="#3949AB"))
        pdf_btn.bind("<Leave>", lambda e: pdf_btn.config(bg="#5C6BC0"))

        tk.Label(p, text="Tip: Press F11 for fullscreen  |  Esc to exit",
                 font=("Segoe UI", 8), fg=TEXT_GREY, bg=BG_CARD).pack(
                     anchor="w", pady=(10, 0))

    # ── Right panel (results) ─────────────────────────────────

    def _build_right(self, p):
        tk.Label(p, text="Your BMI", font=("Segoe UI", 14),
                 fg=TEXT_GREY, bg=BG_RESULT).pack(anchor="center", pady=(20, 0))

        self.bmi_number = tk.Label(p, text="—",
                                   font=("Segoe UI", 56, "bold"),
                                   fg=TEXT_DARK, bg=BG_RESULT)
        self.bmi_number.pack()

        self.cat_pill = tk.Label(p, text="",
                                 font=("Segoe UI", 14, "bold"),
                                 fg="white", bg=TEAL, padx=28, pady=8)
        self.cat_pill.pack(pady=(8, 0))

        self.desc_label = tk.Label(
            p, text="Enter your details\nand press Calculate BMI",
            font=("Segoe UI", 11), fg=TEXT_GREY, bg=BG_RESULT,
            justify="center", wraplength=280)
        self.desc_label.pack(pady=(16, 20))

        self.gauge_canvas = tk.Canvas(p, height=80, bg=BG_RESULT,
                                      highlightthickness=0)
        self.gauge_canvas.pack(fill="x", padx=10, pady=(0, 20))
        self.gauge_canvas.bind(
            "<Configure>",
            lambda e: draw_slider_gauge(
                self.gauge_canvas,
                self._last["bmi"] if self._last else 22))

        # Classification mini-cards
        class_frame = tk.Frame(p, bg=BG_RESULT)
        class_frame.pack(fill="x", pady=(0, 10))
        self.class_labels = {}
        for cat, color, rng in [
            ("Underweight", "#5C85D6", "< 18.5"),
            ("Normal",       TEAL,     "18.5–24.9"),
            ("Overweight",  "#F59E0B", "25–29.9"),
            ("Obese",       "#EF4444", "≥ 30"),
        ]:
            cf = tk.Frame(class_frame, bg=color, padx=8, pady=6)
            cf.pack(side="left", fill="x", expand=True, padx=3)
            tk.Label(cf, text=cat,  font=("Segoe UI", 8, "bold"),
                     fg="white", bg=color).pack()
            tk.Label(cf, text=rng,  font=("Segoe UI", 8),
                     fg="white", bg=color).pack()
            self.class_labels[cat] = cf

    # ── Helpers ───────────────────────────────────────────────

    def _entry(self, parent) -> tk.Entry:
        return tk.Entry(parent,
                        font=("Segoe UI", 13),
                        relief="solid", bd=1,
                        highlightthickness=2,
                        highlightcolor=TEAL,
                        highlightbackground="#D1D5DB",
                        fg=TEXT_DARK, bg=WHITE)

    def set_mode(self, mode: str):
        self.mode.set(mode)
        if mode == "Metric":
            self.height_unit_var.set("cm");  self.weight_unit_var.set("kg")
            self.height_unit_menu.config(values=["cm", "m"])
            self.weight_unit_menu.config(values=["kg", "grams"])
            self.imperial_btn.config(text="Imperial", bg=TEAL,     fg="white")
            self.metric_btn.config(  text="(ft/lbs)", bg="#D8EDE9", fg=TEXT_GREY)
        else:
            self.height_unit_var.set("feet"); self.weight_unit_var.set("lbs")
            self.height_unit_menu.config(values=["feet", "inches"])
            self.weight_unit_menu.config(values=["lbs", "oz"])
            self.imperial_btn.config(text="Imperial", bg="#D8EDE9", fg=TEXT_GREY)
            self.metric_btn.config(  text="Metric",   bg=TEAL,     fg="white")

    # ── Actions ───────────────────────────────────────────────

    def _calculate(self):
        wt   = self.weight_entry.get().strip()
        ht   = self.height_entry.get().strip()
        name = self.name_entry.get().strip() or "User"

        if not wt or not ht:
            messagebox.showerror("Missing Input", "Please enter both weight and height.")
            return
        try:
            wv, hv = float(wt), float(ht)
        except ValueError:
            messagebox.showerror("Invalid Input", "Numbers only please.")
            return
        if wv <= 0 or hv <= 0:
            messagebox.showerror("Invalid Input", "Values must be > 0.")
            return

        wunit = self.weight_unit_var.get()
        hunit = self.height_unit_var.get()
        wkg   = convert_weight_to_kg(wv, wunit)
        hm    = convert_height_to_meters(hv, hunit)

        err = validate_inputs(wkg, hm)
        if err:
            messagebox.showerror("Invalid Input", err)
            return

        bmi              = calculate_bmi(wkg, hm)
        category, color, desc = get_category(bmi)

        self._last = dict(bmi=bmi, category=category, color=color,
                          name=name, wv=wv, wunit=wunit, hv=hv, hunit=hunit)

        save_result(name, bmi, category, wv, wunit, hv, hunit)

        self.bmi_number.config(text=str(bmi), fg=color)
        self.cat_pill.config(text=category, bg=color)
        self.desc_label.config(text=desc)
        draw_slider_gauge(self.gauge_canvas, bmi)

        for cat, cf in self.class_labels.items():
            cf.config(highlightthickness=3 if cat == category else 0,
                      highlightbackground="white")

    def _reset(self):
        for entry, val in [(self.weight_entry, "65"),
                           (self.height_entry, "170"),
                           (self.age_entry,    "25"),
                           (self.name_entry,   "User")]:
            entry.delete(0, tk.END)
            entry.insert(0, val)
        self.bmi_number.config(text="—", fg=TEXT_DARK)
        self.cat_pill.config(text="", bg=TEAL)
        self.desc_label.config(text="Enter your details\nand press Calculate BMI")
        self.gauge_canvas.delete("all")
        self._last = None
        self.set_mode("Metric")

    def _export_pdf(self):
        if not self._last:
            messagebox.showwarning("No Result", "Please calculate BMI first.")
            return
        d = self._last
        path = filedialog.asksaveasfilename(
            title="Save BMI Report",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"BMI_Report_{d['name']}_{datetime.now().strftime('%Y%m%d')}.pdf")
        if not path:
            return
        try:
            generate_pdf(
                name=d["name"], bmi=d["bmi"],
                category=d["category"], color_hex=d["color"],
                weight_val=d["wv"],  weight_unit=d["wunit"],
                height_val=d["hv"], height_unit=d["hunit"],
                history_rows=load_history(), save_path=path)
            messagebox.showinfo("PDF Exported!", f"Report saved!\n\n{path}")
            if os.name == "nt":
                os.startfile(path)
            elif hasattr(os, "uname") and os.uname().sysname == "Darwin":
                os.system(f"open '{path}'")
            else:
                os.system(f"xdg-open '{path}'")
        except Exception as exc:
            messagebox.showerror("Export Failed", f"Error:\n{exc}")
