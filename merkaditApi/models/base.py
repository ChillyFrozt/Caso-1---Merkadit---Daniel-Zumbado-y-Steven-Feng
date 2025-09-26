from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL de conexión a PostgreSQL
DATABASE_URL = "postgresql://stevenfeng@localhost:5432/merkadit_db"

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear la sesión de la base de datos
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base para declarar los modelos
Base = declarative_base()
