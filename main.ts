// The World Today — Friday, 20 November 2026.
// Entry for the make.fun bounty "Sum up 20 November's world news in one
// image" (news-image-20261120).
//
// The front page (entry.png, drawn in this session) is shipped with the
// repository; this program copies it byte for byte to the output directory
// the grader points at, so both runs produce identical bytes.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set");
}

mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);

// Guard against a truncated copy: the output must be the same file, byte
// for byte, so the sizes must match exactly.
if (statSync(source).size !== statSync(target).size) {
  throw new Error("entry.png copy is incomplete");
}
console.log(`wrote ${target} (${statSync(target).size} bytes)`);
