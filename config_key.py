import sys
def configureFlaskSecretKey(app):
    app.secret_key = '' #set this key before doing anything!
    # see http://flask.pocoo.org/docs/0.12/quickstart/#sessions
    if app.secret_key == '': 
        #try to force the server to stop
        print("Error: Set the secret key! Flask disabled.")
        sys.exit("Set the secret key!")
        raise RuntimeError("Set the secret key!")