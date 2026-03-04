from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.shipping.routes import router as shipping_router

app = FastAPI(
    title="Always Beautiful API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shipping_router)

@app.get("/health")
def health():
    return {"status": "ok"}
