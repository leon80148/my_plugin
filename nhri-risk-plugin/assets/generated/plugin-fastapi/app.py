from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# TODO: import evaluate/evaluate_all from your evaluator implementation.

app = FastAPI(title="nhri-plugin-api")


class EvaluateRequest(BaseModel):
    model: str
    input: dict


class EvaluateAllRequest(BaseModel):
    input: dict


@app.post("/risk/evaluate")
def evaluate_one(request: EvaluateRequest):
    model = request.model.lower().strip()
    if model not in {"chd", "stroke", "hypertension", "diabetes", "mace"}:
        raise HTTPException(status_code=400, detail="unsupported model")

    # result = evaluate(model, request.input)
    result = {"status": 1, "error": "connect evaluator", "version": 0}
    return result


@app.post("/risk/evaluate-all")
def evaluate_all_models(request: EvaluateAllRequest):
    # result = evaluate_all(request.input)
    result = {"error": "connect evaluator"}
    return result
