import sqlite3

def create_connection():
    return sqlite3.connect("net.db")  # Database name is net.db

def create_tables():
    with create_connection() as conn:
        cursor = conn.cursor()
        
        # Profiles Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        """)
        
        # Movies Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            language TEXT NOT NULL
        )
        """)
        
        # Wishlist Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            FOREIGN KEY (profile_id) REFERENCES profiles(id),
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        )
        """)

        # Insert default profiles (if not exists)
        cursor.executemany(
            "INSERT OR IGNORE INTO profiles (name) VALUES (?)",
            [("Mine",), ("Mom's",), ("Dad's",)]
        )

        # Insert default movies (Genre, Language)
        default_movies = [
            ("Inception", "Sci-Fi", "English"),
            ("Parasite", "Thriller", "Korean"),
            ("Dangal", "Drama", "Hindi"),
            ("Avengers", "Action", "English"),
            ("Spirited Away", "Animation", "Japanese"),
            ("The Godfather", "Crime", "English"),
            ("3 Idiots", "Comedy", "Hindi"),
            ("Your Name", "Romance", "Japanese"),
            ("Coco", "Animation", "Spanish"),
            ("Money Heist", "Thriller", "Spanish")
        ]
        cursor.executemany(
            "INSERT OR IGNORE INTO movies (title, genre, language) VALUES (?, ?, ?)",
            default_movies
        )

        conn.commit()

# 🎬 Get all movies
def get_movies():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies")
        return cursor.fetchall()

# 🔍 Search for movies by title
def search_movies(search_query):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE title LIKE ?", ('%' + search_query + '%',))
        return cursor.fetchall()

# ❤️ Add a movie to wishlist
def add_to_wishlist(profile_id, movie_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO wishlist (profile_id, movie_id) VALUES (?, ?)", (profile_id, movie_id))
        conn.commit()

# 📜 Get wishlist for a profile
def get_wishlist(profile_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT movies.id, movies.title, movies.genre, movies.language 
        FROM movies JOIN wishlist ON movies.id = wishlist.movie_id
        WHERE wishlist.profile_id = ?
        """, (profile_id,))
        return cursor.fetchall()

