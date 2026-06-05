# List of Upgrades Needed

> Status as of 2026-06-05. All versions listed were EOL or had known CVEs at time of writing.

---

## 🔴 P0 — Critical / Immediate (Security)

### Python 2.7
- **Current**: 2.7 (EOL January 2020)
- **Short-term target**: Strict 2.7.18 freeze (last release, no new patches)
- **Long-term target**: 3.11 / 3.12
- **Effort**: XL
- **Risk**: High
- **Known issues**: No security patches since EOL. Many CVEs accumulate. `print` as statement (not function) causes syntax errors in Python 3. `dict.iteritems()` used in `settings.py` (L839) breaks on Py3. `importlib==1.0.3` is a Python 2 backport, not needed in Py3.

### Django 1.8.18
- **Current**: 1.8.18 (EOL April 2018)
- **Short-term target**: 1.11.29 (last LTS for Python 2, EOL April 2020)
- **Long-term target**: 4.2 LTS
- **Effort**: XL
- **Risk**: High
- **Known issues**: Multiple CVEs (SQL injection, XSS, CSRF bypass) unfixed since EOL. `MIDDLEWARE_CLASSES` (used in `settings.py` L256) deprecated in 1.10, removed in 2.0. `set_dynamic_settings()` from Mezzanine tied to this version.

### Pillow 2.6.2
- **Current**: 2.6.2 (EOL, released 2014)
- **Short-term target**: 6.2.2 (last Python 2 compatible with security backports)
- **Long-term target**: 10.x
- **Effort**: M
- **Risk**: High
- **Known issues**: CVE-2016-0775, CVE-2016-2533, CVE-2019-19911, CVE-2020-5310 and many others. Remote code execution via crafted image files.

### requests 2.11.1
- **Current**: 2.11.1 (released 2016)
- **Short-term target**: 2.27.1 (last Python 2 compatible)
- **Long-term target**: 2.32+
- **Effort**: S
- **Risk**: Medium
- **Known issues**: CVE-2018-18074 (credential leak via redirect), CVE-2023-32681 (header injection via URL redirect). Missing modern TLS defaults.

### bleach 2.0.0
- **Current**: 2.0.0
- **Short-term target**: 3.3.1 (last Python 2 compatible)
- **Long-term target**: 6.x
- **Effort**: M
- **Risk**: High
- **Known issues**: CVE-2020-6802, CVE-2021-23980 (XSS bypass via malformed HTML). Used for user input sanitization — high risk if outdated.

### lxml 3.4.0
- **Current**: 3.4.0 (released 2014)
- **Short-term target**: 4.3.5 (last with Python 2 + security backports)
- **Long-term target**: 5.x
- **Effort**: M
- **Risk**: High
- **Known issues**: CVE-2018-19787, CVE-2021-28957 (XSS via SVG/HTML parsing). Used heavily in `digipal_text` XML processing.

---

## 🟠 P1 — Short-term (Infrastructure / EOL)

### Ubuntu 18.04 (Docker base image)
- **Current**: `ubuntu:18.04` (EOL standard support April 2023, ESM until 2028)
- **Short-term target**: Keep with ESM or move to `ubuntu:22.04`
- **Long-term target**: `ubuntu:24.04 LTS`
- **Effort**: M
- **Risk**: Medium
- **Known issues**: Many unpatched system-level CVEs. `python` package = Python 2.7 by default; no longer in 22.04+. Affects `build/Dockerfile`.

### PostgreSQL 10
- **Current**: 10 (EOL November 2022)
- **Short-term target**: 12 or 13
- **Long-term target**: 16
- **Effort**: L
- **Risk**: High
- **Known issues**: No security patches. CVE-2023-2454, CVE-2023-2455 among others. pg_hba.conf sets `0.0.0.0/0` trust access (no auth).

### Mezzanine 4.2.3
- **Current**: 4.2.3 (targets Django 1.8–1.11)
- **Short-term target**: Evaluate 6.x (Python 3 / Django 3.2+) — requires significant migration effort
- **Long-term target**: Replace or upgrade as part of Django 4.2 migration
- **Effort**: XL
- **Risk**: High
- **Known issues**: Incompatible with Django 2+. Grappelli/Filebrowser via `grappelli-safe` / `filebrowser_safe` forks — unmaintained.

