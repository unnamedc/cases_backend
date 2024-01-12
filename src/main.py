from typing import Union
from initil.postsql import return_about_case, all_cases, examination
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
    "https://0692-178-214-248-19.ngrok-free.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/cases")
def read_root():
    return all_cases()

@app.get("/money/{user_id}")
def get_money(user_id: int):
    return examination(user_id)

@app.get("/cases/{caseId}")
def read_item(caseId: int):
    return return_about_case(caseId)

@app.post("/cases/{caseId}/open")
def update_item(caseId: int):
    return {"caseId": caseId}
