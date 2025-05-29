from flask import Flask, render_template, render_template_string
import configparser
import ssl
from routes.main_routes import main_bp
from routes.edit_routes import edit_bp
from utils.stats_utils import fetch_haproxy_stats, parse_haproxy_stats
from auth.auth_middleware import setup_auth
from log_parser import parse_log_file

app = Flask(__name__)

# Load basic auth credentials
auth_config = configparser.ConfigParser()
auth_config.read('/etc/haproxy-configurator/auth/auth.cfg')
BASIC_AUTH_USERNAME = auth_config.get('auth', 'username')
BASIC_AUTH_PASSWORD = auth_config.get('auth', 'password')

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(edit_bp)

# Setup authentication (placeholder, not currently used)
setup_auth(app)

# SSL Configuration
config2 = configparser.ConfigParser()
config2.read('/etc/haproxy-configurator/ssl.ini')
certificate_path = config2.get('ssl', 'certificate_path')
private_key_path = config2.get('ssl', 'private_key_path')
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.load_cert_chain(certfile=certificate_path, keyfile=private_key_path)

# Statistics Route
@app.route('/statistics')
def display_haproxy_stats():
    haproxy_stats = fetch_haproxy_stats()
    parsed_stats = parse_haproxy_stats(haproxy_stats)
    return render_template_string('''
        <style>
            /* Custom CSS for the header */
            header {
                background-color: #f2f2f2;
                padding: 20px;
                display: flex;
                padding-left: 100px;
                align-items: center;
            }

            .logo {
                width: 300px; /* Adjust the width as needed */
                height: auto;
            }

            .menu-link {
                text-decoration: none;
                padding: 10px 20px;
                color: #333;
                font-weight: bold;
            }

            .menu-link:hover {
                background-color: #3B444B;
                color: white;
                text-decoration: none;
            }
        </style>
        <header>
            <a href="/home" style="text-decoration: none;">
                <h3 style="color: grey; font-size: 22px;" class="logo">
                    <i style="margin: 8px;" class="fas fa-globe"></i>Haproxy Configurator
                </h3>
            </a>
            <a href="/home" class="menu-link">Home</a>
            <a href="/" class="menu-link">Add Frontend&Backend</a>
            <a href="/edit" class="menu-link">Edit HAProxy Config</a>
            <a href="/logs" class="menu-link">Security Events</a>
            <a href="/statistics" class="menu-link">Statistics</a>
            <a href="http://{{ request.host.split(':')[0] }}:8080/stats" class="menu-link">HAProxy Stats</a>
        </header>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <div class="container">
            <h1 class="my-4">HAProxy Stats</h1>
            <div class="table-responsive">
                <table class="table table-bordered table-striped">
                    <thead>
                        <tr>
                            <th>Frontend Name</th>
                            <th>Server Name</th>
                            <th>4xx Errors</th>
                            <th>5xx Errors</th>
                            <th>Bytes In (MB)</th>
                            <th>Bytes Out (MB)</th>
                            <th>Total Connections</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for stat in stats %}
                        <tr>
                            <td>{{ stat.frontend_name }}</td>
                            <td>{{ stat.server_name }}</td>
                            <td>{{ stat['4xx_errors'] }}</td>
                            <td>{{ stat['5xx_errors'] }}</td>
                            <td>{{ stat.bytes_in_mb }}</td>
                            <td>{{ stat.bytes_out_mb }}</td>
                            <td>{{ stat.conn_tot }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    ''', stats=parsed_stats)

# Logs Route
@app.route('/logs')
def display_logs():
    log_file_path = '/var/log/haproxy.log'
    parsed_entries = parse_log_file(log_file_path)
    return render_template('logs.html', entries=parsed_entries)

if __name__ == '__main__':
    app.run(host='::', port=5000, ssl_context=ssl_context, debug=True)
