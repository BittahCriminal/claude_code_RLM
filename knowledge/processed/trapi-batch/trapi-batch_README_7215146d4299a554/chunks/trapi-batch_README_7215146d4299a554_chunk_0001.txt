stamp desc
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
