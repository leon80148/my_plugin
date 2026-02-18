use axum::{routing::{get, post}, Router, Json};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;

/// Canonical input for NHRI V4 risk evaluation.
/// See references/input-output-contract.json for field definitions.
#[derive(Deserialize)]
struct RiskInput {
    gender: i32,
    age: i32,
    sbp: f64,
    #[serde(default)]
    tg: f64,
    #[serde(default)]
    ua: f64,
    #[serde(default)]
    chol: f64,
    #[serde(default)]
    hdlc: f64,
    #[serde(default)]
    ldlc: f64,
    #[serde(default)]
    glu: f64,
    #[serde(default)]
    bmi: f64,
    #[serde(default)]
    height: f64,
    #[serde(default)]
    weight: f64,
    #[serde(default)]
    ratio: f64,
    #[serde(default)]
    waist: f64,
    #[serde(default)]
    hip: f64,
    #[serde(default)]
    hbp: i32,
    #[serde(default)]
    diabetes: i32,
    #[serde(default)]
    smoke: i32,
}

/// Canonical output for NHRI V4 risk evaluation.
/// See references/input-output-contract.json for field definitions.
#[derive(Serialize)]
struct RiskOutput {
    status: i32,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    message: Option<String>,
    risk: f64,
    #[serde(rename = "populationAvg")]
    population_avg: f64,
    #[serde(rename = "multipleDiff")]
    multiple_diff: f64,
    #[serde(rename = "riskType")]
    risk_type: i32,
    version: i32,
}

/// Health check response.
#[derive(Serialize)]
struct HealthResponse {
    status: String,
    version: i32,
}

/// POST /api/v1/evaluate
async fn evaluate_risk(Json(input): Json<RiskInput>) -> Json<RiskOutput> {
    // TODO: Call the NHRI V4 evaluator logic here.
    // Replace this placeholder with actual risk computation.
    Json(RiskOutput {
        status: 0,
        error: None,
        message: Some("evaluation complete".into()),
        risk: 0.0,
        population_avg: 0.0,
        multiple_diff: 0.0,
        risk_type: 0,
        version: 4,
    })
}

/// GET /api/v1/health
async fn health_check() -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "ok".into(),
        version: 4,
    })
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/api/v1/evaluate", post(evaluate_risk))
        .route("/api/v1/health", get(health_check));

    let addr = SocketAddr::from(([0, 0, 0, 0], 8080));
    println!("NHRI Risk API listening on {}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
