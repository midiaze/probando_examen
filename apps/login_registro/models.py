from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UsuarioManager(models.Manager):
    def validacion_registro(self, post_data):
        errors = {}
        if len(post_data['first_name'])<2:
            errors['first_name'] = "El largo del nombre debe tener al menos 2 caracteres"
        if len(post_data['last_name'])<2:
            errors['last_name'] = "El largo del apellido debe tener al menos 2 caracteres"
        if len (post_data['email']) <1:
            errors['email']= "Email es necesario"
        if post_data['password'] != post_data['confirm_password']:
            errors['password'] = 'Contraseñas no coinciden'
        if len(post_data['password']) < 6:
            errors['password']='Password debe tener al menos 6 caracteres'
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email']= "Email no es válido"
        else:
            usuario = Usuario.objects.filter(email=post_data['email'])
            if len(usuario)>0:
                errors['email'] = 'Email ya registrado, porfavor intentar otro email'
        return errors

    def validacion_login(self, post_data):
        login_errores = {}
        if len(post_data['email']) < 1:
            login_errores['email_login'] = 'Email es necesario'
        elif not EMAIL_REGEX.match(post_data['email']):
            login_errores['email_login']= "Email no es válido"
        else:
            email_existente = Usuario.objects.filter(email=post_data['email'])
            if len(email_existente) == 0:
                login_errores['email_login'] = 'Este correo no está registrado'
                return login_errores
            else:
                usuario = email_existente[0]
            if not bcrypt.checkpw(post_data['password'].encode(), usuario.password.encode()):
                login_errores['password_login']='Password incorrecta'
        return login_errores

class Usuario(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    password = models.CharField(max_length=255)
    user_level = models.PositiveSmallIntegerField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsuarioManager()
