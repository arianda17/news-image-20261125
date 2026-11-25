// news-image-20261125 entrypoint: decode the day's image beside this file to the output dir.
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
writeFileSync(join(outDir, 'entry.png'), Buffer.from(readFileSync(join(here, 'entry.png.b64'), 'utf8').trim(), 'base64'));