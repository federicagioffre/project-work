from sqlalchemy import Column, Integer, String, Date, Time
from .database import Base

# Modello che rappresenta la tabella "clienti"
class Cliente(Base):
    __tablename__ = "clienti"

    id_clienti = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cognome = Column(String)
    telefono = Column(String)
    email = Column(String, unique=True, index=True)
    numero_persone = Column(Integer)
    data = Column(Date)
    ora_arrivo = Column(Time)
