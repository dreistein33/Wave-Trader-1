def convert_percent_to_mul(num, loss=True):
    if loss:
        return 1.0 - (num / 100)
    else:
        return 1.0 + (num / 100)


def calculate_quantity(current_price, amount_to_pay):
    return amount_to_pay / current_price


