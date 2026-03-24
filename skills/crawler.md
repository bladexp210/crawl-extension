# Crawler Skill

This skill defines the behavior for an agent tasked with researching a topic by crawling relevant websites and building a local documentation folder.

## Research Loop Protocol

Follow these steps when a user asks to "crawl" or "research" a technical topic:

### Step 1 — Discovery
Use a search tool (e.g., Tavily or Wikipedia) to identify high-quality, authoritative URLs related to the research topic.

### Step 2 — Refinement
Present the discovered URLs to the user and ask for approval or refinement.
- Summarize why each URL was chosen.
- Ask if any URLs should be removed or if specific pages are missing.

### Step 3 — Template Selection
Recommend an extraction template based on the research context:
- `technical-docs` (Default): Optimized for preserving tables, code blocks, and deep structure. Best for tutorials and guides.
- `api-reference`: Optimized for extracting structured signatures and technical specifications. Ignores decorative images.
- `minimal`: Basic extraction with standard clutter removal. Good for simple articles.

Ask the user to confirm the recommended template.

### Step 4 — Execution
Once URLs and the template are approved, use the `crawl_urls` tool to capture the content.
- `urls`: The list of approved URLs.
- `output_dir`: A descriptive directory name based on the topic.
- `template`: The approved extraction template.

### Step 5 — Synthesis
After the crawl completes, notify the user and suggest next steps, such as summarizing the captured knowledge or answering specific questions from the local docs.

## Tool Usage: `crawl_urls`

When calling `crawl_urls`, ensure you provide:
- **urls**: An array of strings.
- **output_dir**: A string path (e.g., "docs/my-topic").
- **template**: (Optional) One of `technical-docs`, `api-reference`, or `minimal`. Defaults to `technical-docs`.

Example:
```json
{
  "urls": ["https://docs.python.org/3/library/argparse.html"],
  "output_dir": "docs/argparse-guide",
  "template": "technical-docs"
}
```
