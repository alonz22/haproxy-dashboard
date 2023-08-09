from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect, url_for, render_template_string
import subprocess
import csv
import requests
import re
from OpenSSL import SSL
import configparser
app = Flask(__name__)





def is_frontend_exist(frontend_name, frontend_ip, frontend_port):
    with open('/etc/haproxy/haproxy.cfg', 'r') as haproxy_cfg:
        frontend_found = False
        for line in haproxy_cfg:
            if line.strip().startswith('frontend'):
                _, existing_frontend_name = line.strip().split(' ', 1)
                if existing_frontend_name.strip() == frontend_name:
                    frontend_found = True
                else:
                    frontend_found = False
            elif frontend_found and line.strip().startswith('bind'):
                _, bind_info = line.strip().split(' ', 1)
                existing_ip, existing_port = bind_info.split(':', 1)
                if existing_ip.strip() == frontend_ip and existing_port.strip() == frontend_port:
                    return True
    return False


def is_backend_exist(backend_name):
    with open('/etc/haproxy/haproxy.cfg', 'r') as haproxy_cfg:
        backend_found = False
        for line in haproxy_cfg:
            if line.strip().startswith('backend'):
                _, existing_backend_name = line.strip().split(' ', 1)
                if existing_backend_name.strip() == backend_name:
                    backend_found = True
                else:
                    backend_found = False
    return backend_found
                    
# Function to update HAProxy config file


