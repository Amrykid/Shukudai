import sys
def configureFlaskSecretKey(app):
    app.secret_key = '\xf5m\xa8\xc5\x95)\x14\xdd\x0cV\xe4c.\xfb\xde\xaa(a\x04j\x92\xde\x99M' #set this key before doing anything!
    # see http://flask.pocoo.org/docs/0.12/quickstart/#sessions
    if app.secret_key == '': 
        #try to force the server to stop
        print("Error: Set the secret key! Flask disabled.")
        sys.exit("Set the secret key!")
        raise RuntimeError("Set the secret key!")