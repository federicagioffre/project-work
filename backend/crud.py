from sqlalchemy.orm import Session
from .models import Cliente  # Importa direttamente Cliente
from . import models, schemas  # Importa models e schemas correttamente
from datetime import datetime

# Funzione per creare una prenotazione (cliente) con il limite di 80 al giorno
def create_cliente(db: Session, cliente: schemas.ClienteCreate) -> schemas.Cliente:
    # Conta le prenotazioni per la data selezionata
    count = db.query(Cliente).filter(Cliente.data == cliente.data).count()

    if count >= 80:
        raise ValueError("Limite di prenotazioni raggiunto per questa data.")
    
    db_cliente = Cliente(
        nome=cliente.nome,
        cognome=cliente.cognome,
        telefono=cliente.telefono,
        email=cliente.email,
        numero_persone=cliente.numero_persone,
        data=cliente.data,
        ora_arrivo=cliente.ora_arrivo
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Funzione per cercare una prenotazione tramite email
def get_cliente_by_email(db: Session, email: str):
    return db.query(Cliente).filter(Cliente.email == email).first()

# Funzione per ottenere tutte le prenotazioni
def get_clienti(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cliente).offset(skip).limit(limit).all()


