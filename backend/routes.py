from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas
from .database import get_db

router = APIRouter()

@router.post("/prenotazioni/", response_model=schemas.Cliente)
def create_prenotazione(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_cliente(db, cliente)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prenotazioni/email/", response_model=schemas.Cliente)
def read_prenotazione(email: str, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente_by_email(db, email)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    return db_cliente

@router.get("/cerca/prenotazioni/", response_model=List[schemas.Cliente])
def get_all_prenotazioni(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_clienti(db, skip=skip, limit=limit)
