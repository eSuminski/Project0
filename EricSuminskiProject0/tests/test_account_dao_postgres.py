from daos.accounts_dao import AccountsDAO
from daos.accounts_dao_postgre import AccountDAOPostgres
from entities.account import Account

account_dao: AccountsDAO = AccountDAOPostgres()

def test_create_account():
    account = Account(0, "first checking", 1000, 1)
    returned = account_dao.create_account(account)
    assert returned.account_id == 1

def test_select_account_by_id():
    account = Account(0, "second checking", 2000, 1)
    returned= account_dao.create_account(account)
    selected = account_dao.get_account_by_id(1)
    assert selected.account_id != returned.account_id

def test_select_all_accounts():
    l = account_dao.get_all_accounts()
    assert len(l) == 2

def test_update_account():
    new_account = Account(1, "was first checking", 1000, 1)
    new_account = account_dao.update_account(new_account)
    print("for clarity")
    print(str(new_account))
    reference = account_dao.get_account_by_id(1)
    print(str(reference))
    assert new_account.account_id == reference.account_id

def test_delete_account():
    result = account_dao.delete_account(2)
    assert result
