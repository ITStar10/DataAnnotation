# decode.py

Fetches a published Google Doc, reads a table of `(x, y, character)` cells, and prints the characters as a 2D grid so the hidden message is visible in the terminal.

## Requirements

- Python 3
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

```sh
python -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4
```

## Usage

The script currently calls `decode_secret_message()` with a published Google Doc URL. Run it from this directory:

```sh
python decode.py
```

To decode a different document, change the URL passed to `decode_secret_message()`:

```python
decode_secret_message("https://docs.google.com/document/d/e/.../pub")
```

The document must be published to the web (`File → Share → Publish to web`) so the script can fetch it without auth.

## Input format

The published page must contain an HTML table with these headers (order can vary):

| x-coordinate | Character | y-coordinate |
|--------------|-----------|--------------|
| 0            | █         | 0            |
| 1            | ░         | 0            |
| …            | …         | …            |

Each data row is one grid cell. Missing coordinates are filled with a space.

## How it works

1. Download the published HTML.
2. Find the first table whose headers include `x-coordinate`, `character`, and `y-coordinate`.
3. Place each character at `(x, y)`.
4. Print rows from highest `y` to lowest so the graphic is right-side up.

## Example

The included URL prints this message:

```
██░     ██░    ███████░     ██░     ██░     ██████░ ████████░    ████████░     ████████░
██░     ██░  ███░    ██░   ████░   ████░      ██░   ██░     ██░  ██░     ██░ ███░     ███░
██░     ██░ ███░           ██░██░ ██░██░      ██░   ██░      ██░ ██░     ██░ ██░       ██░
██████████░ ██░           ███░ ██░██░ ██░     ██░   ██░      ██░ ████████░   ██░       ██░
██░     ██░ ███░          ██░  █████░ ███░    ██░   ██░      ██░ ██░     ██░ ██░       ██░
██░     ██░  ███░    ██░ ███░   ███░   ██░    ██░   ██░     ██░  ██░     ██░ ███░     ███░
██░     ██░    ███████░  ██░           ███░ ██████░ ████████░    ████████░     ████████░
```
