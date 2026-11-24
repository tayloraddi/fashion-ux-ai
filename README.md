# Fashion UX AI

An AI tool that reviews fashion websites and apps from a real shopper's point of view.

**Live demo:** https://fashion-ux-ai.onrender.com
*(Hosted on a free tier, so the first load may take up to a minute to wake up.)*

Built as a summer 2026 research project on how AI can support UX research in fashion technology.

## What it does

1. Upload a screenshot of a fashion website or shopping interface.
2. Pick a preset persona (college student, young professional, fashion enthusiast) or enter your own age, location, and occupation.
3. Get a UX score from 0 to 100 and feedback written from that persona's perspective, covering:
   - First impression
   - Visual design
   - Usability
   - Trust and credibility
   - Shopping experience
   - Pain points
   - Five recommended fixes

## How it works

- The **front end** (HTML, CSS, JavaScript) collects the screenshot and persona details and sends them to the backend.
- The **backend** (Python, FastAPI) builds a prompt around the persona and sends it with the screenshot to the Google Gemini API.
- The prompt tells the AI to comment only on what is visible in the screenshot, so it doesn't invent features.
- The AI's reply follows a fixed format. The front end pulls out the score, splits the text into sections, and cleans up garbled characters before displaying it.

## Tech stack

Python, FastAPI, Jinja2, Google Gemini API (`google-genai`), HTML, CSS, JavaScript, deployed on Render. Built with Cursor.

## Run it locally

1. Clone the repo and open the folder.
2. Install dependencies:
   
   pip install -r requirements.txt
   
3. Create a file named `.env` in the project folder with your Gemini API key:
   GEMINI_API_KEY=your_key_here

4. Start the server:
 
   uvicorn app:app --reload
   
5. Open http://127.0.0.1:8000 in your browser.

## Project structure


app.py               FastAPI app and Gemini request
templates/index.html The web interface
requirements.txt     Python dependencies
.env                 Your API key (not committed)


What I learned

- AI replies don't always arrive in a clean format, so the app needs code to parse and clean them.
- Clear prompt instructions (like "only describe what is visible") make AI feedback more trustworthy.
- Deploying a project and keeping API keys out of the code.

## Author

Taylor Chen, University of Georgia
