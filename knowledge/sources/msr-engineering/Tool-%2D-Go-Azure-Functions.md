# Introduction
This page attempts to put together the various considerations in making a Go (or golang) application in an Azure Function.

# Layout
The layout can adopt a few philosophies, but it's best to use Go workspaces to break up your application into _packages_ which will take the form of directories and .go code files. Let's make a functionapp called `hotness`.

``` 

| /cmd/hotness
|  hotness.go
|  /functionapp
|    host.json
|    local.settings.json
|    /runhotness
|      function.json
| host.json
| /internal
|   /hotness
|     myfunctionapp.go
|   /aztable
|     aztable.go
| go.work
```
The `go.work` file would need to know about all dirs holding your go code, so for the above it would look like:
```go
go 1.19

use (
	./cmd/hotness
	./internal/hotness
	./internal/aztable
)
```

Once you create the above, you can run `go work sync`.
Inside of each of your `internal` dirs with go files, you'll also need to create module dependency files, so within them you'll need to do something like:
```bash
cd /internal/aztable
go mod init aztable
go mod tidy
```

and then to build your app, from the root directory of your project

```bash
GOOS=linux GOARCH=amd64 go build -buildmode=pie -o /cmd/hotness/functionapp/handler hotness
```

For windows it would be
```bash
GOOS=windows GOARCH=amd64 go build -buildmode=pie -o /cmd/hotness/functionapp/handler.exe hotness
```

