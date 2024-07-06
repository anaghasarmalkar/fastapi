import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db
from app.routers import user, auth, room


def main():
    init_db()
    # seed_data()

    app = FastAPI()
    app.include_router(auth.router)
    app.include_router(user.router)
    app.include_router(room.router)

    origins = [
        "http://localhost:3000",
        "http://0.0.0.0:3000",
        "http://127.0.0.1:3000"
    ]

    # A "middleware" is a function that works with every request before it is processed by any specific path operation. And also with every response before returning it.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = main()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8081, reload=True)
