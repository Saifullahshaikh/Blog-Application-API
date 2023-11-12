from model import userModel
import bcrypt
import jwt
import secrets

# Generate a random secret key of 256 bits (32 bytes)
# secret_key = secrets.token_hex(32)

# print(secret_key)

def create_jwt_token(user_id):
    payload = {"id": user_id}
    secret_key = secrets.token_hex(32)  # Replace with your secret key
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token



class userService:
    def __init__(self):
        pass

    def userSignup(userData:{}):
        print("xxxxxxxxx userSignup >>", userData)
        name = userData.name
        email = userData.email
        password = userData.password
        password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        # salt = salt
        hashed_password = bcrypt.hashpw(password, salt)
        print(f"Salt: {salt}")
        print(f"Hashed Password: {hashed_password}")
        create_table = userModel.userModel.user_table()
        # code to sign up a new user with the given data.
        result = userModel.userModel.add_user(name, email,salt.decode('utf-8'),hashed_password.decode('utf-8'))
        return result
    
    def loginUser(loginData:{}):
        user = userModel.userModel.get_user_by_email(loginData.email)

        if user is None:
            return {"error": "User not found"}

        hashed_password = user["password"].encode('utf-8')
        stored_salt = user["salt"]
        # hashed_password = bcrypt.hashpw(hashed_password,stored_salt)

        provided_password = loginData.password.encode('utf-8')
        print(f"Salt: {stored_salt}")
        print(f"Hashed Password: {hashed_password}")
        
        
        if bcrypt.checkpw(provided_password, hashed_password):
            # Passwords match, user is authenticated
            # You can generate and return a JWT token here for authentication if needed
            token = create_jwt_token(user["id"])
            return {"message": "Login successful", "token": token}
        else:
            return {"error": "Invalid password"}
        
    def createBlogPost(blogData: {}):
        print("xxxxxxxxx createBlogPost >>", blogData)
        title = blogData.get("title")
        content = blogData.get('content')
        user_id = blogData.get('user_id')  # Assuming you have the user ID available in the blogData
        blog_table = userModel.userModel.create_blog_table()
        if not title or not content or not user_id:
            return {"error": "Title, content, and user_id are required fields."}

        result = userModel.userModel.create_blog_post(user_id, title, content)
        return result

    def postComment(commentData: {}):
        print("xxxxxxxxx postComment >>", commentData)
        user_id = commentData.get("user_id")  # Assuming you have the user ID available in the commentData
        post_id = commentData.get("post_id")
        comment = commentData.get("comment")
        comment_table = userModel.userModel.create_comment_table()

        if not user_id or not post_id or not comment:
            return {"error": "user_id, post_id, and comment are required fields."}

        result = userModel.userModel.post_comment(user_id, post_id, comment)
        return result

# Example usage:
blog_data = {"user_id": 1, "title": "Sample Blog Post", "content": "This is the content of the blog post."}
comment_data = {"user_id": 1, "post_id": 1, "comment": "This is a comment on the blog post."}
