const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Connect to the database
const db = new sqlite3.Database("net.db", (err) => {
    if (err) {
        console.error("Database connection failed:", err.message);
    } else {
        console.log("Connected to SQLite database.");
    }
});

// 🎥 API to get all movies
app.get("/movies", (req, res) => {
    db.all("SELECT * FROM movies", [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

// ❤️ API to get wishlist for a profile
app.get("/wishlist/:profile_id", (req, res) => {
    const profileId = req.params.profile_id;
    db.all("SELECT movies.* FROM movies JOIN wishlist ON movies.id = wishlist.movie_id WHERE wishlist.profile_id = ?", 
        [profileId], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

// 🔥 API to add a movie to wishlist
app.post("/wishlist", (req, res) => {
    const { profile_id, movie_id } = req.body;
    db.run("INSERT INTO wishlist (profile_id, movie_id) VALUES (?, ?)", [profile_id, movie_id], function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json({ message: "Movie added to wishlist", id: this.lastID });
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
