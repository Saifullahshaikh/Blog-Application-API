from fastapi import FastAPI
from schema import userSchema

app = FastAPI()


app.include_router(userSchema.router)