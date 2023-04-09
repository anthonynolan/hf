const request = require("supertest");
const app = require("../index");

describe("notes API", () => {
  let notes = [];

  beforeEach(async () => {
    notes = [
      { text: "Note 1", tags: ["tag1", "tag2"] },
      { text: "Note 2", tags: ["tag1"] },
      { text: "Note 3", tags: ["tag2"] },
    ];

    for (const note of notes) {
      await request(app).post("/notes").send(note);
    }
  });

  afterEach(() => {
    notes = [];
  });

  describe("POST /notes", () => {
    it("adds a new note to the database", async () => {
      const newNote = { text: "New note", tags: ["tag3"] };
      const response = await request(app)
        .post("/notes")
        .send(newNote)
        .expect(201);
      expect(response.body).toMatchObject({
        text: newNote.text,
        tags: newNote.tags,
      });
      expect(response.body).toHaveProperty("id");
      expect(typeof response.body.id).toBe("number");
    });
  });

  describe("GET /notes", () => {
    it("returns all notes when no tags are specified", async () => {
      const response = await request(app).get("/notes").expect(200);
      expect(response.body).toEqual(notes);
    });

    it("returns only notes with matching tags when tags are specified", async () => {
      const response = await request(app).get("/notes?tags=tag1").expect(200);
      const expectedNotes = notes.filter((note) => note.tags.includes("tag1"));
      expect(response.body).toEqual(expectedNotes);
    });
  });
});
