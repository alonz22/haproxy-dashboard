![Contributors](https://img.shields.io/github/contributors/alonz22/HAProxy-Configurator.svg)
![GitHub Stars](https://img.shields.io/github/stars/alonz22/HAProxy-Configurator.svg?style=social)
![GitHub Forks](https://img.shields.io/github/forks/alonz22/HAProxy-Configurator.svg?style=social)
![Downloads](https://img.shields.io/github/downloads/alonz22/HAProxy-Configurator/total.svg)
![Last Commit](https://img.shields.io/github/last-commit/alonz22/HAProxy-Configurator.svg)
![Issues](https://img.shields.io/github/issues/alonz22/HAProxy-Configurator.svg)
![Pull Requests](https://img.shields.io/github/issues-pr/alonz22/HAProxy-Configurator.svg)



[![Version](https://img.shields.io/badge/version-1.3.2-brightgreen.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)




## HAProxy Configurator - v1.3.2
### Disclaimer
This HAProxy Configurator is a tool to assist in generating configurations for HAProxy, a powerful and widely used open-source load balancer and proxy server. It is intended to simplify the process of creating HAProxy configurations for specific use cases.
This HAProxy Configurator is not affiliated with, endorsed, or maintained by the HAProxy project. HAProxy is a registered trademark of its respective owners.

## Description
The HAProxy Configurator provides a user-friendly web interface where users can input their desired configuration parameters, such as frontend and backend settings, backend servers, load balancing methods, health checks, sticky sessions, SSL certificates, ACLs, and more. The tool then generates the corresponding HAProxy configuration file based on the provided inputs.

Important Notes
This tool is intended to be used as an aid in generating HAProxy configurations and to make the process more accessible and efficient. However, it does not replace or outperform HAProxy's built-in functionality or configuration capabilities.

While we strive to ensure the accuracy and correctness of the generated configurations, it is essential to review the resulting configuration file carefully before deploying it in production environments. The user is responsible for thoroughly testing and verifying the configuration for their specific use case.

## Requirements
Before using the HAProxy Configurator, ensure that your system meets the following requirements:

1.A user with high privileges (sudo or root).

2.HAProxy: HAProxy must be installed on your system. The configurator relies on HAProxy to manage load balancing and proxying. Please install HAProxy using the package manager for your specific OS.

3.Python 3: The HAProxy Configurator is implemented in Python 3. Make sure Python 3 is installed on your system to run the configurator.

4.Port 5000 Available: The configurator runs as a web application and listens on port 5000. Ensure that port 5000 is available and not occupied by any other process.

## Install:

1. clone the repository:
   ```git clone https://github.com/alonz22/HAProxy-Configurator```

2. Install flask and the app dependencies:
   ```pip install flask```
   ```pip install requests```
   ```pip install subprocess```
   ```pip install pyOpenSSL```

4. enter the root folder of the app:
   ```cd haproxy-configurator```

5. run the installation script:
   ```chmod +x install.sh```
   if the script failes to run with "bad interpreter" error, run the following:
   ```sed -i 's/\r//' install.sh```
   ```./install.sh```

6. the path of the root directory of the app should be located now at ```/etc/haproxy-configurator```

7. run ```service haproxy-configurator status``` to see if the service is running.


7.browse the app:
   ```browse https://your-haproxy-server-ip:5000```

## SSL Certificate

The application comes with a self signed certificate related to tthe domain "haproxy-configurator.local". The path to the PEM file can be changed inside ssl.ini configuration file.

## Usage
Launch the HAProxy Configurator by navigating to https://your-haproxy-server-ip:5000.

Fill in the required parameters and options for your HAProxy configuration.

### Frontend Section:

![image](https://github.com/alonz22/HAProxy-Configurator/assets/72250573/04413c22-c947-4599-9659-e0274730f061)



### backend section:

![image](https://github.com/alonz22/HAProxy-Configurator/assets/72250573/6af98d59-734a-4272-84aa-87c47123017a)


### You may as well edit the config file itself via "Edit HAProxy Config":

![image](https://github.com/alonz22/HAProxy-Configurator/assets/72250573/c61ed725-37a4-4ad5-908f-6164311c7fd4)



Click the "Save & Check" button to validate the configuration without reloading HAProxy.

Click the "Save & Reload" button to save the configuration and trigger HAProxy's reload.

Review the generated configuration output and verify its accuracy.

## Review And Analyze Security Events Related To Triggered ACL's Activated:

![image](https://github.com/alonz22/HAProxy-Configurator/assets/72250573/ce0fc97e-0622-4fab-92f1-dd71fdb3e1ba)



## Features

Frontend and Backend Configuration
Easily add and manage frontend and backend configurations through our intuitive GUI. Define your load balancing, SSL termination, and ACL rules with just a few clicks.

Direct Edit of haproxy.cfg
Edit your HAProxy configuration file directly from the GUI. Make quick modifications, add custom settings, and see changes in real-time.

Configuration Validation
Ensure the accuracy of your HAProxy configuration by validating it for errors. Receive clear feedback and suggestions for improvements before applying changes.

Save and Restart HAProxy Service
With the click of a button, save your configuration changes and smoothly restart the HAProxy service, ensuring uninterrupted traffic flow.

Traffic Statistics
Monitor traffic distribution across your frontends and backends. Gain insights into usage patterns and identify performance bottlenecks.

WAF and Security
Enhance security with integrated Web Application Firewall (WAF) features:

* Defend against DOS attacks
* Mitigate SQL injection
* Prevent Cross-Site Scripting (XSS)
* Block access to sensitive paths
* Stop remote file uploads
* Add custom response headers
* Security Event Logs Analysis
* Analyze security event logs directly from the app. Gain visibility into potential threats and anomalies, empowering you to take proactive measures.
* Add path based redirects on Layer7 LoadBalancing (http mode)
* Use SSL Certificate for your frontend and enable redirect to https
* Add forwardfor to your backend, to forward the real client ip address to your backend servers
* Enable Layer4 & Layer7 Healthchecks to your backend servers
* Add Session Persistence to your backend servers by using client ip or a cookie.

Homepage Summary
Get an overview of your entire configuration on the homepage:

Count ACLs, frontends, and backends
View load balancing methods in use
Quick access to critical configuration details


## Roadmap Overview
### Phase 1: User Experience Enhancements
1.Dark Mode: Introduce a sleek and comfortable dark mode interface, providing an alternative visual style for users who prefer reduced screen brightness during prolonged usage.

### Phase 2: Performance and Flexibility

1.HTTP Keep-Alive Option: Implement an option to enable HTTP Keep-Alive within the frontend configurations. This feature enhances connection efficiency by allowing multiple requests and responses to be sent over a single TCP connection.

2.Backup Servers for Backend: Enhance backend resilience by adding support for specifying backup servers. These servers will be used when the primary servers are unavailable, improving overall service availability.

3.Dynamic Backend Server Addition: Introduce an intuitive button to dynamically add backend servers directly from the GUI, eliminating the need to manually edit configuration files.

### Phase 3: Optimizations and Security

1.Frontend Caching Mechanism: Implement a frontend caching mechanism to optimize content delivery and reduce backend load. This feature will help accelerate user experiences and decrease response times.

2.Advanced WAF Protection: Bolster our existing WAF features with a more robust and comprehensive set of protections against emerging threats. Enhancements will include:

* Advanced SQL injection detection and prevention
* Enhanced XSS attack mitigation
* Fine-grained controls for blocking sensitive data leaks
* Improved anomaly detection for DOS attacks

Feedback and Contributions
Your feedback and suggestions for improvements are welcome! Please feel free to open issues or submit pull requests on our GitHub repository.

Note: This tool is provided as-is, and we do not offer any warranties or guarantees regarding its performance or suitability for any specific use case.


## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it in accordance with the terms of the license.

Thank you for using the HAProxy Configurator! We hope it simplifies your HAProxy configuration process and makes managing your load balancer easier. If you have any questions or encounter any issues, please let us know. Happy load balancing!
