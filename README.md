# Web Piano

Web Piano is a simple web-based piano application that allows users to play piano directly from their web browser.

## Features

- Play piano using your hands or mouse
- Simple and intuitive user interface
- Lightweight and fast

## Hosting

To host the Web Piano application using Docker, follow these steps:

1. **Build the Docker image:**

    ```sh
    docker build -t webpiano .
    ```

2. **Run the Docker container:**

    ```sh
    docker run -d -p 80:80 webpiano
    ```

3. **Access the application:**

    Open your web browser and navigate to `http://localhost`.

## Description

Web Piano is designed to be a lightweight and easy-to-use piano application that can be accessed from any device with a web browser. It is built using a simple static file server provided by BusyBox.


Enjoy playing piano on the web!