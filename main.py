from contextlib import contextmanager, asynccontextmanager

from fastapi import FastAPI, Request

from app.db.session import Base, engine
from app.router import router
from app.db.entities import Country


@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)

    yield

app = FastAPI(title='Currency & Exchange API', lifespan=lifespan)
app.include_router(router)


@app.middleware("http")
async def log_request(request: Request, call_next):
    print('\n\n')
    print(f"➡️  {request.method} {request.url}")
    try:
        body = await request.json()
        print(f"📦 Body: {body}")
    except Exception:
        print("📭 No JSON body")

    print('\n\n')

    response = await call_next(request)
    return response


from app.exceptions.handlers import register_exception_handlers
register_exception_handlers(app)


@app.get('/')
def read_root():
    return {"message": "Welcome!"}