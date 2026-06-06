// BornSystem Backend - Node Entry Point

import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

// Basic health check endpoint
app.get("/health", (req, res) => {
  res.json({ status: "ok", system: "BornSystem Backend (Node)" });
});

// Start server
const PORT = 3001;
app.listen(PORT, () => {
  console.log(`BornSystem Node backend running on port ${PORT}`);
});
