"""test_app.py
Unit tests verifying prompts, nutrition parsing, and formatting.
"""

from prompts import SYSTEM_PROMPT, get_welcome_message, get_whatsapp_summary_prompt
from app import extract_nutrition_data, format_whatsapp_number

def test_welcome_message():
    msg = get_welcome_message("Salman")
    assert "Hey Salman! 🥗" in msg
    assert "Welcome to MacroSnap" in msg
    assert "calories, protein, carbs, and fat" in msg

def test_phone_formatting():
    assert format_whatsapp_number("+91 98765 43210") == "whatsapp:+919876543210"
    assert format_whatsapp_number("+1 (415) 523-8886") == "whatsapp:+14155238886"
    assert format_whatsapp_number("919876543210") == "whatsapp:+919876543210"

def test_json_nutrition_extraction():
    ai_raw = """
Here is the nutrition breakdown for your salad:

```json
{
  "is_meal_analysis": true,
  "meal_name": "Mediterranean Grilled Chicken Salad",
  "calories": 420,
  "protein": 36,
  "carbs": 16,
  "fat": 22,
  "protein_label": "Lean Protein",
  "carbs_label": "Low GI",
  "fat_label": "Healthy Monounsaturated",
  "observation": "High protein, rich in vitamins A & C from mixed greens.",
  "disclaimer": "Estimates vary with portion size, ingredients, and preparation."
}
```

Enjoy your meal! Let me know if you had any dressing on the side.
"""
    data, cleaned = extract_nutrition_data(ai_raw)
    assert data is not None
    assert data["calories"] == 420
    assert data["protein"] == 36
    assert data["meal_name"] == "Mediterranean Grilled Chicken Salad"
    assert "Here is the nutrition breakdown" in cleaned
    assert "```json" not in cleaned

def test_conversational_fallback():
    chat_text = "Drinking water before meals can help support digestion and hydration."
    data, cleaned = extract_nutrition_data(chat_text)
    assert data is None
    assert cleaned == chat_text

def test_whatsapp_summary_prompt():
    conv = "User: Grilled chicken bowl\nMacroSnap: 450 kcal, 38g Protein"
    prompt = get_whatsapp_summary_prompt("Salman", conv)
    assert "Salman" in prompt
    assert "MacroSnap Nutrition Summary" in prompt

if __name__ == "__main__":
    test_welcome_message()
    test_phone_formatting()
    test_json_nutrition_extraction()
    test_conversational_fallback()
    test_whatsapp_summary_prompt()
    print("ALL TESTS PASSED SUCCESSFULLY! [OK]")
