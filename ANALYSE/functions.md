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
- **Route sources**: `digipal/urls_digipal.py`
- **Model clusters**:
  - `Image`, `Graph`, `Annotation`, `Hand`, `Idiograph`, `Allograph`, `Character`
- **UI surfaces**:
  - `digipal/templates/digipal/image_annotation.html`
  - `digipal/templates/digipal/image_annotation_control_bar.html`
  - `digipal/templates/digipal/image_annotation_settings.html`
  - `digipal/templates/digipal/image_allograph.html`
  - `digipal/templates/digipal/dialog.html`

### Function inventory (implemented)

| View function                 | API endpoint                                                                                     | UI triggering action                                                                 | Primary model action                                                                                               | Evidence refs                                                                                                                             |
|-------------------------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `image`                       | `GET /digipal/page/<image_id>/` and tab variants `/allographs                                    | metadata                                                                             | copyright                                                                                                          | pages                                                                                                                                     |hands|texts/` | User opens page image from search/record and lands on annotator page | Reads `Image`, `Annotation` (with `Graph`, `Hand`, `Idiograph`, `Allograph`), prepares form/context | `digipal/views/annotation.py` (`image`), `digipal/urls_digipal.py` |
| `image_annotations`           | `GET /digipal/page/<image_id>/annotations/`                                                      | Annotator boot loads vector/features list (`annotator.url_annotations`)              | Reads `Annotation` (+ editorial), joins `Graph`/components/aspects, returns JSON map by annotation id              | `digipal/templates/digipal/image_annotation.html`, `digipal/views/annotation.py` (`image_annotations`)                                    |
| `image_allographs`            | `GET /digipal/page/<image_id>/image_allographs/`                                                 | In allographs tab, UI refresh (`allographs.js` -> AJAX `image_allographs/`)          | Reads annotations and groups by hand + allograph; returns rendered HTML fragment                                   | `digipal/static/digipal/scripts/allographs.js`, `digipal/views/annotation.py` (`image_allographs`)                                        |
| `get_allographs_by_graph`     | `GET /digipal/page/<image_id>/graph/<graph_id>/allographs_by_graph/`                             | User opens allograph examples from selected annotation (`open_allographs`)           | Reads annotations with same allograph/character on current image; returns preview list JSON                        | `digipal/static/digipal/scripts/annotator-digipal.js` (`open_allographs`), `digipal/views/annotation.py`                                  |
| `get_allographs_by_allograph` | `GET /digipal/page/<image_id>/allographs/<allograph_id>/<character_id>/allographs_by_allograph/` | UI refreshes examples after allograph selection change (`refresh_letters_container`) | Reads annotations filtered by allograph + character; returns JSON list                                             | `digipal/static/digipal/scripts/annotator-digipal.js` (`refresh_letters_container`), `digipal/views/annotation.py`                        |
| `form_dialog`                 | `GET /digipal/page/dialog/<image_id>/`                                                           | Annotator opens edit/create modal (`Dialog.create_dialog`)                           | Reads `Image`, instantiates `ImageAnnotationForm`, returns dialog HTML                                             | `digipal/static/digipal/scripts/dialog.js`, `digipal/views/annotation.py` (`form_dialog`)                                                 |
| `save`                        | `POST /digipal/api/graph/save/<graphs>/`                                                         | User clicks Save annotation(s) in annotator                                          | Creates/updates `Graph`, `Annotation`, `Idiograph`, `GraphComponent`, graph aspects; may update geometry and notes | `digipal/static/digipal/scripts/annotator-digipal.js` (save flow), `digipal/views/annotation.py` (`save`)                                 |
| `save_editorial`              | `POST /digipal/api/graph/save_editorial/<graphs>/`                                               | User saves editorial annotation mode in annotator; also used in lightbox flow        | Creates/updates editorial `Annotation` with geometry/notes; returns annotation payload                             | `digipal/static/digipal/scripts/annotator-digipal.js`, `digipal/static/digipal/scripts/lightbox_basket.js`, `digipal/views/annotation.py` |
| `delete`                      | `POST /digipal/page/<image_id>/delete/<graph_id>/`                                               | User confirms delete on selected annotation (`delete_annotation`)                    | Deletes matching `Annotation` (by `graph` or direct annotation id) in transaction                                  | `digipal/static/digipal/scripts/annotator-digipal.js` (`delete_annotation`), `digipal/views/annotation.py`                                |
| `get_content_type_data`       | `GET /digipal/api/<content_type>/<ids>/` (+ optional format params)                              | API-driven clients and annotation editor utilities (`api_root='/digipal/api/'`)      | Delegates to generic API (`API.process_request`), supports JSON/JSONP/XSLT conversions                             | `digipal/static/digipal/scripts/annotation_editor.js`, `digipal/views/annotation.py` (`get_content_type_data`)                            |
| `get_old_api_request`         | `GET /digipal/api/old/<content_type>/<ids>/<only_features>`                                      | Legacy dialog/allograph feature refresh (`update_onChange`)                          | Legacy reads for graph/allograph/hand feature payloads                                                             | `digipal/static/digipal/scripts/dialog.js` (`update_onChange`), `digipal/views/annotation.py`                                             |
| `get_allograph`               | `GET /digipal/page/<image_id>/graph/<graph_id>/`                                                 | No direct JS trigger found in current annotator scripts (likely legacy/helper)       | Reads `Graph` and returns associated allograph id                                                                  | `digipal/views/annotation.py` (`get_allograph`), `digipal/urls_digipal.py`                                                                |
| `hands_list`                  | `GET /digipal/page/<image_id>/hands_list/?hands=[...]`                                           | No direct JS trigger found in current annotator scripts (likely legacy/helper)       | Reads `Hand` labels for selected ids; returns JSON array                                                           | `digipal/views/annotation.py` (`hands_list`), `digipal/urls_digipal.py`                                                                   |
| `get_vector`                  | `GET /digipal/page/<image_id>/<graph>/graph_vector/`                                             | No direct JS trigger found in current annotator scripts (likely legacy/helper)       | Reads `Annotation` by graph id and returns geojson vector payload                                                  | `digipal/views/annotation.py` (`get_vector`), `digipal/urls_digipal.py`                                                                   |

