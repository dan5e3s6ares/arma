import yaml

a = {
    "AcctInfo": {
        "properties": {
            "chAccAgeInd": {
                "description": "Length of time that the cardholder has had the account with the 3DS Requestor. \nAllowed values:\n* **01** — No account\n* **02** — Created during this transaction\n* **03** — Less than 30 days\n* **04** — 30–60 days\n* **05** — More than 60 days",
                "enum": ["01", "02", "03", "04", "05"],
                "maxLength": 2,
                "minLength": 2,
                "type": "string",
            },
            "chAccChange": {
                "description": "Date that the cardholder’s account with the 3DS Requestor was last changed, including Billing or Shipping address, new payment account, or new user(s) added. \nFormat: **YYYYMMDD**",
                "type": "string",
            },
            "chAccChangeInd": {
                "description": "Length of time since the cardholder’s account information with the 3DS Requestor was last changed, including Billing or Shipping address, new payment account, or new user(s) added. \nAllowed values:\n* **01** — Changed during this transaction\n* **02** — Less than 30 days\n* **03** — 30–60 days\n* **04** — More than 60 days",
                "enum": ["01", "02", "03", "04"],
                "maxLength": 2,
                "minLength": 2,
                "type": "string",
            },
            "chAccPwChange": {
                "description": "Date that cardholder’s account with the 3DS Requestor had a password change or account reset. \nFormat: **YYYYMMDD**",
                "type": "string",
            },
            "chAccPwChangeInd": {
                "description": "Indicates the length of time since the cardholder’s account with the 3DS Requestor had a password change or account reset. \nAllowed values:\n* **01** — No change\n* **02** — Changed during this transaction\n* **03** — Less than 30 days\n* **04** — 30–60 days\n* **05** — More than 60 days",
                "enum": ["01", "02", "03", "04", "05"],
                "maxLength": 2,
                "minLength": 2,
                "type": "string",
            },
            "chAccString": {
                "description": "Date that the cardholder opened the account with the 3DS Requestor. \nFormat: **YYYYMMDD**",
                "type": "string",
            },
            "nbPurchaseAccount": {
                "description": "Number of purchases with this cardholder account during the previous six months. Max length: 4 characters.",
                "type": "string",
            },
            "paymentAccAge": {
                "description": "String that the payment account was enrolled in the cardholder’s account with the 3DS Requestor. \nFormat: **YYYYMMDD**",
                "type": "string",
            },
            "paymentAccInd": {
                "description": "Indicates the length of time that the payment account was enrolled in the cardholder’s account with the 3DS Requestor. \nAllowed values:\n* **01** — No account (guest checkout)\n* **02** — During this transaction\n* **03** — Less than 30 days\n* **04** — 30–60 days\n* **05** — More than 60 days",
                "enum": ["01", "02", "03", "04", "05"],
                "maxLength": 2,
                "minLength": 2,
                "type": "string",
            },
            "provisionAttemptsDay": {
                "description": "Number of Add Card attempts in the last 24 hours. Max length: 3 characters.",
                "type": "string",
            },
            "shipAddressUsage": {
                "description": "String when the shipping address used for this transaction was first used with the 3DS Requestor. \nFormat: **YYYYMMDD**",
                "type": "string",
            },
            "shipAddressUsageInd": {
                "description": "Indicates when the shipping address used for this transaction was first used with the 3DS Requestor. \nAllowed values:\n* **01** — This transaction\n* **02** — Less than 30 days\n* **03** — 30–60 days\n* **04** — More than 60 days",
                "enum": ["01", "02", "03", "04"],
                "maxLength": 2,
                "minLength": 2,
                "type": "string",
            },
            "shipNameIndicator": {
                "description": "Indicates if the Cardholder Name on the account is identical to the shipping Name used for this transaction. \nAllowed values:\n* **01** — Account Name identical to shipping Name\n* **02** — Account Name different to shipping Name",
                "enum": ["01", "02"],
                "maxLength": 2,
                "minLength": 2,
                "type": "string",
            },
            "suspiciousAccActivity": {
                "description": "Indicates whether the 3DS Requestor has experienced suspicious activity (including previous fraud) on the cardholder account. \nAllowed values:\n* **01** — No suspicious activity has been observed\n* **02** — Suspicious activity has been observed",
                "enum": ["01", "02"],
                "maxLength": 2,
                "minLength": 2,
                "type": "string",
            },
            "txnActivityDay": {
                "description": "Number of transactions (successful and abandoned) for this cardholder account with the 3DS Requestor across all payment accounts in the previous 24 hours. Max length: 3 characters.",
                "maxLength": 3,
                "type": "string",
            },
            "txnActivityYear": {
                "description": "Number of transactions (successful and abandoned) for this cardholder account with the 3DS Requestor across all payment accounts in the previous year. Max length: 3 characters.",
                "maxLength": 3,
                "type": "string",
            },
        },
        "type": "object",
    }
}

print(yaml.dump(a))


def build_dict(data):
    """
    Builds a nested dictionary from a list representing a hierarchical structure.

    Args:
        data: A list of lists, where each inner list represents a path in the hierarchy.

    Returns:
        A nested dictionary representing the data structure.
    """
    result = {}
    for path in data:
        current_dict = result
        for element in path:
            if element not in current_dict:
                current_dict[element] = {}
            current_dict = current_dict[element]
    return result


# Example usage
data = [
    ["applePay", "sessions"],
    ["cancels"],
    ["cardDetails"],
    ["donations"],
    ["orders"],
    ["orders", "cancel"],
    ["originKeys"],
    ["paymentLinks"],
    ["paymentLinks", "{linkId}"],
    ["paymentMethods"],
    ["paymentMethods", "balance"],
    ["paymentSession"],
    ["payments"],
    ["payments", "details"],
    ["payments", "result"],
    ["payments", "{paymentPspReference}", "amountUpdates"],
    ["payments", "{paymentPspReference}", "cancels"],
    ["payments", "{paymentPspReference}", "captures"],
    ["payments", "{paymentPspReference}", "refunds"],
    ["payments", "{paymentPspReference}", "reversals"],
    ["sessions"],
    ["storedPaymentMethods"],
    ["storedPaymentMethods", "{recurringId}"],
]

nested_dict = build_dict(data)
print(nested_dict)
