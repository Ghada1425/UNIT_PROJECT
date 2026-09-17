import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-5.6-luna"
client = OpenAI(api_key=api_key)

def get_care_plan(plant_name, location, weather):
    """Ask the AI to create a short care plan for one plant."""

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY is missing. Add your API key first."
        )

    client = OpenAI()

    prompt = f"""
You are a practical plant-care assistant.

Plant name: {plant_name}
Plant location: {location}
Current weather: {weather}

Return ONLY valid JSON with exactly these keys:
watering_days
light
care_tip

Rules:
- watering_days must be one integer from 1 to 30.
- light must be one short sentence.
- care_tip must be one short practical sentence.
- Adjust the advice using indoor/outdoor and weather.
- Keep the advice simple for a beginner.
"""

    try:
        response = client.responses.create(
            model=MODEL_NAME,
            input=prompt
        )

        # Clean accidental Markdown fences before reading the JSON.
        text = response.output_text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        care = json.loads(text)

        if (
            "watering_days" not in care
            or "light" not in care
            or "care_tip" not in care
        ):
            raise ValueError("AI care plan is missing required information.")

        days = int(care["watering_days"])
        if days < 1 or days > 30:
            raise ValueError("AI returned an invalid watering schedule.")

        care["watering_days"] = days
        return care

    except json.JSONDecodeError:
        raise ValueError("AI returned an invalid care plan. Please try again.")
    except ValueError:
        raise
    except Exception:
        raise ConnectionError(
            "Could not connect to the AI service. "
            "Check your internet, API key, and API account."
        )
