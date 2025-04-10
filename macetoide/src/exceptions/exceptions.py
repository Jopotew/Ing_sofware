
class RepositoryError(Exception):
    pass


class DatabaseOperationError(RepositoryError):
    
    def __init__(self, message: str = "Database operation failed"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(RepositoryError):
    pass

class UserFieldValidationError(RepositoryError):
    pass

class UserUpdateError(RepositoryError):
    pass


class PotNotFoundError(RepositoryError):
    pass


class LogDataFetchError(RepositoryError):
    pass



class PlantError(RepositoryError):
    pass
