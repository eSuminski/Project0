from daos.customers_dao import CustomerDAO
from daos.customers_dao_postgre import CustomerDAOPostgres
from entities.customer import Customer

customer_dao: CustomerDAO = CustomerDAOPostgres()


# DROP AND RECREATE TEST TABLES BEFORE RUNNING EACH TEST TO RESET COUNTER
def test_create_customer():
    tester = Customer(0, "test", "testington")
    returned = customer_dao.create_customer(tester)
    assert returned.customer_id == 1


def test_get_customer_by_id():
    tester = Customer(0, "test2", "testington2")
    returned = customer_dao.create_customer(tester)
    selected = customer_dao.get_customer_by_id(1)
    assert returned.customer_id != selected.customer_id


def test_get_all_customers():
    l = customer_dao.get_all_customers()
    assert len(l) == 2


def test_update_customer():
    new_name = Customer(2, "new name", "for a new function")
    new_name = customer_dao.update_customer(new_name)
    print("for clarity")
    print(str(new_name))
    reference = customer_dao.get_customer_by_id(2)
    print(str(reference))
    assert new_name.customer_id == reference.customer_id


def test_delete_customer():
    result = customer_dao.delete_customer(2)
    assert result
