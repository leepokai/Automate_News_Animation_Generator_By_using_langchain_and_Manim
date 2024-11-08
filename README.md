# Manim News Animation Generator

An automated tool that generates Manim animations from news articles using AI. This project combines news API integration, AI-powered code generation, and Manim animation rendering to create engaging visual news presentations.

## Features

- Automatic news fetching using NewsAPI
- AI-powered animation code generation using Claude 3 Sonnet
- High-quality animation rendering with Manim
- Configurable news topics and animation styles
- Error handling and logging

## Important Notes

### Model Selection
- **Recommended**: Use Claude 3 Sonnet or more powerful models
- **Not Recommended**: Smaller models or lower-tier alternatives
- Reason: Smaller models may generate unstable or incomplete Manim code, leading to rendering failures

### Rendering Stability
- Claude 3 Sonnet provides consistent and stable Manim code generation
- The generated code includes proper scene structure and animation timing
- Helps avoid common rendering issues like:
  - Missing imports
  - Incorrect class definitions
  - Invalid animation sequences
  - Memory management problems

## Prerequisites

- Python 3.10+
- Manim Community Edition
- NewsAPI key
- Anthropic API key (for Claude 3)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/leepokai/Automate_News_Animation_Generator_By_Manim.git
cd Automate_News_Animation_Generator_By_Manim
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required packages:
```bash
pip install langchain langchain-anthropic anthropic manim newsapi-python
```

4. Set up environment variables:
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export NEWSAPI_KEY="your-newsapi-key"
```

## Project Structure

- `mainfile.ipynb`: Main application file containing core functionality
- `NewsCollector`: Class for fetching news from NewsAPI
- `ManimAutomation`: Class for generating and rendering animations
- Generated files:
  - `generated_animation.py`: Generated Manim animation code
  - Output videos in media/videos/generated_animation/

## Usage

1. Run the main script:
```bash
python mainfile.py
```

2. The script will:
   - Fetch latest news from NewsAPI
   - Generate Manim animation code using Claude
   - Render the animation using Manim
   - Save the output video

## Key Components

### NewsCollector
- Handles news API integration
- Configurable keywords and language
- Returns formatted news data

### ManimAutomation
- Manages the animation generation pipeline
- Integrates with Claude 3 Sonnet for stable code generation
- Handles Manim rendering process
- Includes error handling and output parsing

## Configuration

### Model Configuration
```python
self.llm = ChatAnthropic(
    model="claude-3-sonnet-20240229",  # Use Sonnet or more powerful models
    anthropic_api_key=anthropic_api_key,
    temperature=0.7
)
```

### News API Configuration
```python
params = {
    "q": keywords,
    "language": language,
    "sortBy": "publishedAt",
    "pageSize": 5,
    "apiKey": self.newsapi_key
}
```

### Rendering Configuration
```bash
manim -pqh generated_animation.py NewsVisualizationScene
```
- `-p`: Preview
- `-q`: Quality (High)
- `-h`: 1080p resolution

## Error Handling

The project includes comprehensive error handling for:
- API failures
- Code generation issues
- Rendering problems
- File operations
- Encoding issues

## Troubleshooting

Common issues and solutions:
1. Encoding errors:
   - Set PYTHONIOENCODING='utf-8'
   - Use proper file encoding in write operations

2. Rendering failures:
   - Check generated code completeness
   - Verify Manim imports
   - Monitor memory usage

3. Model output stability:
   - Stick to Claude 3 Sonnet or above
   - Avoid reducing model capabilities
   - Maintain proper prompt structure

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Manim Community Edition
- Anthropic's Claude 3
- NewsAPI
- LangChain framework