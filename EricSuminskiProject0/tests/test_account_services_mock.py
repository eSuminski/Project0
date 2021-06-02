from unittest.mock import MagicMock

from daos.accounts_dao import AccountsDAO
from daos.accounts_dao_imp import AccountDAOImp
from daos.customers_dao import CustomerDAO
from daos.customers_dao_imp import CustomerDAOImp
from entities.account import Account
from entities.customer import Customer
from exceptions.not_found_exception import ResourceNotFound
from services.account_service_imp import AccountServiceImp
from services.customer_service_imp import CustomerServiceImp

account1 = Account(1, "fail", 25.00, 1)
account2 = Account(2, "pass", 100.00, 1)
account3 = Account(3, "FAILURE", 150.00, 2)
account4 = Account(4, "correct account", 223.00, 2)
account5 = Account(5, "FAILURE & Withdraw", 500.00, 2)
accounts = [
    account1,
    account2,
    account3,
    account4,
    account5
]
client1 = Customer(1, "Test", "Testington")
client2 = Customer(2, "Testina", "Testington")
clients = [
    client1,
    client2
]

mock_dao_a = AccountDAOImp()
mock_dao_a.get_all_accounts = MagicMock(return_value=accounts)
accounts = mock_dao_a.get_all_accounts()
account_service: AccountServiceImp = AccountServiceImp(mock_dao_a)

mock_da_c = CustomerDAOImp()
mock_da_c.get_all_customers = MagicMock(return_value=clients)
clients = mock_da_c.get_all_customers()
clients_service: CustomerServiceImp = CustomerServiceImp(mock_da_c)


def test_get_all_clients_accounts_mock():
    account = account_service.get_all_clients_accounts(2)
    assert len(account) == 3


def test_get_client_by_id_not_found_exception():
    try:
        fail = clients_service.retrieve_customer_by_id(3)
        print(str(fail))
        assert False
    except ResourceNotFound as e:
        assert str(e) == "The client could not be found"


def test_update_client_by_id_not_found_exception():
    try:
        client3 = Customer(3, "Shouldn't", "Work")
        clients_service.update_customer(client3)
        assert False
    except ResourceNotFound as e:
        assert str(e) == "The client could not be found"


def test_delete_client_by_id_not_found_exception():
    try:
        customer_id = 3
        clients_service.remove_customer(customer_id)
        assert False
    except ResourceNotFound as e:
        assert str(e) == f"Customer with the id of {customer_id} could not be found"


def test_get_client_accounts_by_id_not_found_exception():
    try:
        account = account_service.get_client_account_by_id(2, 7)
        assert False
    except ResourceNotFound as e:
        assert str(e) == "The resource could not be found"


def test_get_range_accounts_client_not_found_exception():
    try:
        faulty = account_service.get_range_of_client_accounts(3, 100, 200)
        assert False
    except ResourceNotFound as e:
        assert str(e) == "No accounts match the given client ID"


def test_get_client_account_by_id_account_id_not_found_exception():
    try:
        oops = account_service.get_client_account_by_id(2, 12)
        assert False
    except ResourceNotFound as e:
        assert str(e) == "The resource could not be found"


def test_get_client_account_by_id_client_not_found_exception():
    try:
        oops2 = account_service.get_client_account_by_id(12, 2)
        assert False
    except ResourceNotFound as e:
        assert str(e) == "No accounts match the given client ID"


def test_update_client_account_by_id_account_id_not_found_exception():
    try:
        bad_account = Account(0, "wrong", 10000000, 32)
        account_service.update_client_account(2, 32, bad_account)
        assert False
    except ResourceNotFound as e:
        assert str(e) == "The resource could not be found"


def test_update_client_account_by_id_client_not_found_exception():
    try:
        bad_account = Account(0, "wrong", 10000000, 32)
        account_service.update_client_account(32, 1, bad_account)
        assert False
    except ResourceNotFound as e:
        assert str(e) == "No accounts match the given client ID"


def test_delete_client_account_by_id_account_id_not_found_exception():
    try:
        account_service.delete_client_account(2, 15)
        assert False
    except ResourceNotFound as e:
        assert str(e) == "The resource could not be found"


def test_delete_client_account_by_id_client_not_found_exception():
    try:
        account_service.delete_client_account(17, 2)
        assert False
    except ResourceNotFound as e:
        assert str(e) == "No accounts match the given client ID"


def test_withdraw_account_id_not_found_exception():
    try:
        account_service.withdraw(1, 4, 30)
        assert False
    except ResourceNotFound as e:
        assert str(e) == "The resource could not be found"


def test_withdraw_client_id_not_found_exception():
    try:
        account_service.withdraw(4, 1, 30)
        assert False
    except ResourceNotFound as e:
        assert str(e) == "No accounts match the given client ID"

