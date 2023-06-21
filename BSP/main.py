from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi_limiter import FastAPILimiter
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.routes import clients, accounts, creditcards
from src.database.connect import get_db

app = FastAPI()


# @app.on_event("startup")
# async def startup():
# r = await redis.Redis(
#     host=settings.redis_host,
#     port=settings.redis_port,
#     password=settings.redis_password,
#     db=0,
#     encoding="utf-8",
#     decode_responses=True,
# )
# await FastAPILimiter.init(r)


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to Bank System!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


@app.get("/")
def info():
    return {"message": "Welcome to Bank System"}


app.include_router(clients.router, prefix="/api")
app.include_router(accounts.router, prefix="/api")
app.include_router(creditcards.router, prefix="/api")
