# URL Shortener - Flask Server

A simple URL shortener built with Flask. This server allows users to shorten long URLs and retrieve the original URLs using a short code.

## Features
- Shorten long URLs
- Redirect shortened URLs to their original destinations
- Store and retrieve shortened URLs using a database
- Logging setup for tracking requests and errors

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)

### Clone the Repository
```sh
git clone https://github.com/Ravindrayadavrk1006/shortly.git
cd shortly
```

### Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Configuration
### Setting Up config for the environment 
rename `config_sample.json` to `config.json` file in the project root

## Running the Server

### Running Directly (only for development purpose)
```sh
python server.py
```

The server should now be running at, visit it to see the swagger page:
```
http://127.0.0.1:5000/
```

## API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/url-shortner` | Shortens a given URL |
| GET  | `/url-shortner` | Redirects to the original URL |

## Logging
Logging is set up using Python's `logging` module. Logs are stored in the `logs/` directory.

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

## License

## Contact
For any inquiries, reach out to [ravindrayadavrk1012@gmail.com].

