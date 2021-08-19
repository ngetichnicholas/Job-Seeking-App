from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_verification_email(first_name,last_name,receiver):
    # Creating message subject and sender
    subject = 'Profile Verification'
    sender = 'ngetij.nick@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/verification.txt',{"first_name": first_name,"last_name":last_name})
    html_content = render_to_string('email/verification.html',{"first_name": first_name,"last_name":last_name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()

def send_contact_email(name,receiver):
    # Creating message subject and sender
    subject = 'Message recieved'
    sender = 'ngetij.nick@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/contact.txt',{"name": name})
    html_content = render_to_string('email/contact.html',{"name": name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()