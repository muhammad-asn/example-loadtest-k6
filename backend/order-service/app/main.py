from fastapi import FastAPI, HTTPException
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
import httpx
from . import schemas

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
apm = make_apm_client({
    'SERVICE_NAME': 'order-service',
    'SECRET_TOKEN': os.getenv("APM_SECRET_TOKEN"),
    'SERVER_URL': os.getenv("APM_SERVER_URL"),
    'ENVIRONMENT': os.getenv("APM_ENVIRONMENT"),
})
app.add_middleware(ElasticAPM, client=apm)


@app.get("/health", status_code=200)
def health_check():
    return {"status": "ok"}

@app.post("/orders/")
async def create_order(order: schemas.OrderCreate):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://user-service:8000/users/{order.user_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        user = response.json()
    return {"order_id": 1, "user": user, "item": order.item}
