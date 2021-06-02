from daos.accounts_dao import AccountsDAO
from entities.account import Account
from exceptions.not_found_exception import ResourceNotFound
from services.account_service import AccountService


class AccountServiceImp(AccountService):

    def __init__(self, account_dao: AccountsDAO):
        self.account_dao = account_dao

    def add_account(self, account: Account):
        return self.account_dao.create_account(account)

    def retrieve_all_accounts(self):
        return self.account_dao.get_all_accounts()

    def retrieve_account_by_id(self, account_id: int):
        return self.account_dao.get_account_by_id(account_id)

    def update_account(self, account: Account):
        return self.account_dao.update_account(account)

    def remove_account(self, account_id: int):
        try:
            result = self.account_dao.delete_account(account_id)
            return result
        except KeyError:
            raise ResourceNotFound(f"Account with the id of {account_id} could not be found")

    def get_all_clients_accounts(self, client_id: int):
        accounts = self.account_dao.get_all_accounts()
        client_accounts = []
        for a in accounts:
            if a.client_id == client_id:
                client_accounts.append(a)
        if len(client_accounts) == 0:
            raise ResourceNotFound("No accounts match the given client ID")
        else:
            return client_accounts

    def get_range_of_client_accounts(self, client_id: int, lower_num: int, upper_num: int):
        try:
            accounts = self.get_all_clients_accounts(client_id)
            accounts_range = []
            for a in accounts:
                if lower_num < float(a.account_value) < upper_num:
                    accounts_range.append(a)
            return accounts_range
        except KeyError:
            raise ResourceNotFound("The client could not be found")

    def get_client_account_by_id(self, client_id: int, account_id: int):
        try:
            accounts = self.get_all_clients_accounts(client_id)
            for a in accounts:
                if a.account_id == account_id:
                    target = a
            return target
        except UnboundLocalError:
            raise ResourceNotFound("The resource could not be found")
        # might need ResourceNotFound to get correct error message?

    def update_client_account(self, client_id: int, account_id: int, account: Account):
        try:
            a = self.get_client_account_by_id(client_id, account_id)
            return self.update_account(account)
        except UnboundLocalError:
            raise ResourceNotFound("The resource could not be found")

    def delete_client_account(self, client_id: int, account_id: int):
        accounts = self.get_all_clients_accounts(client_id)
        length = len(accounts)
        for a in accounts:
            if a.account_id == account_id:
                self.remove_account(a.account_id)
                accounts = self.get_all_clients_accounts(client_id)
        if len(accounts) == length:
            raise ResourceNotFound("The resource could not be found")

    def withdraw(self, client_id: int, account_id: int, withdraw: int):
        if withdraw < 0:
            raise ValueError("Invalid withdraw amount (negative number)")
        account = self.get_client_account_by_id(client_id, account_id)
        if withdraw > float(account.account_value):
            raise ValueError("Invalid withdraw amount (insufficient funds)")
        new_value = float(account.account_value) - withdraw
        account.account_value = new_value
        return self.update_client_account(client_id, account_id, account)

    def deposit(self, client_id: int, account_id: int, deposit: int):
        if deposit < 0:
            raise ValueError("Invalid deposit amount (negative number)")
        account = self.get_client_account_by_id(client_id, account_id)
        new_value = float(account.account_value) + deposit
        account.account_value = new_value
        return self.update_client_account(client_id, account_id, account)

    def transfer_money(self, client_id: int, from_id: int, to_id: int, amount: int):
        from_account = self.get_client_account_by_id(int(client_id), int(from_id))
        to_account = self.get_client_account_by_id(int(client_id), int(to_id))
        self.withdraw(client_id, from_id, amount)
        self.deposit(client_id, to_id, amount)
        return "Transfer Complete"

