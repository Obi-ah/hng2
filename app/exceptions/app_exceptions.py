
class NotFoundError(Exception):
    """Raised when a requested entity does not exist."""
    pass

class DatabaseError(Exception):
    """Raised when a database operation fails."""
    pass
