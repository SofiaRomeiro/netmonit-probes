from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
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

@app.on_event("startup")
@repeat_every(seconds=60*10) # 10 minutes
def pingScheduler():
    monitorRouter.monitorPing()

@app.on_event("startup")
@repeat_every(seconds=60*30) # 30 minutes
def updatePingScheduler():
    monitorRouter.updateMonitorController()

@app.on_event("startup")
@repeat_every(seconds=60*60*6) # 6 hours
def performanceScheduler():
    monitorRouter.performanceController()

@app.on_event("startup")
@repeat_every(seconds=60*60*6) # 6 hours
def updatePerformanceScheduler():
    monitorRouter.updatePerformanceController()

if __name__ == "__main__": 
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=env.PORT)