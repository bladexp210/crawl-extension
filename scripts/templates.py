from crawl4ai import CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator

# Template definitions for different types of documentation
# Each template is a CrawlerRunConfig preset that optimizes for specific content depth.

CRAWL_TEMPLATES = {
    "technical-docs": CrawlerRunConfig(
        # Use DefaultMarkdownGenerator with options to preserve structure
        markdown_generator=DefaultMarkdownGenerator(
            options={
                "ignore_links": False,
                "ignore_images": False,
                "ignore_tables": False,
                "body_width": 0,  # Do not wrap lines
            }
        ),
        cache_mode=CacheMode.BYPASS,
        process_iframes=True,
        remove_overlay_elements=True,
    ),
    "api-reference": CrawlerRunConfig(
        # More aggressive on cleaning but preserving code signatures
        markdown_generator=DefaultMarkdownGenerator(
            options={
                "ignore_links": False,
                "ignore_images": True, # Usually decorative in API docs
                "ignore_tables": False,
                "body_width": 0,
            }
        ),
        cache_mode=CacheMode.BYPASS,
        process_iframes=True,
        remove_overlay_elements=True,
    ),
    "minimal": CrawlerRunConfig(
        # Basic extraction with default clutter removal
        markdown_generator=DefaultMarkdownGenerator(),
        cache_mode=CacheMode.BYPASS,
    )
}

if __name__ == "__main__":
    # Simple validation check
    print("CRAWL_TEMPLATES defined successfully.")
    for name, config in CRAWL_TEMPLATES.items():
        print(f"Template '{name}': cache_mode={config.cache_mode}")
