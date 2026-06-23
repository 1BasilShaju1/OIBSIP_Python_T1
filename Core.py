from core.constants import TEAL, CATEGORY_COLORS


# ── Unit Converters

WEIGHT_TO_KG = {
    "kg":     lambda v: v,
    "grams":  lambda v: v / 1000,
    "lbs":    lambda v: v * 0.453592,
    "oz":     lambda v: v * 0.0283495,
}

HEIGHT_TO_M = {
    "m":      lambda v: v,
    "cm":     lambda v: v / 100,
    "feet":   lambda v: v * 0.3048,
    "inches": lambda v: v * 0.0254,
}


def convert_weight_to_kg(value: float, unit: str) -> float:
    """Convert any supported weight unit to kilograms."""
    return WEIGHT_TO_KG[unit](value)


def convert_height_to_meters(value: float, unit: str) -> float:
    """Convert any supported height unit to metres."""
    return HEIGHT_TO_M[unit](value)


# ── Core Calculation

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Return BMI rounded to 2 decimal places."""
    return round(weight_kg / (height_m ** 2), 2)


def get_category(bmi: float) -> tuple[str, str, str]:
    """
    Return (category_name, hex_color, description_text) for a given BMI.
    """
    if bmi < 18.5:
        return ("Underweight",
                CATEGORY_COLORS["Underweight"],
                "Your BMI is below the healthy range.")
    elif bmi < 25.0:
        return ("Normal",
                CATEGORY_COLORS["Normal"],
                "Great job! Keep up your healthy habits.")
    elif bmi < 30.0:
        return ("Overweight",
                CATEGORY_COLORS["Overweight"],
                "Your BMI is above the healthy range.")
    else:
        return ("Obese",
                CATEGORY_COLORS["Obese"],
                "Your BMI is well above the healthy range.")


# ── Validation ────────────────────────────────────────────────────────────────

def validate_inputs(weight_kg: float, height_m: float) -> str | None:
    """
    Returns an error message string if inputs are invalid, else None.
    """
    if not (0.5 <= height_m <= 2.7):
        return "Height seems unrealistic. Please check your value."
    if not (2 <= weight_kg <= 500):
        return "Weight seems unrealistic. Please check your value."
    return None
