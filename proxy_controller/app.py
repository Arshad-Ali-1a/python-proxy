from flask import Flask, jsonify
import os
import docker

app = Flask(__name__)

# Docker client to restart the proxy
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

# Path to the toggle file
TOGGLE_FILE = "toggle/BLOCK_WEBSITE"
PROXY_CONTAINER_NAME = "proxy"  # Change this to match your container name

@app.route('/restart', methods=['GET'])
def restart_proxy():
    """Restart the Squid proxy container to apply changes."""
    try:
        container = client.containers.get(PROXY_CONTAINER_NAME)
        container.restart()
    except Exception as e:
        return str(e)

@app.route('/status', methods=['GET'])
def get_status():
    """Check if the proxy is in blocking or non-blocking mode."""
    if os.path.exists(TOGGLE_FILE):
        return jsonify({"status": "blocking"})
    else:
        return jsonify({"status": "non-blocking"})

@app.route('/block', methods=['GET'])
def enable_blocking():
    """Enable blocking mode."""
    open(TOGGLE_FILE, 'w').close()  # Create the toggle file
    restart_proxy()
    return jsonify({"message": "Blocking enabled", "status": "blocking"})

@app.route('/unblock', methods=['GET'])
def disable_blocking():
    """Disable blocking mode."""
    if os.path.exists(TOGGLE_FILE):
        os.remove(TOGGLE_FILE)  # Remove the toggle file
    restart_proxy()
    return jsonify({"message": "Blocking disabled", "status": "non-blocking"})

@app.route('/docs', methods=['GET'])
def api_docs():
    """API documentation."""
    docs = {
        "endpoints": {
            "/status": "GET - Check current proxy mode (blocking or non-blocking)",
            "/block": "POST - Enable blocking mode",
            "/unblock": "POST - Disable blocking mode",
            "/docs": "GET - View API documentation"
        }
    }
    return jsonify(docs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9002)
