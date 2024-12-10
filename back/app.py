from flask import Flask, request, jsonify, render_template, redirect
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import mysql.connector

app = Flask(__name__)

def set_connection():
    """
    Sets a conection with the database
    """
    conn = mysql.connector.connect(
        user='ivetranotask',
        password='tasks123',
        host='ivetranotask.mysql.pythonanywhere-services.com',
        database='ivetranotask$default')
    return conn


# TASKS

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Gets all the tasks
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()

        tasks_list = []
        for task in tasks:
            tasks_list.append({
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'priority': task[3],
                'status': task[4],
                'creation_date': task[5],
                'end_date': task[6],
                'was_made_by': task[7]
            })
        return jsonify(tasks_list), 200
    
    except SQLAlchemyError as e:
        return str(e)
    
    finally:
        conn.close()

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    try:
        conn = set_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM tasks WHERE id = %s"
        cursor.execute(query, (task_id))
        task = cursor.fetchone()

        if task:
            task_data = {
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'priority': task[3],
                'status': task[4],
                'creation_date': task[5],
                'end_date': task[6],
                'was_made_by': task[7]
            }
            return jsonify(task_data), 200
        else:
            return jsonify({"error": "Task not found"}), 404

    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
    finally:
        conn.close()

@app.route('/tasks', methods=['GET'])
def get_tasks_with_filters():
    """
    Gets the tasks that match the filter
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()

        filters = {
            'title': request.args.get('title'),
            'status': request.args.get('status'),
            'priority': request.args.get('priority'),
            'was_made_by': request.args.get('was_made_by'),
            'assigned_to': request.args.get('assigned_to'),
            'end_date': request.args.get('end_date'),
            'creation_date': request.args.get('creation_date')
        }
        tags = request.args.getlist("tags")
        
        query = """
            SELECT DISTINCT * t.*
            FROM tasks t
            LEFT JOIN assignedTo at ON t.id = at.id_task
            LEFT JOIN hasTag ht ON t.id = ht.id_task
            WHERE 1=1
            """
        params = []
        
        if filters['title']:
            query += " AND t.title LIKE %s"
            params.append(f"%{filters['title']}")
        
        if filters['status']:
            query += " AND t.status = %s"
            params.append(filters['status'])

        if filters['priority']:
            query += " AND t.priority = %s"
            params.append(filters['priority'])
        
        if filters['was_made_by']:
            query += " AND t.was_made_by = %s"
            params.append(filters['was_made_by'])
        
        if filters['assigned_to']:
            query += " AND at.username = %s"
            params.append(filters['assigned_to'])
        
        if filters['end_date']:
            query += " AND t.end_date = %s"
            params.append(filters['end_date'])
        
        if filters['creation_date']:
            query += " AND t.creation_date = %s"
            params.append(filters['creation_date'])
        
        if tags:
            query += """
            AND t.id IN (
                SELECT ht.id_task
                FROM hasTag ht
                WHERE ht.tag_name IN ({})
                GROUP BY ht.id_task
                HAVING COUNT(ht.tag_name) = %s
            )
            """.format(', '.join(['%s'] * len(tags)))
            params.extend(tags)
            params.append(len(tags))
        
        cursor.execute(query, params)
        tasks = cursor.fetchall()
        return jsonify(tasks), 200

    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    
    finally:
        conn.close()
        
        

@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Creates a task with the specified data
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()
        new = request.get_json()
        query = """
        INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query,(
            new['title'],
            new['description'],
            new['priority'],
            new['status'],
            new['creation_date'],
            new['end_date'],
            new['was_made_by']
        ))
        conn.commit()
        return jsonify({'message': 'Task created successfully'}), 201
    
    except KeyError as e:
        missing_field = str(e).strip("'")
        return jsonify({'error': f'Missing required field: {missing_field}'}), 400

    except mysql.connector.errors.IntegrityError as e:
        return jsonify({"error": "Integrity error", "details": str(e)}), 400
    
    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    
    finally:
        conn.close()

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """
    Updates the task that matches the id with the specified data
    """
    try:
        data = request.get_json()
        conn = set_connection()
        cursor = conn.cursor()

        query = """
        UPDATE tasks
        SET title = %s, description = %s, priority = %s, status = %s, creation_date = %s, end_date = %s, was_made_by = %s
        WHERE id = %s
        """
        cursor.execute(query, (
            data['title'],
            data['description'],
            data['priority'],
            data['status'],
            data['creation_date'],
            data['end_date'],
            data['was_made_by'],
            id
        ))

        conn.commit()
        return jsonify({'message': 'Task updated successfully'}), 200
    
    except KeyError as e:
        missing_field = str(e).strip("'")
        return jsonify({'error': f'Missing required field: {missing_field}'}), 400

    except mysql.connector.errors.IntegrityError as e:
        return jsonify({"error": "Integrity error", "details": str(e)}), 400
    
    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

    finally:
        cursor.close()


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    """
    Deletes the task that matches the id
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()

        query = "DELETE FROM tasks WHERE id = %s"
        cursor.execute(query, (id))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({'message': 'Task deleted successfully'}), 200
    
    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    finally:
        cursor.close()

@app.route('/tasks/subtasks/<int:parent_id>', methods=['GET'])
def get_subtasks(parent_id):
    try:
        conn = set_connection
        cursor = conn.cursor()
        
        query = """
            SELECT t.*
            FROM subtasks s
            LEFT JOIN tasks t ON s.id_subtask = t.id
            WHERE s.id_task = %s
        """
        cursor.execute(query, (parent_id))
        subtasks = cursor.fetchall()
        
        subtasks_list = []
        for task in subtasks:
            subtasks_list.append({
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'priority': task[3],
                'status': task[4],
                'creation_date': task[5],
                'end_date': task[6],
                'was_made_by': task[7]
            })
        return jsonify(subtasks_list), 200
    
    except SQLAlchemyError as e:
        return str(e)
    
    finally:
        conn.close()


@app.route('/tasks/subtasks', methods=['POST'])
def create_subtask():
    try:
        conn = set_connection()
        cursor = conn.cursor()

        new = request.get_json()
        title = new['title']
        description = new['description']
        priority = new['priority']
        status = new['status']
        creation_date = new['creation_date']
        end_date = new['end_date']
        was_made_by = new['was_made_by']
        parent_task_id = new['parent_task_id']

        # Verify the existence of the parent task
        cursor.execute("SELECT id FROM tasks WHERE id = %s", (parent_task_id,))
        parent_task = cursor.fetchone()
        if not parent_task:
            return jsonify({"error": "Parent task not found"}), 404

        # Create the new task
        query_create_task = """
        INSERT INTO tasks (title, description, priority, status, creation_date, end_date, was_made_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_create_task, (
            title, description, priority, status, creation_date, end_date, was_made_by
        ))
        new_task_id = cursor.lastrowid  # Get the last task id

        # Create the subtask relationship
        query_create_subtask = """
        INSERT INTO subtasks (id_subtask, id_task)
        VALUES (%s, %s)
        """
        cursor.execute(query_create_subtask, (new_task_id, parent_task_id))
        conn.commit()

        return jsonify({
            "message": "Subtask created successfully",
            "subtask_id": new_task_id,
            "parent_task_id": parent_task_id
        }), 201
    
    except KeyError as e:
        missing_field = str(e).strip("'")
        return jsonify({'error': f'Missing required field: {missing_field}'}), 400

    except mysql.connector.errors.IntegrityError as e:
        return jsonify({"error": "Integrity error", "details": str(e)}), 400
    
    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    
    finally:
        conn.close()


# USERS

@app.route('/users', methods=['GET'])
def get_users():
    """
    Gets all the users
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        users_list = []
        for user in users:
            users_list.append({
                'id': user[0],
                'title': user[1],
                'description': user[2],
                'priority': user[3],
                'status': user[4],
                'creation_date': user[5],
                'end_date': user[6],
                'was_made_by': user[7]
            })
        return jsonify(users_list), 200
    
    except SQLAlchemyError as e:
        return str(e)
    
    finally:
        conn.close()

@app.route('/users', methods=['POST'])
def create_user():
    """
    Creates a user with the specified data
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()
        new = request.get_json()
        query = """
        INSERT INTO users()
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query,(
            new['title'],
            new['description'],
            new['priority'],
            new['status'],
            new['creation_date'],
            new['end_date'],
            new['was_made_by']
        ))
        conn.commit()
        return jsonify({'message': 'Task created successfully'}), 201
    
    except KeyError as e:
        missing_field = str(e).strip("'")
        return jsonify({'error': f'Missing required field: {missing_field}'}), 400

    except mysql.connector.errors.IntegrityError as e:
        return jsonify({"error": "Integrity error", "details": str(e)}), 400
    
    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    
    finally:
        conn.close()


if __name__ == '__main__':
    app.run()