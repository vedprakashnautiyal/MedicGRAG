from langchain.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.chains import create_extraction_chain
from typing import Optional, List
from langchain.chains import create_extraction_chain_pydantic
from pydantic import BaseModel
from langchain import hub
import os
from dataloader import load_high
from agentic_chunker import AgenticChunker

# Pydantic data class
class Sentences(BaseModel):
    sentences: str


def get_propositions(text, runnable, extraction_chain):
    runnable_output = runnable.invoke({
    "input": text
    }).content
    
    propositions = extraction_chain.invoke(runnable_output)
    print(propositions)
    print("-----------------------------------")
    return propositions
    

def run_chunk(essay):

    obj = hub.pull("wfh/proposal-indexing")
    print(obj)
    llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0.5,
    num_predict=500,
)

    runnable = obj | llm

    # Extraction
    extraction_chain = llm.with_structured_output(Sentences)

    paragraphs = essay.split("\n\n")

    essay_propositions = []

    for i, para in enumerate(paragraphs):
        propositions = get_propositions(para, runnable, extraction_chain)
        
        essay_propositions.extend(propositions)
        print (f"Done with {i}")

    ac = AgenticChunker()
    ac.add_propositions(essay_propositions)
    ac.pretty_print_chunks()
    chunks = ac.get_chunks()

    print(chunks)
    return chunks

if __name__ == "__main__":
    run_chunk("/dataset/mimic_ex/report_0.txt")


