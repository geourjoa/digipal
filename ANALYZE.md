# Software Review Notes

## 2026-06-01 - Repository folder utility map

### Top-level folders
- `build/`: deployment/infrastructure layer (Docker/runtime scripts, bootstrap, upgrades, repair tooling).
- `digipal/`: main Django app (core models, views, API, templates/static, migrations, management commands).
- `digipal_project/`: Django project wrapper (project-level settings/URL wiring).
- `digipal_text/`: companion Django app for text/transcription workflows.

### Key subfolders
- `build/archetype/`: starter/demo deployment artifacts.
- `build/schema_upgrades/`: manual SQL upgrade scripts.
- `digipal/api/`: core API endpoints/helpers.
- `digipal/doc/`: product/admin/developer docs.
- `digipal/iipfield/`: image server/storage integration helpers.
- `digipal/management/commands/`: custom Django CLI commands.
- `digipal/migrations/`: schema history for `digipal`.
- `digipal/static/`, `digipal/templates/`: assets + templates.
- `digipal/views/`: core web views/controllers.
- `digipal_text/management/commands/`: text module CLI tasks.
- `digipal_text/migrations/`: schema history for `digipal_text`.
- `digipal_text/static/`, `digipal_text/templates/`, `digipal_text/views/`: text UI + endpoints.
- `digipal_text/doc/`: text module docs.

### Architecture snapshot
- `digipal` = core manuscript/image/annotation platform.
- `digipal_text` = text/transcription extension.
- `digipal_project` = project glue/config.
- `build` = deployment packaging and operational automation.

## 2026-06-01 - Build folder deep review

### What is inside `build/`
- **Container build/runtime**: `Dockerfile`, `startup.sh`, `supervisord.conf`, `nginx.conf`, `wsgi.ini`, `wsgi.py`, `uwsgi_params`, `iipsrv_params`.
- **Bootstrap/upgrade scripts**: `repair_digipal_project.sh`, `upgrade_project_content.sh`, `restore_database.sh`, `fix_permissions.sh`.
- **Image server build**: `build-iipsrv.sh` (builds `iipsrv` from source).
- **Python dependency manifests**: `prerequirements.txt`, `requirements.txt`, `unrequirements.txt`.
- **Initial app fixtures**: `data_init.json`, `data_char.json`, `data_menu.json`, `data_test.json`.
- **Legacy/maintenance utilities**: `zip_digipal_project.py`, `jscmp.py`, `todo.txt`, deprecated `iipsrv.sh`, `lighttpd-iipsrv.conf`.
- **Packaged archetype assets**: `archetype/` (`Dockerfile`, `startup.sh`, `compose.yaml`, `archetype.tar.gz`).
- **Manual SQL migration patch**: `schema_upgrades/1.2.2.sql`.

### What can be better (prioritized)
1. **Critical security baseline**
   - `build/requirements.txt` pins very old dependencies (`Django==1.8.18`, `Pillow==2.6.2`, `requests==2.11.1`, etc.).
   - CVE check confirms multiple known vulnerabilities on these pins.
   - Action: define an upgrade path (at least Python/Django LTS target) and lock with `pip-compile`/constraints.
   - 

2. **Secrets and DB hardening**
   - `build/repair_digipal_project.sh` creates DB user with hardcoded password (`dppsqlpass`) and opens host auth to `0.0.0.0/0`.
   - Action: move credentials/network policy to env vars + restrict DB exposure by default.

3. **Permissions model is too broad**
   - `build/fix_permissions.sh` applies `chmod o+rwx -R digipal_project`.
   - Action: replace world-writable permissions with group-based ACLs for `www-data`/`postgres` only.

4. **Build reproducibility and lifecycle**
   - `build/Dockerfile` uses EOL stack (`ubuntu:18.04`, Python 2 toolchain, apt packages without pinning) and clones `develop` branch at build time.
   - Action: use pinned commit/tag, multi-stage build, reproducible base image, explicit package versions.

5. **Entrypoint/process management robustness**
   - `build/startup.sh` uses polling loop + background `supervisord`; shutdown relies on pid file handling.
   - Action: run `supervisord` as PID 1 directly (or use tini), simplify traps, fail fast on service startup errors.

6. **Technical debt cleanup**
   - Deprecated artifacts remain active in tree (`iipsrv.sh`, `lighttpd-iipsrv.conf`, WIP `archetype/compose.yaml`, legacy notes in `todo.txt`).
   - Action: archive/remove deprecated files or clearly separate `legacy/` to reduce operator confusion.

