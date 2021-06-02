import json

from flask import Flask, request, jsonify
import logging
from daos.accounts_dao_postgre import AccountDAOPostgres
from daos.customers_dao_postgre import CustomerDAOPostgres
from entities.account import Account
from entities.customer import Customer
from exceptions.negative_number_exception import NegativeNumberException
from exceptions.not_found_exception import ResourceNotFound
from exceptions.value_too_large_exception import ValueTooLargeException
from services.account_service_imp import AccountServiceImp
from services.customer_service_imp import CustomerServiceImp

app: Flask = Flask(__name__)
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(message)s")

account_dao = AccountDAOPostgres()
account_service = AccountServiceImp(account_dao)
customer_dao = CustomerDAOPostgres()
customer_service = CustomerServiceImp(customer_dao)


@app.get("/hello")
def hello():
    return "hello"


@app.post("/clients")
def create_customer():
    body = request.json
    customer = Customer(body["customerID"], body["customerFirstName"], body["customerLastName"])
    customer_service.add_customer(customer)
    return f"Created Customer with id {customer.customer_id}", 201


@app.get("/clients")
def get_all_customers():
    customers = customer_service.retrieve_all_customers()
    json_customers = [c.as_json_dict() for c in customers]
    return jsonify(json_customers), 200


@app.get("/clients/<client_id>")
def get_client_by_id(client_id: str):
    try:
        client = customer_service.retrieve_customer_by_id(int(client_id))
        return jsonify(client.as_json_dict())
    except ResourceNotFound as e:
        return "there was an error: check your values and try again", 404
    except ValueError:
        return "there was an error: check your values and try again", 404


@app.put("/clients/<client_id>")
def update_client(client_id: str):
    try:
        body = request.json
        customer = Customer(body["customerID"], body["customerFirstName"], body["customerLastName"])
        customer.customer_id = int(client_id)
        customer_service.update_customer(customer)
        return "updated successfully"
    except ResourceNotFound as e:
        return "there was an error: check your values and try again", 404
    except ValueError:
        return "there was an error: check your values and try again", 404


@app.put("/clients/<client_id>/accounts/<account_id>")
def update_client_account(client_id: str, account_id: str, ):
    try:
        original = account_service.get_client_account_by_id(int(client_id), int(account_id))
        body = request.json
        account = Account(body["accountID"], body["accountType"], body["accountValue"], body["clientID"])
        account.client_id = int(client_id)
        account.account_id = int(account_id)
        account.account_value = original.account_value
        account_service.update_client_account(int(client_id), int(account_id), account)
        return "updated successfully"
    except ResourceNotFound as e:
        return "there was an error: check your values and try again", 404
    except ValueError:
        return "there was an error: check your values and try again", 4


@app.delete("/clients/<client_id>")
def delete_customer(client_id: str):
    try:
        client = customer_service.retrieve_customer_by_id(int(client_id))
        customer_service.remove_customer(int(client_id))
        return "Customer removed successfully", 205
    except ResourceNotFound as e:
        return "there was an error: check your values and try again", 404
    except ValueError:
        return "there was an error: check your values and try again", 404


@app.delete("/clients/<client_id>/accounts/<account_id>")
def delete_account(client_id: str, account_id: str):
    try:
        account_service.delete_client_account(int(client_id), int(account_id))
        return "Account removed successfully", 205
    except ResourceNotFound as e:
        return "there was an error: check your values and try again", 404
    except ValueError as e:
        return "there was an error: check your values and try again", 404


@app.post("/clients/<client_id>/accounts")
def create_client_account(client_id: str):
    try:
        client = customer_service.retrieve_customer_by_id(int(client_id))
        body = request.json
        account = Account(body["accountID"], body["accountType"], body["accountValue"], int(client_id))
        account_service.add_account(account)
        return f"Created an account for client {client_id}", 201
    except ResourceNotFound as e:
        return "there was an error: check your values and try again", 404
    except ValueError:
        return "there was an error: check your values and try again", 404


@app.get("/clients/<client_id>/accounts")
def get_clients_accounts(client_id: str):
    try:
        less_than = request.args.get("amountLessThan")
        greater_than = request.args.get("amountGreaterThan")
        if less_than is not None:
            if greater_than is not None:
                if less_than.isnumeric():
                    if greater_than.isnumeric():
                        customer_accounts = account_service.get_range_of_client_accounts(int(client_id),
                                                                                         int(greater_than),
                                                                                         int(less_than))
        else:
            customer_accounts = account_service.get_all_clients_accounts(int(client_id))
        json_customer_accounts = [a.as_json_dict() for a in customer_accounts]
        return jsonify(json_customer_accounts)
    except ResourceNotFound as e:
        return "there was an error: check your values and try again", 404
    except ValueError:
        return "there was an error: check your values and try again", 404
    except UnboundLocalError:
        return "there was an error: check your values and try again", 404


@app.get("/clients/<client_id>/accounts/<account_id>")
def get_account_by_id(client_id: str, account_id: str):
    try:
        account = account_service.get_client_account_by_id(int(client_id), int(account_id))
        json_account = account.as_json_dict()
        return jsonify(json_account)
    except ResourceNotFound as e:
        return "there was an error: check your values and try again", 404
    except ValueError:
        return "there was an error: check your values and try again", 404


@app.patch("/clients/<client_id>/accounts/<account_id>")
def deposit_withdraw(client_id: str, account_id: str):
    try:
        body = request.json
        if "deposit" in body:
            deposit = body["deposit"]
            account_service.deposit(int(client_id), int(account_id), float(deposit))
            return "Deposit complete"
        elif "withdraw" in body:
            withdraw = body["withdraw"]
            account_service.withdraw(int(client_id), int(account_id), float(withdraw))
            return "Withdrawal complete"
        else:
            return "there was an error: check your values and try again", 422
    except ValueError as e:
        return "there was an error: check your values and try again", 422
    except ResourceNotFound as e:
        return "there was an error: check your values and try again", 404
    except NegativeNumberException:
        return "there was an error: check your values and try again", 422
    except ValueTooLargeException:
        return "there was an error: check your values and try again", 422


@app.patch("/clients/<client_id>/accounts/<from_id>/transfer/<to_id>")
def transfer(client_id: str, from_id: str, to_id: str):
    body = request.json
    try:
        return account_service.transfer_money(int(client_id), int(from_id), int(to_id), int(body["amount"]))
    except ResourceNotFound as e:
        return "there was an error: check your values and try again", 404
    except ValueError as e:
        return "there was an error: check your values and try again", 422


if __name__ == '__main__':
    app.run()
