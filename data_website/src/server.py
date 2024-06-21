from app import app
import webbrowser
from threading import Timer

def open_browser():
    """
    This function opens the default web browser to the Dash app's URL.
    """
    webbrowser.open_new("http://127.0.0.1:8050/")

if __name__ == '__main__':
    # Set a timer to open the browser 1 second after the script starts
    Timer(1, open_browser).start()
    
    # Run the Dash app's server with debug mode enabled
    app.run_server(debug=True)
