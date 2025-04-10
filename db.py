import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Load the environment variable
database_url = os.getenv("DATABASE_URL")


def get_db_connection():
    """Create and return a new database connection"""
    return psycopg2.connect(database_url)


def insert_game(title: str, code: str, username: str):
    """
    Insert a new game record into the games table

    Args:
        title (str): The title of the game
        code (str): The code of the game
        username (str): Telegram username of the game idea author
    Returns:
        int: The ID of the newly inserted game, or None if insertion fails
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "INSERT INTO games (title, code, username) VALUES (%s, %s, %s) RETURNING id"
            cur.execute(query, (title, code, username))
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
            query = (
                "SELECT id, title, code, username, created_at FROM games WHERE id = %s"
            )
            cur.execute(query, (game_id,))
            result = cur.fetchone()
            if result:
                return {
                    "id": result[0],
                    "title": result[1],
                    "code": result[2],
                    "username": result[3],
                    "created_at": result[4],
                }
            return None
    except psycopg2.Error as e:
        print(f"Error retrieving game: {e}")
        return None
    finally:
        conn.close()


def get_games(limit=20):
    """
    Retrieve the most recent games, ordered by creation date (newest first)

    Args:
        limit (int): Maximum number of games to retrieve (default: 20)
    Returns:
        list: List of dictionaries containing game details, or empty list if no games found
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT id, title, code, username, created_at FROM games ORDER BY created_at DESC LIMIT %s"
            cur.execute(query, (limit,))
            results = cur.fetchall()

            games = []
            for result in results:
                games.append(
                    {
                        "id": result[0],
                        "title": result[1],
                        "code": result[2],
                        "username": result[3],
                        "created_at": result[4],
                    }
                )
            return games
    except psycopg2.Error as e:
        print(f"Error retrieving games: {e}")
        return []
    finally:
        conn.close()
