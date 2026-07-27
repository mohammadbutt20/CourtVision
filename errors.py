class CourtVisionError(Exception):
    """Base for every error this project raises. Catch this at the CLI."""

class PlayerNotFoundError(CourtVisionError):
    pass

class PlayerAmbiguousError(CourtVisionError):
    pass

class InsufficientGamesError(CourtVisionError):
    pass

class InvalidStatCategoryError(CourtVisionError):
    pass