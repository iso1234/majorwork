import smtplib

FROMADDRS = "lapisnoreply@gmail.com"

def sendEmail(toAddrs, user_email, key):
    """ Send a confimation email to the student at 'toAddrs' 
    Input:
    toAddrs (str) = the address the email will be sent to
    user_email (str) = the email of the user that is requesting access to the students information
    key (str) = a randomly generated key used to verify the person trying to confirm access to the information
    Output:
    True (Bool) = the email was successfully sent
    False (Bool) = something went wrong """
    
    msgHead = "From: {}\r\nTo: {}\r\nSubject: Request from user to access your information\r\n".format(FROMADDRS, toAddrs)
    msgBody = [
            "Hello,",
            "'{}' has requested that they have access to your arrival and departure times at after school study recorded by lapis".format(user_email),
            "\n",
            "Visit the link below to accept this", "www.localhost:5000/confirm/{}".format(key)
    ]
    
    # Construct a connection with the smtp server "smtp.gmail.com" through defaut port 25
    smtpConnection = smtplib.SMTP("smtp.gmail.com", 25)
    smtpConnection.ehlo()
    
    # Put the connection into TLS (Transport Layer Security) mode
    try:
        smtpConnection.starttls()
    except SMTPException:
        print("### Error caught ###")
        print("error: 'SMTPException'")
        print("The current server dosen't support TLS encryption")
        return False
    
    # Login to the main account (lapisnoreply@gmail.com)
    try:
        smtpConnection.login(FROMADDRS, "I.gr33n3")
    except Exception:
        print("### Error caught ###")
        print("error: 'SMTPException'")
        print("The username/password that was provided is incorrect")
        return False
    
    try:
        smtpConnection.sendmail(FROMADDRS,
                                  toAddrs,
                                  msgHead + "\n".join(msgBody))
    except Exception:
        print("Something went wrong in the .sendmail() part.")
        return False
        
    smtpConnection.quit()
    return True
