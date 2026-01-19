---
name: dagger
description: Run Dagger CI/CD pipelines for building, testing, and deploying containerized workloads. Provides a programmable, reproducible automation engine with multi-language SDK support.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Dagger CLI Skill

This skill provides CI/CD automation using Dagger - a programmable automation engine that runs containers locally, in CI, or in the cloud.

## What is Dagger?

Dagger is a platform for automating software delivery:
- **Programmable**: Replaces shell scripts and YAML with real code
- **Local-first**: Runs identically on laptops, CI servers, and cloud
- **Repeatable**: Container-based with content-addressed caching
- **Observable**: Built-in OpenTelemetry tracing

## Prerequisites

```bash
# Check if Dagger is installed
dagger version

# If not installed, install via:
# macOS
brew install dagger/tap/dagger

# Linux/WSL
curl -fsSL https://dl.dagger.io/dagger/install.sh | sh

# Container runtime must be available (Docker, Podman, etc.)
docker version
```

## Inputs

This Skill reads `$ARGUMENTS`. Accept these patterns:
- `action=<init|call|run|shell>` - Primary action to perform
- `module=<path>` - Path to Dagger module (default: current directory)
- `sdk=<go|python|typescript>` - SDK language for init
- `function=<name>` - Function to call
- `args=<arguments>` - Arguments to pass to function

## Actions

### 1. Initialize a New Dagger Module

```bash
# Initialize with Go SDK
dagger init --sdk=go --name=my-pipeline

# Initialize with Python SDK
dagger init --sdk=python --name=my-pipeline

# Initialize with TypeScript SDK
dagger init --sdk=typescript --name=my-pipeline
```

This creates:
- `dagger.json` - Module configuration
- `src/` or language-specific source directory
- Initial module code

### 2. Interactive Shell

Launch an interactive Dagger shell for exploration:

```bash
dagger
```

Common shell commands:
```
# Get a container
container | from alpine

# Execute commands
container | from alpine | with-exec uname | stdout

# Open terminal in container
container | from alpine | terminal

# Get help on any object
container | from alpine | .help
```

### 3. Call Functions

Execute functions from a Dagger module:

```bash
# Call a function
dagger call <function-name> [arguments]

# Call with arguments
dagger call build --source=.

# Chain function calls
dagger -c 'container | from alpine | with-exec cat /etc/os-release | stdout'
```

### 4. Run Pipelines

Execute predefined pipelines:

```bash
# Run default pipeline
dagger run

# Run specific pipeline
dagger call ci

# Run with environment variables
dagger call deploy --env=production
```

## Example Module: Go

```go
// main.go
package main

import (
    "context"
)

type MyPipeline struct{}

// Build builds the application
func (m *MyPipeline) Build(ctx context.Context, source *Directory) *Container {
    return dag.Container().
        From("golang:1.22").
        WithDirectory("/src", source).
        WithWorkdir("/src").
        WithExec([]string{"go", "build", "-o", "app", "."})
}

// Test runs the tests
func (m *MyPipeline) Test(ctx context.Context, source *Directory) string {
    return dag.Container().
        From("golang:1.22").
        WithDirectory("/src", source).
        WithWorkdir("/src").
        WithExec([]string{"go", "test", "./..."}).
        Stdout(ctx)
}

// Publish builds and publishes the container
func (m *MyPipeline) Publish(ctx context.Context, source *Directory, registry string) string {
    return m.Build(ctx, source).
        Publish(ctx, registry)
}
```

## Example Module: Python

```python
# src/main.py
import dagger
from dagger import dag, function, object_type

@object_type
class MyPipeline:
    @function
    def build(self, source: dagger.Directory) -> dagger.Container:
        """Build the application."""
        return (
            dag.container()
            .from_("python:3.12")
            .with_directory("/src", source)
            .with_workdir("/src")
            .with_exec(["pip", "install", "-r", "requirements.txt"])
        )

    @function
    async def test(self, source: dagger.Directory) -> str:
        """Run tests."""
        return await (
            dag.container()
            .from_("python:3.12")
            .with_directory("/src", source)
            .with_workdir("/src")
            .with_exec(["pytest"])
            .stdout()
        )

    @function
    async def publish(self, source: dagger.Directory, registry: str) -> str:
        """Build and publish container."""
        return await self.build(source).publish(registry)
```

## Example Module: TypeScript

```typescript
// src/index.ts
import { dag, Container, Directory, object, func } from "@dagger.io/dagger"

@object()
class MyPipeline {
  @func()
  build(source: Directory): Container {
    return dag
      .container()
      .from("node:20")
      .withDirectory("/src", source)
      .withWorkdir("/src")
      .withExec(["npm", "install"])
      .withExec(["npm", "run", "build"])
  }

  @func()
  async test(source: Directory): Promise<string> {
    return await dag
      .container()
      .from("node:20")
      .withDirectory("/src", source)
      .withWorkdir("/src")
      .withExec(["npm", "install"])
      .withExec(["npm", "test"])
      .stdout()
  }

  @func()
  async publish(source: Directory, registry: string): Promise<string> {
    return await this.build(source).publish(registry)
  }
}
```

## Workflow for Platform API

### Build and Deploy Container Apps

```bash
# Initialize Dagger module for platform
dagger init --sdk=go --name=platform-deploy

# Define deployment pipeline
dagger call deploy-container-app \
  --source=. \
  --registry=myacr.azurecr.io \
  --environment=production
```

### Integration with Score Workloads

```bash
# Generate Score manifest and deploy
dagger call score-deploy \
  --score-file=score.yaml \
  --target=kubernetes
```

## Common Patterns

### Caching Dependencies

```bash
# Use content-addressed cache
dagger -c '
container |
from node:20 |
with-mounted-cache /root/.npm "`cache-volume npm-cache`" |
with-directory /src . |
with-workdir /src |
with-exec npm install
'
```

### Secrets Handling

```bash
# Use secrets securely
dagger call deploy --token=env:DEPLOY_TOKEN
```

### Multi-Platform Builds

```bash
# Build for multiple platforms
dagger call build --platforms=linux/amd64,linux/arm64
```

## CI Integration

### GitHub Actions

```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dagger/dagger-for-github@v6
        with:
          verb: call
          args: build --source=.
```

### GitLab CI

```yaml
build:
  image: registry.dagger.io/engine:latest
  services:
    - docker:dind
  script:
    - dagger call build --source=.
```

## Troubleshooting

### Check Dagger Engine

```bash
# Check engine status
dagger version

# View engine logs
docker logs dagger-engine
```

### Debug Pipeline

```bash
# Run with debug output
dagger call --debug build

# Interactive debugging
dagger -c 'container | from alpine | terminal'
```

## References

- [Dagger Documentation](https://docs.dagger.io)
- [Dagger GitHub](https://github.com/dagger/dagger)
- [Dagger Discord](https://discord.gg/dagger-io)
- [SDK Reference](https://docs.dagger.io/reference)
