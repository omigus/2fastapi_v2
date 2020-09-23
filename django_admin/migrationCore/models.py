from django.db import models
import uuid
import datetime
from django import forms

# Create your models here.
class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        db_table = "status"

    def __str__(self):
        return str(self.status_name)
### module ในการทำงานของฟังก์ชัน ###
class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=80, blank=True, null=True)
    module_is_active = models.BooleanField(default=False)
    class Meta:
        db_table = "module"
    def __str__(self):
        return str(self.module_name)
###  Permission ในการใช้งานของ Module ###
class Permission(models.Model):
    permission_id = models.AutoField(primary_key=True) 
    permission_name = models.CharField(max_length=80, blank=True, null=True)
    permission_is_active = models.BooleanField(default=False)
    permission_admin =  models.BooleanField(default=False)
    permission_user =  models.BooleanField(default=False)
    class Meta:
        db_table = "permission"
    def __str__(self):
        return str(self.permission_name)
    
class Permission_has_module(models.Model):
    permission_has_module_id = models.AutoField(primary_key=True) 
    permission = models.ForeignKey(Permission, models.CASCADE)
    module = models.ForeignKey(Module, models.CASCADE)
    class Meta:
        db_table = "permission_has_module"
    def __str__(self):
        return str(self.permission_has_module_id)
    
    
###  system_feature ในการใช้งานของ Company ###
class System_group_all(models.Model):
    system_group_all_id = models.AutoField(primary_key=True) 
    system_group_all_name = models.CharField(max_length=80, blank=True, null=True)
    class Meta:
        db_table = "system_group_all"
    def __str__(self):
        return str(self.system_group_all_name)
    
class System_permission_all(models.Model):
    system_permission_all_id = models.AutoField(primary_key=True) 
    system_group_all = models.ForeignKey(System_group_all, models.CASCADE)
    permission = models.ForeignKey(Permission, models.CASCADE)
    class Meta:
        db_table = "system_permission_all"
    def __str__(self):
        return str(self.system_permission_all_id)
    
class Purchased_plan(models.Model):
    purchased_plan_id = models.AutoField(primary_key=True) 
    purchased_plan_name = models.CharField(max_length=80, blank=True, null=True)
    system_group_all = models.ForeignKey(System_group_all, models.CASCADE)
    purchased_plan_is_active = models.BooleanField(default=False)
    class Meta:
        db_table = "purchased_plan"
    def __str__(self):
        return str(self.purchased_plan_name)
    
class System_create_limit (models.Model):
    system_create_limit_id = models.AutoField(primary_key=True) 
    system_create_limit_user = models.IntegerField()
    system_create_limit_admin = models.IntegerField()
    system_create_limit_storage = models.IntegerField(default = 0)
    class Meta:
        db_table = "system_create_limit"
    def __str__(self):
        return str(self.system_create_limit_id)
class System_group_limit (models.Model):
    system_group_limit_id = models.AutoField(primary_key=True) 
    system_create_limit = models.ForeignKey(System_create_limit, models.CASCADE)
    system_group_all = models.ForeignKey(System_group_all, models.CASCADE)
    class Meta:
        db_table = "system_group_limit"
    def __str__(self):
        return str(self.system_group_limit_id)
    
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_public_id = models.UUIDField(
         default=uuid.uuid4, editable=False ,unique = True
    )
    company_name = models.CharField(max_length=180, blank=True, null=True , unique =True)
    company_is_active = models.BooleanField(default=False)
    created_on = models.DateField( default=datetime.datetime.now)
    class Meta:
        db_table = "company"
    def __str__(self):
        return self.company_name
    
class Company_has_system_group_all(models.Model):
    company_has_system_group_all_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, models.CASCADE)
    system_group_all = models.ForeignKey(System_group_all, models.CASCADE)
    created_on = models.DateField(auto_now=False, auto_now_add=False)
    class Meta:
        db_table = "company_has_system_group_all"
    def __str__(self):
        return str(self.company_has_system_group_all_id)

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_public_id =  models.UUIDField(
         default=uuid.uuid4, editable=False
    )
    company = models.ForeignKey(Company, models.CASCADE)
    admin_username = models.CharField(max_length=100, unique=True , blank=False, null=False )
    admin_password = models.CharField(max_length=80, blank=True, null=True)
    admin_is_active = models.BooleanField(default=False)
    class Meta:
        db_table = "admin"
    def __str__(self):
        return str(self.admin_public_id)
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_public_id =  models.UUIDField(
         default=uuid.uuid4, editable=False
    )
    company = models.ForeignKey(Company, models.CASCADE)
    user_username = models.CharField(max_length=100, unique=True , blank=False, null=False )
    user_password = models.CharField(max_length=80, blank=True, null=True)
    user_is_active = models.BooleanField(default=False)
    class Meta:
        db_table = "users"
    def __str__(self):
        return str(self.user_public_id)

class System_token(models.Model):
    system_token_id = models.AutoField(primary_key=True)
    system_token = models.CharField(max_length=250, unique=True , blank=False, null=False )
    member_public_id =  models.CharField(max_length=220, )
    created_on = models.DateTimeField()
    class Meta:
        db_table = "system_token"
    def __str__(self):
        return str(self.system_token)

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_public_id =  models.UUIDField(
         default=uuid.uuid4, editable=False,unique=True
    )
    company = models.ForeignKey(Company, models.CASCADE)
    team_name = models.CharField(max_length=120,  blank=False, null=False )
    team_avatar = models.CharField(max_length=180,  blank=True, null=True )
    team_is_active = models.BooleanField(default=False)
    admin = models.ForeignKey(Admin, models.CASCADE)
    created_on = models.DateTimeField()
    class Meta:
        db_table = "team"
    def __str__(self):
        return str(self.team_public_id)

class Team_has_users(models.Model):
    team_has_users_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    team =  models.ForeignKey(Team, models.CASCADE)
    class Meta:
        db_table = "team_has_users"
    def __str__(self):
        return str(self.team_has_users_id)

class Userdetails(models.Model):
    userdetails_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    userdetails_employee_id = models.CharField(max_length=80, blank=True, null=True)
    userdetails_firstname = models.CharField(max_length=80, blank=True, null=True)
    userdetails_lastname = models.CharField(max_length=80, blank=True, null=True)
    userdetails_phone = models.CharField(max_length=80, blank=True, null=True)
    userdetails_email = models.CharField(max_length=80, blank=True, null=True)
    userdetails_position = models.CharField(max_length=80, blank=True, null=True)
    userdetails_avatar = models.CharField(max_length=104, blank=True, null=True)
    class Meta:
        db_table = "userdetails"
    def __str__(self):
        return str(self.userdetails_id)
