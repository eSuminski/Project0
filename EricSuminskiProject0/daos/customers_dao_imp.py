from typing import List
from daos.customers_dao import CustomerDAO
from entities.customer import Customer


class CustomerDAOImp(CustomerDAO):

    id_maker = 0
    customer_list = {}

    def create_customer(self, customer: Customer) -> Customer:
        CustomerDAOImp.id_maker += 1
        customer.customer_id = CustomerDAOImp.id_maker
        CustomerDAOImp.customer_list[CustomerDAOImp.id_maker] = customer
        return customer

    def get_customer_by_id(self, customer_id: int) -> Customer:
        customer = CustomerDAOImp.customer_list[customer_id]
        return customer

    def get_all_customers(self) -> List[Customer]:
        customer_list = list(CustomerDAOImp.customer_list.values())
        return customer_list

    def update_customer(self, customer: Customer) -> Customer:
        CustomerDAOImp.customer_list[customer.customer_id] = customer
        return customer

    def delete_customer(self, customer_id: int) -> bool:
        try:
            del CustomerDAOImp.customer_list[customer_id]
            return True
        except KeyError:
            return False
