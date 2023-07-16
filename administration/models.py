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
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    ocupation = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    cellphone = models.CharField(max_length=30, null=True, blank=True)
    identification = models.CharField(max_length=20, null=True, blank=True)
    civil_status = models.CharField(max_length=1, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    reason_consultation = models.CharField(max_length=200, null=True, blank=True)
    disease = models.CharField(max_length=200, null=True, blank=True)
    doctor = models.CharField(max_length=100, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f'{self.id}'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Church(models.Model):
    global_title = models.CharField(max_length=255)
    local_title = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    shepherd = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True, related_name="pastor")
    zone = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f'{self.id}'
    
    @property
    def shepherd_full_name(self):
        if self.shepherd:
            return f'{self.shepherd.first_name} {self.shepherd.last_name}'
        
        return ''


class Concept(models.Model):
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=1, default='E') # Entrada/Salida
    ocurrences = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f'{self.id}'