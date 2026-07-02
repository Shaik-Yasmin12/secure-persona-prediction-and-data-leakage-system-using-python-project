from django.db import models

# Create your models here.
class User_Details(models.Model):
    Full_name = models.CharField(max_length=50,default = None)
    Age = models.CharField(max_length=50,default = None)
    Gender = models.CharField(max_length=10,default = None)
    Phone = models.IntegerField(default=None)
    Email = models.EmailField()
    Username = models.CharField(max_length=100,default = None)
    Password = models.CharField(max_length=100,default = None)
   
        
    class Meta:
        db_table = 'User_Details'


class Prediction_Details(models.Model):
    Cluster = models.CharField(max_length=50,default = None)
    Password = models.CharField(max_length=50,default = None)
    User_ID = models.CharField(max_length=50,default = None)

    class Meta:
        db_table = 'Prediction_Details'


class DataDetails(models.Model):
    cluster_no = models.CharField(max_length=100,default = None)
    Sender_ID = models.CharField(max_length=100,default = None)
    Sender_name = models.CharField(max_length=100,default = None)
    Receiver_ID = models.CharField(max_length=100,default = None)
    Receiver_name = models.CharField(max_length=100,default = None)
    files = models.FileField(upload_to = "Files",default = None )
    password = models.CharField(max_length=100,default = None)
    date = models.CharField(max_length = 100,default = None )
    time = models.CharField(max_length = 100,default = None )
    data_type = models.CharField(max_length = 100,null = True )
    User1=models.CharField(max_length=100,null = True)
    User2=models.CharField(max_length=100,null = True)
    

    class Meta:
        db_table = 'DataDetails'

