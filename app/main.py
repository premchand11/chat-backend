from fastapi import FastAPI
from app.api.routes.analysis import router as analysis_router
from app.core.database import engine, Base
from app.models.chat_analysis import ChatAnalysis  # IMPORTANT import model

app = FastAPI(title="WhatsApp Multiverse Analyzer", version="1.0.0")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(analysis_router)
