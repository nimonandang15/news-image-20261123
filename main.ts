// news-image-20261123 — "The World in One Day", Monday 23 November 2026.
// Node 22, standard library only. The poster is entry.png next to this
// file, drawn for this competition by render.py; this program copies it,
// byte for byte, to /output/entry.png, refusing anything that is not a
// whole PNG inside the gate limits (at most 1 MiB, at most 1024 x 1024).
// Deterministic: the same entry.png always yields the same output bytes.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const image = readFileSync(new URL('./entry.png', import.meta.url));

if (image.length > MAX_BYTES) {
  throw new Error(`entry.png is ${image.length} bytes, over the 1 MiB limit`);
}
if (image.length < 24) {
  throw new Error('entry.png is too short to hold a PNG header');
}
if (!image.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG (bad magic bytes)');
}
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
// The first chunk must be IHDR, and neither side may be zero: a file
// with the right magic but a forged header must not slip through.
const IHDR = Buffer.from([0x49, 0x48, 0x44, 0x52]);
if (!image.subarray(12, 16).equals(IHDR)) {
  throw new Error('entry.png has no IHDR chunk (not a valid PNG)');
}
if (width === 0 || height === 0) {
  throw new Error('entry.png has a zero dimension');
}
if (width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}
// A whole image ends with its IEND chunk: refuse a truncated file.
const IEND = Buffer.from([0x49, 0x45, 0x4e, 0x44]);
if (!image.subarray(image.length - 12).includes(IEND)) {
  throw new Error('entry.png is truncated (no IEND chunk at the end)');
}

mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, 'entry.png');
writeFileSync(outPath, image);

// Read the output back: a partial or corrupted write must fail loudly.
const written = readFileSync(outPath);
if (!written.equals(image)) {
  throw new Error('output entry.png differs from entry.png after writing');
}

const sha256 = createHash('sha256').update(image).digest('hex');
console.log(`wrote entry.png: ${width}x${height}, ${image.length} bytes, sha256 ${sha256}`);
