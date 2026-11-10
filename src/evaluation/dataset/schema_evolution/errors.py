"""Errors raised by schema evolution operations."""


class SchemaEvolutionError(ValueError):
    """Invalid schema, incompatible record, or unsafe migration."""
