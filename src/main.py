from fastapi import FastAPI
from routes.webhook import webhook_router

app = FastAPI()

app.include_router(webhook_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the WhatsApp AI Integration Service"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
