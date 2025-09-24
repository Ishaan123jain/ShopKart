from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Hash():
    def hashpassword(password:str):
        return pwd_cxt.hash(password)
    
    def verify(plane_password:str, hashed_password:str):
        return pwd_cxt.verify(plane_password,hashed_password)