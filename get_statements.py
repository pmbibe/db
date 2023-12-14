import re

def get_statements(file_name):
    statements = []
    statement = ""
    is_not_complete = False # Statement is end or not
    regex = r"^(CREATE|INSERT|UPDATE|ALTER|DELETE|MERGE|DROP|RENAME)"
    regex_pl = r"(CREATE OR REPLACE|ALTER|CREATE) (PROCEDURE|FUNCTION)(.*)"
    regex2 = r".+;$"
    begin_if_case_count = 0 # number of lines start with BEGIN, IF, CASE
    pl = 0
    is_begin = 0
    is_if_case_for = 0
    with open(file_name, encoding="utf8") as f:
        for line in f:
            # Check statement is PROCEDURE or FUNCTION or not
            if re.match(regex_pl, line.strip().upper()):
                pl = 1            
                
            # Increase number of lines start with BEGIN, IF, FOR and CASE
            if re.match(r"^\s*(IF|CASE|FOR).*", line.upper()):
                begin_if_case_count += 1
                is_if_case_for += 1

            # Increase number of lines start with BEGIN but not in IF statement
            if re.match(r"^\s*(BEGIN).*", line.upper()) and is_if_case_for == 0:
                begin_if_case_count += 1
                is_begin += 1

            # If line has END. Decrease number of lines start with BEGIN, IF, FOR and CASE
            if re.match(r"^\s*(END).*", line.upper()):
                begin_if_case_count -= 1
                if is_if_case_for > 0:
                    is_if_case_for -= 1

            # Check statement is inline or not
            if re.match(regex, line.strip().split(" ")[0].upper()) and (is_begin == 0 or is_if_case_for == 0):
                if re.match(regex2, line.strip()):
                    statements.append(line.strip())
                else:
                    is_not_complete = True    
            # Complete statement if statement is not inline

            # Check line is end with ";" or not
            if not re.match(regex2, line.strip()) and is_not_complete :
                statement = "\n".join([statement,format(line.strip())])

            # Check line end with ";" but statement is not complete and line is in other line start with BEGIN
            elif not re.match(regex2, line.strip()) and is_not_complete and (is_begin > 0 and begin_if_case_count > 0):
                statement = "\n".join([statement,format(line.strip())])

            elif pl > 0 and re.match(regex2, line.strip()) and is_not_complete and ( is_begin == 0 or (is_begin > 0 and begin_if_case_count > 0)):
                    statement = "\n".join([statement,format(line.strip())])
        
            elif  re.match(regex2, line.strip()) and begin_if_case_count == 0 and is_not_complete :
                statement = "\n".join([statement,format(line.strip())])
                statements.append(statement.strip())
                statement = ""
                is_not_complete = 0
                pl = 0
                is_begin = 0
    return statements