def update_haproxy_config(frontend_name, frontend_ip, frontend_port, lb_method, protocol, backend_name, backend_servers, health_check,health_check_tcp, health_check_link, sticky_session,add_header, header_name,header_value, sticky_session_type, is_acl, acl_name,acl_action, acl_backend_name, use_ssl,ssl_cert_path, https_redirect, is_dos, ban_duration, limit_requests, forward_for, is_forbidden_path, forbidden_name, allowed_ip, forbidden_path, sql_injection_check, is_xss, is_remote_upload, add_path_based, redirect_domain_name, root_redirect, redirect_to, is_webshells ):
    
    if is_backend_exist(backend_name):
            return f"Backend {backend_name} already exists. Cannot add duplicate."
    
    with open('/etc/haproxy/haproxy.cfg', 'a') as haproxy_cfg:
        haproxy_cfg.write(f"\nfrontend {frontend_name}\n")
        if is_frontend_exist(frontend_name, frontend_ip, frontend_port):
            return "Frontend or Port already exists. Cannot add duplicate."
        haproxy_cfg.write(f"    bind {frontend_ip}:{frontend_port}")
        if use_ssl:
            haproxy_cfg.write(f" ssl crt {ssl_cert_path}\n")
            if https_redirect:
                haproxy_cfg.write(f" redirect scheme https code 301 if !{{ ssl_fc }}")
        haproxy_cfg.write("\n")
        if forward_for:
            haproxy_cfg.write(f"    option forwardfor\n")
        haproxy_cfg.write(f"    mode {protocol}\n")
        haproxy_cfg.write(f"    balance {lb_method}\n")
        if is_dos:
            haproxy_cfg.write(f"    stick-table type ip size 1m expire {ban_duration} store http_req_rate(1m)\n")
            haproxy_cfg.write(f"    http-request track-sc0 src\n")
            haproxy_cfg.write(f"    acl abuse sc_http_req_rate(0) gt {limit_requests}\n")
            haproxy_cfg.write(f"    http-request silent-drop if abuse\n")
        if sql_injection_check:
            haproxy_cfg.write(f"    acl is_sql_injection urlp_reg -i (union|select|insert|update|delete|drop|@@|1=1|`1)\n")
            haproxy_cfg.write(f"    acl is_long_uri path_len gt 400\n")
            haproxy_cfg.write(f"    acl semicolon_path path_reg -i ^.*;.*\n")
            haproxy_cfg.write(f"    acl is_sql_injection2 urlp_reg -i (;|substring|extract|union\s+all|order\s+by)\s+(\d+|--\+)\n")
            haproxy_cfg.write(f"    http-request deny if is_sql_injection or is_long_uri or semicolon_path or is_sql_injection2\n")
        if is_xss:
            haproxy_cfg.write(f"    acl is_xss_attack urlp_reg -i (<|>|script|alert|onerror|onload|javascript)\n")
            haproxy_cfg.write(f"    acl is_xss_attack_2 urlp_reg -i (<\s*script\s*|javascript:|<\s*img\s*src\s*=|<\s*a\s*href\s*=|<\s*iframe\s*src\s*=|\bon\w+\s*=|<\s*input\s*[^>]*\s*value\s*=|<\s*form\s*action\s*=|<\s*svg\s*on\w+\s*=)\n")
            haproxy_cfg.write(f"    acl is_xss_attack_hdr hdr_reg(Cookie|Referer|User-Agent) -i (<|>|script|alert|onerror|onload|javascript)\n")
            haproxy_cfg.write("     acl is_xss_cookie hdr_beg(Cookie) -i \"<script\" \"javascript:\" \"on\" \"alert(\" \"iframe\" \"onload\" \"onerror\" \"onclick\" \"onmouseover\"\n")

            haproxy_cfg.write(f"    http-request deny if is_xss_attack or is_xss_attack_hdr or is_xss_attack_2 or is_xss_cookie\n")
        if is_remote_upload:
            haproxy_cfg.write(f"    acl is_put_request method PUT\n")
            haproxy_cfg.write(f"    http-request deny if is_put_request\n")
        if is_acl:
            haproxy_cfg.write(f"    acl {acl_name} {acl_action}\n")
            haproxy_cfg.write(f"    use_backend {acl_backend_name} if {acl_name}\n")
        
        if is_forbidden_path:
            haproxy_cfg.write(f"    acl {forbidden_name} src {allowed_ip}\n")
            haproxy_cfg.write(f"    http-request deny if !{forbidden_name} {{ path_beg {forbidden_path} }}\n")
        
        if add_path_based:
            haproxy_cfg.write(f"    acl is_test_com hdr(host) -i {redirect_domain_name}\n")
            haproxy_cfg.write(f"    acl is_root path {root_redirect}\n")
            haproxy_cfg.write(f"    http-request redirect location {redirect_to} if is_test_com or is_root\n")
        
        if is_webshells:
            haproxy_cfg.write(f"    option http-buffer-request\n")
            haproxy_cfg.write(f"    acl is_webshell urlp_reg(payload,eval|system|passthru|shell_exec|exec|popen|proc_open|pcntl_exec)\n")
            haproxy_cfg.write(f"    acl is_potential_webshell urlp_reg(payload,php|jsp|asp|aspx)\n")
            haproxy_cfg.write(f"    acl blocked_webshell path_reg -i /(cmd|shell|backdoor|webshell|phpspy|c99|kacak|b374k|log4j|log4shell|wsos|madspot|malicious|evil).*\.php.*\n")
            haproxy_cfg.write(f"    acl is_suspicious_post hdr(Content-Type) -i application/x-www-form-urlencoded multipart/form-data\n")
            haproxy_cfg.write(f"    http-request deny if blocked_webshell or is_webshell or is_potential_webshell or is_suspicious_post \n")
            
        haproxy_cfg.write(f"    default_backend {backend_name}\n")

    with open('/etc/haproxy/haproxy.cfg', 'a') as haproxy_cfg:
        haproxy_cfg.write(f"\nbackend {backend_name}\n")
        
        if sticky_session and sticky_session_type == 'cookie':
            haproxy_cfg.write("    cookie SERVERID insert indirect nocache\n")
        if sticky_session and sticky_session_type == 'stick-table':
            haproxy_cfg.write("    stick-table type ip size 200k expire 5m\n")
            haproxy_cfg.write("    stick on src\n")
        if add_header:
            haproxy_cfg.write(f"   http-request set-header {header_name} \"{header_value}\"\n")
        if protocol == 'http':
            if health_check:
                haproxy_cfg.write(f"    option httpchk GET {health_check_link}\n")
                haproxy_cfg.write(f"    http-check disable-on-404\n")
                haproxy_cfg.write(f"    http-check expect string OK\n")
        if protocol == 'tcp':
            if health_check_tcp:
                haproxy_cfg.write(f"    option tcp-check\n")
                haproxy_cfg.write("    tcp-check send PING" + r"\r\n" + "\n")
                haproxy_cfg.write("    tcp-check send QUIT" + r"\r\n" + "\n")       
        for backend_server_info in backend_servers:
            backend_server_name, backend_server_ip, backend_server_port, backend_server_maxconn = backend_server_info
            if backend_server_name and backend_server_ip and backend_server_port:
                haproxy_cfg.write(f"    server {backend_server_name} {backend_server_ip}:{backend_server_port} check")
            if sticky_session and sticky_session_type == 'cookie':
                if backend_server_name and backend_server_ip and backend_server_port:
                    haproxy_cfg.write(f" cookie {backend_server_name}")
            if backend_server_maxconn:
                haproxy_cfg.write(f" maxconn {backend_server_maxconn}")
            haproxy_cfg.write("\n")
    
    return "Frontend and Backend added successfully."