### Notes for next increment on Group 2
- Validate endpoints flagged as "legacy/helper" against runtime usage logs or browser network traces.
- Split each row into CRUD operation(s) and permission rules (`login_required`, `has_edit_permission`, hidden/editorial filters).

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

### Function inventory (implemented)

| View function                                     | API endpoint                                                    | UI triggering action                                                                             | Primary model action                                                                                                          | Evidence refs                                                                                                                                          |
|---------------------------------------------------|-----------------------------------------------------------------|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `images_lightbox`                                 | `GET /digipal/collection/<collection_name>/images/?data=<json>` | Collection page boot (`lightbox_basket.js` `main()`), when loading current collection table/grid | Reads `Annotation`, `Image`, and `TextUnit` (optional) by IDs from request payload; returns JSON arrays used by collection UI | `digipal/static/digipal/scripts/lightbox_basket.js` (`url_request`), `digipal/views/annotation.py` (`images_lightbox`)                                 |
| `direct_to_template` (collection manager page)    | `GET /digipal/collection/`                                      | User opens “Manage My Collections”                                                               | No direct model action in route; serves `lightbox_basket.html` and client-side collection logic (localStorage)                | `digipal/urls_digipal.py`, `digipal/templates/digipal/lightbox_basket.html`, `digipal/static/digipal/scripts/collections.js`                           |
| `direct_to_template` (single collection page)     | `GET /digipal/collection/<collection_name>/`                    | User opens a collection from manager                                                             | No direct model action in route; serves `collection.html`, then JS calls `/images/` endpoint to resolve IDs to records        | `digipal/urls_digipal.py`, `digipal/templates/digipal/collection.html`, `digipal/static/digipal/scripts/lightbox_basket.js`                            |
| `direct_to_template` (shared collection page)     | `GET /digipal/collection/shared/1/?collection=<json>`           | User opens a shared collection URL created by Share action                                       | No direct model action in route; serves `collection.html`, then JS reads `collection` query payload and calls `/images/`      | `digipal/static/digipal/scripts/collections-utils.js` (`share`), `digipal/urls_digipal.py`, `digipal/static/digipal/scripts/lightbox_basket.js`        |
| `save_editorial` (shared dependency from Group 2) | `POST /digipal/api/graph/save_editorial/<graphs>/`              | In collection table, user edits and saves editorial note (popup in lightbox basket page)         | Updates/creates editorial `Annotation` notes/geometry; response updates UI cache                                              | `digipal/static/digipal/scripts/lightbox_basket.js` (editorial save at `/api/graph/save_editorial/`), `digipal/views/annotation.py` (`save_editorial`) |

### Notes for next increment on Group 3
- Current collection creation/rename/delete/select/share logic is primarily client-side (`localStorage`) in `collections.js`/`lightbox_basket.js`; only data hydration uses server endpoint `images_lightbox`.
- `save_editorial` is listed here as a cross-group dependency because Group 3 UI invokes it, while ownership remains Group 2 (annotation CRUD).

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

