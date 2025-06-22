from datetime import date, timedelta
from typing import List

from app.common.enums import PaymentTermsEnum


class Utils:
    @staticmethod
    def generate_due_date(invoice_date: date, payment_terms: PaymentTermsEnum) -> date:
        # Calculate the due date based on the payment terms
        if payment_terms == PaymentTermsEnum.ONE:
            return invoice_date + timedelta(days=1)
        elif payment_terms == PaymentTermsEnum.SEVEN:
            return invoice_date + timedelta(days=7)
        elif payment_terms == PaymentTermsEnum.FOURTEEN:
            return invoice_date + timedelta(days=14)
        elif payment_terms == PaymentTermsEnum.THIRTY:
            return invoice_date + timedelta(days=30)

    @staticmethod
    def calculate_total(items: List) -> float:
        # Calculate the total cost of the items
        total = 0
        for item in items:
            total += item.total
        return round(total, 2)
