from abc import ABC,abstractmethod
import sqlite3
import os

class Service(ABC):
    @abstractmethod
    def main():
        pass

    def get_db():
        try:
            conn = sqlite3.connect("data.db")
        except Exception as e:
            print(e)
        conn.row_factory = sqlite3.Row
        return conn


    def addService(title:str,description:str,img):
        if title and description and img:
            upload = f"./static/images/services/{img.filename}"
            img.save(upload)
            upload_save = "."+upload
            conn = Service.get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO services(img,title,description) values(?,?,?)", (upload_save,title,description))
            conn.commit()
            conn.close()

    def removeService(id):
        conn = Service.get_db()
        cursor = conn.cursor()
        Service.deleteServiceImg(id)
        cursor.execute("delete from services where id = ?",(id,))
        conn.commit()
        conn.close()

    def updateService(id,newtitle,newdescription,newimage):
        conn = Service.get_db()
        cursor = conn.cursor()
        if id and newtitle and newdescription:
            cursor.execute("update services set title=?,description=? where id=? ;",(newtitle,newdescription,id))
            conn.commit()
        if newimage:
            Service.deleteServiceImg(id)
            upload_save = Service.saveServiceImg(newimage)
            cursor.execute("update services set img=? where id=? ;",(upload_save,id))
            
        conn.commit()
        conn.close()
    
    def getService(sername):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services WHERE description LIKE ?;",(sername,))
        servs = cursor.fetchall()
        conn.close()
        return servs

    def getAllService():
        pass

    def saveServiceImg(img):
        path = f"./static/images/services/{img.filename}"
        img.save(path)
        upload_save = "."+path
        return upload_save
    
    def deleteServiceImg(id):
        conn = Service.get_db()
        cursor = conn.cursor()
        cursor.execute("select img from services where id = ?;",(id,))
        conn.commit()
        img = cursor.fetchone()
        name = img[0].split('/')
        file_path = f"./static/images/services/{name[-1]}"
        if os.path.exists(file_path):
            os.remove(file_path)
