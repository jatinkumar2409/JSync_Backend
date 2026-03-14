import ssl

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False  # Neon recommends this for default certs
ssl_context.verify_mode = ssl.CERT_NONE
engine = create_async_engine(os.getenv("DB_URI_ASYNC") ,connect_args = {"ssl" : ssl_context})
AsyncSessionLocal = sessionmaker(
    bind=engine , class_= AsyncSession , expire_on_commit=False
)
Base = declarative_base()

async def getdb():
    async with AsyncSessionLocal() as session:
        yield session