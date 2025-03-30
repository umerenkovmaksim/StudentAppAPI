from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.feedback.router import router as feedback_router
from app.schedule.router import router as schedule_router
from app.students.router import router as student_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return 'API is running'

app.include_router(schedule_router)
app.include_router(student_router)
app.include_router(auth_router)
app.include_router(feedback_router)
