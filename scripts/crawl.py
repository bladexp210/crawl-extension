# /// script
# dependencies = [
#   "crawl4ai",
# ]
# ///

import asyncio
import sys
import re
from pathlib import Path
from datetime import datetime
from crawl4ai import AsyncWebCrawler

def slugify(text: str) -> str:
    """
    Convert a string to a URL-friendly slug.
    """
    # Remove protocol and common prefixes if it's a URL
    text = re.sub(r'^https?://(www\.)?', '', text)
    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text).strip().lower()
    # Replace whitespace and multiple hyphens with a single hyphen
    text = re.sub(r'[\s-]+', '-', text)
    return text

async def crawl_and_save(urls: list[str], output_dir: Path):
    """
    Crawl a list of URLs and save them as Markdown files in the output directory.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    index_entries = []

    async with AsyncWebCrawler() as crawler:
        for url in urls:
            print(f"Crawling: {url}...")
            try:
                result = await crawler.arun(url=url)
                
                if not result.success:
                    print(f"Error crawling {url}: {result.error_message}")
                    continue

                # Determine filename from title or URL
                title = result.metadata.get('title') if result.metadata else None
                if not title:
                    title = url
                
                filename = slugify(title)
                if not filename:
                    filename = "untitled"
                
                # Ensure filename is unique in the output directory
                base_filename = filename
                counter = 1
                while (output_dir / f"{filename}.md").exists():
                    filename = f"{base_filename}-{counter}"
                    counter += 1
                
                file_path = output_dir / f"{filename}.md"
                
                # Prepare content with Obsidian-style YAML frontmatter
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                frontmatter = (
                    "---\n"
                    f"url: {url}\n"
                    f"date: {now}\n"
                    "---\n\n"
                )
                
                markdown_content = result.markdown if result.markdown else ""
                full_content = frontmatter + markdown_content
                
                file_path.write_text(full_content, encoding="utf-8")
                print(f"Saved: {file_path}")
                
                index_entries.append(f"- [[{filename}]]")
                
            except Exception as e:
                print(f"Unexpected error crawling {url}: {e}")

    # Create _Index.md
    index_path = output_dir / "_Index.md"
    index_content = "# Index\n\n" + "\n".join(index_entries)
    index_path.write_text(index_content, encoding="utf-8")
    print(f"Created index: {index_path}")

async def main():
    if len(sys.argv) < 3:
        print("Usage: uv run scripts/crawl.py <output_dir> <url1> [url2 ...]")
        sys.exit(1)

    output_dir = Path(sys.argv[1])
    urls = sys.argv[2:]

    await crawl_and_save(urls, output_dir)

if __name__ == "__main__":
    asyncio.run(main())
