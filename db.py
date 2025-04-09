import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

# Load the environment variable
database_url = os.getenv('DATABASE_URL')

def get_db_connection():
    """Create and return a new database connection"""
    return psycopg2.connect(database_url)

def insert_game(title, code):
    """
    Insert a new game record into the games table
    
    Args:
        title (str): The title of the game
        code (str): The code of the game
    Returns:
        int: The ID of the newly inserted game, or None if insertion fails
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "INSERT INTO games (title, code) VALUES (%s, %s) RETURNING id"
            cur.execute(query, (title, code))
            game_id = cur.fetchone()[0]
            conn.commit()
            return game_id
    except psycopg2.Error as e:
        print(f"Error inserting game: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_game(game_id):
    """
    Retrieve a game record by its ID
    
    Args:
        game_id (int): The ID of the game to retrieve
    Returns:
        dict: Game details (id, title, code, created_at) or None if not found
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT id, title, code, created_at FROM games WHERE id = %s"
            cur.execute(query, (game_id,))
            result = cur.fetchone()
            if result:
                return {
                    'id': result[0],
                    'title': result[1],
                    'code': result[2],
                    'created_at': result[3]
                }
            return None
    except psycopg2.Error as e:
        print(f"Error retrieving game: {e}")
        return None
    finally:
        conn.close()
