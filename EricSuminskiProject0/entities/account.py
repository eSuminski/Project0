class Account:

    def __init__(self, account_id: int, account_type: str, account_value: float, client_id: int = 0):
        self.account_id = account_id
        self.account_type = account_type
        self.account_value = account_value
        self.client_id = client_id

    def __str__(self):
        return f"account ID: {self.account_id}, account owner ID: {self.client_id}, account type: {self.account_type}, value in account: {self.account_value}"

    def as_json_dict(self):
        return {
            "accountID": self.account_id,
            "accountType": self.account_type,
            "accountValue": self.account_value,
            "clientID": self.client_id
        }
