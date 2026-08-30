# muziToolset

A Maya rigging toolkit focused on maintainable production tools, reusable Core APIs, and clear rig-system boundaries.

## Runtime package

The repository root itself is the production Python package:

```text
muziToolset/
├─ app/          # toolbox entry and application-level Maya window management
├─ ui/           # shared theme, widgets, and standalone Tool window helpers
├─ core/         # reusable Maya/Python logic without UI dependencies
├─ tools/        # standalone user-facing tools
├─ systems/      # reusable rig builders and larger workflows
├─ resources/    # icons and controller shape data
├─ tests/        # Maya smoke tests and static architecture gates
├─ docs/         # MkDocs documentation
├─ scripts/      # AST API documentation generator
└─ legacy_reference/
```

Historical implementations are stored under `legacy_reference/`. They are reference-only and must not be imported by production modules.

## Maya target

- Maya 2023 first
- PySide2 first, with PySide6 fallback where practical
- `maya.cmds` preferred for scene operations
- New production code should not add PyMel dependencies
- Production module names use `snake_case`; classes use `PascalCase`

## Launch

Place the repository where Maya can import `muziToolset`, then run:

```python
import muziToolset

window = muziToolset.show()
```

## Core naming

Production Core modules use snake_case, for example:

```text
animation_utils.py
scene_utils.py
attr_utils.py
hierarchy_utils.py
joint_utils.py
name_utils.py
rename_utils.py
matrix_utils.py
curve_utils.py
skin_utils.py
```

The former CamelCase compatibility modules have completed migration and were removed:

```text
attrUtils.py
hierarchyUtils.py
jointUtils.py
nameUtils.py
```

A static AST gate prevents these retired module names or files from returning to production code.

## Tool windows

UI Tools support direct use from Maya's Python Script Editor:

```python
from muziToolset.tools.controller import create_ctrl_tool

window = create_ctrl_tool.main()
```

Standalone Tool lifetime is handled by `ui.window_utils`; the main toolbox still uses `app.window_manager` for application-level window behavior.

Non-UI action tools are not forced into a QWidget lifecycle.

## Documentation

MkDocs Material documentation is published at:

```text
https://muzimuzi.github.io/muziToolset/
```

API Reference pages are generated from Python source using the standard-library `ast` module. The generator does not import Maya modules, so documentation can be built on GitHub Actions Linux runners.

## Quality gates

Static CI:

```bash
python tests/core_import_style_test.py
python scripts/generate_mkdocs_reference.py
mkdocs build --strict
```

Maya 2023 runtime checks include:

```python
import muziToolset

muziToolset.pipeline_smoke_test()
muziToolset.extended_core_smoke_test()
muziToolset.tool_window_smoke_test()
```

Recorded Maya 2023 results for the current refactor:

```text
Extended Core Smoke: 6 passed / 0 failed
Tool Window Smoke:   17 passed / 0 failed
```

## Architecture rules

- `core` must not depend on `ui`, `tools`, `systems`, or `app`.
- `tools` collect user input and call Core/System APIs.
- `systems` contain reusable rig-building workflows.
- `ui.window_utils` keeps directly launched standalone UI Tools alive and visible.
- `app.window_manager` owns application-level toolbox window behavior.
- Historical code is used only as a source for algorithms that are rewritten into the production architecture.
- Large one-click workflows must not grow back into a universal Core utility class.

See `README.md`, `ARCHITECTURE.md`, and the MkDocs site for the detailed project documentation.
