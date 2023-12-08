import re

def get_statements(file_name):
    statements = []
    statement = ""
    i = 0
    regex = r"^(CREATE|INSERT|UPDATE|ALTER|DELETE|MERGE|DROP|RENAME)"
    regex_pl = r"(CREATE OR REPLACE|ALTER|CREATE) (PROCEDURE|FUNCTION)(.*)"
    regex2 = r".+;$"
    begin_if_count = 0
    pl = 0
    is_begin = False
    with open(file_name, encoding="utf8") as f:
        for line in f:
            if re.match(regex_pl, line.strip()):
                pl = 1            
                
            if re.match(r"^\s*(BEGIN|IF)$", line.upper()):
                begin_if_count += 1
                is_begin = True

            if re.match(r"^\s*(END).*", line.upper()):
                begin_if_count -= 1

            if re.match(regex, line.strip().split(" ")[0].upper()):
                if re.match(regex2, line.strip()):
                    statements.append(line.strip())
                else:
                    i=1    
            if not re.match(regex2, line.strip()) and i > 0 : # and "--" not in line.strip():
                statement = "\n".join([statement,format(line.strip())])

            elif not re.match(regex2, line.strip()) and i > 0 and (not is_begin == False or (is_begin and begin_if_count > 0)):
                statement = "\n".join([statement,format(line.strip())])

            elif pl > 0 and re.match(regex2, line.strip()) and i > 0 and ( not is_begin or (is_begin and begin_if_count > 0)):
                    statement = "\n".join([statement,format(line.strip())])
        
            elif  re.match(regex2, line.strip()) and begin_if_count == 0 and i > 0 :
                statement = "\n".join([statement,format(line.strip())])
                statements.append(statement.strip())
                statement = ""
                i = 0
                pl = 0
                is_begin = False
        return statements
