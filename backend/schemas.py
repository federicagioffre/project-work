from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

# Schema per la prenotazione
class ClienteBase(BaseModel):
    nome: str
    cognome: str
    telefono: str
    email: str
    numero_persone: int
    data: date
    ora_arrivo: time

    class Config:
        populate_by_name = True  # Permette di usare l'alias nei modelli Pydantic

# Schema per creare una nuova prenotazione
class ClienteCreate(ClienteBase):
    pass

# Schema per restituire le prenotazioni
class Cliente(ClienteBase):
    id: int

    class Config:
        from_attributes = True
        
class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    cognome: Optional[str] = None
    telefono: Optional[str] = None
    numero_persone: Optional[int] = None
    data: Optional[date] = None
    ora_arrivo: Optional[time] = None

