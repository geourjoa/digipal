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

---

## 2026-06-01 - Global synthesis

### Level 1 — IT / Development team

#### System overview
DigiPal is a Django-based (1.x) monolithic web platform for palaeographic research. It is composed of four main layers:
- **`build/`** — Docker/infrastructure packaging, startup, DB bootstrap scripts, dependency manifests.
- **`digipal/`** — Core Django app: rich domain model, views, REST-like API, admin, full-text search, annotation engine.
- **`digipal_text/`** — Companion app for the scholarly text lifecycle (ingest, XML editing, status workflow, image-text linking, pattern analysis).
- **`digipal_project/`** — Minimal project shell (thin `settings.py`/`urls.py` wrappers delegating to `digipal/`).

#### Critical findings (ranked by urgency)

| Priority             | Area                                  | Issue                                                                                                                                                                     | Files                                                                                  |
|----------------------|---------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| **P0 — Immediate**   | Security: secrets                     | Hardcoded DB password (`dppsqlpass`), DB network opened to `0.0.0.0/0`                                                                                                    | `build/repair_digipal_project.sh`, `build/restore_database.sh`                         |
| **P0 — Immediate**   | Security: filesystem                  | World-writable project path (`chmod o+rwx -R`)                                                                                                                            | `build/fix_permissions.sh`                                                             |
| **P0 — Immediate**   | Security: API surface                 | `@csrf_exempt` on write endpoints, permissive CORS (`*`), default `['crud','ALL']` API permission                                                                         | `digipal/views/annotation.py`, `digipal_text/views/patterns.py`, `digipal/settings.py` |
| **P1 — Short-term**  | Infrastructure: EOL stack             | `ubuntu:18.04`, Python 2.7, Django 1.8, PostgreSQL 10 — all EOL with known CVEs                                                                                           | `build/Dockerfile`, `build/requirements.txt`                                           |
| **P1 — Short-term**  | Infrastructure: build reproducibility | Dockerfile clones `develop` branch at build time; no pinned dependency lockfile                                                                                           | `build/Dockerfile`, `build/build-iipsrv.sh`                                            |
| **P1 — Short-term**  | Infrastructure: process management    | `startup.sh` polls in background loops, hides startup failures                                                                                                            | `build/startup.sh`, `build/supervisord.conf`                                           |
| **P2 — Medium-term** | Maintainability: monolith files       | `models.py` (~3 966 lines), `admin.py` (~1 283 lines), `views/viewer.py` (~1 310 lines), `management/commands/extxt.py` (~2 605 lines) — all heavily multi-responsibility | `digipal/`, `digipal_text/`                                                            |
| **P2 — Medium-term** | Maintainability: layering             | Business logic spread across models/views/utils with no service boundary                                                                                                  | `digipal/models.py`, `digipal/views/`, `digipal/utils.py`                              |
| **P2 — Medium-term** | Maintainability: coupling             | Hard dependency from `digipal_text` on `exon.customisations`; cross-app URL/model discovery without abstraction                                                           | `digipal/urls.py`, `digipal_text/views/`                                               |
| **P2 — Medium-term** | Security: input validation            | Unbounded regex/text processing on user-supplied data (DoS risk)                                                                                                          | `digipal_text/views/patterns.py`, `digipal_text/views/viewer.py`                       |
| **P2 — Medium-term** | Testing                               | Near-zero test coverage in `digipal_text/`; narrow tests in `digipal/` vs. app size                                                                                       | `digipal/tests.py`, `digipal_text/`                                                    |
| **P3 — Long-term**   | Modernization                         | Python 3 + Django 4.2 LTS migration required; Mezzanine CMS evaluation                                                                                                    | Full stack                                                                             |

#### Recommended phased action plan

