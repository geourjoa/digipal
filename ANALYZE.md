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

