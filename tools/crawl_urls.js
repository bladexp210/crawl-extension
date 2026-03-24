#!/usr/bin/env node
const { spawn } = require('child_process');
const path = require('path');

/**
 * Tool script for crawling URLs.
 * Accepts an array of URLs and an output directory.
 * Spawns 'uv run scripts/crawl.py <output_dir> <urls...>'.
 */
async function main() {
  let input;
  try {
    // Gemini CLI usually passes tool arguments as a JSON string in the first argument
    if (process.argv[2]) {
      input = JSON.parse(process.argv[2]);
    } else {
      // Fallback: read from stdin
      const data = await readStdin();
      if (data) {
        input = JSON.parse(data);
      }
    }
  } catch (e) {
    console.error('Error: Failed to parse input as JSON.');
    console.error(e.message);
    process.exit(1);
  }

  if (!input || !input.urls || !input.output_dir) {
    console.error('Error: Missing required parameters "urls" or "output_dir".');
    process.exit(1);
  }

  let { urls, output_dir } = input;
  const urlsArray = Array.isArray(urls) ? urls : [urls];

  // Sanitize and resolve output_dir relative to current working directory
  output_dir = path.resolve(process.cwd(), output_dir);
  
  // Prevent writing outside the current working directory
  if (!output_dir.startsWith(process.cwd())) {
    console.error('Error: output_dir must be within the current working directory.');
    process.exit(1);
  }

  // The Python script is expected to be in scripts/crawl.py relative to the project root
  const pythonScript = path.join(__dirname, '..', 'scripts', 'crawl.py');
  
  // Command: uv run scripts/crawl.py <output_dir> <url1> <url2> ...
  const args = ['run', pythonScript, output_dir, ...urlsArray];

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

/**
 * Reads from stdin and returns the content as a string.
 */
function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.on('data', chunk => {
      data += chunk;
    });
    process.stdin.on('end', () => {
      resolve(data);
    });
    process.stdin.on('error', reject);
  });
}

main().catch(err => {
  console.error('Unhandled error:', err);
  process.exit(1);
});
