"""Reversible anonymisation of Swiss personal data. Local only: no network, no telemetry."""

from importlib.metadata import version

from .core import Finding, Mapping, Restorer, anonymize, detect, restore, restore_stream

__version__ = version("isomorphism")
__all__ = [
    "Finding",
    "Mapping",
    "Restorer",
    "__version__",
    "anonymize",
    "detect",
    "restore",
    "restore_stream",
]
