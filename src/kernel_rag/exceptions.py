class KernelRAGError(Exception):
    """Base exception for the application."""


class ConfigurationError(KernelRAGError):
    """Raised when required configuration is missing or invalid."""


class KnowledgeBaseNotReadyError(KernelRAGError):
    """Raised when the vector database has not been ingested yet."""
