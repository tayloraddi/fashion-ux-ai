from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/upload")
async def upload_image(request: Request):

    form = await request.form()

    print("========== FORM DATA RECEIVED ==========")
    print("FORM KEYS:", list(form.keys()))
    print("========================================")

    file = form.get("file")
    age = form.get("age")
    location = form.get("location")
    occupation = form.get("occupation")

    if not file or not age or not location or not occupation:
        return {
            "message": "Something is missing.",
            "received_keys": list(form.keys()),
            "file_received": file is not None,
            "age_received": age is not None,
            "location_received": location is not None,
            "occupation_received": occupation is not None
        }

    image_bytes = await file.read()

    persona_prompt = f"""
You are a {age}-year-old person living in {location}.
Your occupation is {occupation}.

You are conducting a UX evaluation of a fashion website or fashion shopping interface.

Analyze the screenshot from the perspective of this specific user persona.

Your analysis should be specific to what you can actually see in the screenshot.
Do not invent features, buttons, or information that are not visible.

First, assign the interface a UX SCORE from 0 to 100.

The score should reflect:
- Visual design
- Usability
- Clarity
- Trust and credibility
- Navigation
- Shopping experience
- Overall user experience

A score of:
90-100 = Excellent UX
80-89 = Very good UX
70-79 = Good but has noticeable issues
60-69 = Needs improvement
Below 60 = Significant UX problems

IMPORTANT:
The UX score should be based ONLY on what is visible in the screenshot.

Format your response EXACTLY like this:

UX_SCORE: [number between 0 and 100]

FIRST IMPRESSION:
[Your analysis]

VISUAL DESIGN:
[Your analysis]

USABILITY:
[Your analysis]

TRUST & CREDIBILITY:
[Your analysis]

SHOPPING EXPERIENCE:
[Your analysis]

PAIN POINTS:
[Your analysis]

RECOMMENDATIONS:
1. [Recommendation]
2. [Recommendation]
3. [Recommendation]
4. [Recommendation]
5. [Recommendation]

IMPORTANT:
- Base your feedback only on what is visible in the screenshot.
- Consider the user's age, location, and occupation when relevant.
- Do not assume the user has information that is not shown.
- Be honest if something cannot be determined from the screenshot.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[
                persona_prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=file.content_type
                )
            ]
        )

        return {
            "filename": file.filename,
            "age": age,
            "location": location,
            "occupation": occupation,
            "analysis": response.text
        }

    except Exception as e:

        print("GEMINI ERROR:", str(e))

        return {
            "message": "The upload worked, but the AI analysis failed.",
            "error": str(e)
        }