@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        frontend_name = request.form['frontend_name']
        frontend_ip = request.form['frontend_ip']
        frontend_port = request.form['frontend_port']
        lb_method = request.form['lb_method']
        protocol = request.form['protocol']
        backend_name = request.form['backend_name']
        add_header = 'add_header' in request.form  if 'add_header' in request.form else ''
        header_name = request.form['header_name']
        header_value = request.form['header_value']
        backend_server_names = request.form.getlist('backend_server_names')
        backend_server_ips = request.form.getlist('backend_server_ips')
        backend_server_ports = request.form.getlist('backend_server_ports')
        backend_server_maxconns = request.form.getlist('backend_server_maxconns')
        is_acl = 'add_acl' in request.form
        acl_name = request.form['acl'] if 'acl' in request.form else ''
        acl_action = request.form['acl_action'] if 'acl_action' in request.form else ''
        acl_backend_name = request.form['backend_name_acl'] if 'backend_name_acl' in request.form else ''
        use_ssl = 'ssl_checkbox' in request.form
        ssl_cert_path = request.form['ssl_cert_path']
        https_redirect = 'ssl_redirect_checkbox' in request.form
        is_dos = 'add_dos' in request.form if 'add_dos' in request.form else ''
        ban_duration = request.form["ban_duration"]
        limit_requests = request.form["limit_requests"]
        forward_for = 'forward_for_check' in request.form
        
        is_forbidden_path = 'add_acl_path' in request.form
        forbidden_name = request.form["forbidden_name"]
        allowed_ip = request.form["allowed_ip"]
        forbidden_path = request.form["forbidden_path"]
        

        sql_injection_check = 'sql_injection_check' in request.form if 'sql_injection_check' in request.form else ''
        is_xss = 'xss_check' in request.form if 'xss_check' in request.form else ''
        is_remote_upload = 'remote_uploads_check' in request.form if 'remote_uploads_check' in request.form else ''
        
        
        
        add_path_based = 'add_path_based' in request.form
        redirect_domain_name = request.form["redirect_domain_name"]
        root_redirect = request.form["root_redirect"]
        redirect_to = request.form["redirect_to"]
        is_webshells = 'webshells_check' in request.form if 'webshells_check' in request.form else ''
        # Combine backend server info into a list of tuples (name, ip, port, maxconns)
        
        backend_servers = zip(backend_server_names, backend_server_ips, backend_server_ports, backend_server_maxconns)
        
        # Check if frontend or port already exists
        if is_frontend_exist(frontend_name, frontend_ip, frontend_port):
            return render_template('index.html', message="Frontend or Port already exists. Cannot add duplicate.")

        # Get health check related fields if the protocol is HTTP
        health_check = False
        health_check_link = ""
        if protocol == 'http':
            health_check = 'health_check' in request.form
            if health_check:
                health_check_link = request.form['health_check_link']
                
        health_check_tcp = False
        if protocol == 'tcp':
            health_check_tcp = 'health_check2' in request.form

        # Get sticky session related fields
        sticky_session = False
        sticky_session_type = ""
        if 'sticky_session' in request.form:
            sticky_session = True
            sticky_session_type = request.form['sticky_session_type']

        # Update the HAProxy config file
        message = update_haproxy_config(frontend_name, frontend_ip, frontend_port, lb_method, protocol, backend_name, backend_servers, health_check,health_check_tcp, health_check_link, sticky_session ,add_header, header_name, header_value, sticky_session_type, is_acl, acl_name,acl_action, acl_backend_name, use_ssl, ssl_cert_path,https_redirect, is_dos, ban_duration, limit_requests, forward_for , is_forbidden_path, forbidden_name, allowed_ip, forbidden_path, sql_injection_check, is_xss, is_remote_upload, add_path_based, redirect_domain_name, root_redirect, redirect_to, is_webshells )
        return render_template('index.html', message=message)

    return render_template('index.html')

