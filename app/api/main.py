from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.infrastructure.database import create_db, populate_tables
from app.api.routers import location_router, auth_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event("startup")
async def startup_event():
    create_db()
    populate_tables()

@app.get("/", include_in_schema=False)
def read_root():
    """
    redirect to Autodocumentation.
    """
    return RedirectResponse('/docs')


# include routers
app.include_router(location_router)
app.include_router(auth_router)


if __name__ == '__main__':
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)
