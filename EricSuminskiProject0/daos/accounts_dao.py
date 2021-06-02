from abc import ABC, abstractmethod
from typing import List

from entities.account import Account


class AccountsDAO(ABC):
    # Need to support basic CRUD operations

    @abstractmethod
    def create_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_account_by_id(self, account_id: int) -> Account:
        pass

    @abstractmethod
    def get_all_accounts(self) -> List[Account]:
        pass

    @abstractmethod
    def update_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def delete_account(self, account_id: int) -> bool:
        pass
