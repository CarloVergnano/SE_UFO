from database.dao import DAO

result = DAO.get_avvistamenti(2012, "triangle")
print (result)