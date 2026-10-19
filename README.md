# Lambda Management Tool

A Python-based tool for managing and updating AWS Lambda function configurations.

## Features

- ✅ Get Lambda function configurations
- ✅ Update function settings (timeout, memory, environment variables)
- ✅ List all Lambda functions
- ✅ Update from configuration files (JSON/YAML)

## Installation

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### CLI Commands

```bash
# List all functions
python -m src.cli list-functions

# Get function configuration
python -m src.cli get-config my-function

# Update function settings
python -m src.cli update-config my-function --timeout 60 --memory 512

# Update from configuration file
python -m src.cli update-from-file my-function config/my-config.json
```

### Configuration File Example

**config/my-config.json:**
```json
{
  "Timeout": 60,
  "MemorySize": 512,
  "Environment": {
    "Variables": {
      "LOG_LEVEL": "INFO",
      "API_KEY": "your-key"
    }
  }
}
```

## AWS Credentials

Set up AWS credentials using one of these methods:
- AWS CLI: `aws configure`
- Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- IAM role (if running on EC2/Lambda)

## Project Structure

```
lambda-hub/
├── src/
│   ├── __init__.py
│   ├── lambda_manager.py      # Core Lambda management logic
│   └── cli.py                 # CLI interface
├── config/                    # Configuration files
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── requirements.txt
└── README.md
```

## Development

```bash
# Run tests
pytest tests/

# Format code
black src/

# Type checking
mypy src/
```

## License

MIT
