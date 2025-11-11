# Ansible automation

This directory keeps the automation needed to spin up a local Supabase stack with Docker.

## Layout
- `inventory/hosts.ini` – single-host inventory targeting `localhost`.
- `playbooks/install_supabase.yml` – entrypoint playbook that installs Docker (if needed) and launches Supabase.
- `roles/supabase` – self-contained role that downloads Supabase's upstream `docker-compose.yml` and `.env.example` (stored locally as `.env`), then runs `docker compose up -d`.

## Usage
```bash
ansible-playbook -i ansible/inventory/hosts.ini ansible/playbooks/install_supabase.yml
```

The playbook expects:
1. Ansible to run locally with `sudo` privileges (it installs packages, adds the Docker apt repository, and manages Docker).
2. Debian/Ubuntu hosts are supported out of the box—the role adds Docker's official repository and installs `docker-ce`, `docker-compose-plugin`, etc.

### Customisation
You can override role defaults at run time, for example:

```bash
ansible-playbook -i ansible/inventory/hosts.ini ansible/playbooks/install_supabase.yml \
  -e supabase_install_dir=/srv/supabase \
  -e supabase_env_force_overwrite=true
```

Available defaults live in `roles/supabase/defaults/main.yml` and include:
- `supabase_install_dir` – where compose assets are stored (`/opt/supabase` by default).
- `supabase_compose_url` / `supabase_env_url` – upstream resources fetched with `get_url` (defaults point to Supabase's `master` branch).
- `supabase_project_name` – Compose project name to reuse existing containers.
- `supabase_env_force_overwrite` – set to `true` to re-download `.env` on every run (useful when upstream changes but you do not keep manual secrets there).

If you prefer to manage the `.env` file yourself, update it under `{{ supabase_install_dir }}/.env` after the first run and keep `supabase_env_force_overwrite` as `false`.
