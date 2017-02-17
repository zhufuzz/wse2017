import MySQLdb

def get_conn():
    host = "127.0.0.1"
    port = 3306
    db = "jikexueyuan"
    user = "root"
    password = "dashizi"
    conn = MySQLdb.connect(host=host,
                           user=user,
                           passwd=password,
                           db=db,
                           port=port,
                           charset="utf8")
    return conn

class User(object):
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name


    def save(self):
        conn = get_conn()
        cursor = conn.cursor()
        sql = "insert into user(user_id, user_name) VALUE (%s, %s)"
        cursor.execute(sql, (self.user_id,self.user_name))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def query_all():
        conn = get_conn()
        cursor = conn.cursor()
        sql = "select * from user"
        cursor.execute(sql)
        rows = cursor.fetchall()
        users = []
        for r in rows:
            user = User(r[0], r[1])
            users.append(user)
        conn.commit()
        cursor.close()
        conn.close()
        return users
    
    def __str__(self):
        return "id:{}-name:{}".format(self.user_id, self.user_name)