### oauthlib 0.7.1
- **Current**: 0.7.1 (released 2015)
- **Short-term target**: 3.2.x
- **Effort**: S
- **Risk**: Medium
- **Known issues**: CVE-2022-36087 (ReDoS via crafted redirect URI). Breaks OAuth token validation.

### beautifulsoup4 4.6.0
- **Current**: 4.6.0
- **Short-term target**: 4.9.3 (last Python 2 compatible)
- **Long-term target**: 4.12+
- **Effort**: S
- **Risk**: Low
- **Known issues**: Minor parser inconsistencies fixed in later versions; not a critical CVE risk, but outdated.

### TypeScript 2.1.5
- **Current**: 2.1.5 (released 2016, pinned due to known compilation issue noted in Dockerfile)
- **Short-term target**: 3.9.x (validate against Text Viewer before upgrading)
- **Long-term target**: 5.x
- **Effort**: M
- **Risk**: Medium
- **Known issues**: Missing modern type-checking features; no security patches on that branch.

---

## 🟡 P2 — Medium-term (Deprecated / Maintenance risk)

### django-reversion 1.8.7
- **Current**: 1.8.7 (targets Django 1.8)
- **Target**: 3.x (Python 3 / Django 2.2+)
- **Effort**: M
- **Risk**: Medium
- **Known issues**: API breaking changes from 2.0 onward; must be migrated alongside Django upgrade.

### django-tinymce 2.6.0
- **Current**: 2.6.0 (TinyMCE 3.x-era)
- **Target**: 3.x (TinyMCE 4/5/6 API)
- **Effort**: M
- **Risk**: Medium
- **Known issues**: TinyMCE 3 config keys (`theme_advanced_*`) in `settings.py` will not work with any modern TinyMCE version. XSS sanitization in TinyMCE 3 is weak.

### django-compressor 1.5
- **Current**: 1.5
- **Target**: 4.x
- **Effort**: M
- **Risk**: Medium
- **Known issues**: Incompatible with Django 2.0+; `CSSMinFilter` references a deprecated internal API.

### Whoosh 2.7.3
- **Current**: 2.7.3 (pure-Python, no CVEs but unmaintained since 2015)
- **Target**: Evaluate replacing with PostgreSQL full-text search or Elasticsearch, or pin and accept risk.
- **Effort**: L
- **Risk**: Medium
- **Known issues**: No security patches; not compatible with Python 3 on large corpora without workarounds.

### feedparser 5.1.3
- **Current**: 5.1.3
- **Target**: 6.x (Python 3 compatible)
- **Effort**: S
- **Risk**: Low
- **Known issues**: Python 2-only series; not maintained.

### six 1.10.0
- **Current**: 1.10.0
- **Target**: 1.16.0 (last release, then drop when on Py3)
- **Effort**: S
- **Risk**: Low
- **Known issues**: Compatibility shim only — no risk per se, but upgrade to ensure latest shim coverage.

### pytz 2015.7
- **Current**: 2015.7 (missing 10+ years of timezone data)
- **Target**: 2024.x, then migrate to `zoneinfo` (stdlib, Py3.9+)
- **Effort**: S
- **Risk**: Medium
- **Known issues**: Incorrect DST/offset calculations for timezones updated since 2015. Affects all datetime logic.

### html5lib 0.999999999
- **Current**: 0.999999999 (pinned by bleach; this pre-release version had parser bugs)
- **Target**: 1.1
- **Effort**: S
- **Risk**: Medium
- **Known issues**: XSS parsing inconsistencies; used as bleach's HTML parser backend.

---

## Notes

- `importlib==1.0.3` — Python 2 stdlib backport; **remove** entirely on Python 3 migration. **Effort**: S. **Risk**: Low.
- `disqus-python 0.4.2` — Disqus API client; Disqus deprecated its API in 2018. Evaluate removal. **Effort**: S. **Risk**: Low.
- `django-contrib-comments < 1.9.0` — version cap exists to work around a Mezzanine incompatibility; remove cap when upgrading Mezzanine. **Effort**: M. **Risk**: Medium.
- Git-pinned forks (`geoffroy-noel-ddh/Digital-Lightbox`, `django-iipimage`, `django-pagination`) — no version pinning; **pin to a specific commit hash** for build reproducibility. **Effort**: S. **Risk**: Low.
