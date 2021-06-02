from daos.customers_dao import CustomerDAO
from exceptions.not_found_exception import ResourceNotFound
from services.customer_service import CustomerService
from entities.customer import Customer


class CustomerServiceImp(CustomerService):
    def __init__(self, customer_dao: CustomerDAO):
        self.customer_dao = customer_dao

    def add_customer(self, customer: Customer):
        return self.customer_dao.create_customer(customer)

    def retrieve_all_customers(self):
        return self.customer_dao.get_all_customers()

    def retrieve_customer_by_id(self, customer_id: int):
        try:
            c = self.customer_dao.get_customer_by_id(customer_id)
            return c
        except KeyError:
            raise ResourceNotFound("The client could not be found")

    def update_customer(self, customer: Customer):
        try:
            c = self.customer_dao.get_customer_by_id(customer.customer_id)
            return self.customer_dao.update_customer(customer)
        except KeyError:
            raise ResourceNotFound("The client could not be found")

    def remove_customer(self, customer_id: int):
        result = self.customer_dao.delete_customer(customer_id)
        if result:
            return result
        else:
            raise ResourceNotFound(f"Customer with the id of {customer_id} could not be found")
