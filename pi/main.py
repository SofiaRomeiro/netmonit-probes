from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import monitor.router as monitorRouter
import session.register as register

import uvicorn
import env

app = FastAPI(title="Network Monitoring")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(monitorRouter.router, prefix='/monitor')

@app.on_event("startup") #call this function when app starts
def start():
    register.registration()

if __name__ == "__main__": 
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=env.PORT)