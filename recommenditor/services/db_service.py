
import MySQLdb
import sys

class db_service(object):

    def __init__(self):
        self.cnxn = MySQLdb.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            db = "reddit",
            charset = "utf8"
            )
        self.cur = self.cnxn.cursor()


    def execute(self, q, tup=None):
        try:
            if tup is None:
                self.cur.execute(q)
            else:
                tup_clean = []
                for bit in tup:
                    if isinstance(bit, basestring):
                        try:
                            bit = bit.encode("utf-8")
                        except:
                            bit = bit.encode("windows-1251")
                    tup_clean.append(bit)

                self.cur.execute(q, tup_clean)
        except:
            return {"status": 0, "errmsg": str(sys.exc_info())}
        return {"status": 1}


    def executemany(self, q, tups):
        try:
            print tups
            self.cur.executemany(q, tups)
            return {"status": 1}
        except:
            return {"status": 0, "errmsg": str(sys.exc_info())}


    def get_results(self):
        try:
            return self.cur.fetchall()
        except:
            return {"status": 0, "errmsg": str(sys.exc_info())}


    def commit(self):
        try:
            self.cnxn.commit()
            return {"status": 1}
        except:
            return {"status": 0, "errmsg": str(sys.exc_info())}


    def close(self):
        try:
            self.cnxn.close()
            return {"status": 1}
        except:
            return {"status": 0, "errmsg": str(sys.exc_info())}

