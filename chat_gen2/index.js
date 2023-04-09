const express = require("express");
const bodyParser = require("body-parser");
const sqlite3 = require("sqlite3").verbose();
const app = express();
const port = 3000;

const db = new sqlite3.Database(":memory:"); // create an in-memory database

// create a 'notes' table with 'id', 'text', 'date', and 'tags' columns
db.serialize(() => {
  db.run(
    "CREATE TABLE notes (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, date TEXT, tags TEXT)"
  );
});

app.use(bodyParser.json());

app.post("/notes", (req, res) => {
  const note = {
    text: req.body.text,
    date: new Date(),
    tags: req.body.tags || [],
  };
  db.run(
    "INSERT INTO notes (text, date, tags) VALUES (?, ?, ?)",
    [note.text, note.date.toISOString(), note.tags.join(", ")],
    function (err) {
      if (err) {
        console.error(err);
        res.status(500).send("Error inserting note");
        return;
      }
      note.id = this.lastID; // set the note's ID to the ID generated by the database
      res.status(201).json(note);
    }
  );
});

app.get("/notes", (req, res) => {
  const { tags } = req.query;
  let query = "SELECT * FROM notes";
  let params = [];
  if (tags) {
    query += " WHERE tags LIKE ?";
    params.push(`%${tags}%`);
  }
  db.all(query, params, (err, rows) => {
    if (err) {
      console.error(err);
      res.status(500).send("Error retrieving notes");
      return;
    }
    const notes = rows.map((row) => ({
      id: row.id,
      text: row.text,
      date: new Date(row.date),
      tags: row.tags.split(", "),
    }));
    res.json(notes);
  });
});

app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});

module.exports = app;
