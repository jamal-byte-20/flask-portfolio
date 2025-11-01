from abc import ABC,abstractmethod
import sqlite3
import os

class Project(ABC):
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

    def addProject(img,title,description,link):
        if img and title and description and link:
            upload = f"./static/images/projects/{img.filename}"
            img.save(upload)
            upload_save = "."+upload
            conn = Project.get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO project(img,title,description,link) values(?,?,?,?)", (upload_save,title,description,link))
            conn.commit()
            conn.close()
    
    def removeProject(id):
        conn = Project.get_db()
        cursor = conn.cursor()
        Project.deleteServiceImg(id)
        cursor.execute("delete from project where id = ?",(id,))
        conn.commit()
        conn.close()

    def updateProject(id,newtitle,newdescription,newlink,newimage):
        conn = Project.get_db()
        cursor = conn.cursor()
        if id and newtitle and newdescription and newlink:
            cursor.execute("update project set title=?,description=?,link=? where id=? ;",(newtitle,newdescription,newlink,id))
            conn.commit()
        if newimage:
            Project.deleteServiceImg(id)
            upload_save = Project.saveServiceImg(newimage)
            cursor.execute("update project set img=? where id=? ;",(upload_save,id))
            
        conn.commit()
        conn.close()

    def getProject(projname):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM project WHERE title LIKE ?;",(projname,))
        servs = cursor.fetchall()
        conn.close()
        return servs

    def saveServiceImg(img):
        path = f"./static/images/projects/{img.filename}"
        img.save(path)
        upload_save = "."+path
        return upload_save
    
    def deleteServiceImg(id):
        conn = Project.get_db()
        cursor = conn.cursor()
        cursor.execute("select img from project where id = ?;",(id,))
        conn.commit()
        img = cursor.fetchone()
        name = img[0].split('/')
        file_path = f"./static/images/projects/{name[-1]}"
        if os.path.exists(file_path):
            os.remove(file_path)

