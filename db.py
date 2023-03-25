from databases import Database
from sqlalchemy import MetaData, create_engine
import ormar

metadata = MetaData()
database = Database('sqlite:///sqlite.db')
engine = create_engine("sqlite:///sqlite.db")

class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
     