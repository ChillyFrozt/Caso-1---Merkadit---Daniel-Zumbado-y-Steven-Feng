from database import engine, Base
from models.models import *

print("Creando tablas en la base de datos")
Base.metadata.create_all(bind=engine)
print("Finalizado")