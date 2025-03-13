from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Assicurati di avere il file database.py con il corretto motore di connessione

# Modello di prenotazione nel database
class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    date = Column(Date)
    time = Column(Time)
    number_of_people = Column(Integer)

    # Relazione con il modello Cliente
    cliente_id = Column(Integer, ForeignKey('clienti.id'))
    cliente = relationship("Cliente", back_populates="reservations")  # Assicurati che il modello Cliente abbia "reservations" come back_populates

# Funzione per creare una prenotazione nel database
from sqlalchemy.exc import IntegrityError

def create_reservation(db, reservation):
    try:
        db_reservation = Reservation(
            name=reservation.name,
            email=reservation.email,
            phone=reservation.phone,
            date=reservation.date,
            time=reservation.time,
            number_of_people=reservation.number_of_people,
            cliente_id=reservation.cliente_id  # Assicurati che questa proprietà venga passata nel parametro
        )
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        return db_reservation
    except IntegrityError as e:
        db.rollback()  # rollback per evitare problemi nel database
        raise ValueError("Email già esistente o errore nel database.")

# Funzione per ottenere tutte le prenotazioni
def get_reservations(db):
    return db.query(Reservation).all()
