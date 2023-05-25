import psycopg2 as pg
import csv
import argparse
import glob
import pathlib
import io

parser = argparse.ArgumentParser(description = 'ipl')

parser.add_argument('--name', type = str)
parser.add_argument('--user', type = str)
parser.add_argument('--pswd', type = str)
parser.add_argument('--host', type = str)
parser.add_argument('--port', type = str)
parser.add_argument('--ddl', type = str)
parser.add_argument('--data', type = str)

args = parser.parse_args()


files = glob.glob(args.data + "/*.csv")
files.sort()

order = [5, 3, 8, 1, 4, 0, 6, 7, 2]
files = [files[i] for i in order]


conn = pg.connect(user=args.user,
    password=args.pswd,
    host=args.host,
    port=args.port,
    database=args.name)
cursor = conn.cursor()
conn.autocommit = True

with io.open('ipl_ddl.sql','r') as f:
    text = f.read()
sqlStatements = text.split(sep=';')


for statement in sqlStatements[:-1]:
# it will slice out the last element of your sqlStatements list
    cursor.execute(f'{statement}')
    conn.commit()


#with open('ipl_ddl.sql','r', encoding='utf-8') as f:
#    for statement in f.readlines():    
#        try:
#            cursor.execute(f'{statement.rstrip()}')
#            conn.commit()
#        except pg.Error as errorMsg:
#            print(errorMsg)        
#            conn.rollback()





if (conn):
    cursor.close()
    conn.close()
    



for file in files:

    
        
    #file = f"team.csv"
    with open(file, 'r') as f:
        reader = csv.reader(f)
        row1 = next(reader)

        s = str(row1)
        s1 = s.replace("[", "")
        s = s1.replace("]", "")
        s1 = s.replace("'", "")
        s = s1.replace("'", "")

    sql_insert = """"""
    
    if file == f"{args.data}/team.csv":

        
        sql_insert = """INSERT INTO team({})
                        VALUES(%s, %s)""".format(s)
    if file == f"{args.data}/all_by_ball.csv":

        
        sql_insert = """INSERT INTO ball_by_ball({})
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(s)
    if file == f"{args.data}/match.csv":

        
        sql_insert = """INSERT INTO match({})
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(s)
    if file == f"{args.data}/owner.csv":

        
        sql_insert = """INSERT INTO owner({})
                        VALUES(%s, %s, %s, %s, %s)""".format(s)
    if file == f"{args.data}/player.csv":

        
        sql_insert = """INSERT INTO player({})
                        VALUES(%s, %s, %s, %s, %s, %s)""".format(s)
    if file == f"{args.data}/player_match.csv":

        
        sql_insert = """INSERT INTO player_match({})
                        VALUES(%s, %s, %s, %s, %s)""".format(s)
    if file == f"{args.data}/umpire.csv":

        
        sql_insert = """INSERT INTO umpire({})
                        VALUES(%s, %s, %s)""".format(s)
    if file == f"{args.data}/umpire_match.csv":

        
        sql_insert = """INSERT INTO umpire_match({})
                        VALUES(%s, %s, %s, %s)""".format(s)
    if file == f"{args.data}/venue.csv":

        
        sql_insert = """INSERT INTO venue({})
                        VALUES(%s, %s, %s, %s, %s)""".format(s)


    try:
        conn = pg.connect(user=args.user,
            password=args.pswd,
            host=args.host,
            port=args.port,
            database=args.name)
        cursor = conn.cursor()
        
        with open(file, 'r') as f:
            reader = csv.reader(f)
            row1 = next(reader) # This skips the 1st row which is the header.
            for record in reader:
                cursor.execute(sql_insert, record)
                conn.commit()
    except (Exception, pg.Error) as e:
        x = 1
    finally:
        if (conn):
            cursor.close()
            conn.close()
            
