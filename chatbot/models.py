from django.db import models

# Create your models here.
class Datetoevent(models.Model):
    date = models.CharField(primary_key=True, max_length=20)
    event1 = models.CharField(max_length=45, blank=True, null=True)
    event2 = models.CharField(max_length=45, blank=True, null=True)
    event3 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datetoevent'

class Eventtodate(models.Model):
    event = models.CharField(primary_key=True, max_length=50)
    eventdate = models.CharField(db_column='eventDate', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eventtodate'


class Officeinfo(models.Model):
    officename = models.CharField(db_column='officeName', primary_key=True, max_length=50)  # Field name made lowercase.
    officetel = models.CharField(db_column='officeTel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    officelocation = models.CharField(db_column='officeLocation', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'officeinfo'
