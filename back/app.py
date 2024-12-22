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

# ----------------------------------------------------------------------------
# TASKS

@app.route('/tasks', methods=['GET'])
def get_tasks():
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
            'creation_date': request.args.get('creation_date'),
            'id_parent': request.args.get('id_parent')
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
        
        if filters['id_parent']:
            query += " AND t.id_parent = %s"
            params.append(filters['id_parent'])
        
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
                'was_made_by': task[7],
                'id_parent': task[8]
            })
        return jsonify(tasks_list), 200

    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    
    finally:
        conn.close()

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    try:
        conn = set_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM tasks WHERE id = %s"
        cursor.execute(query, (task_id,))
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
                'was_made_by': task[7],
                'id_parent': task[8]
            }
            return jsonify(task_data), 200
        else:
            return jsonify({"error": "Task not found"}), 404

    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
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
        data_task = {
            'title': request.args.get('title'),
            'description': request.args.get('description'),
            'priority': request.args.get('priority'),
            'status': request.args.get('status'),
            'end_date': request.args.get('end_date'),
            'was_made_by': request.args.get('was_made_by'),
            'id_parent': request.args.get('id_parent')
        }
        tags = request.args.getlist("tags")
        assigned_users = request.args.getlist("assigned_to")
        if not data_task['id_parent']: data_task['id_parent'] = "NULL"

        query = """
        INSERT INTO tasks(title, description, priority, status, end_date, was_made_by, id_parent)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query,(
            data_task['title'],
            data_task['description'],
            data_task['priority'],
            data_task['status'],
            data_task['end_date'],
            data_task['was_made_by'],
            data_task['id_parent']
        ))

        task_id = cursor.lastrowid

        for tag in tags:
            cursor.execute("INSERT INTO hastag(id_task, tag_name) VALUES (%s, %s)", (task_id, tag))
        
        for user in assigned_users:
            cursor.execute("INSERT INTO assignedTo(id_task, username) VALUES (%s, %s)", (task_id, user))

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

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Updates a task with the specified data
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()

        data_task = request.get_json()

        cursor.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404

        fields = []
        values = []

        for key in ['title', 'description', 'priority', 'status', 'end_date']:
            if key in data_task:
                fields.append(f"{key} = %s")
                values.append(data_task[key])

        if fields:
            update_query = f"""
            UPDATE tasks
            SET {', '.join(fields)}
            WHERE id = %s
            """
            values.append(task_id)
            cursor.execute(update_query, values)

        if 'tags' in data_task:
            tags = data_task['tags']
            cursor.execute("DELETE FROM hasTag WHERE id_task = %s", (task_id,))
            for tag in tags:
                cursor.execute("INSERT INTO hasTag (id_task, tag_name) VALUES (%s, %s)", (task_id, tag))

        if 'assigned_users' in data_task:
            assigned_users = data_task['assigned_users']
            cursor.execute("DELETE FROM assignedTo WHERE id_task = %s", (task_id,))
            for user in assigned_users:
                cursor.execute("INSERT INTO assignedTo (id_task, username) VALUES (%s, %s)", (task_id, user))

        conn.commit()
        return jsonify({'message': 'Task updated successfully'}), 200

    except mysql.connector.errors.IntegrityError as e:
        return jsonify({"error": "Integrity error", "details": str(e)}), 400

    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

    finally:
        conn.close()




@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    """
    Deletes the task that matches the id
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()

        query = "DELETE FROM tasks WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({'message': 'Task deleted successfully'}), 200
    
    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    finally:
        cursor.close()

# -------------------------------------------------------------------------
# USERS

@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = set_connection()
        cursor = conn.cursor()
        filters = {
            'name': request.args.get('name')
        }

        query = """
            SELECT * FROM users u
            WHERE 1=1
        """
        params = []

        if filters['name']:
            query += " AND u.name LIKE %s"
            params.append(filters['name'])

        cursor.execute(query, params)
        users = cursor.fetchall()

        users_list = []
        for user in users:
            users_list.append({
                'username': user[0],
                'name': user[2],
                'email': user[3],
                'role': user[4]
            })
        return jsonify(users_list), 200
    
    except SQLAlchemyError as e:
        return str(e)
    
    finally:
        conn.close()

