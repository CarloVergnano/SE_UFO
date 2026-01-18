from database.DB_connect import DBConnect
from model.avvistamenti import Avvistamento
from model.connessioni import Connessione
from model.stati import Stato

class DAO:

    @staticmethod
    def get_anni():
        conn = DBConnect.get_connection()

        result = set()

        cursor = conn.cursor(dictionary=True)
        query = """select s.s_datetime
                    from  sighting s 
                    order by s.s_datetime"""

        cursor.execute(query)

        for row in cursor:
            anno = row['s_datetime'].year
            result.add(anno)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_forme(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.shape 
                    from  sighting s 
                    where year(s.s_datetime) = %s
                    order by s.s_datetime"""

        cursor.execute(query, (anno,))

        for row in cursor:
            if row['shape']!= '':
                result.append(row['shape'])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_avvistamenti(anno, forma):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select s.id, count(*) as num_avvistamenti
                    from  state s, sighting s2 
                    where s.id = s2.state and year(s2.s_datetime) = %s and s2.shape = %s
                    group by s.id"""

        cursor.execute(query, (anno, forma))

        for row in cursor:
            result[row['id']] = row['num_avvistamenti']

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connesioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from  neighbor n 
                    group by n.state1 """

        cursor.execute(query,)

        for row in cursor:
            result.append(Connessione(row['state1'], row["state2"]))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_stati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s.id, s.name
                    from  state s  
                    group by s.id  """

        cursor.execute(query,)

        for row in cursor:
            result.append(Stato(row['id'], row["name"]))

        cursor.close()
        conn.close()
        return result

