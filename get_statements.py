import validate

def get_statements(file_name):
    statements = []
    statement = ""
    is_not_complete = False # Statement is end or not
    begin_if_case_count = 0 # number of lines start with BEGIN, IF, CASE
    pl = 0
    is_begin = 0
    is_if_case_for = 0
    with open(file_name, encoding="utf8") as f:
        for line in f:
            # Check statement is PROCEDURE or FUNCTION or not
            if validate.validate_func_procedure(line.strip().upper()):
                pl = 1            
            
            # Increase number of lines start with BEGIN, IF, FOR and CASE
            if validate.validate_if_case_for(line.upper()):
                begin_if_case_count += 1
                is_if_case_for += 1

            # Increase number of lines start with BEGIN but not in IF statement
            if validate.validate_begin(line.upper()) and is_if_case_for == 0:
                begin_if_case_count += 1
                is_begin += 1

            # If line has END. Decrease number of lines start with BEGIN, IF, FOR and CASE
            if validate.validate_end(line.upper()):
                begin_if_case_count -= 1
                if is_if_case_for > 0:
                    is_if_case_for -= 1

            # Check statement is inline or not
            if validate.validate_ddl_dml(line.strip().split(" ")[0].upper()) and (is_begin == 0 or is_if_case_for == 0):
                if validate.validate_eos(line.strip()):
                    statements.append(line)
                else:
                    is_not_complete = True    
            # Complete statement if statement is not inline

            # Check line is end with ";" or not
            if not validate.validate_eos(line.strip()) and is_not_complete :
                statement = "\n".join([statement,format(line)])

            # Check line end with ";" but statement is not complete and line is in other line start with BEGIN
            elif not validate.validate_eos(line.strip()) and is_not_complete and (is_begin > 0 and begin_if_case_count > 0):
                statement = "\n".join([statement,format(line)])

            elif pl > 0 and validate.validate_eos(line.strip()) and is_not_complete and ( is_begin == 0 or (is_begin > 0 and begin_if_case_count > 0)):
                    statement = "\n".join([statement,format(line)])
            elif  validate.validate_eos(line.strip()) and begin_if_case_count == 0 and is_not_complete :
                statement = "\n".join([statement,format(line)])
                statements.append(statement)
                statement = ""
                is_not_complete = 0
                pl = 0
                is_begin = 0
    return statements
