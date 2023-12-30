import re

r_date = r"\d{4}\.((1[012]|0[13456789])\.(3[01]|[012]\d)|(02)\.[012]\d)"
r_index = r"\d+\.(0|1|2)\.\d+"
r_include_index = r"Y|N"
r_date_1 = r"Checklist ((\d{4})(1[012]|0[13456789])(3[01]|[012]\d)|(02)\.[012]\d)"

# Common SQL Statement
r_ddl_dml_all = r"^(CREATE|INSERT|UPDATE|ALTER|DELETE|MERGE|DROP|RENAME)"

# Statement is Proceduer or Function
r_func_procedure = r"^(CREATE OR REPLACE|ALTER|CREATE) (PROCEDURE|FUNCTION)(.*)"

# End of statement with semicolon ";"
r_eos = r"(.*);$"

# Statement begin with IF, CASE, FOR
r_if_case_for = r"^\s*(IF|CASE|FOR)\b.*"

# Statement begin with BEGIN
r_begin = r"^\s*(BEGIN)\b.*"

# Statement begin with END
r_end = r"^\s*(END)\b.*"

# DDL that define or modify database objects exclude VIEW, PROCEDURE, FUNCTION
r_ddl_exc_vpf = r"^(CREATE|ALTER|DROP|RENAME|TRUNCATE)"

# DDL that define or modify database objects include VIEW, PROCEDURE, FUNCTION
r_ddl_inc_vpf = r"^(CREATE OR REPLACE|ALTER|CREATE) (VIEW|PROCEDURE|FUNCTION)(.*)"

# Module, Sub Module, Feature format
r_m_sm_f = r"^\d+\..*"

def validate_date(date):
    return re.match(r_date, date)

def validate_date_1(date):
    match = re.search(r_date_1, date)
    return match

def validate_index(index):
    return re.match(r_index, index)

def validate_include_index(include_index):
    return re.match(r_include_index, include_index)

def validate_ddl_dml(statement):
    return re.match(r_ddl_dml_all, statement)

def validate_func_procedure(statement):
    return re.match(r_func_procedure, statement)    

def validate_eos(statement):
    return re.match(r_eos, statement)
    # return re.finditer(r_eos, statement, re.MULTILINE)

def validate_if_case_for(statement):
    return re.match(r_if_case_for, statement)

def validate_begin(statement):
    return re.match(r_begin, statement)

def validate_end(statement):
    return re.match(r_end, statement)

def validate_ddl_exc_vpf(statement):
    return re.match(r_ddl_exc_vpf, statement)

def validate_ddl_inc_vpf(statement):
    return re.match(r_ddl_inc_vpf, statement)

def validate_m_sm_f(statement):
    return re.match(r_m_sm_f, statement)
