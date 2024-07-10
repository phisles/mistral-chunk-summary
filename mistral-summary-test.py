import requests
import json
import nltk

# Download the Punkt tokenizer models if not already downloaded
nltk.download('punkt')

# Define the number of iterations and rounds
NUM_ITERATIONS = 5
NUM_ROUNDS = 3

# Define the API endpoint
url = "http://localhost:11434/api/generate"

# Define headers if needed, e.g., for authentication (assuming no auth is needed for localhost)
headers = {
    'Content-Type': 'application/json',
}

# Function to read a transcript from a file
def read_transcript(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to split text into sentences
def split_into_sentences(text):
    return nltk.sent_tokenize(text)

# Function to split sentences into chunks
def split_into_chunks(sentences, chunk_size=2):
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunks.append(' '.join(sentences[i:i+chunk_size]))
    return chunks

# Function to summarize a text using the Mistral model
def summarize_text(text, prompt_suffix="Summarize the following text:"):
    # Define the request payload
    payload = {
        "model": "mistral",
        "prompt": f"{prompt_suffix} {text}",
        "params": {
            "stop": ["[INST]", "[/INST]"]
        }
    }
    
    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Check the response status and process the result
    if response.status_code == 200:
        try:
            # Split the response content by lines
            lines = response.content.decode('utf-8').splitlines()
            # Collect the responses
            responses = []
            for line in lines:
                # Parse each line as a JSON object
                json_line = json.loads(line)
                # Extract the response field and add it to the list
                responses.append(json_line.get('response', ''))
            
            # Join all parts of the response
            full_response = ''.join(responses)
            return full_response
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", str(e))
            print("Raw response content (as text):", response.text)
    else:
        print("Failed to get a response:", response.status_code, response.text)
        return None

# Function to select the best summary
def select_best_summary(summaries):
    combined_summaries = " ".join(f"Summary {i + 1}: {summary}" for i, summary in enumerate(summaries))
    selection_prompt = f"Select the best summary from the following summaries. The best summary should make the most sense, avoid any opinions or logical gaps, and be the most concise and clear. Return only the best final summary without any additional language, context, or opinion:\n\n{combined_summaries}"
    
    # Define the request payload
    payload = {
        "model": "mistral",
        "prompt": selection_prompt,
        "params": {
            "stop": ["[INST]", "[/INST]"]
        }
    }
    
    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Check the response status and process the result
    if response.status_code == 200:
        try:
            # Split the response content by lines
            lines = response.content.decode('utf-8').splitlines()
            # Collect the responses
            responses = []
            for line in lines:
                # Parse each line as a JSON object
                json_line = json.loads(line)
                # Extract the response field and add it to the list
                responses.append(json_line.get('response', ''))
            
            # Join all parts of the response
            best_summary = ''.join(responses)
            # Strip any leading "Summary X: " text
            best_summary = best_summary.split(': ', 1)[-1].strip()
            return best_summary
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", str(e))
            print("Raw response content (as text):", response.text)
    else:
        print("Failed to get a response:", response.status_code, response.text)
        return None

# Path to the transcript file
transcript_file_path = '/Users/philip/Desktop/Code/transcript-summary/Transcripts/completed/Interview Sample.txt'

# Read the transcript
transcript = read_transcript(transcript_file_path)

# Split transcript into sentences
sentences = split_into_sentences(transcript)

# Ensure at least two chunks
chunk_size = max(1, len(sentences) // 2)

# List to store the best final summaries
best_final_summaries = []

for j in range(NUM_ITERATIONS):
    print(f"\n{'=' * 40}\nIteration {j + 1}\n{'=' * 40}\n")
    
    # Repeat the summarization process for the specified number of rounds
    final_summaries = []
    for i in range(NUM_ROUNDS):
        print(f"\n{'*' * 40}\nProcessing Round {i + 1}\n{'*' * 40}\n")
        
        # Split sentences into chunks
        chunks = split_into_chunks(sentences, chunk_size)

        # Summarize each chunk
        chunk_summaries = []
        for idx, chunk in enumerate(chunks):
            summary = summarize_text(chunk)
            chunk_summaries.append(summary)
            # Print the first 50 characters of the chunk and its summary
            print(f"Chunk {idx + 1} (first 50 characters):\n{chunk[:50]}\n")
            print(f"Summary {idx + 1}:\n{summary}\n")
            print(f"{'-' * 40}\n")
        
        # Combine chunk summaries and summarize them
        combined_summary = ' '.join(chunk_summaries)
        final_summary = summarize_text(
            f"Summarize the following text, which is a collection of summaries from different chunks of the same transcript, into a single paragraph no longer than 600 characters: {combined_summary}",
            prompt_suffix="Summarize the following text into a single paragraph no longer than 600 characters:"
        )
        
        # Add final summary to list
        if final_summary:
            final_summaries.append(final_summary)
        
        # Print the final summary of this round
        print(f"\n{'>' * 40}\nFinal Summary for Round {i + 1}:\n{final_summary}\n{'<' * 40}\n")

    # Select the best summary from the final summaries
    best_summary = select_best_summary(final_summaries)
    best_final_summaries.append(best_summary)

# Write results to Final-Summary.txt
with open('Final-Summary.txt', 'w') as file:
    file.write(f"Original Transcript:\n{transcript}\n\n")
    file.write(f"Number of chunks: {len(split_into_chunks(sentences, chunk_size))}\n")
    file.write(f"Character count of each chunk: {[len(chunk) for chunk in split_into_chunks(sentences, chunk_size)]}\n\n")
    
    for j, best_final_summary in enumerate(best_final_summaries, 1):
        file.write(f"Final Summary {j}:\n{best_final_summary}\n")
        file.write(f"Character count of best final summary {j}: {len(best_final_summary)}\n\n")
        file.write(f"{'=' * 40}\n")

print("\nSummary process completed. Check the 'Final-Summary.txt' file for results.")
