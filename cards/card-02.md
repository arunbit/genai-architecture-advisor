# [Tok K Vector Retrieval Augmented Generation (RAG) ]

**Card ID:** CARD-002

## Problem and context

When highly relevant data can be retrieved  in chunks from a huge corpus  (usually from a vertical database using embedings) and the queries need updated or specific data

## How it works

Before any generation, queries retrieve relevant chunks of inforation (using embeding usually) that are used for the generation

## Use when

When relavant information can be retrieved and other non-relevant information can be easily avoided before generation  by using information retreival systems

## Avoid when

Data is too large or complicated to be retrieved before generation, or data is too small and its perfectly ok to have all the data in one spot on the prompt

## Trade-offs

Significant trade off dues to the need to maintain the relevance, freshness and size of the chunks of the data retived using data pipelines and databases

## Rejected alternative

Having all the relevant and non-relevant data in the prompt, when this system is possible and size of the data chunks demand this approach

## What breaks first at 10×

Relevant chunks dont appear as the first sign of problem. When important and highly relevant documents dont even make it before generation, either the full pipeline has to be updated OR this whole RAG approach might even have to be evaluated.

## More Info
RAG NeurIPS paper by Patrick Lewis et al:  https://proceedings.neurips.cc/paper_files/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf
