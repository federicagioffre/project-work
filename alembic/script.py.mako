"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}

def upgrade() -> None:
    # Aggiungi la colonna 'id_clienti' alla tabella 'clienti'
    op.add_column('clienti', sa.Column('id_clienti', sa.Integer(), primary_key=True, autoincrement=True))
    
    # Aggiungi la colonna 'nome'
    op.add_column('clienti', sa.Column('nome', sa.String(50), nullable=False))
    
    # Aggiungi la colonna 'cognome'
    op.add_column('clienti', sa.Column('cognome', sa.String(50), nullable=False))
    
    # Aggiungi la colonna 'email'
    op.add_column('clienti', sa.Column('email', sa.String(100), nullable=False))
    op.create_index('ix_clienti_email', 'clienti', ['email'])  # Creiamo un indice su 'email'
    
    # Aggiungi la colonna 'telefono'
    op.add_column('clienti', sa.Column('telefono', sa.String(15), nullable=False))
    
    # Aggiungi la colonna 'numero_persone'
    op.add_column('clienti', sa.Column('numero_persone', sa.Integer(), nullable=False))
    
    # Aggiungi la colonna 'data'
    op.add_column('clienti', sa.Column('data', sa.Date(), nullable=False))
    
    # Aggiungi la colonna 'ora_arrivo'
    op.add_column('clienti', sa.Column('ora_arrivo', sa.Time(), nullable=False))

def downgrade() -> None:
    # Rimuovi la colonna 'id_clienti'
    op.drop_column('clienti', 'id_clienti')
    
    # Rimuovi la colonna 'nome'
    op.drop_column('clienti', 'nome')
    
    # Rimuovi la colonna 'cognome'
    op.drop_column('clienti', 'cognome')
    
    # Rimuovi la colonna 'email' e l'indice associato
    op.drop_index('ix_clienti_email', table_name='clienti')
    op.drop_column('clienti', 'email')
    
    # Rimuovi la colonna 'telefono'
    op.drop_column('clienti', 'telefono')
    
    # Rimuovi la colonna 'numero_persone'
    op.drop_column('clienti', 'numero_persone')
    
    # Rimuovi la colonna 'data'
    op.drop_column('clienti', 'data')
    
    # Rimuovi la colonna 'ora_arrivo'
    op.drop_column('clienti', 'ora_arrivo')

