# MuziTools structure

The root `tools/` package has been merged into `MuziTools/`.

- `MuziTools/*.py`: legacy large PySide2 implementations kept for compatibility.
- `MuziTools/tools/<category>/*.py`: clean entries discovered by `rigging_toolbox.py`.
- `MuziTools/image`, `icon`, `qss`, `ui`: unified resources.

Recommended Maya entry:

```python
import muziToolset
muziToolset.show()
```

The old hard-coded scripts path is no longer required.
