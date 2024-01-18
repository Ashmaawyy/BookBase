from pymongo import MongoClient
from dotenv import dotenv_values
from fastapi import FastAPI
from routes import router as book_router
from models import Book

config = dotenv_values('.env')

async def lifespan(app: FastAPI):
    # Launch the Mongodb client when the app starts
    app.mongodb_client = MongoClient(config['ATLAS_URI'])
    app.database = app.mongodb_client['DB_NAME']
    print('Connected to the Mongodb successfully ;)')

    yield

    # Shutdown the connection after the app has finished
    app.mongodb_client.close()

app = FastAPI(lifespan = lifespan)
app.include_router(book_router, tags = ["books"], prefix = "/book")
