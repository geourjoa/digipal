# `digipal_text/` folder review

## Purpose
- `digipal_text/` is the text-processing companion app for `digipal/`.
- It manages transcription/translation content, text viewer/editor endpoints, text-to-image linking, and pattern analysis.

## What is inside
- `models.py`: text domain models (`TextContent`, `TextContentXML`, statuses, annotations, patterns, entry-hand links).
- `views/`:
  - `viewer.py`: text viewer UI + text API endpoints.
  - `patterns.py`: pattern analysis UI/API.
  - `pdfview.py`: HTML-to-PDF rendering helper.
  - `test.py`: debug/testing endpoints.
- `urls.py`: routes for manuscript text viewer/API and pattern API.
- `admin.py`: admin screens/filters for text content, XML status workflow, duplicate/empty detection.
- `management/commands/`:
  - `dptext.py`: import/export/transform/fix text operations.
  - `extxt.py`: additional text tooling.
- `templates/digipal_text/`: text viewer templates.
- `static/digipal_text/`: viewer/editor frontend assets.
- `migrations/`: schema evolution history.
- `doc/`: module-specific docs.

## Data model signal (from `migrations/0001_initial.py`)
- Core entities:
  - `TextContentType`: taxonomy of text types.
  - `TextContent`: text metadata per `ItemPart` and type.
  - `TextContentXML`: the XML body + workflow status.
  - `TextContentXMLStatus`: editorial workflow states.
  - `TextAnnotation`: links text element IDs to image annotations.
  - `EntryHand`: hand assignment at entry level.
  - `TextPattern`: reusable regex/segment patterns.
  - `TextContentXMLCopy`: text snapshots/versions.
- This confirms the app is designed for a full editorial workflow: storage, status, linkage, and analysis.

## Short conclusion
- `digipal_text/` is a feature-complete text subsystem layered on top of the manuscript/image core in `digipal/`.
- It is responsible for the scholarly text lifecycle: ingest -> edit/view -> annotate/link -> analyse/export.

## Maintainability concerns
- **Large multi-responsibility modules**: `views/viewer.py` (~1310 lines), `views/patterns.py` (~726), `models.py` (~557), `management/commands/extxt.py` (~2605), `management/commands/dptext.py` (~693), `admin.py` (~214).
  - Impact: high cognitive load and difficult isolated refactoring.
- **Tight project-specific coupling** to Exon customisations (`from exon.customisations...`) in runtime paths and commands.
  - Impact: portability/reuse is reduced; deployments without those modules can fail or require special handling.
- **Legacy ORM/API patterns** in admin (`.raw()`, `.extra()`) and broad backward-compatible code style.
  - Impact: harder framework upgrades and higher maintenance friction.
- **Weak test safety net**: no test suite found under `digipal_text/` (`TestCase`/`pytest` patterns not found).
  - Impact: higher regression risk for text viewer/API and transformation workflows.

## Security concerns
- **CSRF disabled on pattern endpoints**: `@csrf_exempt` on `patterns_view` and `patterns_api_view`.
  - Files: `digipal_text/views/patterns.py`.
  - Risk: write operations (`POST`/`PUT`/`DELETE` logic in API handler) become vulnerable if session-authenticated contexts are reachable.
- **Potential unbounded processing on user-controlled data** in pattern analysis and text processing endpoints.
  - Files: `digipal_text/views/patterns.py`, `digipal_text/views/viewer.py`.
  - Risk: expensive regex/text operations may enable resource exhaustion (DoS-style behavior) on large payloads.
- **Raw SQL usage in admin filters** (`.raw()`) and `.extra()` expressions.
  - File: `digipal_text/admin.py`.
  - Risk: current queries are static (low injection risk here), but they increase long-term audit and upgrade risk.
- **Legacy dependency/runtime context** (Python2/Django1.x patterns inherited from project architecture).
  - Risk: reduced upstream security coverage and patchability.

## Recommended priorities (short)
1. Re-enable CSRF protection (or scoped token/auth strategy) on pattern write endpoints first.
2. Add input and execution guards for pattern/text processing (size/time limits, stricter validation).
3. Introduce tests around `viewer` and `patterns` critical paths before refactoring.
4. Reduce coupling to `exon.customisations` behind adapters/feature flags.
5. Gradually replace `.raw()`/`.extra()` with ORM-safe equivalents during upgrade prep.
