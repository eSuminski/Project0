from typing import List
from daos.accounts_dao import AccountsDAO
from entities.account import Account
from utils.connection_util import connection


class AccountDAOPostgres(AccountsDAO):
    def create_account(self, account: Account) -> Account:
        sql = """INSERT INTO "Project0".account VALUES (DEFAULT, %s, %s, %s) returning account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.account_type, account.account_value, account.client_id))
        connection.commit()
        a_id = cursor.fetchone()[0]
        account.account_id = a_id
        return account

    def get_account_by_id(self, account_id: int) -> Account:
        sql = """SELECT * FROM "Project0".account WHERE account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        record = cursor.fetchone()
        account = Account(*record)
        return account

    def get_all_accounts(self) -> List[Account]:
        sql = """SELECT * FROM "Project0".account"""
        cursor = connection.cursor()
        cursor.execute(sql)
        account_record = cursor.fetchall()
        account_list = []
        for a in account_record:
            account_list.append(Account(*a))
        return account_list

    def update_account(self, account: Account) -> Account:
        sql = """UPDATE "Project0".account SET account_type = %s, account_value = %s WHERE account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.account_type, account.account_value, account.account_id))
        connection.commit()
        return account

    def delete_account(self, account_id: int) -> bool:
        sql = """DELETE FROM "Project0".account WHERE account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        connection.commit()
        return True
