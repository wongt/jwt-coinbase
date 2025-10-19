# jwt-coinbase

Tiny FastAPI service that generates **Coinbase CDP JWTs** for internal callers.

## Endpoints
- `POST /token`
  - Body:
    ```json
    {
      "request_domain": "https://api.coinbase.com",
      "request_method": "GET",
      "request_path": "/api/v3/brokerage/accounts",
      "expires_in": 120
    }
    ```
  - Response:
    ```json
    {
      "jwt": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9...",
      "request_method": "GET",
      "request_path": "/api/v3/brokerage/accounts",
      "date": "2025-10-18 20:17:32"
    }
    ```

- `GET /healthz` → `{ "status": "ok" }`

## Secrets
Provide via environment variables (Kubernetes Secret recommended):
- `COINBASE_API_KEY_ID`
- `COINBASE_API_KEY_SECRET` (PEM with BEGIN/END and newlines)

### Create k8s secret
```bash
kubectl create ns jwt-coinbase || true
kubectl -n jwt-coinbase create secret generic jwt-coinbase-secret \
  --from-literal=COINBASE_API_KEY_ID='YOUR-ID' \
  --from-file=COINBASE_API_KEY_SECRET=./coinbase_private_key.pem