### Function inventory (implemented)

| View function           | API endpoint                                                                                                             | UI triggering action                                                                                         | Primary model action                                                                                                                                            | Evidence refs                                                                                                                                                                                                   |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `search_ms_image_view`  | `GET /digipal/page/`                                                                                                     | User opens “Browse Images” page and submits filter form (`search_ms_image.html`)                             | Reads `Image` queryset with repository/date filters, permission filtering, locus sorting, pagination                                                            | `digipal/views/search.py` (`search_ms_image_view`), `digipal/templates/search/search_ms_image.html`                                                                                                             |
| `search_record_view`    | `GET /digipal/search/` and alias `GET /digipal/quicksearch/`                                                             | Quick search submit from top navbar, advanced search form submit (`search_record.html`)                      | Reads multi-content search results via `Search*` content types (`Manuscripts`, `Hands`, `Scribes`, `Graphs`), builds query summary and result tabs              | `digipal/templates/base_default.html` (quick search form), `digipal/templates/search/search_record.html`, `digipal/views/search.py` (`search_record_view`, `set_search_results_to_context`)                     |
| `search_whoosh_view`    | `GET /digipal/search/facets/`                                                                                            | User clicks “Faceted Search” from advanced search; facet links/forms/pagination trigger full or AJAX refresh | Runs Whoosh faceted query, resolves IDs to Django records (`FacetedModel.get_requested_records`), computes facets/sorting/pagination, renders faceted templates | `digipal/templates/search/search_record.html` (`#link-faceted-search`), `digipal/templates/search/faceted/search_whoosh_fragment.html`, `digipal/views/faceted_search/faceted_search.py` (`search_whoosh_view`) |
| `search_suggestions`    | `GET /digipal/search/suggestions.json?q=<term>&l=<n>`                                                                    | Autocomplete on `#search-terms` (quick search + search forms)                                                | Reads suggestion candidates via `SearchContentType.get_suggestions(...)`, returns JSON list                                                                     | `digipal/static/js/search_page.js` (`init_suggestions`), `digipal/views/search.py` (`search_suggestions`)                                                                                                       |
| `record_view`           | `GET /digipal/<content_type>/<objectid>[/<tabid>]/` where `content_type in {hands, manuscripts, scribes, graphs, pages}` | User clicks “View” in search results/content tables; navigates previous/next record links                    | Resolves typed record handler (`process_record_view_request`), reads target record and related data for tab template                                            | `digipal/templates/search/content_type/*.html` (View links), `digipal/views/search.py` (`record_view`)                                                                                                          |
| `index_view`            | `GET /digipal/<content_type>/` where `content_type in {hands, manuscripts, scribes, pages}`                              | User lands on type index pages from internal links/record navigation                                         | Reads index list through content-type adapter (`set_index_view_context`), builds A-Z paging metadata                                                            | `digipal/views/search.py` (`index_view`), `digipal/urls_digipal.py`                                                                                                                                             |
| `catalogue_number_view` | `GET /digipal/catalogue/<source>/<number>/`                                                                              | User opens catalogue permalink (direct link/bookmark/reference)                                              | Reads `CatalogueNumber`, `ItemPartItem`, resolves `ItemPart`, redirects to manuscript/page URL                                                                  | `digipal/views/search.py` (`catalogue_number_view`), `digipal/urls_digipal.py`                                                                                                                                  |
| `search_graph_view`     | `GET /digipal/search/graph/`                                                                                             | Legacy graph-search entry points redirect to unified search page                                             | No direct model action; redirects to `/digipal/search/?basic_search_type=graphs...`                                                                             | `digipal/views/search.py` (`search_graph_view`), `digipal/urls_digipal.py`                                                                                                                                      |
| `search_index_view`     | `GET/POST /digipal/search/index/`                                                                                        | Staff user clicks “Indexing” in footer                                                                       | Index management workflow (Whoosh index stats/reindex/cancel) + package create/remove; primarily indexing/filesystem operations, not core model CRUD            | `digipal/templates/includes/footer.html`, `digipal/views/search.py` (`search_index_view`)                                                                                                                       |

### Notes for next increment on Group 4
- `quicksearch` behaves as route alias of `search_record_view`; no separate implementation.
- `record_view`/`index_view` are polymorphic through content-type classes; next pass can split per content type (`hands`, `manuscripts`, `scribes`, `graphs`, `pages`) if you want finer granularity.

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




