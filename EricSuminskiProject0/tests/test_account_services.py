from daos.accounts_dao import AccountsDAO
from daos.accounts_dao_imp import AccountDAOImp
# from daos.accounts_dao_postgre import AccountDAOPostgres
from daos.customers_dao import CustomerDAO
from daos.customers_dao_imp import CustomerDAOImp
# from daos.customers_dao_postgre import CustomerDAOPostgres
from entities.account import Account
from entities.customer import Customer
from services.account_service_imp import AccountServiceImp

account_dao: AccountsDAO = AccountDAOImp()
account_service = AccountServiceImp(account_dao)
client_dao: CustomerDAO = CustomerDAOImp()


def test_get_all_clients_accounts():
    account1 = Account(0, "fail", 25.00, 1)
    account2 = Account(0, "pass", 100.00, 1)
    account3 = Account(0, "FAILURE", 150.00, 2)
    account_dao.create_account(account1)
    account_dao.create_account(account2)
    account_dao.create_account(account3)
    account = account_service.get_all_clients_accounts(2)
    assert len(account) == 1


def test_get_range_of_client_accounts():
    account4 = Account(0, "correct account", 223.00, 2)
    account5 = Account(0, "FAILURE & Withdraw", 500.00, 2)
    account_dao.create_account(account4)
    account_dao.create_account(account5)
    account_range = account_service.get_range_of_client_accounts(2, 100, 500)
    assert len(account_range) == 2


def test_get_client_account_by_id():
    customer1 = Customer(0, "Test", "Testington")
    customer2 = Customer(0, "Fail", "Failure")
    client_dao.create_customer(customer1)
    client_dao.create_customer(customer2)
    customer1 = client_dao.get_customer_by_id(1)
    customer2 = client_dao.get_customer_by_id(2)
    print()
    print(customer1.customer_id)
    print(customer2.customer_id)
    target: Account = account_service.get_client_account_by_id(1, 2)
    assert target.client_id == 1 and target.account_id == 2


def test_update_client_account():
    account = account_dao.get_account_by_id(1)
    account.account_type = "no longer failing"
    account_service.update_client_account(1, 1, account)
    test = account_dao.get_account_by_id(1)
    assert test.account_type == account.account_type


def test_delete_client_account():
    accounts = account_service.get_all_clients_accounts(2)
    account_service.delete_client_account(2, 4)
    accounts = account_service.get_all_clients_accounts(2)
    assert len(accounts) == 2


def test_withdraw():
    withdraw = 250
    account = account_service.get_client_account_by_id(2, 5)
    print("help")
    print(account.account_value)
    account.account_value -= withdraw
    print("after withdraw")
    print(account.account_value)
    account_service.withdraw(2, 5, withdraw)
    print("after withdraw method")
    print(account.account_value)
    account2 = account_service.get_client_account_by_id(2, 5)
    print("account2 value")
    print(account2.account_value)
    assert account.account_value == account2.account_value


def test_withdraw_negative():
    withdraw = -10
    try:
        account_service.withdraw(2, 5, withdraw)
        assert False
    except ValueError as e:
        assert str(e) == "Invalid withdraw amount (negative number)"


def test_withdraw_too_much():
    withdraw = 500
    try:
        account_service.withdraw(2, 5, withdraw)
        assert False
    except ValueError as e:
        assert str(e) == "Invalid withdraw amount (insufficient funds)"


def test_deposite():
    deposit = 250
    account = account_service.get_client_account_by_id(2, 5)
    print(account.account_value)
    account.account_value += deposit
    account_service.deposit(2, 5, deposit)
    account2 = account_service.get_client_account_by_id(2, 5)
    print(account2.account_value)
    assert account.account_value == account2.account_value


def test_deposit_negative():
    deposit = -10
    try:
        account_service.deposit(2, 5, deposit)
        assert False
    except ValueError as e:
        assert str(e) == "Invalid deposit amount (negative number)"


def test_transfer_money():
    transfer = 150
    account1 = account_service.get_client_account_by_id(2, 3)
    account2 = account_service.get_client_account_by_id(2, 5)
    test_accounts = [account1, account2]
    print(test_accounts)
    print("next")
    account_service.transfer_money(2, 3, 5, transfer)
    account1 = account_service.get_client_account_by_id(2, 3)
    account2 = account_service.get_client_account_by_id(2, 5)
    test_accounts = [account1, account2]
    print(test_accounts)
    print("next")
    assert account1.account_value == 0.0 and account2.account_value == 650.0
