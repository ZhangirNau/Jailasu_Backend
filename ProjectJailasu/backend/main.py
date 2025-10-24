# ProjectJailasu/backend/main.py
# uvicorn ProjectJailasu.backend.main:app --reload
# ngrok http 8000

from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import json
import os
from datetime import datetime

from ProjectJailasu.backend.routers import services, booking, contact
from ProjectJailasu.backend.database import Base, engine
from ProjectJailasu.backend.schemas import ContactMessage
from ProjectJailasu.backend import models


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jailasu-backend")

app = FastAPI(title="Jailasu API", version="0.1.0")


@app.on_event("startup")
def on_startup():
    logger.info("Creating DB tables (if not exists)...")
    Base.metadata.create_all(bind=engine)
    os.makedirs("ProjectJailasu/backend/data", exist_ok=True)
    logger.info("Startup complete.")


# Разрешаем CORS для Tilda
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Подключаем роутеры
app.include_router(services.router)
app.include_router(booking.router)
app.include_router(contact.router)


# Проверка API
@app.get("/")
def home():
    return {"status": "running", "message": "Backend connected!"}


# Простой endpoint для теста формы
@app.post("/feedback")
def feedback(email: str = Form(...), message: str = Form(...)):
    logger.info("Feedback received: %s — %s", email, message)
    return {"status": "ok", "detail": "Message received"}


# ----------- Webhook от Tilda -----------
@app.get("/webhook")
@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Принимает данные из Tilda webhook (GET или POST).
    Сохраняет сообщения локально в JSON.
    """
    try:
        if request.method == "POST":
            content_type = request.headers.get("content-type", "")
            payload = {}

            # 1. Если Tilda отправила form-data
            if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
                form_data = await request.form()
                payload = dict(form_data)

            # 2. Если Tilda отправила JSON
            elif "application/json" in content_type:
                payload = await request.json()

            logger.info("POST от Tilda: %s", payload)

            # Валидируем через ContactMessage (использует alias: Name, Email, Textarea)
            try:
                message = ContactMessage(**payload)
            except Exception as e:
                logger.warning("Ошибка валидации webhook: %s", e)
                return {"status": "error", "detail": f"Validation failed: {e}"}

            # Создаём/дополняем файл с обратной связью
            feedback_path = "ProjectJailasu/backend/data/tilda_feedback.json"
            with open(feedback_path, "a", encoding="utf-8") as f:
                json.dump(
                    {
                        "name": message.name,
                        "email": message.email,
                        "message": message.message,
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                    f,
                    ensure_ascii=False,
                )
                f.write("\n")

            logger.info(" Сообщение от Tilda сохранено в %s", feedback_path)
            return {"status": "ok", "received": message.dict(by_alias=True)}

        # Если GET-запрос (например, тест с Tilda)
        else:
            logger.info("GET от Tilda: %s", request.url)
            return {"status": "ok", "method": "GET", "url": str(request.url)}

    except Exception as e:
        logger.error("Ошибка при приёме данных от Tilda: %s", e)
        return {"status": "error", "detail": str(e)}
