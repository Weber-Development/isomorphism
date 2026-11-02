"""Reversible anonymisation of Swiss personal data. Local only: no network, no telemetry."""

from importlib.metadata import version

from .core import Finding, Mapping, anonymize, detect, restore

__version__ = version("isomorphism")
__all__ = ["Finding", "Mapping", "__version__", "anonymize", "detect", "restore"]
