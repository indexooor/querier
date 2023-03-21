from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder


router = APIRouter()


@router.get("/test")
async def test():
    return {"message": "Welcome to Indexooor Querier Rest API!"}
