import uvicorn
from fastapi import FastAPI
from org_struct.interfaces.http_api.routes import router



app = FastAPI()
app.include_router(router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
