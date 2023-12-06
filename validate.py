import re

r_date = r"\d{4}\.((1[012]|0[13456789])\.(3[01]|[012]\d)|(02)\.[012]\d)"
r_index = r"\d+\.(0|1|2)\.\d+"
r_include_index = r"YES|NO"

def validate_date(date):
    return re.match(r_date, date)
def validate_index(index):
    return re.match(r_index, index)
def validate_include_index(include_index):
    return re.match(r_include_index, include_index)