from proxyUtils.proxy_checker import proxy_checker
import sys
from sqlite.sqlite import db_connector


def show_usage():
    print("""
    Usage: 
    beehive.py check_all_proxy DB_PATH\n
    beehive.py check_unknown_proxy DB_PATH\n
    beehive.py parse_email DB_PATH EMAIL_PATH
    """)


def parse_email(file_path, db_path):
    db = db_connector(db_path)
    db.crete_table("mails", "login string UNIQUE", "password string")
    with open(file_path, "r") as f:
        data = f.read()
    
    for line in data.split("\n"):
        login, password = line.split(":")
        db.insert("mails", "'{}','{}'".format(login, password)
        
def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        show_usage()
        return
    
    path = sys.argv[2]
    command = sys.argv[1]

    if(command == "check_all_proxy"):
        checker = proxy_checker(path)
        checker.check_all()
    if(command == "check_unknown_proxy"):
        checker = proxy_checker(path)
        checker.check_unknown()
    if(command == "parse_email"):
        email_path = sys.argv[3]
        parse_email(email_path, db_path)


  
  

if __name__ == "__main__":
    main()