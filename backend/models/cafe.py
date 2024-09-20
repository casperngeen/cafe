from config import DbConfig
from datetime import date
import mysql.connector
from exceptions.exceptions import AppError, DatabaseError

class CafeModel:
    @classmethod
    def get_all_cafes(cls, location=None):
        query_no_location = '''
            SELECT c.name, c.description, c.location, c.logo, c.id, COUNT(e.id) AS employee_count
            FROM employees e
            JOIN cafe c ON e.cafe_id = c.id
            GROUP BY c.name, c.description, c.location, c.logo, c.id
            ORDER BY employee_count DESC
        '''
        if location:
            query_location = '''
            SELECT c.name, c.description, c.location, c.logo, c.id, COUNT(e.id) AS employee_count
            FROM employees e
            JOIN cafe c ON e.cafe_id = c.id
            WHERE c.location = %s
            GROUP BY c.name, c.description, c.location, c.logo, c.id
            ORDER BY employee_count DESC
        '''
        
        with DbConfig.get_db_connection() as db_connection:
            try:
                with db_connection.cursor(dictionary=True) as cursor:
                    if location:
                        cursor.execute(query_location, (location,))
                    else:
                        cursor.execute(query_no_location)
                    result = cursor.fetchall()
                    return result
            except mysql.connector.Error as err:
                raise DatabaseError(err)
            except Exception as err:
                raise AppError(err)
            
    @classmethod
    def add_cafe(cls, data):
        query = '''
            INSERT INTO Cafe (name, description, location)
            VALUES(%s, %s, %s)
        '''
        
        with DbConfig.get_db_connection() as db_connection:
            with db_connection.cursor(dictionary=True) as cursor:
                try:
                    values = (data['name'], 
                            data['description'], 
                            data['location'])
                    cursor.execute(query, values)
                    db_connection.commit()
                    cafe_id = cursor.lastrowid
                    return {"success": True, "cafe_id": cafe_id}
                except mysql.connector.Error as err:
                    db_connection.rollback()
                    raise DatabaseError(err)
                except Exception as err:
                    raise AppError(err)
                
    @classmethod
    def update_cafe(cls, data):
        query = '''
            UPDATE Cafe
            SET name=%s, 
                description=%s,
                location=%s
            WHERE id=%s
        '''
        
        with DbConfig.get_db_connection() as db_connection:
            with db_connection.cursor(dictionary=True) as cursor:
                try:
                    values = (data['name'], 
                            data['description'], 
                            data['location'],
                            data['cafe_id'])
                    cursor.execute(query, values)
                    db_connection.commit()
                    return {"success": True, "message": f"Updated cafe {data['cafe_id']}"}
                except mysql.connector.Error as err:
                    db_connection.rollback()
                    raise DatabaseError(err)
                except Exception as err:
                    raise AppError(err)

    @classmethod
    def delete_cafe(cls, data):
        query = '''
            DELETE FROM Cafe
            WHERE id=%s
        '''
        
        with DbConfig.get_db_connection() as db_connection:
            with db_connection.cursor(dictionary=True) as cursor:
                try:
                    values = (data['cafe_id'],)
                    cursor.execute(query, values)
                    db_connection.commit()
                    return {"success": True, "message": f"Deleted cafe {data['cafe_id']}"}
                except mysql.connector.Error as err:
                    db_connection.rollback()
                    raise DatabaseError(err)
                except Exception as err:
                    raise AppError(err)
