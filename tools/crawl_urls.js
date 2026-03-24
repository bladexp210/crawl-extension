#!/usr/bin/env node
const { spawn } = require('child_process');
const path = require('path');

/**
 * Tool script for crawling URLs.
 * Accepts an array of URLs, an output directory, and an optional template.
 * Spawns 'uv run scripts/crawl.py <output_dir> <urls...> --template <template>'.
 */
async function main() {
  let input;
  try {
    // Gemini CLI usually passes tool arguments as a JSON string in the first argument
    if (process.argv[2] && process.argv[2].startsWith('{')) {
      input = JSON.parse(process.argv[2]);
    } else {
      // Manual execution or positional arguments
      input = {
        output_dir: process.argv[2],
        urls: [],
        template: 'technical-docs'
      };
      
      let urlsStarted = false;
      for (let i = 3; i < process.argv.length; i++) {
        if (process.argv[i] === '--template') {
          input.template = process.argv[i+1];
          i++;
        } else {
          input.urls.push(process.argv[i]);
        }
      }
    }
  } catch (e) {
    console.error('Error: Failed to parse input.');
    console.error(e.message);
    process.exit(1);
  }

  if (!input || !input.urls || !input.output_dir) {
    console.error('Error: Missing required parameters "urls" or "output_dir".');
    console.error('Usage: node tools/crawl_urls.js <output_dir> <url1> [url2...] [--template <template>]');
    process.exit(1);
  }

  let { urls, output_dir, template } = input;
  const urlsArray = Array.isArray(urls) ? urls : [urls];
  const templateName = template || 'technical-docs';

  // Sanitize and resolve output_dir relative to current working directory
  const absoluteOutputDir = path.resolve(process.cwd(), output_dir);
  
  // Prevent writing outside the current working directory
  if (!absoluteOutputDir.startsWith(process.cwd())) {
    console.error('Error: output_dir must be within the current working directory.');
    process.exit(1);
  }

  // The Python script is expected to be in scripts/crawl.py relative to the project root
  const pythonScript = path.join(__dirname, '..', 'scripts', 'crawl.py');
  
  // Command: uv run scripts/crawl.py <output_dir> <url1> <url2> ... --template <template>
  const args = ['run', pythonScript, output_dir, ...urlsArray, '--template', templateName];

  const child = spawn('uv', args, {
    stdio: 'inherit',
    cwd: path.join(__dirname, '..')
  });

  await new Promise((resolve, reject) => {
    child.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python script exited with code ${code}`);
        process.exit(code);
      }
      resolve();
    });
    child.on('error', reject);
  });
}

main().catch(err => {
  console.error('Unhandled error:', err);
  process.exit(1);
});