- **Phase 0 (now)**: Externalize secrets to env vars, restrict DB network, fix filesystem permissions, add CSRF guards on write endpoints.
- **Phase 1**: Pin dependency versions + git refs for reproducible builds; run supervisor as PID 1; quarantine deprecated artifacts (`iipsrv.sh`, `lighttpd-iipsrv.conf`, `todo.txt`).
- **Phase 2**: Apply safe patch-level dependency bumps (`Pillow` → `6.2.2`, `requests` → `2.27.1`, `lxml` → `4.3.5`); add input/execution guards on text processing; begin incremental file splitting (start with `models.py`).
- **Phase 3**: Expand test coverage around annotation, API, search, and viewer before any major refactor; introduce service layer boundaries.
- **Phase 4**: Dedicated Python 3 / Django 4.2 / PostgreSQL 16 upgrade stream, with dual-track compatibility testing.

#### Target version matrix (summary)

| Component  | Current      | Short-term           | Long-term        |
|------------|--------------|----------------------|------------------|
| OS         | Ubuntu 18.04 | Freeze (ESM)         | Ubuntu 24.04 LTS |
| Python     | 2.7          | Strict 2.7.18 freeze | 3.11/3.12        |
| Django     | 1.8.18       | 1.11.29 bridge       | 4.2 LTS          |
| PostgreSQL | 10           | 12/13                | 16               |
| Pillow     | 2.6.2        | 6.2.2                | 10.x             |
| Requests   | 2.11.1       | 2.27.1               | 2.32+            |
| lxml       | 3.4.0        | 4.3.5                | 5.x              |
| TypeScript | 2.1.5        | 3.9.x                | 5.x              |

---

### Level 2 — Non-developer / Management / Product team

#### What is the overall health of the software?

**Functional**: The software works and covers a rich domain. It has been built over many years and contains substantial research value.

**Technical age**: The technology underneath is very old. The foundation (programming language, web framework, operating system) has not been updated for several years and is no longer officially supported by its authors.

#### What are the risks?

| Risk                              | Plain-language description                                                                                                                                                                                                        | Level                                 |
|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| Security exposure                 | Some administrative passwords are written directly in configuration files, visible to anyone who can read the server files.                                                                                                       | 🔴 High — to address immediately      |
| Security exposure                 | The web application has some endpoints that are not fully protected against unauthorised write requests.                                                                                                                          | 🔴 High — to address immediately      |
| No safety net if server fails     | The system start-up process can hide failures silently, making diagnosis difficult when something goes wrong.                                                                                                                     | 🟠 Medium                             |
| Hard to update safely             | The software stack (Python, Django framework, database) is EOL (End of Life), meaning manufacturers no longer publish security patches. Running on EOL software means known security vulnerabilities will accumulate without fix. | 🔴 High — structural risk             |
| Hard to maintain                  | Some source files are very large (thousands of lines), making it difficult and time-consuming for developers to make changes without introducing bugs.                                                                            | 🟠 Medium — affects velocity and cost |
| Hard to test                      | There are very few automated tests. Any change to the software carries a risk of breaking something that worked before, and detecting that breakage is mostly manual.                                                             | 🟠 Medium                             |
| Dependency on a specific customer | Parts of the text module are tightly linked to a specific client's customisations, making the software less reusable for other projects.                                                                                          | 🟡 Low-medium                         |

#### What needs to happen — in plain language

1. **Immediately**: remove hardcoded passwords from configuration files and put proper access restrictions in place. This has zero tolerance.
2. **Short-term (next 1–3 months)**: stabilise the deployment infrastructure so that deployments are reproducible and server failures are visible.
3. **Medium-term (next 3–6 months)**: progressively update the key libraries to safer versions (where technically possible without a full rewrite), and start adding automated tests.
4. **Long-term (6–18 months)**: plan and execute a full technology modernisation project (Python 3, modern framework), which will require dedicated developer time and a structured migration budget.

#### Bottom line
The software delivers real value but is running on an ageing and increasingly risky foundation. The immediate security issues can be fixed quickly with limited effort. The deeper modernisation requires planned investment but is necessary to ensure the long-term viability of the platform.