# Function App Basics
The first thing to consider, is that Golang applications (or any application) in an Azure Function needs to run as a web service. Fortunately in Go, this is fairly trivial. This is documented in [Azure's documentation](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-other?tabs=go%2Clinux#create-and-build-your-function)

Not documented is that Azure will ping the / endpoint to see if you app is alive. I usually create an empty handler, something like the below:

```go
func main() {
	httpPort := getHTTPPort()
	fmt.Println("Starting http server on port ", httpPort)
	mux := http.NewServeMux()
	mux.HandleFunc("/", emptyHandler)
	err := http.ListenAndServe(fmt.Sprintf(":%d", httpPort), mux)
	if err != nil {
		fmt.Printf("error starting http server: ", err)
		return
	}
}
func emptyHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNoContent)
}
```

# Azure SDK for Go
When developing a Go Azure Function the most essential software you'll be working with is the Azure SDK for Go. When choosing methods to use, ensure you choose the methods that don't use `autorest` as sometimes they'll rely on the Azure Metadata service to authenticate, which doesn't exist in Azure Functions. Autorest also has been deprecated in favor of Azure Identity.

Typically your `import` list from the SDKs will include:
```go
import (
	"github.com/Azure/azure-sdk-for-go/sdk/azcore/to"
	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
)
```
as well as something under the tree `github.com/Azure/azure-sdk-for-go/sdk/resourcemanager`. For example, in the past I've used the following (not all in one package, though you could):
```go
import (
"github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/compute/armcompute"
"github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/resources/armresources"
"github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/resourcegraph/armresourcegraph"
"github.com/Azure/azure-sdk-for-go/sdk/data/aztables"
"github.com/Azure/azure-sdk-for-go/sdk/keyvault/azsecrets"
)
```

# Logging
For the best experience, so you can see the results of your function and alert on it like below, you'll want to get logging working with your Azure Function.
![image.png](/.attachments/image-01aa5dc7-8bec-4788-a0c4-6dc2298cfc94.png)

This documented in the [Azure Functions custom handlers](https://learn.microsoft.com/en-us/azure/azure-functions/functions-custom-handlers) document. Whet it comes down to, is that the Azure Function needs to respond with some log json when it's done. What you can do, is create a package that declares a `[]string`, and then you can append to that `[]string` and emit when you're done.

Below you'll see `responseLogs []string` which is appended to by the LogInfo function. Once the function is done, you would call `SendJsonResponse()` once you're done.

 ```go
var (
	responseLogs []string
)
// Struct for Azure Function JSON
type InvokeRequest struct {
	Data     map[string]json.RawMessage
	Metadata map[string]interface{}
}

// Struct for Azure Function JSON
type InvokeResponse struct {
	Outputs     map[string]interface{}
	Logs        []string
	ReturnValue interface{}
}

func LogInfo(message string) {
	klog.Infoln(message)
	if strings.HasSuffix(message, "\n") {
		responseLogs = append(responseLogs, message)
	} else {
		responseLogs = append(responseLogs, message+"\n")
	}
}

// Create vars to put together a JSON response and logging for the timer trigger
func SendJsonResponse(w http.ResponseWriter, r *http.Request) {
	var invokeRequest InvokeRequest

	d := json.NewDecoder(r.Body)
	d.Decode(&invokeRequest)

	var reqData map[string]interface{}
	json.Unmarshal(invokeRequest.Data["req"], &reqData)

	outputs := make(map[string]interface{})
	outputs["message"] = reqData["Body"]

	resData := make(map[string]interface{})
	resData["body"] = "Beginning groupsync"
	outputs["res"] = resData
	invokeResponse := InvokeResponse{outputs, responseLogs, nil}
	responseJson, _ := json.Marshal(invokeResponse)
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.Write(responseJson)
}

```

# Testing
You can run your functionapp as just a web server on your workstation, and see if you can send commands to it like:
```bash
curl -i http://127.0.0.1:8080/deploygpumetrics 
```

A better way is to use the [Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools). Once installed, you can use your Azure Function dir that you're about to deploy, and test it. The core tools will check your Azure Function for a number of errors. Running it is as simple as installing the core tools, going to the dir where your handler binary is, and running:

```bash
func start
```
Ensure that you're running func on the same OS that your handler has been bulit for.


# Packaging and Deploying
What an Azure Function needs from a Go custom handler is minimal and simple. From the documentation, this would be all the files needed for a valid function:
```
| /MyQueueFunction
|   function.json
|
| host.json
| local.settings.json
| handler
```
Handler is the name of the binary, but if your Azure Function was Windows hosted, of course it would be `handler.exe` (or the name of your choice set in `host.json`.

To deploy, the above simply needs to be in a zip file, and then can be deployed with the cli with:
```bash
az functionapp deployment source config-zip -g <resourcegroup> -n <functionappname> --src publish.zip
```

## host.json
`host.json` specifies some features for the function such as the version, what the name of the binary is that it runs. Also importantly, it also lets you set the timeout from the default 5 minutes via `functionTimeout`. You can read [Azure Functions Hosting Options](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale) for more about timeout limits.

```json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    }
  },
  "functionTimeout": "00:10:00",
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[3.3.0, 4.0.0)"
  },
  "customHandler": {
    "description": {
      "defaultExecutablePath": "handler",
      "workingDirectory": "",
      "arguments": []
    },
    "enableForwardingHttpRequest": true
  }
}
```
## local.settings.json 
`local.settings.json` is useful for any local testing, and to set defaults within the Azure Function if you're setting things like environment variables. Here's an example from a project I built

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "custom",
     "AZURETABLEACCOUNT": "gpumetricstome",
     "AZURESTORAGEACCOUNT": "gpumetricstome",
     "AZURECONTAINERNAME": "gpumetricsdeploy",
     "AZURETABLENAME": "gpumetricsdeploy"
  }
}
```

# References

## Documentation
[Azure Functions custom handlers](https://learn.microsoft.com/en-us/azure/azure-functions/functions-custom-handlers)
[Deploying a Function App](https://docs.microsoft.com/en-us/azure/azure-functions/functions-deployment-technologies)
[Quickstart: Create a Go or Rust function in Azure using VSCode](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-other?tabs=go%2Clinux)
[How to configure monitoring for Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/configure-monitoring?tabs=v2)
[Azure Functions Hosting Options](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)
[Azure CLI - az functionapp deployment source](https://learn.microsoft.com/en-us/cli/azure/functionapp/deployment/source?view=azure-cli-latest#az-functionapp-deployment-source-config-zip)

## Repositories + Documentation
[Azure SDK for Go](https://github.com/Azure/azure-sdk-for-go)
[Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools)

## Model Projects

[Azure Functions - DeployGPUMetrics](https://dev.azure.com/msresearch/MSR%20Engineering/_git/Azure_Functions-DeployGPUMetrics)
[Azure Functions - groupsyncdirpgsql](https://dev.azure.com/msresearch/MSR%20Engineering/_git/Azure_Functions-groupsyncdirpgsql)