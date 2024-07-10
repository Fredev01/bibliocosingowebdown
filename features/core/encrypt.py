from passlib.context import CryptContext

obj_crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def encrypt(password: str):
        return obj_crypt.hash(password)

    def are_equals(hashed_password, plain_password):
        #print (hashed_password + "  -  " + plain_password)
        return obj_crypt.verify(plain_password,hashed_password)
    