from typing import List

from app.api import crud
from app.api.models import StockIn, StockOut, PredictionSchema
from app.prediction_engine import generate_prediction
from fastapi import APIRouter, HTTPException, BackgroundTasks


router = APIRouter()


@router.post("/", response_model=StockOut, status_code=201)
async def create_prediction(payload: StockIn,
                            background_tasks: BackgroundTasks):
    prediction_id = await crud.post(payload)

    background_tasks.add_task(generate_prediction,
                              prediction_id, payload.ticker)

    response_object = {
            "id": prediction_id,
            "ticker": payload.ticker
            }

    return response_object


@router.get("/{id}/", response_model=PredictionSchema)
async def get_prediction(id: int):
    prediction = await crud.get(id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction


@router.get("/", response_model=List[PredictionSchema])
async def get_all_predictions():
    return await crud.get_all()
