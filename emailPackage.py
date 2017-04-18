import smtplib

FROMADDRS = "lapisnoreply@gmail.com"

def sendEmail(toAddrs, user_email, key, emailType):
    """ Send a confimation email to the email stored in 'toAddrs' 
    Input:
    toAddrs (str) = the address the email will be sent to
    user_email (str) = the email of the user that is requesting access to the students information (in the case of
                    account confirmation this will be the same as the toAddrs)
    key (str) = a randomly generated key used to verify the email address
    emailType (str) = this indicates whether it is a student confirmation ('s') or an account confirmation ('a')
    Output:
    True (Bool) = the email was successfully sent
    False (Bool) = something went wrong """
    
    
    if emailType == "s": # Student confirmaiton
        msgHead = "From: {}\r\nTo: {}\r\nSubject: Request from user to access your information\r\n".format(FROMADDRS, toAddrs)
        msgBody = [
                "Hello,",
                "'{}' has requested that they have access to your arrival and departure times at after school study recorded by lapis".format(user_email),
                "\n",
                "Visit the link below to accept this",
                "www.localhost:5000/confirmStudentRequest/{}".format(key)
        ]
    elif emailType == "a": # Account confirmation
        msgHead = "From: {}\r\nTo: {}\r\nSubject: Confirm your account\r\n".format(FROMADDRS, toAddrs)
        msgBody = [
                "Hello,",
                "Thanks for signing up with lapis!",
                "\n",
                "Visit the link below to confirm your account",
                "www.localhost:5000/confirmAccount/{}".format(key)
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
        smtpConnection.login(FROMADDRS, "7P=WD+3~[q~PS,vGmgs3%@ep5Yp.,f*-5][E@A<")
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
