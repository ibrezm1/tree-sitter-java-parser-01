# Java Code Parser and Visualizer

## Description

This project is a Python-based tool for parsing Java source code, building a graph representation of the code, and performing semantic search on it. It uses the `tree-sitter` library for parsing, `networkx` for graph representation, `ChromaDB` for vector storage and semantic search, and `pyvis`/`matplotlib` for visualization.

## Features

- Parses Java source code to extract classes, methods, and method calls.
- Builds a directed graph representing the relationships between code elements.
- Stores the code graph in ChromaDB for semantic search.
- Performs semantic search on the code graph to find relevant code snippets.
- Visualizes the code graph in both interactive HTML and static PNG formats.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd JavaCodeparser
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    - Create a `.env` file by copying the `sample.env` file.
    - Add your Gemini API key to the `.env` file.

## Usage

1.  **Place your Java project in the `ejb` directory.**
    - The default configuration parses the project located at `./ejb/ejb/src/java/com`.

2.  **Run the main script:**
    ```bash
    python main.py
    ```

3.  **View the output:**
    - An interactive graph visualization will be saved as `project_code_graph.html`.
    - A static graph visualization will be saved as `project_code_graph.png`.
    - The console will display the results of the semantic search.

## Project Structure

```
.
├── .gitignore
├── chroma_manager.py       # Manages ChromaDB interactions
├── Code_parser.ipynb       # Jupyter notebook for experimentation
├── graph_builder.py        # Builds the graph from parsed code elements
├── main.py                 # Main entry point of the application
├── project_code_graph.html # Output interactive graph visualization
├── project_code_graph.png  # Output static graph visualization
├── requirements.txt        # Python dependencies
├── sample.env              # Sample environment file
├── tree_sitter_parser.py   # Parses the source code using tree-sitter
├── visualizer.py           # Visualizes the code graph
├── ejb/                    # Directory for the Java project to be parsed
└── venv/                   # Python virtual environment
```

## Dependencies

The project uses the following Python libraries:

- `tree-sitter`
- `tree-sitter-java`
- `networkx`
- `chromadb`
- `google-generativeai`
- `python-dotenv`
- `pyvis`
- `matplotlib`

## Future Work

- Support for more programming languages.
- More advanced graph analysis features.
- Integration with IDEs.
- Enhanced visualization options.
