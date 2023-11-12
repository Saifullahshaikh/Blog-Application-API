from fastapi import APIRouter,Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from service import userService
from fastapi.security import OAuth2PasswordBearer
from typing import List





router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class SignupData(BaseModel):
    name: str
    password: str
    email: EmailStr


@router.post("/user/signup")
def signup(data: SignupData):
    
    user = userService.userService.userSignup(data)
    if user['error']:
        return {"code":200, "Data": user, "Message": "Signup UnSuccessful"}
    return {"code":200, "Data": user, "Message": "Signup Successful"}



class LoginData(BaseModel):
    email: EmailStr
    password: str
@router.post("/user/login")
def signup(data: LoginData):
    user = userService.userService.loginUser(data)
    print("xxxxxxxxxxxxxxxxxxxxx login")
    return {"code":200, "Data": user}

# function to get current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return userService.verify_jwt_token(token, userService.secret_key)

class BlogData(BaseModel):
    title: str
    content: str
    user_id: int

@router.post("/blog/create")
# def create_blog(data: BlogData, current_user: dict = Depends(userService.verify_token)):
    # print(get_current_user)
def create_blog(data: BlogData):
    blog_data = {"user_id": data.user_id, "title": data.title, "content": data.content}
    result = userService.userService.createBlogPost(blog_data)
    return result

class CommentData(BaseModel):
    post_id: int
    user_id: int
    comment: str
    
# @router.post("/comment/create", response_model=dict)
@router.post("/comment/create")
def create_comment(data: CommentData):
    comment_data = {"user_id":data.user_id, "post_id": data.post_id, "comment": data.comment}
    result = userService.userService.postComment(comment_data)
    return result

