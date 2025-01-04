# Text Summarization Tool

This repository contains a Python-based project that implements a **text summarization tool** using **Singular Value Decomposition (SVD)** for extractive text summarization. The project includes a Tkinter-based graphical user interface (GUI) for user interaction.

## Features

- **Extractive Summarization**: Generates concise summaries by selecting key sentences from the text.
- **Latent Semantic Analysis (LSA)**: Employs SVD to identify and rank the importance of sentences.
- **Customizable Parameters**: Users can specify summary length and the number of topics for dimensionality reduction.
- **Graphical User Interface**: Built with Tkinter for easy file selection and parameter input.

## Motivation

With the exponential growth of data, summarizing information efficiently is increasingly important. This tool aids in reducing information overload by providing concise summaries while retaining key information.

## Key Components

1. **Text Preprocessing**:
   - Converts text to lowercase.
   - Removes stop words and punctuation.
   - Creates a term-document matrix for SVD analysis.

2. **Singular Value Decomposition (SVD)**:
   - Reduces dimensionality of the term-document matrix.
   - Retains critical relationships between sentences and topics.

3. **Tkinter GUI**:
   - File upload and parameter selection.
   - Displays the generated summary and similarity scores.

## Implementation

1. **Input**: A text file, desired summary length, and the number of topics.
2. **Processing**:
   - Build a term-document matrix.
   - Apply SVD to extract latent semantic structures.
   - Compute similarities to identify key sentences.
3. **Output**: A concise summary displayed in the GUI.

## Results

The tool was tested on text from the textbook *Artificial Intelligence: A Modern Approach* by Russell and Norvig. Results showed that:
- Varying the number of topics (hyperparameters) affects the quality of the generated summary.
- The tool effectively balances dimensionality reduction and information retention.

## Requirements

- Python 3.x
- Tkinter (pre-installed with Python)
- NumPy
- Any other dependencies mentioned in the source code

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/text-summarization-tool.git
   cd text-summarization-tool