### Recommended phased plan
- **Phase 1 (low effort/high impact)**: remove hardcoded secrets, tighten permissions, clean deprecated files, document expected env vars.
- **Phase 2 (medium)**: modernize entrypoint/supervisor flow and make build deterministic (pin git ref + dependency lock).
- **Phase 3 (high)**: platform upgrade path (Python 3 + modern Django/Mezzanine equivalents), with migration test matrix.

## 2026-06-01 - Proposed patch set (`build/`) 

| Priority | Patch set                                    | Scope (main files)                                                                                                    | Effort | Why needed                                                                                             | Risk reduction        | Migration notes                                                                                                                               |
|----------|----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|--------|--------------------------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| P0       | Secrets externalization + DB access lockdown | `build/repair_digipal_project.sh`, `build/restore_database.sh`, `build/startup.sh`, `build/supervisord.conf`          | M      | Removes hardcoded DB password and open `0.0.0.0/0` auth pattern; enforces least privilege defaults.    | Very high             | Add env vars (`DP_DB_USER`, `DP_DB_PASSWORD`, `DP_DB_HOST_CIDR`), default to local-only access, require explicit opt-in for remote DB access. |
| P0       | Filesystem permission hardening              | `build/fix_permissions.sh`, `build/repair_digipal_project.sh`, `build/upgrade_project_content.sh`, `build/startup.sh` | S      | Current world-writable project path (`chmod o+rwx`) allows tampering/corruption and weakens isolation. | High                  | Switch to group-based rights (`www-data`, `postgres`) + minimal ACL; optional compatibility flag for legacy host-mounted volumes.             |
| P1       | Reproducible legacy image build              | `build/Dockerfile`, `build/build-iipsrv.sh`                                                                           | M      | Build currently depends on moving targets (`develop` branch clone, unpinned system stack).             | High                  | Pin git ref (tag/commit), pin iipsrv revision/checksum, document tested base-image digest for repeatable builds.                              |
| P1       | Entrypoint/process supervision stabilization | `build/startup.sh`, `build/supervisord.conf`, `build/archetype/startup.sh`                                            | M      | Poll loops + background supervisor/PID handling can hide startup failures and complicate shutdown.     | Medium-high           | Run supervisor as PID 1 (or with `tini`), fail-fast checks, explicit signal handling, remove infinite sleep loops.                            |
| P2       | Dependency containment for legacy runtime    | `build/prerequirements.txt`, `build/requirements.txt`, `build/unrequirements.txt`                                     | M      | Current stack has many known CVEs; ad-hoc upgrades risk breakage in Python2/Django1.8 context.         | Medium                | Introduce constraints lockfile, apply only compatible patch-level bumps first, keep a tested frozen legacy profile.                           |
| P2       | Legacy artifact quarantine                   | `build/iipsrv.sh`, `build/lighttpd-iipsrv.conf`, `build/todo.txt`, `build/archetype/compose.yaml`                     | S      | Deprecated/WIP files increase operator confusion and misconfiguration risk.                            | Medium                | Move deprecated assets under `build/legacy/` or mark unsupported clearly in headers/README.                                                   |
| P3       | Modernization bridge (parallel track)        | `build/Dockerfile` (modern variant), `build/requirements*`, `build/startup.sh`                                        | L      | Python2 + old OS/toolchain are EOL; long-term maintenance/security impossible otherwise.               | Very high (long-term) | Maintain dual track (`legacy` + `modern`) and migrate infra/runtime in waves to limit regressions.                                            |

### Order rationale
- **P0 first**: immediate risk controls (secrets + permissions) with low migration blast radius.
- **P1 second**: stabilize runtime behavior and make builds reproducible before deeper upgrades.
- **P2 third**: reduce operational confusion and control dependency drift on the legacy branch.
- **P3 last**: structural modernization requiring dedicated migration/testing budget.

## 2026-06-01 - Obsolete component/version scan (`build/`)

| Component                           | Found version/pattern                                              | File                        | Why obsolete/risky                                                                                              |
|-------------------------------------|--------------------------------------------------------------------|-----------------------------|-----------------------------------------------------------------------------------------------------------------|
| Ubuntu base image                   | `ubuntu:18.04`                                                     | `build/Dockerfile`          | 18.04 is end-of-life for standard support; security patch coverage is limited/ended without special support.    |
| Python runtime/tooling              | `python`, `python-pip`, `python-dev`, `pip2`, `python2 get-pip.py` | `build/Dockerfile`          | Python 2 ecosystem is EOL; many packages no longer provide security/compatibility updates.                      |
| Django                              | `Django==1.8.18`                                                   | `build/requirements.txt`    | Django 1.8 is long EOL; known vulnerabilities and no maintained upstream fixes.                                 |
| PostgreSQL binary path              | `/usr/lib/postgresql/10/...`                                       | `build/supervisord.conf`    | PostgreSQL 10 is EOL; fixed version path also reduces portability across base images.                           |
| TypeScript toolchain                | `typescript@2.1.5`                                                 | `build/Dockerfile`          | Very old compiler; potential incompatibility and unmaintained dependency chain.                                 |
| Pillow                              | `Pillow==2.6.2`                                                    | `build/requirements.txt`    | Very old release with many known CVEs in image parsing code paths.                                              |
| Requests                            | `requests==2.11.1`                                                 | `build/requirements.txt`    | Very old release with known security advisories (redirect/proxy/TLS-related history).                           |
| lxml                                | `lxml==3.4.0`                                                      | `build/requirements.txt`    | Old parser/sanitizer stack with multiple known advisories over time.                                            |
| Mezzanine                           | `Mezzanine==4.2.3`                                                 | `build/requirements.txt`    | Old CMS release line; limited maintenance relative to current versions.                                         |
| IIPImage server source tag          | `iipsrv-1.2`                                                       | `build/build-iipsrv.sh`     | Likely legacy release (script itself notes newer build issues); should be reviewed for support/security status. |
| Legacy migration compatibility code | `Pre Django 1.7`, `v1.2.2`, `v1.0` upgrade path                    | `build/restore_database.sh` | Indicates compatibility burden for very old DB states; increases maintenance and test surface.                  |

### Notes
- This scan identifies **version obsolescence signals** from pinned versions and runtime paths.
- CVE validation already confirmed high-risk exposure on several pinned Python dependencies in `build/requirements.txt`.

## 2026-06-01 - Target version matrix (`build/`)

| Component         | Current                            | Short-term target (minimal-change)                             | Long-term target (modernized)                  | Effort | Why this target                                                                     |
|-------------------|------------------------------------|----------------------------------------------------------------|------------------------------------------------|--------|-------------------------------------------------------------------------------------|
| Ubuntu base image | `18.04`                            | Keep `18.04` only as temporary frozen baseline (or ESM-backed) | `24.04 LTS`                                    | M      | Avoid immediate breakage now; full security posture needs modern LTS base.          |
| Python runtime    | `2.7` toolchain (`python`, `pip2`) | Freeze to strict `2.7.18` constraints (no drift)               | `3.11` (or `3.12` after validation)            | L      | Python 2 is EOL; modern dependency/security updates require Python 3.               |
| Django            | `1.8.18`                           | Bridge to `1.11.29` **if compatible**                          | `4.2 LTS` (or `5.x`)                           | L      | `1.8` is EOL; bridge step can reduce migration shock before LTS jump.               |
| Mezzanine         | `4.2.3`                            | `4.3.x` (compatibility-gated)                                  | Latest maintained line or CMS replacement path | L      | Main compatibility constraint in stack; may drive app refactor decisions.           |
| PostgreSQL        | `10` (hardcoded path)              | `12/13`                                                        | `16`                                           | M      | `10` is EOL; staged DB upgrades are safer than one-step major jumps.                |
| TypeScript        | `2.1.5`                            | `3.9.x`                                                        | `5.x`                                          | M      | Reduce frontend toolchain obsolescence with lower break risk via intermediate step. |
| Pillow            | `2.6.2`                            | `6.2.2` (Py2-era ceiling candidate; validate)                  | `10.x`                                         | M      | Significant security improvement short-term; modern secure line requires Python 3.  |
| Requests          | `2.11.1`                           | `2.27.1` (Py2-era ceiling candidate; validate)                 | `2.32+`                                        | S      | Fast risk reduction possible with minimal app impact before full migration.         |
| lxml              | `3.4.0`                            | `4.3.5` (Py2-era ceiling candidate; validate)                  | `5.x`/`6.x`                                    | M      | Parser/sanitizer security and stability improve materially with newer lines.        |
| iipsrv            | `iipsrv-1.2`                       | Keep `1.2` but pin commit + hardening                          | `1.3+` or maintained fork                      | M      | Script already reports 1.3 build issues; requires controlled build validation.      |

### Validation notes
- **Compatibility checkpoints required**: Django <-> Mezzanine, and Python2 ceiling versions (`Pillow`, `requests`, `lxml`).
- **Recommended strategy**: lock short-term targets first (stabilize), then execute Python3/Django modernization as a dedicated stream.
