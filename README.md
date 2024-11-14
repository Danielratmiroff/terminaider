
[![PyPI version](https://badge.fury.io/py/terminaider.svg)](https://badge.fury.io/py/terminaider)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Your AI Assistant for the Terminal 🚀

Terminaider is a CLI that brings AI-powered assistance directly to your terminal. 

Interact with an AI chat interface to get instant help, code analysis, and more — all without leaving your command line.

![Demo](https://github.com/Danielratmiroff/terminaider/blob/a8af911e61877eb7d48a7ebbefd48f1cab5b944a/img/terminaier.png)

## ✨ Features

- **AI Chat Interface**: Engage in conversations with an AI assistant directly from your terminal.
- **Code Analysis**: Receive code summaries and analyses to understand and improve your code.
- **Customizable Interfaces**: Choose between different AI interfaces like Groq or OpenAI.
- **Session Management**: Maintains chat history per session for a seamless experience.
- **Clipboard Integration**: Copy code summaries directly to your clipboard.

## 📦 Installation

Install Terminaider via pip:

```bash
pip install terminaider

# Recommended:
pipx install terminaider
```

## 🚀 Getting Started

Start using Terminaider by simply typing:

```bash
ai
```

Or initiate a chat with an initial prompt:

```bash
ai "How do I calculate Earth's roundness"
```

## ⚙️ Configuration

Set your API tokens as environment variables:

```bash
# If you want to use Groq's API
export GROQ_API_KEY='your_groq_api_key'

# If you want to use OpenAI's API
export OPENAI_API_KEY='your_openai_api_key'
```

## 📖 Usage

### 🗨️ Chat with the AI Assistant

Start an interactive session:

```bash
ai
```

Provide an initial prompt:

```bash
ai "explain the why Python is great"
```

### ⚙️ Options

- `--interface`, `-i`: Specify the AI interface to use (e.g., `groq` or `openai`).
- `--version`, `-v`: Display the current version of Terminaider.

>PD: Interface selection will be stored as default for future use. So you don't need to specify it everytime_
>
>Configuration file is located at `~/.config/terminaider/config.yaml`. 


### 🔍 Code Analysis

The AI will provide code analysis when necessary and automatically copy them to your clipboard for easy access.

## 🛠 Build Instructions

Build from source:

### Clone the Repository

```bash
git clone https://github.com/Danielratmiroff/terminaider.git
```

### Navigate to the Project Directory

```bash
cd terminaider
```

### Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

### Install Dependencies

```bash
pip install build
pip install -r requirements.txt
```

### Build the Package

```bash
python -m build
```

This will generate distribution files in the `dist/` directory.

### Install the Built Package

```bash
pip install dist/terminaider-<VERSION>-py3-none-any.whl
```

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## 📄 License

MIT License - [LICENSE](LICENSE).
