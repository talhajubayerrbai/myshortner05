# myshortner05 — URL Shortener

A minimal URL shortener built with **FastAPI**, **PostgreSQL** (AWS RDS), deployed on **EC2** (Ubuntu 22.04) via Ansible and Terraform.

---

## Architecture

```
User → EC2 :8000 (FastAPI/Uvicorn) → RDS Postgres 16
```

See `.udap/architecture.d2` for the full diagram.

---

## API Endpoints

| Method | Path             | Description                              |
|--------|------------------|------------------------------------------|
| GET    | `/health`        | Health check — returns `{"status":"ok"}` |
| POST   | `/shorten`       | Shorten a URL                            |
| GET    | `/{code}`        | Redirect to the original URL             |
| GET    | `/{code}/stats`  | View stats (hit count, created_at)       |

### Shorten a URL

```bash
curl -X POST http://<HOST>:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Response:
```json
{
  "short_code": "aB3xYz9q",
  "short_url": "http://<HOST>:8000/aB3xYz9q",
  "original_url": "https://example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Custom short code

```bash
curl -X POST http://<HOST>:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "custom_code": "mycode"}'
```

### View stats

```bash
curl http://<HOST>:8000/aB3xYz9q/stats
```

---

## Local Development

**Prerequisites:** Python 3.11+, a running Postgres instance.

```bash
# 1. Clone and enter the repo
git clone https://github.com/<org>/myshortner05.git
cd myshortner05

# 2. Create and activate a virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
export DATABASE_URL="postgresql://shortener:password@localhost:5432/shortener"
export BASE_URL="http://localhost:8000"

# 5. Run migrations
alembic upgrade head

# 6. Start the server
uvicorn app.main:app --reload --port 8000
```

---

## Configuration

All runtime configuration is provided via environment variables (written to `/opt/shortener/.env` on the server by Ansible).

| Variable       | Description                                 | Secret |
|----------------|---------------------------------------------|--------|
| `DATABASE_URL` | SQLAlchemy Postgres connection URL           | Yes    |
| `BASE_URL`     | Public base URL used in shortened link response | No  |

---

## Deployment

The project deploys automatically via the GitHub Actions pipeline on the UDAP platform.

**Pipeline stages:**

1. **provision** — Terraform provisions EC2 + RDS + security groups + EIP.
2. **configure** — Ansible installs Python 3.11, copies the app, writes `.env`, runs Alembic migrations, and starts the `shortener` systemd service.
3. **verify** — `curl` health-checks `GET /health` with retries.

**Secrets required (set by the platform):**

| Secret              | Purpose                              |
|---------------------|--------------------------------------|
| `DB_PASSWORD`       | RDS master password                  |
| `SSH_PRIVATE_KEY`   | EC2 SSH access                       |
| `SSH_PUBLIC_KEY`    | Injected into EC2 key pair           |
| `TF_STATE_BUCKET`   | Terraform remote state bucket        |
| `PROJECT_NAME`      | Branch-scoped resource prefix        |

---

## Operations

### View logs

```bash
ssh -i ~/.ssh/deploy_key ubuntu@<HOST> "journalctl -u shortener -f"
```

### Restart the service

```bash
ssh -i ~/.ssh/deploy_key ubuntu@<HOST> "sudo systemctl restart shortener"
```

### Run a migration manually

```bash
ssh -i ~/.ssh/deploy_key ubuntu@<HOST>
cd /opt/shortener
source .env
/opt/shortener/venv/bin/alembic upgrade head
```

### Destroy the stack

Use the UDAP platform **Destroy** action — it runs `terraform destroy` with the same state key.

---

## Cost estimate

| Resource               | Monthly cost (approx.) |
|------------------------|------------------------|
| EC2 t3.micro           | ~$8.50                 |
| RDS db.t3.micro        | ~$13.00                |
| Elastic IP (attached)  | Free                   |
| **Total**              | **~$21–22/mo**         |
