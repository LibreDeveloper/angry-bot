import requests as req
import urllib.parse as p
import psycopg as pg

DB_NAME = "users.db"


def conn_db():
    res = req.get(url="https://api.heroku.com/apps/<YOUR HEROKU USERNAME HERE>/config-vars",
                  headers={
                      "Accept": "application/vnd.heroku+json; version=3",
                      "Authorization": "<YOUR HEROKU TOKEN HERE>",
                  })
    db_url = res.json()["DATABASE_URL"]
    conn = pg.connect(db_url, sslmode="require")
    # sql = "CREATE TABLE users (uid text,name text,username text,score text,admin integer)"
    # conn.execute(sql)
    # conn.commit()
    print("connected to db!")
    return conn

# add new user to database table
def add_user(uid, name, username, score, admin):
    conn = conn_db()
    sql = f"select uid from users where uid='{uid}'"
    res = conn.execute(sql)
    user = res.fetchall()
    if len(user) == 0:
        sql = f"INSERT INTO users (uid,name,username,score,admin) VALUES('{uid}','{name}','{username}','{score}','{admin}')"
        conn.execute(sql)
        conn.commit()
        conn.close()
        print("user added to database")
    else:
        print("user exists!")

# add score to user
def add_score(uid, score):
    conn = conn_db()
    sql = f"select score from users where uid='{uid}'"
    res = conn.execute(sql)
    sc = res.fetchall()[0][0]
    sc = int(sc) + int(score)
    sql = f"update users set score={sc} where uid='{uid}'"
    conn.execute(sql)
    conn.commit()
    conn.close()
    print("user score updated")

# get user score
def get_score(uid):
    conn = conn_db()
    sql = f"select score from users where uid='{uid}'"
    score = conn.execute(sql)
    score = score.fetchall()[0][0]
    conn.close()
    return score


def get_gift(uid):
    conn = conn_db()
    sql = f"select gift from users where uid='{uid}'"
    res = conn.execute(sql)
    gift = res.fetchall()[0][0]
    return gift

# get list of users
def get_users():
    conn = conn_db()
    sql = f"select uid from users"
    res = conn.execute(sql)
    users = res.fetchall()
    conn.close()
    return len(users)

# check for user permissions
def is_admin(uid) -> int:
    conn = conn_db()
    sql = f"select admin from users where uid='{uid}'"
    res = conn.execute(sql)
    admin = res.fetchall()[0][0]
    conn.close()
    # print("admin:",admin)
    return admin

# add user to admin list
def add_admin(uid):
    conn = conn_db()
    sql = f"update users set admin=1 where uid='{uid}'"
    conn.execute(sql)
    conn.commit()
    conn.close()
    print(f"user {uid} added to admin list")

# delete user from table
def del_user(uid):
    conn = conn_db()
    sql = f"delete from users where uid='{uid}'"
    conn.execute(sql)
    conn.commit()
    conn.close()
    print("user deleted from database")


def check_user(uid):
    conn = conn_db()
    sql = f"select uid from users where uid='{uid}'"
    res = conn.execute(sql)
    user = res.fetchall()
    conn.close()
    # print(len(user))
    return len(user)


def fix_users():
    conn = conn_db()
    sql = f"select uid from users"
    res = conn.execute(sql)
    users = res.fetchall()
    print(users)
    for i in range(len(users)):
        sql = f"update users set gift='5',clown='0' where uid='{users[i][0]}'"
        conn.execute(sql)
        print(f"user {users[i][0]} updated.")
    print("all users updated")
    conn.close()


def check_gift(uid) -> int:
    conn = conn_db()
    sql = f"select gift from users where uid='{uid}'"
    res = conn.execute(sql)
    gift = res.fetchall()[0][0]
    if gift != 0:
        new_gift = int(gift) - 1
        sql = f"update users set gift='{new_gift}' where uid='{uid}'"
        conn.execute(sql)
        conn.close()
        return new_gift
    else:
        return 0
