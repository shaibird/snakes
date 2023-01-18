import sqlite3
from models import Species


def get_all_species():
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.name
        FROM species s
        """)

        species = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            specimen = Species(row['id'], row['name'])

            species.append(specimen.__dict__)
        
        return species

def get_single_species(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.name
        FROM species s
        WHERE s.id = ?
        """, ( id, ))

        species = []

        data = db_cursor.fetchone()
 
        specimen = Species(data['id'], data['name'])

        species.append(specimen.__dict__)

        return species

