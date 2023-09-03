from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import send_notification

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    user_profile  = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='UserProfile')
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor/License')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    def save(self, *args, **kwargs):

        if self.pk is not None:
            #update
            orig =  Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:

                mail_template = 'accounts/emails/vendor_approved.html'
                context = {
                        'user': self.user,
                        'approved': self.is_approved,
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
