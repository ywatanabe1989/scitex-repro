---
name: scitex-repro-env-vars
description: Environment variables read by scitex-repro at import / runtime. Follow SCITEX_<MODULE>_* convention — see general/10_arch-environment-variables.md.
---

# scitex-repro — Environment Variables

| Variable | Purpose | Default | Type |
|---|---|---|---|
| `SCITEX_DIR` | Base SciTeX data / cache directory (shared across ecosystem). Used for resolving reproducibility artefacts. | `~/.scitex` | path |

## Notes

- `SCITEX_DIR` is an **ecosystem-wide** variable (not `SCITEX_REPRO_*`); scitex-repro reads it read-only to anchor artefact paths.
- scitex-repro defines no module-private `SCITEX_REPRO_*` vars yet. Add any new vars under that prefix per the ecosystem convention.

## Audit

```bash
grep -rhoE 'SCITEX_[A-Z0-9_]+' $HOME/proj/scitex-repro/src/ | sort -u
```
