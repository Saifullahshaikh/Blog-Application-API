import json
from db import get_connection, close_connection
from psycopg2 import IntegrityError



class userModel:
    @staticmethod
    def get_user_by_email(email):
        sql = "SELECT * FROM users WHERE email = %s"
        conn = get_connection()

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (email,))
                user = cursor.fetchone()

                if user:
                    user_data = {
                        "id": user[0],
                        "uuid": user[1],
                        "name": user[2],
                        "email": user[3],
                        "salt": user[4],
                        "password": user[5]
                        
                    }
                    return user_data
                else:
                    return None
        close_connection(conn)
        
    def user_table():
        sql = """
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            uuid UUID DEFAULT uuid_generate_v4(),
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            salt VARCHAR(255) NOT NULL ,
            password VARCHAR(255) NOT NULL 
        )
        """
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
                # print("xxxxxxxxxxxxxxxxxxxxx model ", cursor.fetchone()[0])
                # result = cursor.fetchone()
        close_connection(conn)
        return "table created"
    
    def add_user(name, email, salt, password):
        check_existing_email_query = "SELECT id FROM users WHERE email = %s"
        conn = get_connection()

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(check_existing_email_query, (email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    # Email already exists, return an error response
                    return {"error": "Email is already in use."}
        try:    
            sql = """
                INSERT INTO users (name, email, salt, password)
                VALUES (%s, %s, %s, %s)
                RETURNING id, uuid, name, email;
            """
            conn = get_connection()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (name, email, salt, password))
                    conn.commit()
                    # print("xxxxxxxxxxxxxxxxxxxxx model ", cursor.fetchone()[0])
                    result = cursor.fetchone()
                    if result:
                        result_data = {
                            "id": result[0],
                            "uuid": result[1],
                            "name": result[2],
                            "email": result[3]
                        }
        except IntegrityError:
            # Handle any database integrity violation (e.g., unique constraint violation)
            return {"error": "Failed to insert user. Email is already in use."}   
        close_connection(conn)
        return {"error": ""}
    def create_blog_table():
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS blog_posts (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            conn = get_connection()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
            return {"success": True, "message": "Blog table created successfully"}
        except Exception as e:
            return {"error": str(e)}

    def create_comment_table():
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS comments (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    post_id INTEGER REFERENCES blog_posts(id),
                    comment TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            conn = get_connection()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
            return {"success": True, "message": "Comment table created successfully"}
        except Exception as e:
            return {"error": str(e)}
        
    def create_blog_post(user_id, title, content):
        try:
            sql = """
                INSERT INTO blog_posts (user_id, title, content)
                VALUES (%s, %s, %s)
                RETURNING id;
            """
            conn = get_connection()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (user_id, title, content))
                    post_id = cursor.fetchone()[0]
            return {"success": True, "post_id": post_id}
        except Exception as e:
            return {"error": str(e)}

    def post_comment(user_id, post_id, comment):
        try:
            sql = """
                INSERT INTO comments (user_id, post_id, comment)
                VALUES (%s, %s, %s)
                RETURNING id;
            """
            conn = get_connection()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (user_id, post_id, comment))
                    comment_id = cursor.fetchone()[0]
            return {"success": True, "comment_id": comment_id}
        except Exception as e:
            return {"error": str(e)}
