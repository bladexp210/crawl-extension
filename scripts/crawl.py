# /// script
# dependencies = [
#   "crawl4ai",
#   "pandas",
#   "tabulate",
# ]
# ///

import asyncio
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from templates import CRAWL_TEMPLATES

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

async def crawl_and_save(urls: list[str], output_dir: Path, template_name: str = "technical-docs"):
    """
    Crawl a list of URLs and save them as Markdown files in the output directory.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    index_entries = []

    # Get configuration from template
    config = CRAWL_TEMPLATES.get(template_name, CRAWL_TEMPLATES["technical-docs"])
    print(f"Crawling using template '{template_name}'...")

    async with AsyncWebCrawler() as crawler:
        for url in urls:
            print(f"Crawling: {url}...")
            try:
                # Use config in arun
                result = await crawler.arun(url=url, config=config)
                
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
                    f"template: {template_name}\n"
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
    parser = argparse.ArgumentParser(description="Crawl URLs and save as Markdown.")
    parser.add_argument("output_dir", type=str, help="Directory to save the results.")
    parser.add_argument("urls", nargs="+", help="One or more URLs to crawl.")
    parser.add_argument("--template", type=str, default="technical-docs", 
                        choices=list(CRAWL_TEMPLATES.keys()),
                        help="Extraction template to use.")

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    await crawl_and_save(args.urls, output_dir, args.template)

if __name__ == "__main__":
    asyncio.run(main())
