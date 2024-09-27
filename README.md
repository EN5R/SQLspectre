# SQLspectre

SQLspectre is a powerful tool designed to scan for SQL injection vulnerabilities. It sends payloads to the target URL and checks if the responses contain SQL errors.


## Features

- **Web Automation:** Supports browser automation with Selenium based on user needs.
- **Proxy Support:** Allows secure scanning using multiple proxies.
- **Fast and Efficient:** Sends payloads in parallel to speed up the scanning process.
- **User-Friendly Interface:** Collects necessary information from the user.
- **Comprehensive Logging:** Maintains detailed logs to provide information at every step.


## Screenshots

![App Screenshot](https://raw.githubusercontent.com/EN5R/SQLspectre/refs/heads/main/src/SQLspectre.png)


## Videos
[https://github.com/EN5R/SQLspectre/blob/main/src/SQLspectre.mp4
](https://github-production-user-asset-6210df.s3.amazonaws.com/104204586/371546228-28189f01-459f-4a8e-a896-a1197f0ef68e.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20240927%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240927T131619Z&X-Amz-Expires=300&X-Amz-Signature=d87b76de1fe2ea9570382ed3783cc37c5d19bcd76c2509ebf952e3728139d7b1&X-Amz-SignedHeaders=host)


## Usage

You can view the usage instructions with the following command:

```bash
  python3.12 sqlspectre.py
```


## Installation

SQLspectre can be easily installed along with its required libraries as follows:

```bash
  pip3.12 install -r requirements.txt
```
    
## Running

You can run SQLspectre with the following command:

```bash
  python3.12 sqlspectre.py
```

## Important Note

This script should not be run with `sudo`. Running it with `sudo` may lead to unexpected errors and some functions may not work correctly. Please run the script as a normal user.

## About the Project

**SQLSpectre** is a security assessment tool specifically designed to identify SQL injection vulnerabilities in web applications. Key functionalities of the project include:

- **Payload Injection:** SQLSpectre sends preset payloads to the target URL to test for potential vulnerabilities in input handling.

- **Response Analysis:** The tool analyzes HTTP responses to detect SQL error messages, indicating possible vulnerabilities that could be exploited.

- **Proxy Support:** To maintain anonymity and avoid detection, SQLSpectre supports the rotation of multiple proxies while sending requests.

- **Web Automation:** With optional integration of Selenium, SQLSpectre can automate browser interactions, allowing for more complex testing scenarios.

- **Comprehensive Logging:** The tool generates detailed logs of the scanning process, which helps users review results and track any encountered issues effectively.

This project aims to enhance the security assessment process, providing developers and security analysts with a reliable method to identify and address SQL injection vulnerabilities in their applications.


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/EN5R/)
[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=000000)](https://www.buymeacoffee.com/EN5R)
[![Join Telegram](https://img.shields.io/badge/Join%20Telegram-0088cc?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/+K3G9CJmZfShmOGI0)

## License

This project is licensed under the [MIT License.](https://raw.githubusercontent.com/EN5R/SQLspectre/refs/heads/main/LICENSE)

Feel free to modify or add any information as needed! If there's anything more you'd like to include, just let me know!
