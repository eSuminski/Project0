from daos.accounts_dao import AccountsDAO
from daos.accounts_dao_imp import AccountDAOImp
from entities.account import Account

account_dao: AccountsDAO = AccountDAOImp()

test_account = Account(0, "checking", 0,)

# pytests go from top to bottom


def test_create_account():
    account_dao.create_account(test_account)
    print(test_account)
    assert test_account.account_id != 0


def test_get_account_by_id():
    account = account_dao.get_account_by_id(test_account.account_id)
    print(account)
    assert test_account.account_type == account.account_type


def test_get_all_accounts():
    account1 = Account(0, "checking", 0.00, 0)
    account2 = Account(0, "checking", 0.00, 0)
    account3 = Account(0, "checking", 0.00, 0)
    account_dao.create_account(account1)
    account_dao.create_account(account2)
    account_dao.create_account(account3)
    accounts = account_dao.get_all_accounts()
    for a in accounts:
        print(a)
    assert len(accounts) >= 3


def test_update_account():
    test_account.account_value = 5.23
    updated_account = account_dao.update_account(test_account)
    print(updated_account)
    assert updated_account.account_value == test_account.account_value


def test_delete_account():
    result = account_dao.delete_account(test_account.account_id)
    print(result)
    assert result
