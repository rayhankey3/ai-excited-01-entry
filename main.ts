import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const outputPath = join(outputDir, "entry.png");
const judgeSource = "/bot/entry.png";
const localSource = join(process.cwd(), "entry.png");

const main = () => {
  const source = existsSync(judgeSource) ? judgeSource : localSource;
  mkdirSync(outputDir, { recursive: true });
  copyFileSync(source, outputPath);
  console.log(`Copied entry.png to ${outputPath}`);
  process.exit(0);
};

main();