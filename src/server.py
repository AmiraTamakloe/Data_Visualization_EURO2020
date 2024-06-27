from app import app
import webbrowser
from threading import Timer

def open_browser():
    """
    This function opens the default web browser to the Dash app's URL.
    """
    webbrowser.open_new("http://127.0.0.1:8050/")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    
    app.run_server(debug=True)
