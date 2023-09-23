from datetime import time 
from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import send_notification
from datetime import date,datetime,time

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    user_profile  = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='UserProfile')
    vendor_name = models.CharField(max_length=100)
    vendor_slug = models.SlugField(max_length=100,unique=True)
    vendor_license = models.ImageField(upload_to='vendor/License')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    def is_open(self):
        today_date = date.today()
        today = today_date.isoweekday()
        current_opening_hours = OpeningHour.objects.filter(vendor=self,day=today)

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        is_open = None
        for hour in current_opening_hours:
            if not hour.is_closed:
                start = str(datetime.strptime(hour.from_hour, '%I:%M %P').time())
                end = str(datetime.strptime(hour.to_hour, '%I:%M %P').time())
                if current_time >= start and current_time <= end:
                    is_open= True
                    break
                else:
                    is_open= False

        return is_open
    
    def save(self, *args, **kwargs):

        if self.pk is not None:
            #update
            orig =  Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:

                mail_template = 'accounts/emails/vendor_approved.html'
                context = {
                        'user': self.user,
                        'approved': self.is_approved,
                        'to_email': self.user.email,
                    }

                if self.is_approved:
                    #send email to user
                    mail_subject = 'Congratulations!Your account has been approved'
                   
                    send_notification(mail_subject,mail_template,context = context)
                else:
                    #send email to user
                    mail_subject = 'We are sorry! your license has been rejected you are not eligible to be publish foods'
                    
                    send_notification(mail_subject,mail_template,context = context)

        return super(Vendor,self).save(*args, **kwargs)
    


DAYS =[
    (1,("Monday")),
    (2,("Tuesday")),
    (3,("Wednesday")),
    (4,("Thursday")),
    (5,("Friday")),
    (6,("Saturday")),
    (7,("Sunday")),
]
HOUR_OF_DAY = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]

class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY, max_length=10,blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY, max_length=10,blank=True)
    is_closed = models.BooleanField(default=False)
    

    class Meta:
        ordering = ('day','-from_hour')
        unique_together = ('vendor','day','from_hour','to_hour')

    def __str__(self):
        return self.get_day_display()
