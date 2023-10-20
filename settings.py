import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

env = dotenv.dotenv_values(".env")
uri = env.get("DATABASE_URI")
db = create_engine(uri)
Session = sessionmaker(db)
session = Session()
db.connect()
