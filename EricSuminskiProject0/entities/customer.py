class Customer:

    def __init__(self, customer_id: int, customer_first_name: str, customer_last_name: str):
        self.customer_id = customer_id
        self.customer_first_name = customer_first_name
        self.customer_last_name = customer_last_name

    def __str__(self):
        return f"customer ID: {self.customer_id}, name: {self.customer_first_name} {self.customer_last_name}"

    def as_json_dict(self):
        return {
            "customerID": self.customer_id,
            "customerFirstName": self.customer_first_name,
            "customerLastName": self.customer_last_name,
        }
