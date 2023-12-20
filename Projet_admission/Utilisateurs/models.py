import datetime
from django.db import models
from django.contrib.auth import authenticate, login

class Utilisateurs(models.Model):
    code_user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    actifs = models.BooleanField()
    dateCreation = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.code_user

    @classmethod
    def create_user(cls, code_user, password, email):
        user = cls(code_user=code_user, Password=password, Email=email, Actifs=True, DateCreation=datetime.datetime.now())
        user.save()
        return True
    @classmethod
    def login_user(cls, code_user,password):
        try:
            user = cls.objects.get(code_user=code_user,password=password)
            if user.code_user == code_user and user.password== password:
                user_info = {
                    'id': user.id,
                    'code_user': user.code_user,
                    'password': user.password,
                    'email': user.email,
                }
                return user_info,True
            else :
                return False,None
        except cls.DoesNotExist:
            return None ,False
    @classmethod
    def get_user_id(cls,id_user):
        try:
            user = cls.objects.get(id=id_user)
            info ={
                "code_user": user.code_user,
                "email" : user.email,
            }
            return info, True
        except cls.DoesNotExist:
            return None
    @classmethod
    def modify_user_info(cls, id_user, new_code_user, new_email,new_passaword):
        try:
            user = cls.objects.get(id=id_user)
            user.code_user = new_code_user
            user.email = new_email
            user.password = new_passaword
            user.save()
            return True
        except cls.DoesNotExist:
            return False
