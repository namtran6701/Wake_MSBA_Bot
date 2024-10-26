# Wake Forest Business School Q&A Assistant

An interactive Streamlit application that provides information about Wake Forest School of Business programs using AI-powered search and natural language processing.

## Features

- Real-time Q&A about Wake Forest School of Business programs and services
- Intelligent search functionality using Google Serper API
- Web scraping capabilities for detailed information retrieval
- Interactive user interface with example questions
- Persistent conversation memory using SQLite
- GPT-4o powered responses

## Prerequisites

Before running the application, make sure you have the following API keys:
- OpenAI API key
- Jina AI API key
- Google Serper API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in Streamlit secrets or a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key
JINA_API_KEY=your_jina_api_key
SERPER_API_KEY=your_serper_api_key
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Enter your question about Wake Forest School of Business in the text input field or select from the example questions provided

## Technology Stack

- **Frontend**: Streamlit
- **Language Model**: OpenAI GPT-4
- **Search Engine**: Google Serper API
- **Web Scraping**: Jina AI
- **Database**: SQLite
- **Framework**: LangChain & LangGraph

## Features in Detail

- **Intelligent Search**: Utilizes Google Serper API to search specifically within the Wake Forest business.wfu.edu domain
- **Context-Aware Responses**: Combines search results with GPT-4's natural language processing for accurate answers
- **Interactive UI**: Provides example questions and an intuitive interface for users
- **Memory Management**: Maintains conversation context using SQLite database
- **Error Handling**: Robust error handling for API calls and tool execution

## Project Structure

- `app.py`: Main application file containing the Streamlit interface and core logic
- `utils.py`: Utility functions for search result formatting and web scraping
- `requirements.txt`: List of Python dependencies
- `.streamlit/secrets.toml`: Configuration file for API keys (not included in repository)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

Copyright (c) 2024 Nam Tran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Author

Nam Tran, MSBA '24

## Acknowledgments

- Wake Forest School of Business
- OpenAI
- Streamlit
- LangChain & LangGraph communities