from utils.repository import AbstractRepository


class UserServices:

    def __init__(self,user_repo: AbstractRepository) -> None:
        self.user_repo = user_repo()

