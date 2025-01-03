from fastapi import FastAPI
from app.routers import stock, predict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stock Prediction API", version= "1.0.0")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(stock.router, prefix ="/stock", tags=["Stock Data"])
app.include_router(predict.router, prefix="/predict", tags=["Stock Prediction"])


@app.get("/")
async def root():
    return {"message": "Backend is up and running"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
