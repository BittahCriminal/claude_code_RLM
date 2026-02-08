I_CONFIG_DIR` if set)
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
