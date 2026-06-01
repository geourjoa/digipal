# DigiPal Django App Review (`digipal/`)

## Scope
- Reviewed core app architecture in `digipal/`: routing, settings, models, views, API, admin, middleware, signals, and tests.

## Architecture snapshot
- **Style**: legacy monolith Django app (Django 1.x era patterns) with strong domain model and integrated CMS (Mezzanine).
- **Main layers**:
  - `models.py`: core domain + business logic (very large, ~3966 lines).
  - `views/`: UI/API/business flow orchestration (several very large modules).
  - `admin.py`: extensive back-office configuration (very large, ~1283 lines).
  - `api/`: reflective generic API with content-type specific overrides.
  - `settings.py`: central configuration plus dynamic/DB-overridable settings.

## Pros
| Area                    | What is good                                                                                                                               | Evidence                                                                             |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Domain richness         | Data model captures palaeographic domain deeply (annotations, graphs, hands, manuscripts, permissions, etc.).                              | `digipal/models.py`                                                                  |
| Functional completeness | App includes full stack in one place: public views, annotator, search, faceted search, API, admin customizations, import/export utilities. | `digipal/views/`, `digipal/api/`, `digipal/admin.py`, `digipal/management/commands/` |
| Configurability         | Many behavior toggles and override points (`local_settings`, dynamic Mezzanine settings, custom apps).                                     | `digipal/settings.py`, `digipal/defaults.py`                                         |
| Performance awareness   | Uses select/prefetch patterns in search modules and custom cache patch for known Django 1.8 file cache issue.                              | `digipal/views/faceted_search/faceted_search.py`, `digipal/middleware.py`            |
| Operational pragmatism  | Includes migration/patch compatibility code and runtime fixes for third-party limitations.                                                 | `digipal/patches.py`, `digipal/signals.py`                                           |

## Cons
| Area                      | Main issue                                                                                              | Why this is a problem                                                        | Evidence                                                                                   |
|---------------------------|---------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Modularity                | Core files are very large and multi-responsibility (`models.py`, `admin.py`, `utils.py`, large views).  | High cognitive load, harder onboarding, harder isolated refactoring/testing. | `digipal/models.py`, `digipal/admin.py`, `digipal/utils.py`, `digipal/views/annotation.py` |
| Layering                  | Business logic spread across models/views/utils without clear service boundary.                         | Tight coupling; behavior changes require touching many places.               | `digipal/models.py`, `digipal/views/search.py`, `digipal/utils.py`                         |
| Coupling across apps      | Hard-coded dependency between `digipal` and `digipal_text` in URL/API/model discovery.                  | Limits independent evolution and increases regression risk.                  | `digipal/urls.py` (TODO note), `digipal/api/generic.py`                                    |
| API security posture      | `@csrf_exempt` endpoints, permissive CORS (`*`), and broad default API permission (`[['crud','ALL']]`). | Raises risk for misuse/exposure if deployment config is weak.                | `digipal/views/annotation.py`, `digipal/views/search.py`, `digipal/settings.py`            |
| Legacy framework patterns | Old URL style (`patterns`), Python2 syntax/import style, monkey patches to framework internals.         | Upgrade complexity and fragile behavior on dependency changes.               | `digipal/urls*.py`, `digipal/patches.py`, multiple Python2-style modules                   |
| Admin complexity          | Very large centralized admin configuration with broad imports and custom behavior.                      | Difficult to maintain safely; high regression surface for admin changes.     | `digipal/admin.py`                                                                         |
| Test depth                | Tests exist but are relatively narrow compared to app size and complexity.                              | Low confidence during refactor/upgrade; higher change risk.                  | `digipal/tests.py` vs module sizes                                                         |

## Overall assessment
- **Strength**: feature-rich, domain-focused, battle-tested monolith.
- **Weakness**: maintainability and upgradeability are constrained by file size, tight coupling, and legacy patterns.

## Recommended priorities
1. **Stabilize boundaries**: introduce service modules for critical flows (annotation save, search, API write paths) before deep upgrades.
2. **Harden API surface**: reduce `csrf_exempt` usage, tighten default permissions, and restrict CORS policy.
3. **Split monolith files incrementally**: start with `models.py` (domain packages) and `admin.py` (per-domain admin modules).
4. **Increase safety net**: expand tests around annotator, API, and search indexing behavior before refactoring.
5. **Prepare modernization track**: progressive Django/Python upgrade path with compatibility test matrix.

