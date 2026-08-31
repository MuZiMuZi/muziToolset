# Muzi Toolset

Muzi Toolset is being rebuilt as a **PyMEL-first Maya rigging framework**.

The runtime architecture is intentionally small:

```text
core/                 reusable rig algorithms and project rules
systems/              rig systems and components
systems/face/         active Face Rig migration target
tools/                new user-tool layer
legacy_reference/     historical implementations, reference only
```

PyMEL is the default Maya node interaction layer. The framework does not recreate wrapper classes for basic Joint, Transform, Attribute, parenting, or connection operations that PyMEL already expresses clearly.

Old APIs are not maintained for compatibility. Historical tools will be rebuilt against the new architecture when needed.

See `ARCHITECTURE.md` and `systems/face/PYMEL_MIGRATION.md` for the current design and migration rules.
