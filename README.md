# PocketSmart AI

PocketSmart AI is a FastAPI + Jinja2 web application for budget-aware recommendations in three domains: Home, Party and Jewelry.

## Structure

```text
PocketSmart-AI/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── gemini_utils.py
│   ├── recommendation_service.py
│   └── routes/
│       ├── __init__.py
│       ├── pages.py
│       ├── auth_routes.py
│       ├── planners.py
│       └── history.py
├── templates/
├── static/
├── tests/
├── uploads/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Run on Windows

Use Python 3.11 for a straightforward setup.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and set `GEMINI_API_KEY`. The app also works without the key using local fallback recommendations.

Start:

```powershell
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

API docs: `http://127.0.0.1:8000/docs`

## Test

```powershell
python -m pytest -q
```

## Notes

The project documentation describes Gemini 1.5 Flash Pro, but the code keeps the model configurable through `GEMINI_MODEL`. The default here is `gemini-2.5-flash`, because model availability changes over time. For current model names, check Google's Gemini API documentation.

The product/platform names in generated recommendations are illustrative suggestions; this project does not scrape or claim live inventory/pricing from Amazon, Flipkart, IKEA, Swiggy, Zomato or OYO.
