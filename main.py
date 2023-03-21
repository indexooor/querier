# from routes.user import router as UserRouter
# from routes.project import router as ProjectRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.querier import router as QuerierRouter

app = FastAPI(docs_url="/docs", redoc_url="/redocs", debug=True)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(QuerierRouter, tags=["Querier"], prefix="/querier")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Indexooor Querier Rest API!"}
