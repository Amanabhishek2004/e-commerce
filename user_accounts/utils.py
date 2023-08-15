from django.conf import settings
from django.core.mail import send_mail



def send_email(email,token):
     try:
       subject = "THIS IS TO VERIFY YOUR EMAIL"
       message = f"CLICK ON http://127.0.0.1:8000/accounts/verify-email/{token} TO VERIFY YOUR ACCOUNT"
       email_from = settings.EMAIL_HOST_USER
       recipient_list = [email,]
       send_mail(subject, email , email_from , recipient_list)
     except Exception as e:
         return False

     return True
