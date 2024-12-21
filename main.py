from fastapi import FastAPI
from routers import stock
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stock Prediction API", version= "1.0.0")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Allows requests from your Angular app
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Add other methods if necessary
    allow_headers=["*"],  # Allows all headers, you can adjust for more security
)
app.include_router(stock.router, prefix = "/stock", tags=["Stock Data"])

@app.get("/")
async def root():
    return {"message": "Backend is up and running"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
