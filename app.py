# there are two ways of creating REST API in flask
# 1.using flask without adding any external library
# 2.using flask_Restful library 

# we will use the #2 
#   incase your are using your personal computer
# pip3 install flask -restful
from flask import *
# import pymysql for database connection 
import pymysql
from flask_restful import Resource,Api
# create a flask  app 
app = Flask(__name__)

# create an Api object 
api = Api(app )
# we need to make a class for a particular Resource 
# the class will inherit from the resource thus implimenting the post,get,delete and put request methods

class Employees(Resource):
    def get(self):
        connection = pymysql.connect(host='localhost', user='root', password='', database='ampapp')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "select * from employees"
        # execute
        cursor.execute(sql)
        # check ifwe have empty records 
        if cursor.rowcount == 0:
            return jsonify({"message":"NO record Found"})
        else:
            employees = cursor.fetchall()
            return jsonify(employees)
    def post(self):
        data = request.json
        firstname = data["firstname"]
        others = data["others"]
        salary =data ["salary"]
        department = data["department"]
        # connection to db 
        connection = pymysql.connect(host='localhost', user='root', password='', database='ampapp')
        cursor = connection.cursor()
        sql = "INSERT INTO `employees` (`firstname`, `others`, `salary`, `department`) VALUES (%s, %s, %s, %s)"

        try:
            # execute
            data = (firstname,others,salary,department)
            cursor.execute(sql,(data))
            
            # save the changes 
            connection.commit()

            return jsonify({"message":"Employee saved succesfully"})
        except:
            connection.rollback()
            return jsonify({"message":"failed to save"})
            

    def put(self):
        data =request.json
        id = data["id"]
        firstname =data["firstname"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='ampapp')
        cursor = connection.cursor()
        sql = "update employees SET firstname = %s where id =%s"
        try:
            data = (firstname,id)
            cursor.execute(sql,data)
            connection.commit()
            return jsonify({"message":"Employee updated successfully"})
        except:
            connection.rollback()
            return jsonify({"message":"failed to update"})
            

    def delete(self):
       data =request.json
       id = data["id"]
       connection = pymysql.connect(host='localhost', user='root', password='', database='ampapp')
       cursor = connection.cursor()
       sql1 = "select * from employees where id  = %s"
       cursor.execute(sql1,id)
    # check if the id exist the proceed to delete if does not exists dont delete 
       if cursor.rowcount == 0:
           return jsonify({"message":"id not found"})
       else:
             sql = "DELETE FROM employees WHERE id = %s"
        
       try:
           
           cursor.execute(sql,id)
           connection.commit()
           return jsonify({"message":"employee deleted successfully"})
       except:
            connection.rollback()
            return jsonify({"message":"failed to delete"})
# we need to add our resource/resource that we defined along with its corresponding url 
    
api.add_resource(Employees,'/employees')

if __name__== '__main__':

    app.run(debug = True)








