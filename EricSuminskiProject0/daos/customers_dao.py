from abc import ABC, abstractmethod
from typing import List

from entities.customer import Customer


class CustomerDAO(ABC):
    # Need to support basic CRUD operations

    @abstractmethod
    def create_customer(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id: int) -> Customer:
        pass

    @abstractmethod
    def get_all_customers(self) -> List[Customer]:
        pass

    @abstractmethod
    def update_customer(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int) -> bool:
        pass
