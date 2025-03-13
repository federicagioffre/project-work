from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from pydantic import BaseModel  # ✅ Importa BaseModel per gestire il body della richiesta
from .routes import router
from .database import get_db  # Importa get_db
from . import models  # Importa models
from . import schemas

app = FastAPI()

# Configurazione CORS
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Definizione di un modello Pydantic per validare i dati della richiesta
class PrenotazioneRequest(BaseModel):
    nome: str
    cognome: str
    email: str
    telefono: str
    numero_persone: int
    data: str
    ora_arrivo: str

@app.post("/prenotazioni/")
async def prenotazione(prenotazione: PrenotazioneRequest, db: Session = Depends(get_db)):
    nuova_prenotazione = models.Cliente(
        nome=prenotazione.nome,
        cognome=prenotazione.cognome,
        email=prenotazione.email,
        telefono=prenotazione.telefono,
        numero_persone=prenotazione.numero_persone,
        data=prenotazione.data,
        ora_arrivo=prenotazione.ora_arrivo
    )
    
    db.add(nuova_prenotazione)
    db.commit()
    db.refresh(nuova_prenotazione)
    
    return {"message": "Prenotazione ricevuta!", "id": nuova_prenotazione.id_clienti}


@app.get("/prenotazioni/email/")
async def get_prenotazione_by_email(email: str, db: Session = Depends(get_db)):
    prenotazione = db.query(models.Cliente).filter(models.Cliente.email == email).first()
    
    if not prenotazione:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    
    return {
        "id": prenotazione.id_clienti,
        "nome": prenotazione.nome,
        "cognome": prenotazione.cognome,
        "email": prenotazione.email,
        "telefono": prenotazione.telefono,
        "numero_persone": prenotazione.numero_persone,
        "data": str(prenotazione.data),
        "ora_arrivo": str(prenotazione.ora_arrivo)
    }

@app.put("/prenotazioni/{email}/")
async def aggiorna_prenotazione(
    email: str,
    prenotazione_update: schemas.ClienteUpdate,
    db: Session = Depends(get_db)
):
    prenotazione = db.query(models.Cliente).filter(models.Cliente.email == email).first()

    if not prenotazione:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")

    for key, value in prenotazione_update.model_dump(exclude_unset=True).items():
        setattr(prenotazione, key, value)

    db.commit()
    db.refresh(prenotazione)
    
    return {"message": "Prenotazione aggiornata con successo!"}

@app.delete("/prenotazioni/{email}/")
async def cancella_prenotazione(email: str, db: Session = Depends(get_db)):
    prenotazione = db.query(models.Cliente).filter(models.Cliente.email == email).first()

    if not prenotazione:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")

    db.delete(prenotazione)
    db.commit()

    return {"message": "Prenotazione cancellata con successo!"}