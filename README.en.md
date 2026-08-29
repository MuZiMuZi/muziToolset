# muziToolset

A Maya rigging toolkit focused on maintainable production tools and reusable rig systems.

## Runtime package

The repository root itself is the production Python package:

```text
muziToolset/
├─ app/          # toolbox entry and Maya window management
├─ ui/           # shared theme and reusable widgets
├─ core/         # Maya logic without UI dependencies
├─ tools/        # standalone user-facing tools
├─ systems/      # reusable rig builders and larger workflows
├─ resources/    # icons and controller shape data
└─ legacy_reference/
```

There is no additional `muzi_rigging/` runtime package anymore.

Historical implementations are stored under `legacy_reference/`. They are reference-only and must not be imported by production modules.

## Maya target

- Maya 2023 first
- PySide2 first, with PySide6 fallback where practical
- `maya.cmds` preferred for scene operations
- New production code should not add PyMel dependencies

## Launch

Place the repository where Maya can import `muziToolset`, then run:

```python
import muziToolset
muziToolset.show()
```

## Architecture rules

- `core` must not depend on `ui`, `tools`, `systems`, or `app`.
- `tools` collect user input and call Core/System APIs.
- `systems` contain reusable rig-building workflows.
- `app` owns toolbox discovery and window lifecycle.
- PySide windows are managed by the shared Window Manager.
- Historical code is used only as a source for algorithms that are rewritten into the production architecture.

See `README.md` and `ARCHITECTURE.md` for the detailed project documentation.
