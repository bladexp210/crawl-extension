# Crawl Extension

A Gemini CLI extension for crawling web content and saving it as Obsidian-compatible Markdown files. It uses `crawl4ai` under the hood for high-quality extraction.

## Prerequisites

This extension requires the following to be installed on your system:

1.  **Python 3.10+**
2.  **uv**: A fast Python package installer and resolver.
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
3.  **Playwright Browsers**: Required by `crawl4ai`.
    ```bash
    uv run --with playwright playwright install chromium
    ```

## Installation

To install the extension, use the Gemini CLI:

```bash
gemini extension install https://github.com/bladexp210/crawl-extension
```

## Usage

### Direct Tool Usage

You can call the `crawl_urls` tool directly if you already have a list of URLs:

```bash
gemini run "Crawl https://example.com and save to ./research"
```

### Research Skill

The `crawler` skill provides an interactive research loop. It will search for relevant URLs, let you refine the list, and then crawl them all at once.

```bash
gemini run skills crawler "Research the latest developments in quantum computing"
```

## Output Structure

The extension saves content to the specified `output_dir`:

- Each URL is saved as a `.md` file.
- Files include YAML frontmatter with the source URL and crawl date.
- An `_Index.md` file is created with wikilinks to all crawled pages.

## Development

The extension consists of:
- `tools/crawl_urls.js`: The bridge between Gemini CLI and the Python crawler.
- `scripts/crawl.py`: The core crawling logic using `crawl4ai`.
- `skills/crawler.md`: The system prompt defining the research loop.
