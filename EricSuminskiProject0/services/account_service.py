from abc import ABC, abstractmethod

from entities.account import Account


class AccountService(ABC):
    # need general crud functionality

    @abstractmethod
    def add_account(self, account: Account):
        pass

    @abstractmethod
    def retrieve_all_accounts(self):
        pass

    @abstractmethod
    def retrieve_account_by_id(self, account_id: int):
        pass

    @abstractmethod
    def update_account(self, account: Account):
        pass

    @abstractmethod
    def remove_account(self, account_id: int):
        pass

    @abstractmethod
    def get_all_clients_accounts(self, client_id: int):
        pass

    @abstractmethod
    def get_range_of_client_accounts(self, client_id: int, lower_num: int, upper_num: int):
        pass

    @abstractmethod
    def get_client_account_by_id(self, client_id: int, account_id: int):
        pass

    @abstractmethod
    def update_client_account(self, client_id: int, account_id: int, account: Account):
        pass

    @abstractmethod
    def delete_client_account(self, client_id: int, account_id: int):
        pass

    @abstractmethod
    def withdraw(self, client_id: int, account_id: int, withdraw: int):
        pass

    @abstractmethod
    def deposit(self, client_id: int, account_id: int, deposit: int):
        pass

    @abstractmethod
    def transfer_money(self, client_id: int, from_id: int, to_id: int, amount: int):
        pass
