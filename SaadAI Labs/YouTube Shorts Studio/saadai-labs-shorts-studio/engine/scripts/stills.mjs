// Renders one still per requested frame from a props file (bundles once).
// node scripts/stills.mjs <props.json> <outDir> <frame,frame,...> [scale]
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const [, , propsPath, outDir, framesArg, scaleArg] = process.argv;
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const inputProps = JSON.parse(fs.readFileSync(propsPath, 'utf8'));
const frames = framesArg.split(',').map(Number);
const scale = Number(scaleArg || 0.5);
fs.mkdirSync(outDir, {recursive: true});

const serveUrl = await bundle({entryPoint: path.join(root, 'src/index.ts'), publicDir: path.join(root, 'public')});
const composition = await selectComposition({serveUrl, id: 'Short', inputProps});
for (const frame of frames) {
  const output = path.join(outDir, `f${String(frame).padStart(5, '0')}.png`);
  await renderStill({serveUrl, composition, inputProps, frame: Math.min(frame, composition.durationInFrames - 1), output, scale});
  console.log(output);
}
