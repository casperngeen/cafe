from config import DbConfig
from datetime import date
import mysql.connector
from exceptions.exceptions import AppError, DatabaseError

class EmployeeModel:
    @classmethod
    def get_all_employees(cls, cafe=None):
        query_no_cafe = '''
            SELECT e.id, e.name, e.email_address, e.phone_number, DATEDIFF(CURDATE(), e.start_date) AS days_worked, c.name 
            FROM employees e 
            JOIN cafe c 
            ON e.cafe_id = c.id
        '''
        if cafe:
            query_cafe = '''
            SELECT e.id, e.name, e.email_address, e.phone_number, DATEDIFF(CURDATE(), e.start_date) AS days_worked, c.name 
            FROM employees e 
            JOIN cafe c 
            ON e.cafe_id = c.id
            WHERE c.name = %s
        '''
        
        with DbConfig.get_db_connection() as db_connection:
            try:
                with db_connection.cursor(dictionary=True) as cursor:
                    if cafe:
                        cursor.execute(query_cafe, (cafe,))
                    else:
                        cursor.execute(query_no_cafe)
                    result = cursor.fetchall()
                    return result
            except mysql.connector.Error as err:
                raise DatabaseError(err)
            except Exception as err:
                raise AppError(err)
            
    @classmethod
    def add_employee(cls, data):
        query = '''
            INSERT INTO Employee (name, email_address, phone_number, gender, start_date, cafe_id)
            VALUES(%s, %s, %s, %s, %s, (SELECT id FROM Cafe WHERE name = %s))
        '''
        
        with DbConfig.get_db_connection() as db_connection:
            with db_connection.cursor(dictionary=True) as cursor:
                try:
                    values = (data['name'], 
                            data['email_address'], 
                            data['phone_number'], 
                            data['gender'],
                            date.today(), 
                            data['cafe_name'])
                    cursor.execute(query, values)
                    db_connection.commit()
                    employee_id = cursor.lastrowid
                    return {"success": True, "employee_id": employee_id}
                except mysql.connector.Error as err:
                    db_connection.rollback()
                    raise DatabaseError(err)
                except Exception as err:
                    raise AppError(err)
                
    @classmethod
    def update_employee(cls, data):
        query = '''
            UPDATE Employee
            SET name=%s, 
                email_address=%s, 
                phone_number=%s, 
                gender=%s,
                cafe_id=(SELECT id FROM Cafe WHERE name = %s)
            WHERE id=%s
        '''
        
        with DbConfig.get_db_connection() as db_connection:
            with db_connection.cursor(dictionary=True) as cursor:
                try:
                    values = (data['name'], 
                            data['email_address'], 
                            data['phone_number'], 
                            data['gender'], 
                            data['cafe_name'],
                            data['employee_id'])
                    cursor.execute(query, values)
                    db_connection.commit()
                    return {"success": True, "message": f"Updated employee {data['employee_id']}"}
                except mysql.connector.Error as err:
                    db_connection.rollback()
                    raise DatabaseError(err)
                except Exception as err:
                    raise AppError(err)

    @classmethod
    def delete_employee(cls, data):
        query = '''
            DELETE FROM Employee
            WHERE id=%s
        '''
        
        with DbConfig.get_db_connection() as db_connection:
            with db_connection.cursor(dictionary=True) as cursor:
                try:
                    values = (data['employee_id'],)
                    cursor.execute(query, values)
                    db_connection.commit()
                    return {"success": True, "message": f"Deleted employee {data['employee_id']}"}
                except mysql.connector.Error as err:
                    db_connection.rollback()
                    raise DatabaseError(err)
                except Exception as err:
                    raise AppError(err)
