# Security and Observability

## Security
- Enforce request size limits.
- Apply authentication and authorization for non-public endpoints.
- Validate `model` against allow-list.
- Avoid logging raw PHI/PII values.

## Reliability
- Return consistent HTTP status mapping:
- 200 for successful evaluation
- 4xx for malformed request/validation failures
- 5xx for unexpected adapter failures

## Observability
- Add request ID per request.
- Emit latency and error metrics per endpoint and model.
- Log model name and status only; avoid logging full clinical inputs.

## Versioning
- Include evaluator `version` in response.
- Use URL or header versioning if contract changes.
