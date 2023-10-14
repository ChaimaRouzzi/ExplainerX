import asyncpg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Data_Understanding.data_undrstanding_routes import router_understanding
from Data_Gathering.data_gathering_routes import data_gathering_router
from Data_Understanding.Time_Series_Analysis.time_series_routes import time_series_router
from Data_Understanding.Single_Column_Profiling.single_column_profiling_routes import single_column_profiling_router
from Model_Prediction.model_prediction_routes import model_prediction_router
from Model_Building.model_building_routes import model_building_router
from Data_Preparation.feature_selection.feature_selection_routes import feature_selection_router
from Data_Preparation.data_praparation_route import router_data_preparation
from Data_Gathering.db_connection import connect_to_db
from Model_Prediction.model_prediction_logic import load_models
from Authentication.authentication_logic import login_router
from Model_Drift.model_drift_route import model_drift_route
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup_event():
    app.state.pool = await connect_to_db()
    load_models()


    
@app.on_event("shutdown")
async def shutdown_event():
    if "pool" in app.state:
        await app.state.pool.close()


app.include_router(model_drift_route, prefix="/api") 
app.include_router(router_data_preparation, prefix="/api") 
app.include_router(router_understanding, prefix="/api") 
app.include_router(time_series_router, prefix="/api/time_series_analysis") 
app.include_router(data_gathering_router, prefix="/api/data_gathering")
app.include_router(single_column_profiling_router, prefix="/api/single_column_profiling")
app.include_router(model_prediction_router, prefix="/api/models_prediction")
app.include_router(model_building_router, prefix="/api/models_building")
app.include_router(feature_selection_router, prefix="/api/feature_selection")
app.include_router(login_router, prefix="/api/login")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)