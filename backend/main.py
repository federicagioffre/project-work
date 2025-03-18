from fastapi import FastAPI, Depends
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi.responses import JSONResponse
from pydantic import BaseModel  # ✅ Importa BaseModel per gestire il body della richiesta
from .routes import router
from .database import get_db  # Importa get_db
from . import models  # Importa models
from . import schemas
from fastapi import Query

app = FastAPI()

# Configurazione CORS
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permette tutte le origini per sviluppo
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
    # Calcola il totale delle persone già prenotate per quella data
    totale_posti = db.query(func.sum(models.Cliente.numero_persone)).filter(models.Cliente.data == prenotazione.data).scalar() or 0

    # Se il totale supera 80, blocca la prenotazione
    if totale_posti + prenotazione.numero_persone > 80:
        raise HTTPException(status_code=400, detail="Limite posti giornalieri raggiunto. Scegli un'altra data.")
    
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

@app.get("/prenotazioni/disponibilita/")
async def verifica_disponibilita(
    data: str = Query(..., description="Inserisci la data della prenotazione"),
    ora_arrivo: str = Query(None, description="Ora di arrivo (opzionale)"),
    db: Session = Depends(get_db)
):
    try:
        # Calcola la disponibilità dei posti
        totale_posti = db.query(func.sum(models.Cliente.numero_persone)).filter(models.Cliente.data == data).scalar() or 0
        posti_disponibili = max(0, 80 - totale_posti)
        return {"data": data, "ora_arrivo": ora_arrivo, "posti_disponibili": posti_disponibili}
    except Exception as e:
        return {"error": f"Errore durante il calcolo della disponibilità: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "API is working!"}
