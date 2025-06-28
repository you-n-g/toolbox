from importlib import metadata as _meta

# Will be overwritten by semantic-release; fallback lets local “editable”
# installs still expose a version string.
try:
    __version__: str = _meta.version(__package__ or "xytb")
except _meta.PackageNotFoundError:         # pragma: no cover
    __version__ = "0.0.0"

def hello() -> str:
    return "Hello from xytb!"
