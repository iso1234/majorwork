# This generates a random key that is used in confirm() and mystudents() in app.py
try:
    import secrets
    currentModule = "s"
except ImportError:
    # Python3.x (where x < 6) doesn't support the module secrets
    print("")
    print("########################################################################")
    print("It would be preferable to use python3.6 so I can use the secrets module")
    print("########################################################################")
    print("")
    # Import a random module that works for previous versions of python
    import random
    currentModule = "r"
    
    
def _rndKey():
    """ Returns a random key """
    if currentModule == "r":
        return str(random.randrange(100000000000000000000000000000000000000))
    else:
        return str(secrets.token_hex(32))
    
def createRandomKey(keysAlreadyInUse):
    """ Returns a random key that is not already in use """
    key = _rndKey()
    while key in keysAlreadyInUse:
        key = _rndKey()
    return key