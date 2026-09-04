# muziToolset

A Maya 2023 rigging toolkit focused on maintainable production tools, reusable Core APIs, and explicit rig-system boundaries.

Current architecture version: **0.4.0**.

## Runtime package

```text
muziToolset/
├─ app/          # toolbox entry and application-level window management
├─ ui/           # shared theme, widgets, and standalone window helpers
├─ core/         # reusable Maya/Python primitives
├─ tools/        # standalone user-facing tools
├─ systems/      # RigBase, ModuleBase, CtrlBase, and rig systems
├─ resources/    # guide templates and controller shape data
├─ tests/        # Maya smoke tests and static architecture gates
└─ docs/         # MkDocs documentation
```

Historical implementations under `legacy_reference/` are reference-only and must not be imported by production modules.

## Maya target

- Maya 2023 first
- PySide2 first, with PySide6 fallback where practical
- `maya.cmds` preferred for scene operations
- no new PyMel dependencies
- production modules/functions use `snake_case`
- classes use `PascalCase`

## Launch

```python
import muziToolset
window = muziToolset.show()
```

## 0.4 architecture foundations

### RigBase

```text
systems/rig_base.py
```

`RigBase` is an instantiable base class for Rig Object identity. A Rig Object identity contains only:

```text
side
part
index
```

Example:

```python
from muziToolset.systems.rig_base import RigBase

rig = RigBase(
    side="lf",
    part="brow",
    index=1
)

jnt_name = rig.create_name(
    node_type="jnt",
    function="bind"
)

# jnt_lf_brow_bind_001
```

`node_type` and `function` describe the individual Maya node and are not part of the Rig Object identity.

The production naming convention is:

```text
[node_type]_[side]_[part]_[function]_[index]
```

Pure parsing and validation remain class-level operations where appropriate:

```python
fields = RigBase.parse_name(
    "jnt_lf_brow_bind_001"
)

valid = RigBase.validate_name(
    "jnt_lf_brow_bind_001"
)
```

The official naming keyword is `node_type=`. The former `type=` compatibility keyword is retired.

Rig identity and naming no longer belong to Core. The former `core/name_utils.py` has been removed.

`core/rename_utils.py` is limited to generic Maya rename and short-name operations.

### ModuleBase

```text
systems/module_base.py
```

Production business units are called **Modules**, not Components.

Standard lifecycle:

```text
collect_inputs
prepare_data
process_data
finalize_step
```

`RigModuleBase` specializes `process_data` into:

```text
create_jnt
create_controller
create_connection
```

Because `ModuleBase` inherits `RigBase`, each Module carries its own Rig Object identity and naming capability.

The former `systems/component_base.py` has been removed.

### CtrlBase

```text
systems/ctrl_base.py
```

This is the single production controller workflow implementation.

It owns controller hierarchy creation, FK controls, follow, space switch, and space blend behavior.

The former `systems/controller/` package has been removed.

## Face system

```text
systems/face/
├── setup/
├── guide/
├── modules/
├── build/
├── finalize/
├── data/
├── ui/
├── face_base.py
└── config.py
```

The distinction is explicit:

```text
Step
    Setup / Guide / Build / Finalize workflow stage

Module
    complete rig business unit such as Teeth / Jaw / Tongue / Eye

Builder
    reusable build algorithm such as Curve Attachment or Zip Lip

Core
    generic Maya primitive
```

Current production Step 03 module:

```text
TeethModule
```

`FaceBase` uses the default identity `md / face / 001`; concrete business Modules define their own identity, for example `TeethModule` uses `md / teeth / 001`.

## Controller hierarchy

`systems.ctrl_base.create_ctrl()` creates the standard hierarchy:

```text
zero
  ↓
driven
  ↓
space
  ↓
connect
  ↓
offset
  ↓
ctrl
  ↓
output
```

Controller tools and rig modules call `ctrl_base` directly rather than maintaining wrapper builders.

## Quality gates

Static architecture checks include:

```bash
python tests/core_import_style_test.py
python tests/rig_architecture_gate_test.py
python tests/rig_base_contract_test.py
python tests/module_base_contract_test.py
```

Maya 2023 runtime checks include:

```python
import muziToolset

muziToolset.smoke_test()
muziToolset.pipeline_smoke_test()
muziToolset.extended_core_smoke_test()
muziToolset.ctrl_base_smoke_test()
muziToolset.face_build_smoke_test()
muziToolset.rig_integration_test()
muziToolset.maya2023_smoke_test()
muziToolset.functional_smoke_test()
```

`rig_architecture_gate_test.py` prevents retired Component architecture, class-style RigBase naming calls, `RigBase(name=...)`, and the retired `type=` RigBase naming keyword from returning to production code.

## Documentation

The detailed architecture is documented in:

```text
ARCHITECTURE.md
docs/architecture/
docs/development/testing.md
docs/migration/rig-architecture-0.4.md
```

API reference pages are generated from Python source with the standard-library `ast` module, so documentation generation does not require Maya.
