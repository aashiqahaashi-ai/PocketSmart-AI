import json
from typing import Any
from .config import settings

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

def _fallback(planner: str, budget: float, details: dict[str, Any]) -> dict[str, Any]:
    if planner == "home":
        items = [
            ("LED lights", "Amazon", 1200),
            ("Ceiling fan", "Amazon", 2800),
            ("Accent table", "IKEA", 4500),
            ("Wall decor", "Flipkart", 1800),
        ]
    elif planner == "party":
        items = [
            ("Food package", "Swiggy", round(budget * 0.45)),
            ("Venue option", "OYO", round(budget * 0.25)),
            ("Decoration", "Local decor vendor", round(budget * 0.20)),
            ("Entertainment", "Local service", round(budget * 0.10)),
        ]
    else:
        items = [
            ("Stud earrings", "Amazon", 999),
            ("Pendant set", "Flipkart", 1799),
            ("Bangle set", "Amazon", 1299),
            ("Minimal necklace", "Flipkart", 1499),
        ]
    return {
        "summary": f"Fallback recommendations for a {planner} plan within a budget of ₹{budget:,.0f}.",
        "recommendations": [
            {"name": name, "platform": platform, "estimated_price": price, "reason": "Budget-friendly starter option."}
            for name, platform, price in items
        ],
        "source": "local-fallback",
    }

def _prompt(planner: str, budget: float, details: dict[str, Any]) -> str:
    return f"""
You are PocketSmart AI, a budget recommendation assistant.
Planner: {planner}
Budget: ₹{budget:,.2f}
User details: {json.dumps(details, ensure_ascii=False)}
Create practical recommendations that stay within the total budget.
Do not claim that you have live inventory or live prices.
Mention that prices are estimates when appropriate.
Return ONLY valid JSON in this exact shape:
{{
  "summary": "short summary",
  "recommendations": [
    {{
      "name": "item or service",
      "platform": "Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO/local",
      "estimated_price": 0,
      "reason": "short reason"
    }}
  ]
}}
Provide 4 to 8 recommendations.
"""

def generate_recommendations(planner: str, budget: float, details: dict[str, Any], image_bytes: bytes | None = None, mime_type: str | None = None) -> dict[str, Any]:
    if not settings.gemini_api_key or genai is None:
        return _fallback(planner, budget, details)

    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        prompt = _prompt(planner, budget, details)
        contents: list[Any] = [prompt]
        if image_bytes and mime_type and types:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
            contents.append("Use the uploaded outfit image only as a visual style/color reference for the jewelry recommendations.")
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.4,
                response_mime_type="application/json",
            ),
        )
        data = json.loads(response.text or "{}")
        recommendations = data.get("recommendations", [])
        if not isinstance(recommendations, list) or not recommendations:
            return _fallback(planner, budget, details)
        return {
            "summary": str(data.get("summary", "AI-generated budget recommendations.")),
            "recommendations": recommendations,
            "source": "gemini",
        }
    except Exception:
        return _fallback(planner, budget, details)