import subprocess


@app.route('/edit', methods=['GET', 'POST'])
def edit_haproxy_config():
    if request.method == 'POST':
        edited_config = request.form['haproxy_config']
        # Save the edited config to the haproxy.cfg file
        with open('/etc/haproxy/haproxy.cfg', 'w') as f:
            f.write(edited_config)

        if 'save_check' in request.form:
            # Run haproxy -c -V -f to check the configuration
            check_result = subprocess.run(['haproxy', '-c', '-V', '-f', '/etc/haproxy/haproxy.cfg'], capture_output=True, text=True)
            check_output = check_result.stdout

            # Check if there was an error, and if so, append it to the output
            if check_result.returncode != 0:
                error_message = check_result.stderr
                check_output += f"\n\nError occurred:\n{error_message}"

        elif 'save_reload' in request.form:
            # Run haproxy -c -V -f to check the configuration
            check_result = subprocess.run(['haproxy', '-c', '-V', '-f', '/etc/haproxy/haproxy.cfg'], capture_output=True, text=True)
            check_output = check_result.stdout

            # Check if there was an error, and if so, append it to the output
            if check_result.returncode != 0:
                error_message = check_result.stderr
                check_output += f"\n\nError occurred:\n{error_message}"
            else:
                # If no error, run haproxy -D -f to reload HAProxy
                #reload_result = subprocess.run(['haproxy', '-D', '-f', '/etc/haproxy/haproxy.cfg'], capture_output=True, text=True)
                reload_result = subprocess.run(['systemctl', 'restart', 'haproxy', '/etc/haproxy/haproxy.cfg'], capture_output=True, text=True)
                check_output += f"\n\nHAProxy Restart Output:\n{reload_result.stdout}"

        return render_template('edit.html', config_content=edited_config, check_output=check_output)

    # Read the current contents of haproxy.cfg
    with open('/etc/haproxy/haproxy.cfg', 'r') as f:
        config_content = f.read()

    return render_template('edit.html', config_content=config_content)

def count_frontends_and_backends():
    frontend_count = 0
    backend_count = 0
    acl_count = 0
    layer7_count = 0
    layer4_count = 0
    
    with open('/etc/haproxy/haproxy.cfg', 'r') as haproxy_cfg:
        lines = haproxy_cfg.readlines()

        for line in lines:
            line = line.strip()

            if line.startswith('frontend '):
                frontend_count += 1
            if line.startswith('acl '):
                acl_count += 1
            if line.startswith('mode http'):
                layer7_count += 1
            if line.startswith('mode tcp'):
                layer4_count += 1     
            elif line.startswith('backend '):
                backend_count += 1

    return frontend_count, backend_count, acl_count, layer7_count, layer4_count

@app.route('/home')
def home():
    frontend_count, backend_count, acl_count, layer7_count, layer4_count = count_frontends_and_backends()

    return render_template('home.html', frontend_count=frontend_count, backend_count=backend_count, acl_count=acl_count ,layer7_count=layer7_count, layer4_count=layer4_count )


HAPROXY_STATS_URL = 'http://127.0.0.1:8080/;csv'

