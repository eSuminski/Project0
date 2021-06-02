from typing import List
from daos.customers_dao import CustomerDAO
from entities.customer import Customer
from exceptions.not_found_exception import ResourceNotFound
from utils.connection_util import connection


class CustomerDAOPostgres(CustomerDAO):
    def create_customer(self, customer: Customer) -> Customer:
        sql = """INSERT INTO "Project0".customer values(DEFAULT, %s, %s) returning customer_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (customer.customer_first_name, customer.customer_last_name))
        connection.commit()
        c_id = cursor.fetchone()[0]
        customer.customer_id = c_id
        return customer

    def get_customer_by_id(self, customer_id: int) -> Customer:
        sql = """SELECT * FROM "Project0".customer WHERE customer_id = %s;"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        record = cursor.fetchone()
        if record == None:
            raise ResourceNotFound("The client could not be found")
        customer = Customer(*record)
        return customer

    def get_all_customers(self) -> List[Customer]:
        sql = """SELECT * FROM "Project0".customer"""
        cursor = connection.cursor()
        cursor.execute(sql)
        customer_record = cursor.fetchall()
        customer_list = []
        for c in customer_record:
            customer_list.append(Customer(*c))
        return customer_list

    def update_customer(self, customer: Customer) -> Customer:
        sql = """UPDATE "Project0".customer SET customer_first_name = %s, customer_last_name = %s WHERE customer_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (customer.customer_first_name, customer.customer_last_name, customer.customer_id))
        connection.commit()
        return customer

    def delete_customer(self, customer_id: int) -> bool:
        sql = """DELETE FROM "Project0".customer WHERE customer_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        connection.commit()
        return True
