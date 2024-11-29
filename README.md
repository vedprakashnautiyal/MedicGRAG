# MedicGRAG
A medical assistant for remote areas. Build up on GraphRAG utilising doctor in the loop using Langgraph and Global Knowledge Database.

## Simple Graph RAG Pipeline
1. Create Virtual Environment
```
python -m venv .testenv source
./.testenv/bin/activate
```
2. Download [Mimic Dataset Subset](https://huggingface.co/datasets/Morson/mimic_ex) (Using ./dataset/mimic_ex/report_0.txt as RAG doc, "What are the allergies of patient?" as prompt.)
```
python run.py -simple 
```

## Complete RAG Flow

### Dataset
Mimic Subset Dataset Used For Now

### Preparing the Env, Database (Neo4j) and LLM
1. Create Virtual Environment
```
python -m venv .testenv source
./.testenv/bin/activate
```
2. Download Requirements
```
pip install -r requirements
```
Additionl Requirements For Camel Need To Be Installed
```
pip install camel-ai[all]
```

3. Prepare Neo4j and LLM (Ollama), we need .env file for Keys 
```
NEO4J_URL= "your NEO4J_URL"

NEO4J_USERNAME= "your NEO4J_USERNAME"

NEO4J_PASSWORD= "your NEO4J_PASSWORD"
```

### Constructing The Graph (Using "mimic_ex" Dataset)
```
python run.py -dataset mimic_ex -data_path ./dataset/mimic_ex -grained_chunk -ingraphmerge -construct_graph
```

### Model Inference
1. Keep a sample prompt in  
```
./prompt.txt
```

2. Script To Run Inference
``` 
python run.py -dataset mimic_ex -data_path ./dataset/mimic_ex -inference
```
