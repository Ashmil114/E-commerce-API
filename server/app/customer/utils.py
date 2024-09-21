import random
import string
# from django.core.mail import send_mail


# OTP SECTION
def generate_otp(length=4):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp
