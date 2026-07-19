# myshortner05 — Working Notes

## Status
- Plan approved. Generation in progress.

## Stack decisions
- FastAPI (not in scaffold catalog, written manually) + Uvicorn 2 workers
- Alembic migrations — env.py reads DATABASE_URL from env (not alembic.ini) to avoid configparser '%' interpolation bug
- RDS Postgres 16, single-AZ db.t3.micro, not publicly accessible
- EC2 t3.micro Ubuntu 22.04 (ami: ubuntu-jammy, owner 099720109477)
- Elastic IP output (not ephemeral) so verify stage gets a stable IP
- App runs as non-root 'shortener' system user under systemd

## Key contracts
- DB_PASSWORD secret: alphanumeric ≥20 chars (set via set_pipeline_secret before deploy)
- Pipeline configure stage passes DB_PASSWORD + RDS_ENDPOINT as env to ansible-playbook
- Ansible env.j2 template builds DATABASE_URL from those env vars (no_log: true on task)
- ansible/templates/ houses env.j2 and shortener.service.j2
- rds_endpoint output is RDS hostname only (no port) — port appended in DATABASE_URL string

## What remains
- [ ] Set DB_PASSWORD secret
- [ ] create_repo_and_push
- [ ] deploy

## Gotchas
- GitHub SILENTLY DROPS job outputs containing masked secret substrings — rds_endpoint / instance_ip are infra values not derived from secrets so they are safe to thread via outputs
- Alembic env.py overrides sqlalchemy.url from os.environ["DATABASE_URL"] — never use alembic.ini url line for real credentials
- ansible posix.synchronize requires rsync on both ends — Ubuntu 22.04 has it; added to pre_tasks implicitly via apt
