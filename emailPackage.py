import smtplib

FROMADDRS = "lapisnoreply@gmail.com"

def sendEmail(toAddrs, parent, key):
    """ Send a confimation email to the student at 'toAddrs' """
    msgHead = "From: {}\r\nTo: {}\r\nSubject: Parent request\r\n".format(FROMADDRS, toAddrs)
    msgBody = [
            "Hello,",
            "'{}' has requested that they have access to your arrival and departure times at after school study recorded by lapis".format(parent),
            "\n",
            "Visit the link below to accept this", "www.localhost:5000/confirm/{}".format(key)
    ]

    # Construct a connection with the smtp server "smtp.gmail.com" through defaut port 25
    smtpConnection = smtplib.SMTP("smtp.gmail.com", 25)

    # Will need to check if this needed because apparently is shouldn't need to be
    #explicitly called
    # NOTE: .login() calls it anyway so it probably isnt bad to call it
    smtpConnection.ehlo()


    # Put the connection into TLS (Transport Layer Security) mode
    # The following commands will be encrypted
    # Apparently I need to call ehlo() again?
    try:
        smtpConnection.starttls()
    except SMTPException:
        print("### Error caught ###")
        print("error: 'SMTPException'")
        print("The current server dosen't support TLS encryption")
        return False

    # Login to the main account
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
