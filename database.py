import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

from models import PlacementData, Base , Admin

# Define the connection string

DATABASE_URL = 'mysql+pymysql://root:Utkarsha270797@localhost/sunbeam'
engine = create_engine(DATABASE_URL)

# Create a new base class for the model
Base.metadata.create_all(engine)

# Start a session
Session = sessionmaker(bind=engine)

def insert_data_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    df.columns = ['Batch', 'KaradDac', 'DAC', 'DMC', 'DESD', 'DBDA']
    print(df)

    session = Session()
    for index, row in df.iterrows():
        existing_record = session.query(PlacementData).filter_by(Batch=row['Batch']).first()
        if existing_record is None:
            new_record = PlacementData(
                Batch=row['Batch'],
                KaradDac=row['KaradDac'],
                DAC=row['DAC'],
                DMC=row['DMC'],
                DESD=row['DESD'],
                DBDA=row['DBDA']
            )
            session.add(new_record)
        else:
            print(f"Record with Batch '{row['Batch']}' already exists. Skipping insertion.")

    # Commit and close the session
    session.commit()
    session.close()

def add_placement_data(batch, karad_dac, dac, dmc, desd, dbda):
    session = Session()
    new_record = PlacementData(
        Batch=batch,
        KaradDac=karad_dac,
        DAC=dac,
        DMC=dmc,
        DESD=desd,
        DBDA=dbda
    )
    session.add(new_record)
    session.commit()
    session.close()

def update_placement_data(id, batch, karad_dac, dac, dmc, desd, dbda):
    session = Session()
    record = session.query(PlacementData).filter_by(id=id).first()
    if record:
        record.Batch = batch
        record.KaradDac = karad_dac
        record.DAC = dac
        record.DMC = dmc
        record.DESD = desd
        record.DBDA = dbda
        session.commit()
    session.close()

def delete_placement_data(id):
    session = Session()
    record = session.query(PlacementData).filter_by(id=id).first()
    if record:
        session.delete(record)
        session.commit()
    session.close()

def authenticate_admin(username, password):
    session = Session()
    admin = session.query(Admin).filter_by(username=username).first()
    session.close()
    if admin and check_password_hash(admin.password, password):
        return True
    return False

def add_admin(username, password):
    session = Session()
    new_admin = Admin(
        username=username,
        password=generate_password_hash(password)
    )
    session.add(new_admin)
    session.commit()
    session.close()

#add_admin("onkar","123")