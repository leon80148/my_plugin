const express = require("express");

const app = express();
app.use(express.json());

// TODO: connect evaluate(model, input) and evaluateAll(input).

app.post("/risk/evaluate", async (req, res) => {
  const model = String(req.body?.model || "").toLowerCase().trim();
  const input = req.body?.input || {};

  if (!["chd", "stroke", "hypertension", "diabetes", "mace"].includes(model)) {
    return res.status(400).json({ status: 1, error: "unsupported model", version: 0 });
  }

  // const result = await evaluate(model, input);
  return res.json({ status: 1, error: "connect evaluator", version: 0 });
});

app.post("/risk/evaluate-all", async (req, res) => {
  const input = req.body?.input || {};
  // const result = await evaluateAll(input);
  return res.json({ error: "connect evaluator" });
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log("nhri-risk-api listening on " + port);
});