@app.route('/users/<string:username>', methods=['PUT'])
def get_user_by_username(username):
    try:
        conn = set_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user:
            user_data = {
                'username': user[0],
                'name': user[2],
                'email': user[3],
                'role': user[4]
            }
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
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

        data_user = {
            'username': request.args.get('username'),
            'password': request.args.get('password'),
            'name': request.args.get('name'),
            'email': request.args.get('email'),
            'role': request.args.get('role')
        }

        query = """
        INSERT INTO users(username, password, name, email, role)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query,(
            data_user['username'],
            data_user['password'],
            data_user['name'],
            data_user['email'],
            data_user['role']
        ))
        conn.commit()
        return jsonify({'message': 'User created successfully'}), 201
    
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


@app.route('/users/<string:username>', methods=['PUT'])
def update_user(username):
    """
    Updates a user's information based on the specified data
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()

        data_user = request.get_json()

        fields = []
        values = []

        for key in ['name', 'password', 'email', 'role']:
            if key in data_user:
                fields.append(f"{key} = %s")
                values.append(data_user[key])

        if not fields:
            return jsonify({'error': 'No fields provided for update'}), 400

        query = f"""
        UPDATE users
        SET {', '.join(fields)}
        WHERE username = %s
        """
        values.append(username)

        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'message': 'User updated successfully'}), 200
    
    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    
    finally:
        conn.close()

@app.route('/users/<string:username>', methods=['DELETE'])
def delete_user(username):
    """
    Deletes the user that matches the username
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()

        query = "DELETE FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({'message': 'User deleted successfully'}), 200
    
    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    finally:
        cursor.close()

# ----------------------------------------------------------------------------------
# TAGS

@app.route('/tags', methods=['GET'])
def get_tags():
    try:
        conn = set_connection()
        cursor = conn.cursor()
        filters = {
            'name': request.args.get('name')
        }

        query = """
            SELECT * FROM tags t
            WHERE 1=1
        """
        params = []

        if filters['name']:
            query += " AND t.name LIKE %s"
            params.append(filters['name'])

        cursor.execute(query, params)
        tags = cursor.fetchall()

        tags_list = []
        for tag in tags:
            tags_list.append({
                'username': tag[0],
                'colour': tag[1]
            })
        return jsonify(tags_list), 200
    
    except SQLAlchemyError as e:
        return str(e)
    
    finally:
        conn.close()

@app.route('/tags/<string:name>', methods=['PUT'])
def get_tag_by_name(name):
    try:
        conn = set_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM tags WHERE name = %s"
        cursor.execute(query, (name,))
        tag = cursor.fetchone()

        if tag:
            tag_data = {
                'name': tag[0],
                'colour': tag[1]
            }
            return jsonify(tag_data), 200
        else:
            return jsonify({"error": "Tag not found"}), 404

    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
    finally:
        conn.close()

@app.route('/tags', methods=['POST'])
def create_tag():
    """
    Creates a tag with the specified data
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()

        data_tag = {
            'name': request.args.get('name'),
            'colour': request.args.get('colour')
        }

        query = """
        INSERT INTO tags(name, colour)
        VALUES (%s, %s)
        """
        cursor.execute(query,(
            data_tag['name'],
            data_tag['colour']
        ))
        conn.commit()
        return jsonify({'message': 'Tag created successfully'}), 201
    
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

@app.route('/tags/<string:name>', methods=['PUT'])
def update_tag(name):
    """
    Updates a tag's information based on the specified data
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()

        data_tag = request.get_json()

        fields = []
        values = []

        for key in ['name', 'colour']:
            if key in data_tag:
                fields.append(f"{key} = %s")
                values.append(data_tag[key])

        if not fields:
            return jsonify({'error': 'No fields provided for update'}), 400

        query = f"""
        UPDATE tags
        SET {', '.join(fields)}
        WHERE name = %s
        """
        values.append(name)

        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Tag not found'}), 404

        return jsonify({'message': 'Tag updated successfully'}), 200
    
    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    
    finally:
        conn.close()

@app.route('/tags/<string:name>', methods=['DELETE'])
def delete_tag(name):
    """
    Deletes the tag that matches the username
    """
    try:
        conn = set_connection()
        cursor = conn.cursor()

        query = "DELETE FROM tags WHERE name = %s"
        cursor.execute(query, (name,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Tag not found"}), 404

        return jsonify({'message': 'Tag deleted successfully'}), 200
    
    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    finally:
        cursor.close()

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run()