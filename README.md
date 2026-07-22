# PulseIQ AI

PulseIQ AI is an AI-powered clinical document intelligence platform built on AWS that transforms patient medical records and diagnostic PDFs into searchable, context-aware clinical insights using semantic retrieval, generative AI, and multi-agent reasoning.

---

## Live Demo

[Open PulseIQ AI](http://34.224.67.193:8501/)

---

## Key Capabilities

* Converted diagnostic PDFs into searchable text using asynchronous OCR workflows powered by Amazon Textract.
* Automated end-to-end document processing through AWS Step Functions triggered by Amazon S3 event notifications.
* Synchronized processed clinical documents into Amazon Bedrock Knowledge Bases using custom ingestion workflows and OpenSearch Serverless vector indexing.
* Enabled semantic retrieval over patient records using Cohere Embed Multilingual v3 embeddings and OpenSearch Serverless.
* Built a collaborative multi-agent architecture using Amazon Bedrock Agents, including a Supervisor Agent coordinating specialized clinical agents for Q&A, summarization, and entity extraction.
* Maintained end-to-end document traceability using Amazon DynamoDB to track document status, ingestion jobs, processing timestamps, and storage paths.
* Exposed backend capabilities through Amazon API Gateway and AWS Lambda to support document uploads, metadata retrieval, and conversational querying.
* Delivered real-time clinical interactions through a Streamlit interface hosted on Amazon EC2.

---

## AWS Services Used

* Amazon S3
* AWS Lambda
* AWS Step Functions
* Amazon Textract
* Amazon Bedrock
* Amazon Bedrock Agents
* Bedrock Knowledge Bases
* OpenSearch Serverless
* Amazon DynamoDB
* Amazon API Gateway
* Amazon EC2
* Amazon CloudWatch

---

## Architecture Diagram

![PulseIQ Architecture](architecture/pulseiq-architecture1.png)

---

## System Workflow

1. User uploads a clinical PDF through the Streamlit interface
2. API Gateway routes the request to the upload Lambda
3. PDF is stored in Amazon S3 (`raw-pdfs/`)
4. S3 event notification triggers the Step Functions workflow
5. Amazon Textract asynchronously extracts document text
6. Process Lambda converts extracted content into clean text + metadata
7. Bedrock Knowledge Base ingestion syncs embeddings into OpenSearch Serverless
8. Supervisor Agent routes queries to specialized clinical agents
9. AI-generated responses are returned through the Streamlit UI

---

## AI Components

### Supervisor Agent

* Clinical-Supervisor-Agent

### Specialized Agents

* Clinical-QA-Agent
* Medical-Summary-Agent
* Medical-Coding-Agent

### Embedding & Retrieval

* Cohere Embed Multilingual v3
* OpenSearch Serverless vector index
* Amazon Bedrock Knowledge Base

---

## Tech Stack

Python • Streamlit • AWS • Amazon Bedrock • DynamoDB • OpenSearch Serverless • Textract • Step Functions

---
## Challenges & Engineering Decisions
- Implemented a custom Lambda-based Bedrock ingestion trigger because Step Functions does not natively support startIngestionJob.
- Designed polling logic to handle Textract asynchronous workflows reliably.
- Resolved Step Functions JSONPath and Lambda serialization issues during orchestration.
- Used DynamoDB metadata tracking to maintain end-to-end document traceability.
