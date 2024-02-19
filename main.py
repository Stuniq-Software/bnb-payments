from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dtypes import APIResponse, HttpStatus
from controller import PaymentController
import os

if os.getenv("ENV", "dev") == "dev":
    from dotenv import load_dotenv
    load_dotenv()
    print("Running in dev mode\nLoading .env file")

app = FastAPI(
    title="Bnb Clone Payment Service",
    description="A simple service to handle payments",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Abhiram B.S.N.",
        "email": "abhirambsn@gmail.com",
        "url": "https://abhirambsn.com"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(PaymentController)


@app.get("/")
async def root_healthz():
    return APIResponse(
        status=HttpStatus.OK,
        data=None,
        message="ok"
    ).to_dict()


@app.get("/healthz")
async def healthz():
    return APIResponse(
        status=HttpStatus.OK,
        data=None,
        message="ok"
    ).to_dict()


