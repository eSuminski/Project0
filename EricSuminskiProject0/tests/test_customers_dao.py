from daos.customers_dao import CustomerDAO
from daos.customers_dao_imp import CustomerDAOImp
from entities.customer import Customer

customer_dao: CustomerDAO = CustomerDAOImp()

test_customer = Customer(0, "Test", "Testington")


def test_create_customer():
    customer_dao.create_customer(test_customer)
    print(test_customer)
    assert test_customer.customer_id != 0


def test_get_customer_by_id():
    customer = customer_dao.get_customer_by_id(test_customer.customer_id)
    print(customer.customer_id)
    assert customer.customer_id == test_customer.customer_id


def test_get_all_customers():
    customer1 = Customer(0, "first", "last")
    customer2 = Customer(0, "first", "last")
    customer3 = Customer(0, "first", "last")
    customer_dao.create_customer(customer1)
    customer_dao.create_customer(customer2)
    customer_dao.create_customer(customer3)
    customers = customer_dao.get_all_customers()
    for c in customers:
        print(c)
    assert len(customers) >= 3


def test_update_customer():
    test_customer.customer_first_name = "Final"
    print(test_customer)
    updated_customer = customer_dao.update_customer(test_customer)
    print(updated_customer)
    assert updated_customer.customer_first_name == test_customer.customer_first_name


def test_delete_customer():
    result = customer_dao.delete_customer(test_customer.customer_id)
    print(result)
    assert result
