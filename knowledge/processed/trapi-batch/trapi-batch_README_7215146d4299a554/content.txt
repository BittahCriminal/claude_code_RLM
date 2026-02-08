# TRAPI Batch Processing System

## Overview
The TRAPI Batch Processing System enables researchers to submit batches of AI prompts for large-scale, asynchronous processing using a suite of Azure services. This system is designed to offer functionality and an API experience that closely mirrors Azure OpenAI (AOAI) Batch processing capabilities, providing a familiar interface for users.

It facilitates handling large volumes of requests efficiently by decoupling job submission from prompt execution, leveraging robust queuing mechanisms, and providing clear status tracking.

## Table of Contents
- [Architecture](#architecture)
- [How It Works](#how-it-works)
- [API Interaction](#api-interaction)
  - [API Endpoints](#api-endpoints)
  - [JSONL File Format](#jsonl-file-format)
- [Azure Infrastructure (Bicep)](#azure-infrastructure-bicep)
  - [Key Resources](#key-resources)
  - [Deployment](#deployment)
- [Build and Deployment (Application Code)](#build-and-deployment-application-code)
  - [Build Process](#build-process)
  - [Deployment Process](#deployment-process)
- [Monitoring and Logging (Application Insights)](#monitoring-and-logging-application-insights)
  - [Accessing Logs](#accessing-logs)
  - [Key Telemetry](#key-telemetry)
- [Security](#security)
- [Local Development](#local-development)
- [Contributing & Feedback](#contributing--feedback)

## Architecture
The system is composed of several interconnected Azure services:

* **BatchProcessorApi (ASP.NET Core Web API)**: The primary entry point for users. It handles job file upload, job submission triggering, status checks, cancellation, and listing jobs.
* **Azure Blob Storage**:
    * `batch-inputs` container: Stores the user-submitted `.jsonl` files containing prompts.
    * `batch-outputs` container: Stores the results of processed prompts, with each job's results in a directory named after the `jobId`.
* **Azure Table Storage**: Persists metadata and status information for each batch job. This data feeds the API endpoints for job status retrieval.
* **Azure Storage Queues (Job Trigger Queue)**: Receives a message when a user explicitly triggers a job after uploading the input file. This message initiates the job processing.
* **Azure Functions (Job Processor Function - `BlobUploadProcessor`)**: Triggered by new messages in the Azure Storage "Job Trigger Queue". This function:
    1. Retrieves the associated `.jsonl` file from the `batch-inputs` blob container.
    1. Validates the input file.
    1. Parses individual prompts from the `.jsonl` file.
    1. Enqueues each prompt as a separate message onto an Azure Service Bus queue.
* **Azure Service Bus (Prompt Queue)**: Queues individual prompts for processing. This allows for resilient and scalable handling of each prompt within a batch.
* **Azure Functions (Prompt Processing Function `TaskProcessor` - triggered by Service Bus)**: This is the consumer of the Service Bus queue, which performs the capacity check and actual AI call.
* **Application Insights**: Provides comprehensive monitoring, logging, and telemetry across all components of the system.
* **Managed Identities**: Used for secure, secret-less authentication between Azure services.

:::mermaid
graph TD
    User["User"] -->|"Upload .jsonl file (e.g., PUT to presigned URL or specific API endpoint)"| BatchInputsBlob["Azure Blob Storage (batch-inputs)"]
    User -->|"Submit Job (POST to trigger, includes file reference/jobId)"| BatchAPI["BatchProcessorApi"]
    BatchAPI -->|"Create/Update Job Record"| JobTable["Azure Table Storage (Job Info)"]
    BatchAPI -->|"Enqueue Job Trigger Message"| JobTriggerQueue["Azure Storage Queues (Job Trigger Queue)"]
    BatchAPI -->|"Returns jobId"| User
    JobTriggerQueue -->|"Trigger"| JobProcessorFunc["Azure Function (BlobUploadProcessor)"]
    JobProcessorFunc -->|"Read .jsonl"| BatchInputsBlob
    JobProcessorFunc -->|"Parse, Enqueue Prompts"| PromptSBQueue["Azure Service Bus (Prompt Queue)"]
    PromptSBQueue -->|"Trigger per prompt"| PromptConsumer["Prompt Consumer (e.g., TRAPI Core / another Function)"]
    PromptConsumer -->|"Capacity Check"| TRAPI["TRAPI Capacity Check Endpoint"]
    TRAPI -->|"If capacity"| PromptConsumer
    PromptConsumer -->|"Process Prompt"| AIApi["AI Model Endpoint"]
    AIApi -->|"Result"| PromptConsumer
    PromptConsumer -->|"Store Result .jsonl"| BatchOutputsBlob["Azure Blob Storage (batch-outputs/jobId/)"]
    User -->|"Check Status/Results (GET)"| BatchAPI
    BatchAPI -->|"Reads"| JobTable
    BatchAPI -->|"Reads (for results)"| BatchOutputsBlob

    subgraph Azure Resources
        BatchAPI
        BatchInputsBlob
        JobTable
        JobTriggerQueue
        JobProcessorFunc
        PromptSBQueue
        BatchOutputsBlob
    end

    subgraph External Dependencies
        TRAPI
        AIApi
    end
:::
## How It Works

1. **Job File Upload:** A user first uploads their `.jsonl` file (containing the prompts) to the `batch-inputs` container in Azure Blob Storage. This is done via a POST call to the `"/trapi/files"` endpoint.
1. **Job Submission Trigger:** After the file is uploaded, the user makes a separate POST call to the `"/trapi/batches"` endpoint to formally submit and trigger the job. This call includes a reference to the `input_file_id` in the request body, which is the system-generated ID assigned to the uploaded file from the previous step.
1. **Initial Validation & Job Record Creation:** The API validates the submission trigger request. It creates or updates a job record in Azure Table Storage with metadata (e.g., `jobId`, `status: pending`, file reference).
1. **Job Trigger Queuing:** If the submission is valid, the API enqueues a message onto the processing queue in Azure Storage Queue. This message contains information needed to start processing the job, such as the `jobId` and the path to the input file.
1. **Job Processor Function Trigger:** The `BlobUploadProcessor` Azure Function is triggered by the new message in the processing queue.
1. **Prompt Deconstruction & Queuing:** The job processor function:
  - Retrieves the path to the `.jsonl` file from the queue message.
  - Reads the `.jsonl` file from the `batch-inputs` blob container.
  - Extracts each individual prompt.
  - Enqueues each prompt as a separate message onto an Azure Service Bus queue. Each message contains the necessary information for processing that single prompt.
1. **Prompt Processing & Capacity Check:** Messages from the Service Bus queue are processed one by one. Before processing a prompt:
  - A capacity check is made against the target TRAPI endpoint.
  - If TRAPI has capacity, the message is sent for AI processing.
  - If TRAPI does not have capacity, the message is re-queued in Service Bus.
1. **Result Storage:** Once a prompt is successfully processed by the AI model, its result is saved as an individual `.jsonl` file within a directory in the batch-outputs blob container, named after the `jobId`.
1. **Status & Result Retrieval:** Users can check the status of their job and retrieve results via API endpoints, using their `jobId`. Users cannot check the status of jobs submitted by other users. Users are identified by their OID, which is included in the `x-trapi-on-behalf-of` header when TRAPI communicates with the Batch Processing API.

## API Interaction

The Batch Processing API is designed for parity with the Azure OpenAI (AOAI) Batch API.

### API Endpoints

Key endpoints include:

- Upload a new `.jsonl` file: `POST /trapi/files`
- Submit an uploaded file for processing: `POST /trapi/batches`
- Get file status: `GET /files/{fileId}`
- Get job status: `GET /batches/{jobId}`
- Cancel a job: `POST /trapi/batches/{jobId}/cancel`
- Get job results: `GET /files/{jobId}/content`
- Get all jobs for user: `GET /batches`

For detailed API specifications, request/response schemas, and authentication details, please refer to the [Batch API README](https://dev.azure.com/msresearch/TRAPI/_git/trapi-batch?path=/BatchProcessorApi/README.md&_a=preview)

### JSONL File Format

Each line in the user-submitted `.jsonl` file represents an individual batch request to be processed. The name of the uploaded file can be anything, as the system will generate a new ID for this file which will be returned after the POST call to `/trapi/files`. That system-generated `input_file_id` will be used for future API calls.

**Required Format:** Each line must contain:
- `custom_id`: Unique identifier for the request
- `method`: HTTP method (typically "POST") 
- `url`: Endpoint path (e.g., "/chat/completions")
- `body`: Request payload with a **required** `model` field

**Important:** The `model` field is mandatory in each request's body. Requests with missing, null, or empty model fields will be rejected during processing.

**Example User Submission** (Input `.jsonl` file): Filename - `MedicalPrompts.jsonl`

```json
{"custom_id": "request-1", "method": "POST", "url": "/chat/completions", "body": {"model": "gpt-35-turbo_1106", "messages": [{"role": "user", "content": "What are the symptoms of diabetes?"}]}}
{"custom_id": "request-2", "method": "POST", "url": "/chat/completions", "body": {"model": "gpt-35-turbo_1106", "messages": [{"role": "user", "content": "How does the immune system fight infections?"}]}}
```

Each prompt from the input file is processed individually by TRAPI, then stored in a `.jsonl` file in the `batch-outputs` blob container, within a directory specific to that job, using task-based naming combined with the `jobId`. Once all prompts (tasks) are processed for a job, a final "results" file is generated, using the `jobId`, containing responses for every prompt in that job.

For example, here is a response for the first prompt of the input file. The `jobId` is `0001abee-7ade-44c3-922a-eabc0f545703`, so a `.jsonl` file called `0001abee-7ade-44c3-922a-eabc0f545703_task-0.jsonl` was generated with the following contents:

```json
{"custom_id":"0001abee-7ade-44c3-922a-eabc0f545703_task-0","method":"POST","url":"/chat/completions","body":{"model":"gpt-35-turbo_1106","messages":[{"role":"user","content":"What are the symptoms of diabetes?"}]},"response":{"id":"chatcmpl-BXXl3wNRJf3YOXu1yeeykM4pwMFYg","object":"chat.completion","created":1747334289,"model":"gpt-3.5-turbo-1106","choices":[{"index":0,"message":{"role":"assistant","content":"The symptoms of diabetes can include:\n\n1. Frequent urination\n2. Increased thirst and hunger\n3. Unexplained weight loss\n4. Fatigue\n5. Blurred vision\n6. Slow healing of wounds\n7. Tingling or numbness in the hands or feet\n8. Frequent infections\n9. Irritability or mood changes"},"finish_reason":"stop"}],"usage":{"prompt_tokens":14,"completion_tokens":73,"total_tokens":87},"system_fingerprint":"fp_0165350fbb"}}
```

Once each prompt from this job has been processed, a file called `file-0001abee-7ade-44c3-922a-eabc0f545703_results.jsonl` was generated with the following contents:

```json
{"custom_id":"0001abee-7ade-44c3-922a-eabc0f545703_task-0","method":"POST","url":"/chat/completions","body":{"model":"gpt-35-turbo_1106","messages":[{"role":"user","content":"What are the symptoms of diabetes?"}]},"response":{"id":"chatcmpl-BXXl3wNRJf3YOXu1yeeykM4pwMFYg","object":"chat.completion","created":1747334289,"model":"gpt-3.5-turbo-1106","choices":[{"index":0,"message":{"role":"assistant","content":"The symptoms of diabetes can include:\n\n1. Frequent urination\n2. Increased thirst and hunger\n3. Unexplained weight loss\n4. Fatigue\n5. Blurred vision\n6. Slow healing of wounds\n7. Tingling or numbness in the hands or feet\n8. Frequent infections\n9. Irritability or mood changes"},"finish_reason":"stop"}],"usage":{"prompt_tokens":14,"completion_tokens":73,"total_tokens":87},"system_fingerprint":"fp_0165350fbb"}}
{"custom_id":"0001abee-7ade-44c3-922a-eabc0f545703_task-1","method":"POST","url":"/chat/completions","body":{"model":"gpt-35-turbo_1106","messages":[{"role":"user","content":"How does the immune system fight infections?"}]},"response":{"id":"chatcmpl-BXXl3sfqwvwpSBPDIxWa6GgL1TvzF","object":"chat.completion","created":1747334289,"model":"gpt-3.5-turbo-1106","choices":[{"index":0,"message":{"role":"assistant","content":"The immune system fights infections through a complex network of cells, tissues, and organs that work together to identify and eliminate pathogens such as bacteria, viruses, and parasites. \n\nWhen a pathogen enters the body, the immune system responds by first recognizing the antigen, which is a specific molecule on the surface of the pathogen. This recognition triggers the immune system to produce antibodies, which are proteins that can bind to the antigens and neutralize the pathogen.\n\nThe immune system also activates white blood cells, such as T cells and B cells, which can directly attack and destroy the pathogens. Additionally, other immune cells, such as macrophages and dendritic cells, work to engulf and destroy the pathogens.\n\nFurthermore, the immune system also has a memory component, which allows it to remember past infections and respond more effectively to future encounters with the same pathogen.\n\nOverall, the immune system uses a combination of cellular and humoral (antibody-mediated) responses to fight off infections and protect the body from harmful pathogens."},"finish_reason":"stop"}],"usage":{"prompt_tokens":15,"completion_tokens":205,"total_tokens":220},"system_fingerprint":"fp_0165350fbb"}}
```

This file can be retrieved via the `/files/{jobId}/content` API endpoint.

## Azure Infrastructure (Bicep)

All Azure resources for this system are defined and managed using **Bicep**, promoting Infrastructure as Code (IaC) best practices. This ensures consistent, repeatable, and version-controlled deployments.

**Key Resources**

The Bicep templates define:

- Azure App Service Plan and Azure App Service for the `BatchProcessorApi`.
- Azure Storage Account (for Blobs and Tables).
- Azure Service Bus Namespace and Queue.
- Azure Functions App (including its hosting plan).
- Application Insights instance.
- Role assignments for Managed Identities.

**Code Repository**

All code for this project is contained in the following [Azure DevOps Code Repository](https://dev.azure.com/msresearch/TRAPI/_git/trapi-batch)

**Deployment**

A CI/CD process for this project is defined in the `azure-pipelines.yml` file. When a change is checked into the `main` branch of the repository, the build and deploy cycle begins, consisting of the following stages:

- **Build & Test:** Build and Run Tests
  - Install .NET 8 SDK
  - Authenticate to Azure Artifacts NuGet feed
  - Restore NuGet Packages
  - Build Solution
  - Run Tests for BatchProcessorApi.Tests
  - Run Tests for BatchProcessorFunctions.Tests
  - Run Tests for BatchProcessorDomain.Tests
- **Container Build:** Build and Push Function Container Image
  - Authenticate NuGet Feeds for Docker Build
  - Build and Push Functions Image
- **Deploy:** Deploy Infrastructure
  - Deploy Bicep Template and Capture Outputs
- **Deploy Apps:** Deploy .NET Code to API App
  - Deploy API App Code

This build and deploy process can also be run manually, if needed, from the pipeline. For more information on deployments, please visit the [Trapi Batch Deployment](https://dev.azure.com/msresearch/TRAPI/_build?definitionId=5021&_a=summary) pipeline.

## Monitoring and Logging (Application Insights)

Application Insights is integrated across the `BatchProcessorApi` and Azure Functions to provide comprehensive telemetry, including distributed tracing, performance monitoring, and exception logging. The Application Insights instance is generated by a Bicep module and exists within the same Azure resource group as the other Azure services for this system.

### Key Telemetry

- **Requests:** Incoming HTTP requests to the API.
- **Dependencies:** Outgoing calls from the API or Functions to other services (e.g., Azure Storage, Service Bus, TRAPI endpoints).
- **Traces:** Custom log messages (Information, Warning, Error) written using `ILogger`.
- **Exceptions:** Unhandled exceptions caught by the runtime or explicitly tracked.
- **Distributed Tracing:** Look for `operation_Id` to trace a single user request or job submission across multiple components (API -> Function -> Service Bus -> TRAPI). `jobId` and `messageId` are often logged as custom properties for easier correlation.

**Example KQL Query to find logs for a specific Job ID:**

## Metadata Caching Behavior (TMDS)

To reduce amplification of metadata (TMDS) calls (e.g., repeated `/tmds/deployments`, access checks, model listings) the system employs an in-memory caching decorator `CachingTmdsMetadataService` around the raw TMDS client.

Key characteristics:
* Scope: Lives inside each Function / API process (per instance). No cross-instance sharing.
* Covered Lookups:
  * ApiId per API path
  * User access decision (UserOid + ApiPath + ModelName)
  * Model list (UserOid + ApiPath)
* Unified TTL: 5 minutes for all entries (chosen to balance freshness with call reduction).
* Concurrency Collapse: Multiple simultaneous cache misses for the same key coalesce into a single underlying TMDS call using a single-flight TaskCompletionSource pattern.
* Failure Semantics: Failed lookups are NOT cached. All concurrent callers receive the exception; a subsequent call will retry the TMDS request.
* Expiration: On expiry, first caller refreshes; others arriving concurrently during refresh reuse the in‑flight result.
* Logging: Emits `TMDS Cache Hit` or `TMDS Cache Miss` (and occasionally `TMDS Cache Hit (post-lock)` variants) to enable hit/miss ratio tracking in Kusto.

Kusto example to measure effectiveness (adjust timespan):
```kusto
traces
| where timestamp > ago(1h)
| where message startswith "TMDS Cache"
| summarize Hits = countif(message contains "Hit"), Misses = countif(message contains "Miss")
```

Testing:
* Unit tests cover: value caching, list caching, access caching, concurrency collapse, failure propagation (no caching), and forced expiry refresh.

Operational Notes:
* Because cache is per instance, scale-out still multiplies some calls; however per-instance collapse dramatically reduces N-way bursts under high parallelism.
* Adjust TTL via constants in `CachingTmdsMetadataService` if metadata staleness or call volume requirements change.

```
traces
| where customDimensions.JobId == "your-specific-job-id"
| union (requests | where customDimensions.JobId == "your-specific-job-id")
| union (exceptions | where customDimensions.JobId == "your-specific-job-id")
| order by timestamp desc
```

## Security

- **Managed Identities:** The primary mechanism for Azure resource authentication. The API and Azure Functions use system-assigned managed identities to securely access other Azure services (Storage, Service Bus, etc.) without needing to store connection strings or secrets in application configuration.
- **Authentication & Authorization:**
  - Authentication to the BatchProcessorApi is handled via Azure AD (JWT Bearer tokens).

## Local Development Requirements

- .NET 8 SDK
- Azure Functions Core Tools
- Azure CLI
- Azurite (for local Azure Storage emulations)
- Access to a development TRAPI instance

### Configuration

- `BatchProcessorApi`: `appsettings.Development.json`
- Azure Functions: `local.settings.json`

## Contributing & Feedback

If you have suggestions or encounter issues using the TRAPI Batch Processing System, please reach out to the project maintainers or submit feedback through internal channels. [trapi@microsoft.com](trapi@microsoft.com)
