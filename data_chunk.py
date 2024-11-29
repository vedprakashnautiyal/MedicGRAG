from langchain.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from typing import Optional, List
from pydantic import BaseModel
import os
from dataloader import load_high
from agentic_chunker import AgenticChunker

# Pydantic data class
class Sentences(BaseModel):
    sentences: List[str]
    # sentences: str


def get_propositions(text, runnable, extraction_chain):
    runnable_output = runnable.invoke({
    "input": text
    }).content
    
    propositions = extraction_chain.invoke(runnable_output)
    return propositions


def read_file_content(file_path: str) -> str:
    """Read content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {str(e)}")

def run_chunk(text):
    # Read content from file
    # essay_path: str
    # try:
    #     essay = read_file_content(essay_path)
    # except Exception as e:
    #     print(f"Error reading file: {str(e)}")
    #     return None
    # print(essay)
    essay=text

    # obj = hub.pull("wfh/proposal-indexing")
    Template='''
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>  

                Decompose the "Content" into clear and simple propositions, ensuring they are interpretable out of
                context.
                1. Split compound sentence into simple sentences. Maintain the original phrasing from the input whenever possible.
                2. For any named entity that is accompanied by additional descriptive information, separate this information into its own distinct proposition.
                3. Decontextualize the proposition by adding necessary modifier to nouns or entire sentences
                and replacing pronouns (e.g., "it", "he", "she", "they", "this", "that") with the full name of the entities they refer to.
                4. Present the results as a list of strings, formatted in JSON.  

            <|eot_id|><|start_header_id|>user<|end_header_id|>  
                Decompose the following: {input} 
            Strictly follow the instructions provided and output in the desired format only.  
            <|eot_id|><|start_header_id|>assistant<|end_header_id|> 
'''
    llm = ChatOllama(
        model="llama3.2:1b",
        temperature=0,
        num_predict=500,
    )
    PROMPT = PromptTemplate.from_template(Template)

    runnable = PROMPT | llm

    # Extraction
    extraction_chain = llm.with_structured_output(Sentences)

    paragraphs = essay.split("\n\n")

    essay_propositions = []

    for i, para in enumerate(paragraphs):
        propositions = get_propositions(para, runnable, extraction_chain)
        
        # essay_propositions.extend(propositions)
    if hasattr(propositions, '__iter__') and not isinstance(propositions, (str, bytes)):
        essay_propositions.extend(propositions)  # Unpack and add individual items
    else:
        essay_propositions.append(propositions)
        print(f"Done with {i}")

    ac = AgenticChunker()
    ac.add_propositions(essay_propositions)
    ac.pretty_print_chunks()
    chunks = ac.get_chunks()

    print(chunks)
    return chunks

if __name__ == "__main__":
    run_chunk("/Users/vedprakashnautiyal/Desktop/MedicGRAG/dataset/mimic_ex/report_0.txt")