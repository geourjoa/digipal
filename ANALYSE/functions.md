# Implemented Functionalities - Grouped Inventory (Increment 1)

This first increment identifies related groups of functionalities.
Next increment will list individual functions per group with endpoint + UI trigger + model action.

## 1) Site Shell, CMS, and Authentication
- **Scope**: homepage, CMS/blog pages, auth, error/static service routes.
- **Key routes**:
  - `/` (`home` template)
  - `/login/`, `/logout/`
  - `/blog/search/`
  - `/robots.txt`
  - `/404`, `/500`
- **Route sources**: `digipal/urls.py`
- **Model clusters**:
  - `CarouselItem` (homepage carousel)
- **UI surfaces**:
  - `digipal/templates/home.html`
  - `digipal/templates/registration/*`
  - `digipal/templates/errors/*`
  - Mezzanine page templates under `digipal/templates/pages/*`

## 2) Image Annotation and Graph Editing
- **Scope**: manuscript page image viewer, graph/allograph retrieval, annotation CRUD, vector handling.
- **Key routes**:
  - `/digipal/page/<image_id>/`
  - `/digipal/page/<image_id>/annotations/`
  - `/digipal/page/<image_id>/image_allographs/`
  - `/digipal/api/graph/save/<graphs>/`
  - `/digipal/api/graph/save_editorial/<graphs>/`
  - `/digipal/page/<image_id>/delete/<graph_id>/`
  - `/digipal/page/<image_id>/<graph>/graph_vector/`
- **Route sources**: `digipal/urls_digipal.py`
- **Model clusters**:
  - `Image`, `Graph`, `Annotation`, `Hand`, `Idiograph`, `Allograph`, `Character`
- **UI surfaces**:
  - `digipal/templates/digipal/image_annotation.html`
  - `digipal/templates/digipal/image_annotation_control_bar.html`
  - `digipal/templates/digipal/image_annotation_settings.html`
  - `digipal/templates/digipal/image_allograph.html`
  - `digipal/templates/digipal/dialog.html`

## 3) Collection and Lightbox Workflows
- **Scope**: image collections, shared collection state, basket/lightbox interactions.
- **Key routes**:
  - `/digipal/collection/`
  - `/digipal/collection/<collection_name>/`
  - `/digipal/collection/<collection_name>/images/`
  - `/digipal/collection/shared/1/`
- **Route sources**: `digipal/urls_digipal.py`
- **Model clusters**:
  - `Image`, `ItemPart` (collection-related displayed entities)
- **UI surfaces**:
  - `digipal/templates/digipal/collection.html`
  - `digipal/templates/digipal/lightbox_basket.html`
  - `digipal/templates/digipal/add_to_collection.html`

## 4) Search, Browse, Records, and Faceted Discovery
- **Scope**: classic search, quick search, graph search, suggestions, record/index pages, facets.
- **Key routes**:
  - `/digipal/page/`
  - `/digipal/search/`, `/digipal/quicksearch/`
  - `/digipal/search/index/`
  - `/digipal/search/graph/`
  - `/digipal/search/suggestions.json`
  - `/digipal/<content_type>/<objectid>/...` (record view)
  - `/digipal/<content_type>/` (index view)
  - `/digipal/catalogue/<source>/<number>/`
  - `/digipal/search/facets/`
- **Route sources**: `digipal/urls_digipal.py`
- **Model clusters**:
  - `ItemPart`, `Image`, `Hand`, `Graph`, `Scribe` (+ related catalogue entities)
- **UI surfaces**:
  - `digipal/templates/search/*`
  - `digipal/templates/search_results.html`
  - `digipal/templates/digipal/folio_image.html`
  - `digipal/templates/digipal/hands.html`

## 5) Text Viewer, Text API, and Pattern Analysis
- **Scope**: manuscript text viewer modes, text API endpoints, pattern exploration APIs.
- **Key routes**:
  - `/digipal/manuscripts/<id>/texts/view/...`
  - `/digipal/manuscripts/<id>/texts/...` (text API variants)
  - `/digipal/patterns/`
  - `/digipal_text/api/patterns/...`
  - `/digipal_text/api/move_pattern/...`
  - `/digipal_text/api/segunits/...`
- **Route sources**: `digipal_text/urls.py`
- **Model clusters**:
  - `TextContentType`, `TextContent`, `TextContentXML`, `TextAnnotation`, `TextPattern`, `EntryHand`
- **UI surfaces**:
  - `digipal_text/templates/digipal_text/text_viewer.html`
  - `digipal_text/templates/digipal_text/text_view.html`
  - `digipal_text/templates/digipal_text/patterns.html`
  - `digipal_text/templates/digipal_text/patterns_fragment.html`

## 6) Editorial and Django-Admin Extensions
- **Scope**: admin context tools, bulk/admin import, idiograph editor, Stewart import/match, quick add.
- **Key routes**:
  - `/admin/digipal/.../context/`
  - `/admin/digipal/instances/`
  - `/admin/digipal/<model>/import/`
  - `/admin/digipal/stewartrecord/match`
  - `/admin/digipal/stewartrecord/import`
  - `/admin/digipal/idiograph_editor/...`
  - `/digipal/admin/image/bulk_edit`
- **Route sources**: `digipal/urls_admin.py`, `digipal/urls_digipal.py`
- **Model clusters**:
  - `StewartRecord`, `Idiograph`, `ItemPart`, `Image`, and admin-managed DigiPal models
- **UI surfaces**:
  - `digipal/templates/digipal/admin_edit.html`
  - Admin UI + custom idiograph/editor templates served by admin views

## Next increment
For each group, produce a function-level table with:
1. **Function / View name**
2. **API endpoint (HTTP path)**
3. **UI triggering action (button/link/page interaction)**
4. **Primary model write/read action**
5. **Template or JS entry point**

