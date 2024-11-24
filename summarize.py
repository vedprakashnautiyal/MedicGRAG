from concurrent.futures import ThreadPoolExecutor
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import math
import os
from functools import partial

sum_prompt = """
Generate a structured summary from the provided medical source (report, paper, or book), strictly adhering to the following categories. The summary should list key information under each category in a concise format: 'CATEGORY_NAME: Key information'. No additional explanations or detailed descriptions are necessary unless directly related to the categories:

ANATOMICAL_STRUCTURE: Mention any anatomical structures specifically discussed.
BODY_FUNCTION: List any body functions highlighted.
BODY_MEASUREMENT: Include normal measurements like blood pressure or temperature.
BM_RESULT: Results of these measurements.
BM_UNIT: Units for each measurement.
BM_VALUE: Values of these measurements.
LABORATORY_DATA: Outline any laboratory tests mentioned.
LAB_RESULT: Outcomes of these tests (e.g., 'increased', 'decreased').
LAB_VALUE: Specific values from the tests.
LAB_UNIT: Units of measurement for these values.
MEDICINE: Name medications discussed.
MED_DOSE, MED_DURATION, MED_FORM, MED_FREQUENCY, MED_ROUTE, MED_STATUS, MED_STRENGTH, MED_UNIT, MED_TOTALDOSE: Provide concise details for each medication attribute.
PROBLEM: Identify any medical conditions or findings.
PROCEDURE: Describe any procedures.
PROCEDURE_RESULT: Outcomes of these procedures.
PROC_METHOD: Methods used.
SEVERITY: Severity of the conditions mentioned.
MEDICAL_DEVICE: List any medical devices used.
SUBSTANCE_ABUSE: Note any substance abuse mentioned.
Each category should be addressed only if relevant to the content of the medical source. Ensure the summary is clear and direct, suitable for quick reference.
"""

def call_llm_api(chunk: str, sum_prompt: str) -> str:
    """
    Call the Ollama API with a system prompt and user content.
    
    Args:
        chunk: The user content to process
        sum_prompt: The system prompt to use
        
    Returns:
        str: The LLM's response content
    """
    llm = ChatOllama(
        model="llama3.2:1b",
        temperature=0,
        max_tokens=500,  # num_predict should be max_tokens
    )
    
    messages = [
        SystemMessage(content=sum_prompt),
        HumanMessage(content=chunk)
    ]
    
    response = llm.invoke(messages)
    return response.content

# Modify `split_into_chunks` without relying on tiktoken
def split_into_chunks(text, tokens=500):
    # Estimate chunk size in words, assuming average token-to-word ratio
    avg_token_length = 0.75  # Approximate ratio
    words_per_chunk = math.ceil(tokens * avg_token_length)
    
    # Split text into words, then group into chunks
    words = text.split()
    chunks = [
        ' '.join(words[i:i + words_per_chunk])
        for i in range(0, len(words), words_per_chunk)
    ]
    return chunks

def process_chunks(content):
    chunks = split_into_chunks(content)
    # Create a partial function with the fixed sum_prompt
    call_api_with_prompt = partial(call_llm_api, sum_prompt=sum_prompt)
    
    # Process chunks in parallel
    with ThreadPoolExecutor() as executor:
        responses = list(executor.map(call_api_with_prompt, chunks))
    print(responses)
    return responses

# Can take up to a few minutes to run depending on the size of your data input