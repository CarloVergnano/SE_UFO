from database.DB_connect import DBConnect
from model.avvistamenti import Avvistamento
from model.confinanti import Confinante
from model.stati import Stato

class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_anni():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                     select distinct year(s_datetime) as anno
                     from ufo_sightings.sighting
                     order by s_datetime
                     """
        try:
            cursor.execute(query, )
            for row in cursor:
                anno = row["anno"]
                result.append(anno)

        except Exception as e:
            print(f"Errore durante la query get_anni: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_forme(anno_selezionato):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                       select distinct shape
                       from ufo_sightings.sighting
                       where year(s_datetime) = %s and shape <> ""
                       order by shape
                       """
        try:
            cursor.execute(query, (anno_selezionato, ))
            for row in cursor:
                forma = row["shape"]
                result.append(forma)

        except Exception as e:
            print(f"Errore durante la query get_forme: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_stati():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                              select distinct id, name
                              from ufo_sightings.state
                              order by id
                              """
        try:
            cursor.execute(query, )
            for row in cursor:
                stato = Stato(
                    id=row["id"],
                    name=row["name"],
                )
                result.append(stato)

        except Exception as e:
            print(f"Errore durante la query get_all_stati: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_neighbors():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                              select *
                              from ufo_sightings.neighbor
                              where state1 in (select distinct state
                                               from ufo_sightings.sighting s 
                                               order by state)
                              and state2 in (select distinct state
                                             from ufo_sightings.sighting s 
                                             order by state)
                              order by state1, state2
                              """
        try:
            cursor.execute(query, )
            for row in cursor:
                confinante = Confinante(
                    state1=row["state1"],
                    state2=row["state2"],
                )
                result.append(confinante)

        except Exception as e:
            print(f"Errore durante la query get_all_neighbors: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_avvistamenti(anno_selezionato, forma_selezionata, stato):
        cnx = DBConnect.get_connection()
        result = 0

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                          select state, count(*) as num_avvistamenti
                          from ufo_sightings.sighting
                          where year(s_datetime) = %s and shape = %s and state = %s
                          group by state
                          order by state
                          """
        try:
            cursor.execute(query, (anno_selezionato, forma_selezionata, stato))
            for row in cursor:
                num_avvistamenti = row["num_avvistamenti"]
                result = num_avvistamenti

        except Exception as e:
            print(f"Errore durante la query get_avvistamenti: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result