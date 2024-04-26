"""
Class будет описывать состояние текущего пользователя: 
статус авторизации, активности и способ определения
уникального идентификатора.
"""
class UserLogin:
    def fromDB(self, user_id, db):
        """используется при создании объекта в декораторе user_loader"""
        self.__user = db.getUser(user_id)
        return self
 
    def create(self, user):
        """используется при создании объекта в момент авторизации пользователя"""
        self.__user = user
        return self
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        """Get id!!!"""
        return str(self.__user['id'])