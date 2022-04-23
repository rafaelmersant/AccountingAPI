from django.db import models


class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=150)
    name = models.CharField(max_length=255)
    user_hash = models.CharField(max_length=255, blank=True)
    user_role = models.CharField(max_length=20, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id}'


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    identification = models.CharField(max_length=20)
    church = models.ForeignKey("Church", on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.id}'


class Church(models.Model):
    global_title = models.CharField(max_length=255)
    local_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    shepherd = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, related_name="pastor")
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f'{self.id}'


class Concept(models.Model):
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=1, default='E') # Entrada/Salida
    ocurrences = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f'{self.id}'