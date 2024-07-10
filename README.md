![Minstrel Typing](minstrel-typing.png)

# Transcript Summarization Program

This program reads a transcript from a file, splits it into chunks, summarizes each chunk using the Mistral model via the Ollama API, and then iterates through a process to generate and select the best final summaries.

## Prerequisites

1. **Python 3.x**: Make sure you have Python installed on your system.
2. **NLTK**: This library is used for tokenizing the transcript into sentences. Install it using:
    ```sh
    pip install nltk
    python -m nltk.downloader punkt
    ```

## Variables

- **NUM_ITERATIONS**: This variable sets the number of times the entire summarization process will be repeated. Adjust this for testing or deployment.
- **NUM_ROUNDS**: This variable sets the number of summarization rounds per iteration.

## Program Elements

### 1. Reading the Transcript

The program reads the transcript from a file specified by the `transcript_file_path` variable.

### 2. Splitting into Sentences

The transcript is split into sentences using the NLTK library's `sent_tokenize` function.

### 3. Splitting into Chunks

Sentences are grouped into chunks. The chunk size is dynamically calculated to ensure at least two chunks.

### 4. Summarizing Text

The `summarize_text` function sends a POST request to the Mistral model via the Ollama API to summarize the text. The API endpoint and headers are defined for this purpose.

### 5. Selecting the Best Summary

The `select_best_summary` function selects the best summary from a list of summaries based on specified criteria.

### 6. Iterations and Rounds

The program loops through a specified number of iterations and rounds to generate the final summaries. It stores the best summaries from each iteration.

### 7. Writing Results to File

The program writes the original transcript, chunk summaries, final summaries, and the best final summaries to a `Final-Summary.txt` file.

## How to Use

1. **Set Up the Environment**: Ensure you have Python and NLTK installed.
2. **Configure the Variables**: Set the `NUM_ITERATIONS` and `NUM_ROUNDS` variables at the top of the script according to your needs.
3. **Specify the Transcript File Path**: Update the `transcript_file_path` variable to point to your transcript file.
4. **Run the Script**: Execute the script to generate the summaries.

### Example

```python
NUM_ITERATIONS = 5
NUM_ROUNDS = 5
transcript_file_path = '/path/to/your/transcript.txt'
