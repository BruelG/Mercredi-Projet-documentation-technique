from django.db import models
class Admin_Admission(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return self.username
    
    @classmethod
    def login_user(cls, username,password):
        try:
            user = cls.objects.get(username=username,password=password)
            if user.username == username and user.password== password:
                user_info = {
                    'id': user.id,
                    'code_user': user.username,
                    'password': user.password,
                    'email': user.email,
                }
                return user_info,True
            else :
                return False,None
        except cls.DoesNotExist:
            return None ,False