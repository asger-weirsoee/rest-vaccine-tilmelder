import smtplib
import ssl
from email.mime.text import MIMEText
from os import linesep


def get_message(authorname, content, errors):

    return f"""
Hej,
Jeg har {"succesfuld" if not errors else "fejlet i at"} oprettet en anmodning om restvaccine i dit navn {":)" if not errors else ":("}
med følgende oplysninger:
allerede vaccineret: nej
navn: {content['name']}
alder: {content['age']}
telefon: {content['phone']}
vaccinerings sted: 
 - Aalborg.

{"Fejlene der er kommet er: " if errors else ""}
{linesep.join(errors)}

Hvis du har brug for at ændre nogle af disse oplysninger, så kontakt {authorname}!

Vh
Bot    
    
    """


def parse_error_msg(all_errors: dict):
    res_str = ""
    for key in all_errors.keys():
        res_str += f"{key}\n"
        for error in all_errors.get(key):
            res_str += f">{error}\n\n"
        res_str += "\n"
    return res_str


def get_adm_message(authorname, all_errors: dict):
    return f"""
Hej {authorname},

Jeg har kørt, og fået samlet nogle informationer sammen til dig :)

der er blevet sendt ({len(all_errors.keys())}) anmodninger.

Med følgende konfigurationer:
{parse_error_msg(all_errors)}


vh 
Bot
    
    """


def send_mail(usr, passwd, msg: MIMEText):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = usr
    password = passwd

    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.send_message(msg)
