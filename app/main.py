from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# 添加调试日志以验证模块加载
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 确保 FastAPI 实例正确初始化
app = FastAPI()

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "FastAPI app is running"}

# 添加 OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 定义 Token 数据模型
class Token(BaseModel):
    access_token: str
    token_type: str

# 定义 TokenData 数据模型
class TokenData(BaseModel):
    username: str | None = None

# 假设的用户数据库
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedpassword",
        "disabled": False,
    }
}

# 假设的密码验证函数
def fake_hash_password(password: str):
    return "fakehashed" + password

# 假设的用户验证函数
def fake_verify_password(plain_password, hashed_password):
    return fake_hash_password(plain_password) == hashed_password

# 假设的用户获取函数
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return user_dict

# 假设的用户认证函数
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not fake_verify_password(password, user["hashed_password"]):
        return False
    return user

# 登录路由
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = fake_hash_password(form_data.username)
    logger.info(f"Access token generated for user: {user['username']}")
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