def fetch_haproxy_stats():
    try:
        response = requests.get(HAPROXY_STATS_URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return str(e)

def parse_haproxy_stats(stats_data):
    data = []
    # Remove the '#' character from the header row
    header_row = stats_data.splitlines()[0].replace('# ', '')
    reader = csv.DictReader(stats_data.splitlines(), fieldnames=header_row.split(','))
    next(reader)  # Skip the header row
    for row in reader:
        if row['svname'] != 'BACKEND':
            data.append({
                'frontend_name': row['pxname'],
                'server_name': row['svname'],
                '4xx_errors': row['hrsp_4xx'],
                '5xx_errors': row['hrsp_5xx'],
                'bytes_in_mb': f'{float(row["bin"]) / (1024 * 1024):.2f}',
                'bytes_out_mb': f'{float(row["bout"]) / (1024 * 1024):.2f}',
                'conn_tot': row['conn_tot'],
            })
    return data
    
    
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
    <a href="/statistics" class="menu-link">Statictics</a>
    <a href="http://{{ request.host.split(':')[0] }}:8080/stats" class="menu-link" >HAProxy Stats</a>
    
    
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



import re

def parse_log_file(log_file_path):
    parsed_entries = []
    xss_patterns = [
        r'<\s*script\s*',
        r'javascript:',
        r'<\s*img\s*src\s*=?',
        r'<\s*a\s*href\s*=?',
        r'<\s*iframe\s*src\s*=?',
        r'on\w+\s*=?',
        r'<\s*input\s*[^>]*\s*value\s*=?',
        r'<\s*form\s*action\s*=?',
        r'<\s*svg\s*on\w+\s*=?',
        r'script',
        r'alert',
        r'onerror',
        r'onload',
        r'javascript'
    ]
    
    sql_patterns = [
        r';',
        r'substring',
        r'extract',
        r'union\s+all',
        r'order\s+by',
        r'--\+',
        r'union',
        r'select',
        r'insert',
        r'update',
        r'delete',
        r'drop',
        r'@@',
        r'1=1',
        r'`1',
        r'union',
        r'select',
        r'insert',
        r'update',
        r'delete',
        r'drop',
        r'@@',
        r'1=1',
        r'`1'
    ]
    
    webshells_patterns = [
    r'payload',
    r'eval|system|passthru|shell_exec|exec|popen|proc_open|pcntl_exec|cmd|shell|backdoor|webshell|phpspy|c99|kacak|b374k|log4j|log4shell|wsos|madspot|malicious|evil.*\.php.*'
]

    
    combined_xss_pattern = re.compile('|'.join(xss_patterns), re.IGNORECASE)
    combined_sql_pattern = re.compile('|'.join(sql_patterns), re.IGNORECASE)
    combined_webshells_pattern = re.compile('|'.join(webshells_patterns), re.IGNORECASE)

    with open(log_file_path, 'r') as log_file:
        log_lines = log_file.readlines()
        for line in log_lines:
            if " 403 " in line:  # Check if the line contains " 403 " indicating a 403 status code
                match = re.search(r'(\w+\s+\d+\s\d+:\d+:\d+).*\s(\d+\.\d+\.\d+\.\d+).*"\s*(GET|POST|PUT|DELETE)\s+([^"]+)"', line)
                if match:
                    timestamp = match.group(1)  # Extract the date and time
                    ip_address = match.group(2)
                    http_method = match.group(3)
                    requested_url = match.group(4)
                    
                    if combined_xss_pattern.search(line):
                        xss_alert = 'Possible XSS Attack Was Identified.'
                    else:
                        xss_alert = ''
                    if combined_sql_pattern.search(line):
                        sql_alert = 'Possible SQL Injection Attempt Was Made.'
                    else:
                        sql_alert = ''
                    if "PUT" in line:
                        put_method = 'Possible Remote File Upload Attempt Was Made.'
                    else:
                        put_method = ''
                    
                    if "admin" in line:
                        illegal_resource = 'Possible Illegal Resource Access Attempt Was Made.'
                    else:
                        illegal_resource = ''
                        
                    if combined_webshells_pattern.search(line):
                        webshell_alert = 'Possible WebShell Attack Attempt Was Made.'
                    else:
                        webshell_alert = ''
                    
                    parsed_entries.append({
                        'timestamp': timestamp,
                        'ip_address': ip_address,
                        'http_method': http_method,
                        'requested_url': requested_url,
                        'xss_alert': xss_alert,
                        'sql_alert': sql_alert,
                        'put_method': put_method,
                        'illegal_resource': illegal_resource,
                        'webshell_alert': webshell_alert
                        
                    })
    return parsed_entries


import ssl
@app.route('/logs')
def display_logs():
    log_file_path = '/var/log/haproxy.log'
    parsed_entries = parse_log_file(log_file_path)
    return render_template('logs.html', entries=parsed_entries)

config2 = configparser.ConfigParser()
config2.read('/etc/haproxy-configurator/ssl.ini')

certificate_path = config2.get('ssl', 'certificate_path')
private_key_path = config2.get('ssl', 'private_key_path')

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.load_cert_chain(certfile=certificate_path, keyfile=private_key_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=ssl_context, debug=True)
