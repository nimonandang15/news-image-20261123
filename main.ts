// news-image-20261123 — "The World in One Day", Monday 23 November 2026.
//
// A tiny Node 22 program (standard library only) that ships the poster
// drawn by render.py: it reads entry.png from beside this file and
// writes the same bytes to /output/entry.png, after proving the file
// is a whole PNG inside the gate limits (at most 1 MiB, at most
// 1024 by 1024). Running it twice writes the same bytes twice.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const LIMIT_BYTES = 1024 * 1024;
const LIMIT_PX = 1024;

function die(message) {
  throw new Error(message);
}

function u32be(buf, at) {
  return buf.readUInt32BE(at);
}

function chunkTag(buf, at) {
  return buf.subarray(at, at + 4).toString("latin1");
}

const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const png = readFileSync(new URL("./entry.png", import.meta.url));

if (png.length > LIMIT_BYTES) {
  die(`entry.png is ${png.length} bytes, over the 1 MiB limit`);
}
if (png.length < 33) {
  die("entry.png is too short to hold a PNG header and IEND");
}
for (let i = 0; i < MAGIC.length; i += 1) {
  if (png[i] !== MAGIC[i]) die("entry.png is not a PNG (bad magic bytes)");
}
if (chunkTag(png, 12) !== "IHDR") {
  die("entry.png has no IHDR chunk (not a valid PNG)");
}
const pxWide = u32be(png, 16);
const pxHigh = u32be(png, 20);
if (pxWide === 0 || pxHigh === 0) {
  die("entry.png has a zero dimension");
}
if (pxWide > LIMIT_PX || pxHigh > LIMIT_PX) {
  die(`entry.png is ${pxWide}x${pxHigh}, over the 1024x1024 limit`);
}
// The IEND chunk is 12 bytes: a zero length, the tag, and a CRC, so
// the tag itself sits 8 bytes before the end of the file.
if (chunkTag(png, png.length - 8) !== "IEND") {
  die("entry.png is truncated (no IEND chunk at the end)");
}

mkdirSync(targetDir, { recursive: true });
const dest = join(targetDir, "entry.png");
writeFileSync(dest, png);

const back = readFileSync(dest);
if (!back.equals(png)) {
  die("output entry.png differs from entry.png after writing");
}

const digest = createHash("sha256").update(png).digest("hex");
console.log(
  `wrote entry.png: ${pxWide}x${pxHigh}, ${png.length} bytes, sha256 ${digest}`,
);
