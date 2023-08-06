## HAProxy Configurator
Disclaimer
This HAProxy Configurator is a tool to assist in generating configurations for HAProxy, a powerful and widely used open-source load balancer and proxy server. It is intended to simplify the process of creating HAProxy configurations for specific use cases.

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

2. Install flask:
   ```pip install flask```

3. enter the root folder of the app:
   ```cd haproxy-configurator```

4. run the installation script:
   ```chmod +x install.sh```
   if the script failes to run with "bad interpreter" error, run the following:
   ```sed -i 's/\r//' install.sh```
   ```./install.sh```

5. the path of the root directory of the app should be located now at ```/etc/haproxy-configurator```

6. run ```service haproxy-configurator status``` to see if the servcie is running.

7.browse the app:
   ```browse http://your-haproxy-server-ip:5000```

## Usage
Launch the HAProxy Configurator by navigating to http://your-haproxy-server-ip:5000.

Fill in the required parameters and options for your HAProxy configuration.

Click the "Save & Check" button to validate the configuration without reloading HAProxy.

Click the "Save & Reload" button to save the configuration and trigger HAProxy's reload.

Review the generated configuration output and verify its accuracy.



Feedback and Contributions
Your feedback and suggestions for improvements are welcome! Please feel free to open issues or submit pull requests on our GitHub repository.

Note: This tool is provided as-is, and we do not offer any warranties or guarantees regarding its performance or suitability for any specific use case.

Disclaimer: This HAProxy Configurator is not affiliated with, endorsed, or maintained by the HAProxy project. HAProxy is a registered trademark of its respective owners.

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it in accordance with the terms of the license.

Thank you for using the HAProxy Configurator! We hope it simplifies your HAProxy configuration process and makes managing your load balancer easier. If you have any questions or encounter any issues, please let us know. Happy load balancing!
