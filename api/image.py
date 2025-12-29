from flask import Flask, request, make_response
import logging
import sys

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = Flask(__name__)

@app.route('/api/log', methods=['GET'])
def log_image():
    # Log the request details
    logging.info(f"Image requested from {request.remote_addr}")
    logging.info(f"User agent: {request.user_agent}")
    logging.info(f"Referrer: {request.referrer}")
    
    # Create a 1x1 transparent GIF
    # Source: http://probablyprogramming.com/2009/03/15/the-tiniest-gif-ever
    transparent_gif = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    
    response = make_response(transparent_gif)
    response.headers['Content-Type'] = 'image/gif'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

# For Vercel, we need to export the app as a serverless function
# We use `serverless-http` to wrap the Flask app
try:
    import serverless_http
    handler = serverless_http.WsgiMiddleware(app)
except ImportError:
    # For local development
    if __name__ == '__main__':
        app.run(debug=True)
