from typing import List

from daos.accounts_dao import AccountsDAO
from entities.account import Account


class AccountDAOImp(AccountsDAO):

    id_maker = 0  # temporary value, will be replaced by database key generator
    accounts_table = {}  # temporary, will be replaced by postgre table

    def create_account(self, account: Account) -> Account:
        AccountDAOImp.id_maker += 1
        account.account_id = AccountDAOImp.id_maker
        AccountDAOImp.accounts_table[AccountDAOImp.id_maker] = account
        return account

    def get_account_by_id(self, account_id: int) -> Account:
        account = AccountDAOImp.accounts_table[account_id]
        return account

    def get_all_accounts(self) -> List[Account]:
        account_list = list(AccountDAOImp.accounts_table.values())
        return account_list

    def update_account(self, account: Account) -> Account:
        AccountDAOImp.accounts_table[account.account_id] = account
        return account

    def delete_account(self, account_id: int) -> bool:
        try:
            del AccountDAOImp.accounts_table[account_id]
            return True
        except KeyError:
            return False
