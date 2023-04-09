const express = require("express");
const router = express.Router();
const db = require("./db");

// DELETE /notes/:id - delete note by ID
router.delete("/:id", async (req, res) => {
  const { id } = req.params;
  try {
    const result = await db.run("DELETE FROM notes WHERE id = ?", id);
    if (result.changes === 0) {
      res.status(404).json({ error: `Note with ID ${id} not found` });
    } else {
      res.sendStatus(204);
    }
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

module.exports = router;
