# Pathway LLM Application

## Introduction

The **Pathway LLM Application** is a GUI-based solution for a Retrieval-Augmented Generation (RAG) project, designed to help users interact with a local LLM engine while processing data from PDF documents. This project offers a streamlined way to upload PDFs, generate responses based on prompts, and integrate a containerized environment using Docker for production-ready deployments. The system automatically adapts in real time to any changes made to the PDFs in the data folder.

Built with **Pathway** and **Docker**, this project leverages Pathway’s in-memory scalable vector store to enhance responsiveness and adaptability for a variety of use cases.

## Table of Contents

- [Introduction](#introduction)
- [What Problem It Solves](#what-problem-it-solves)
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [Watch the Video](#watch-the-video)

## What Problem It Solves

This project addresses the need for quick and efficient access to information stored in PDF documents. Users can upload documents into the data folder, and the LLM engine processes them to provide answers to prompts in real time. In the future, this project can be extended to connect with **Google Drive** or over **300+ data sources**, enabling live updates as documents are modified.

For more details on the app template used, visit the [Pathway LLM App Template](https://github.com/pathwaycom/llm-app?tab=readme-ov-file#llm-app) or check out additional [Pathway templates](https://pathway.com/app-templates).

## Features

- Upload PDF documents for processing.
- Execute prompts against the LLM and receive dynamic answers.
- Real-time updates with the scalable vector store in memory.
- Start the Docker engine directly from the GUI for easy deployment.
- Ingests PDF data from the data folder with live adaptability.

## Architecture Overview

The **Pathway LLM Application** is structured around the following components:

- **Pathway**: The core RAG (Retrieval-Augmented Generation) framework, powering real-time updates and enabling scalable vector storage.
- **LLM Engine**: A local large language model engine that generates responses based on user inputs.
- **CustomTkinter GUI**: A user-friendly interface to interact with the system, upload PDFs, and manage Docker operations.
- **Docker**: Enables the application to be easily deployed in a containerized environment, making it production-ready.

## Requirements

- Python 3.x
- Docker

## How to Run

1. Clone this repository.
2. Install the required packages:  pip install -r requirements.txt
3. Run the rag_gui.py file from the path pathway\llm-app\examples\pipelines\demo-question-answering.


## Instruction:
Ensure Docker is running in the background before starting the application. The LLM engine will only work if the Docker engine is active.

## Watch the Video

[Watch the video](examples/pipelines/demo-question-answering/video/Rag_application.mp4)
