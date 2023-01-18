import sqlite3
from models import Species, Snakes, Owners

def get_all_snakes():
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.owner_id,
            o.first_name,
            o.last_name,
            o.email,
            s.species_id,
            sp.name,
            s.gender,
            s.color
        FROM snakes s
        JOIN Owners o ON o.id = s.owner_id
        JOIN Species sp ON sp.id = s.species_id
        """)

        snakes = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            snake = Snakes(row['id'], row['name'], row['owner_id'], row['species_id'], row['gender'], row['color'])
            species = Species(row['id'], row['name'])
            owner = Owners(row['id'], row['first_name'], row['last_name'], row['email'])

            snake.species = species.__dict__
            snake.owner = owner.__dict__

            snakes.append(snake.__dict__)
        
        return snakes

def get_single_snake(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.owner_id,
            o.first_name,
            o.last_name,
            o.email,
            s.species_id,
            sp.name,
            s.gender,
            s.color
        FROM snakes s
        JOIN Owners o ON o.id = s.owner_id
        JOIN Species sp ON sp.id = s.species_id
        WHERE s.id = ?
        """, ( id, ))

        snakes = []

        data = db_cursor.fetchone()


        snake = Snakes(data['id'], data['name'], data['owner_id'], data['species_id'], data['gender'], data['color'])
        species = Species(data['species_id'], data['name'])
        owner = Owners(data['owner_id'], data['first_name'], data['last_name'], data['email'])

        snake.species = species.__dict__
        snake.owner = owner.__dict__
        
        if data['species_id'] == 2:
            snakes = []
        else:
            snakes.append(snake.__dict__)
       

        return snakes

def get_snakes_by_species(species):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.owner_id,
            o.first_name,
            o.last_name,
            o.email,
            s.species_id,
            sp.name,
            s.gender,
            s.color
        FROM snakes s
        JOIN Owners o ON o.id = s.owner_id
        JOIN Species sp ON sp.id = s.species_id
        WHERE s.species_id = ?
        """, ( species, ))

        snakes = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            snake = Snakes(row['id'], row['name'], row['owner_id'], row['species_id'], row['gender'], row['color'])
            species = Species(row['id'], row['name'])
            owner = Owners(row['id'], row['first_name'], row['last_name'], row['email'])

            snake.species = species.__dict__
            snake.owner = owner.__dict__

            snakes.append(snake.__dict__)
        
        return snakes

def create_snake(snake):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        db_cursor = conn.cursor()

        if all(val for val in snake.values()) and set(snake.keys()) == {'name', 'owner_id', 'species_id', 'gender', 'color'}:
            db_cursor.execute("""
            INSERT INTO Snakes
                ( name, owner_id, species_id, gender, color )
            VALUES
                ( ?, ?, ?, ?, ?);
            """, (snake['name'], snake['owner_id'], snake['species_id'], snake['gender'], snake['color'], ))

            id = db_cursor.lastrowid

            snake['id'] = id

            return snake
        else:
            return "missing information"