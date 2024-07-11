![Minstrel Typing](minstrel-typing.png)

# Chunked Transcript Summarization Via Mistral

This program reads transcripts from files, splits them into chunks, summarizes each chunk using the Mistral model via the Ollama API, and then iterates through a process to generate and select the best final summaries.

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
- **transcript_folder_path**: This variable sets the path to the folder containing transcript files, if processing multiple transcripts.
- **transcript_file_path**: This variable sets the path to a single transcript file, if processing a single transcript.

## Program Elements

### 1. Reading the Transcript

The program reads transcripts from files specified by the `transcript_folder_path` or `transcript_file_path` variable, depending on whether you are processing multiple transcripts or a single transcript.

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

### 7. Rephrasing as a Single Transcript

The `rephrase_as_single_transcript` function rephrases the final summary to ensure it reads cohesively as a single interview or incident.

### 8. Writing Results to File

The program writes the original transcript, chunk summaries, and the rephrased best final summaries to `Final-Summary-<filename>.txt` files.

## How to Use

1. **Set Up the Environment**: Ensure you have Python and NLTK installed.
2. **Configure the Variables**: Set the `NUM_ITERATIONS`, `NUM_ROUNDS`, and either `transcript_folder_path` or `transcript_file_path` variables at the top of the script according to your needs.
3. **Run the Script**: Execute the script to generate the summaries.

### Example for Single Transcript

```python
NUM_ITERATIONS = 5
NUM_ROUNDS = 5
transcript_file_path = '/path/to/your/transcript.txt'
