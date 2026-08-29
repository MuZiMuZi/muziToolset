# muziToolset

A Maya rigging toolkit focused on maintainable production tools and reusable rig systems.

## Runtime package

The current production code lives in:

```text
muzi_rigging/
├─ app/          # toolbox entry and Maya window management
├─ ui/           # shared theme and reusable widgets
├─ core/         # Maya logic without UI dependencies
├─ tools/        # standalone user-facing tools
├─ systems/      # reusable rig builders and larger workflows
└─ resources/    # icons and controller shape data
```

Historical implementations are stored under:

```text
legacy_reference/
```

They are reference-only and must not be imported by production modules.

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

- `core` must not depend on `ui`, `tools`, or `systems`.
- `tools` collect user input and call Core/System APIs.
- `systems` contain reusable rig-building workflows.
- PySide windows are managed by the shared Window Manager.
- Historical code is used only as a source for algorithms that are rewritten into the production architecture.

See `README.md` and `muzi_rigging/ARCHITECTURE.md` for the detailed Chinese project documentation.
