# Muzi Toolset

Muzi Toolset is a **PyMEL-first Maya rigging framework** focused on procedural face rigging.

```text
UI / Tools
    ↓
Systems
    ↓
Core
    ↓
PyMEL
    ↓
Maya
```

Scene nodes, attributes, connections, parenting and constraints use PyMEL directly. Reusable project algorithms live in `core/`; rig business logic lives in `systems/`. Official runtime code does not use `maya.cmds` or restore the old `*_utils` wrapper layer.

Face workflow:

```text
FaceSetup
FaceGuide
FaceBuild
FaceFinalize
```

Open the UI:

```python
import muziToolset.systems.face as face
face.show()
```

Project-owned folders, files, functions, methods and variables use `snake_case`; classes use `PascalCase`.

The last full cmds-based architecture is preserved on `cmds-archive-2026-08-31`; historical implementations also remain under `legacy_reference/`.
