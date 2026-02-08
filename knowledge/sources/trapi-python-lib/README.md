# TRAPI

TRAPI is a Python module designed to interface with TRAPI-based APIs and services, enabling streamlined access to data and functionality.
It includes:

* `trapi-cli`, a command-line interface similar to Azure's `az` CLI.
* Feature modules that allow direct access to TRAPI and TMDS functionality within your code.
* An injectable OpenAI helper module that enables no-code enhancements for users of the OpenAI and Azure OpenAI Python libraries

# Library Users
## trapi-cli

The trapi-cli includes a number of helpers for providing consistent output-formatting, similar to the `az` CLI.  Run `trapi-cli help` to view available commands, and `trapi-cli <command> help` to view help for subcommands.

The CLI also includes a fast mechanism to verify the most basic functionality of your TRAPI services access.  Run `trapi-cli quickstart show` and after a few moments, you should see the response "Paris" (the quickstart prompt is "Give a one-word answer, what is the capital of France?").

### Batch list pagination

- Page size: `--limit <n>` (default server-side page size applies when omitted).
- Cursor: `--after <last_id>` continues from the `last_id` returned by the previous page (`has_more: true`).
- Example:
  ```
  trapi-cli batch list --limit 2 --api-version 2024-10-21 --api-path /gcr/shared
  trapi-cli batch list --limit 2 --after <last_id_from_previous_page> --api-version 2024-10-21 --api-path /gcr/shared
  ```
There is no `skip`; pagination is cursor-based via `after`.

## Injectable OpenAI Helper

To inject the TRAPI library helper functionality to an existing tool leveraging the OpenAI python libraries, simply add: `import trapi.openai_auto` to the top of your code (before the import of any OpenAI library members).

If you instead wish (or need) a no-code mechanism to leverage the TRAPI helpers, you can modify your python invocation slightly to import the module prior to running the tool/script:

`python -m trapi.openai_auto <script>`

## Persistent Request/Error Cache

Responses are persisted (sanitized) to a JSONL file so they survive process restarts.  A separate ring-buffer is maintained for successful and error responses.  These can be referenced later to aid in debugging/troubleshooting, or reporting errors to the TRAPI team.  In time the `trapi-cli` will provide tools for assisting in extracting necessary troubleshooting information and forwarding that to the team.

* Default directory: `~/.trapi` (or value of `TRAPI_CONFIG_DIR` if set)
* Override directory precedence:
	1. `TRAPI_ERROR_CACHE_DIR` environment variable
	2. Config value `cache.error_cache_dir` (set via `set_error_cache_dir`)
	3. Default directory above
* File name: `error_cache.jsonl`

Each line contains: timestamp, method, url, meta (params / json keys), and a
sanitized response snapshot (status, request headers, first 500 chars of body).

Use `request.set_error_cache_dir(path)` to change where the file lives (persisted
in config unless `persist=False`). Use `request.clear_error_cache()` to clear
both in-memory and on-disk cache.

# Developers

## Installation

After cloning the repository, execute `python init.py` to create a virtual environment and install prerequisites into it, as well as install the module in editible mode.  The script will check for the ability to create virtual environments:  under certain circumstances you may need to complete some package/modules installation before you can continue with the TRAPI library.
