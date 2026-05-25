import uvicorn
from fastapi import FastAPI
from org_struct.interfaces.http_api.routes import departments_router
from org_struct.interfaces.http_api.exceptions import register_exception_handlers



app = FastAPI()
register_exception_handlers(app)
app.include_router(departments_router, prefix="/api/v1")




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
