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
@repeat_every(seconds=60*1) # 2 minutes
def pingScheduler():
    monitorRouter.monitorPing()

@app.on_event("startup")
@repeat_every(seconds=60*5) # 5 minutes
def internalPerformanceScheduler():
    monitorRouter.measureInternalPerformance()

@app.on_event("startup")
@repeat_every(seconds=60*5) # 5 minutes
def externalPerformanceScheduler():
    monitorRouter.measureExternalPerformance()

@app.on_event("startup")
@repeat_every(seconds=60*5) # 7 minutes
def updatePingScheduler():
    monitorRouter.updateMonitor()

@app.on_event("startup")
@repeat_every(seconds=60*7) # 7 minutes
def updateInternalPerformanceScheduler():
    monitorRouter.updateInternalPerformance()

@app.on_event("startup")
@repeat_every(seconds=60*7) # 7 minutes
def updateExternalPerformanceScheduler():
    monitorRouter.updateExternalPerformance()

if __name__ == "__main__": 
    uvicorn.run("main:app", reload=False, host="0.0.0.0", port=env.PORT)
