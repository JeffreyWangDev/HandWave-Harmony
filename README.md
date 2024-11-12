# Web Piano

Web Piano is a simple web-based piano application that allows users to play piano directly from their web browser.

<img width="1280" alt="image" src="https://github.com/user-attachments/assets/4bac2217-ab4b-4190-8859-f9c16e084693">

## Features

- Play piano using your hands or mouse
- Simple and intuitive user interface
- Lightweight and fast
- Record and upload your piano sessions
- View and download shared recordings

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

## Backend

The backend of the Web Piano application is built using Flask. It provides the following endpoints:

- `POST /api/upload`: Upload a new recording.
- `GET /api/recordings`: List all available recordings.
- `GET /uploads/<filename>`: Access a specific uploaded recording.
- `GET /recordings`: View the recordings page.
- `GET /`: View the main application page.

### File Management

The backend manages file storage by ensuring the total size of the upload folder does not exceed a specified limit. If the limit is exceeded, the oldest file is deleted to make space for new uploads.

### Configuration

- `UPLOAD_FOLDER`: The directory where uploaded files are stored.
- `MAX_FILE_SIZE`: The maximum size of an individual file (1MB).
- `MAX_FOLDER_SIZE`: The maximum total size of the upload folder (1GB).

## Description

Web Piano is designed to be a lightweight and easy-to-use piano application that can be accessed from any device with a web browser. It is built using a simple static file server provided by BusyBox.

Enjoy playing piano on the web!