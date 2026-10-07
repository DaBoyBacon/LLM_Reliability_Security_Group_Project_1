# LLM_Reliability_Security_Group_Project_1


# Utilized Technologies
## Prisma workflow
https://github.com/CoLRev-Environment/prisma-flow-diagram

# Magron

found papers:
Prompt: RAG && Data poisoning and backdoors (ACM Digital Library)
Prompt: RAG & Data poisoning and backdoors (IEEE Xplore)
RQ: How resistant are RAG systems to data poisoning?
RQ: How effective are different data poisoning attempts at making RAG models more likely to hallucinate?

https://ieeexplore.ieee.org/document/11547227
https://dl.acm.org/doi/10.1145/3733799.3762976

# Divya
RQ1: When does the retrieval actually improve the correctness and factuality of the LLM responses? 
RQ2: How can RAG systems avoid unnecessary retrieval while, maintaining answer quality? 
RQ3: How does adding external retrieval introduce new attack surfaces for LLM systems? 
RQ4: What happens to efficiency and reliability when we introduce security defenses into RAG?

# Bijaya
https://arxiv.org/pdf/2409.10102 (SUPER helpful for upwards/downwards searching)
https://arxiv.org/pdf/2502.06864
https://dl.acm.org/doi/pdf/10.1145/3769082
https://ieeexplore-ieee-org.ezproxy.lib.ou.edu/document/11405858

# Moving on from previous work

## What are our research questions
RQ1: When does the retrieval actually improve the correctness and factuality of the LLM responses? 
RQ2: How can RAG systems avoid unnecessary retrieval while, maintaining answer quality? 
RQ3: How does adding external retrieval introduce new attack surfaces for LLM systems? 
RQ4: What happens to efficiency and reliability when we introduce security defenses into RAG?
RQ5: How resistant are RAG systems to data poisoning?
# More focused paper #Bijaya 
Primary RQ

To what extent does TrustRAG improve the trustworthiness of RAG-generated responses?

SRQ1

Can ontology-guided retrieval improve evidence relevance and grounding?

SRQ2

Can prediction-powered trust scoring reliably estimate hallucination risk?

SRQ3
Does integrating ontology-guided retrieval and trust scoring improve factual accuracy and reduce hallucinations?
 it directly maps with my architecture:

Ontology/Knowledge Graph → SRQ1
Prediction-Powered Trust Score → SRQ2
Complete TrustRAG System → SRQ3

and it aligns well with papers like OG-RAG, Knowledge Graph-Guided RAG, Self-RAG, FactReasoner, GraphEval, ARES, and RAGAS.
