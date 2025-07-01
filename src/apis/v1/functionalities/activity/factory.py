from src.core.db_repository.activity import ActivityRepositoryAbstract


class ActivityServiceAbstract:
    pass

class ActivityServiceFactory:
    def __init__(
            self,
            repo: ActivityRepositoryAbstract
            ):
        self.repo = repo
