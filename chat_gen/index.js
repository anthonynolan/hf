const express = require("express");
const bodyParser = require("body-parser");
// const swaggerUi = require("swagger-ui-express");
// const swaggerDocument = require("./swagger.json");
const notesRouter = require("./notes");
// const swaggerRouter = require("./swagger");

const app = express();
const port = process.env.PORT || 3000;

// Set up middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Set up API routes
app.use("/notes", notesRouter);

// Set up Swagger API documentation
// app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Mount the Swagger UI router
// app.use("/docs", swaggerRouter);

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
