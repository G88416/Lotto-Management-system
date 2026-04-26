/**
 * generate-icons.js
 *
 * Generates all required PWA and Electron icon sizes from icons/icon.svg.
 *
 * Usage:
 *   npm install --save-dev sharp
 *   node scripts/generate-icons.js
 *
 * On macOS, also generates icon.icns via iconutil.
 * Requires: sharp, and optionally png-to-ico (for .ico).
 */

const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

let sharp;
try {
  sharp = require('sharp');
} catch {
  console.error('sharp is not installed. Run: npm install --save-dev sharp');
  process.exit(1);
}

const ICONS_DIR = path.join(__dirname, '..', 'icons');
const SVG_SOURCE = path.join(ICONS_DIR, 'icon.svg');

const PNG_SIZES = [72, 96, 128, 144, 152, 192, 384, 512];

async function generatePNGs() {
  const svgBuffer = fs.readFileSync(SVG_SOURCE);

  for (const size of PNG_SIZES) {
    const outPath = path.join(ICONS_DIR, `icon-${size}.png`);
    await sharp(svgBuffer).resize(size, size).png().toFile(outPath);
    console.log(`  ✓ icons/icon-${size}.png`);
  }
}

async function generateICNS() {
  if (process.platform !== 'darwin') {
    console.log('  ⚠  Skipping .icns — only supported on macOS (iconutil required).');
    return;
  }

  const iconsetDir = path.join(ICONS_DIR, 'icon.iconset');
  fs.mkdirSync(iconsetDir, { recursive: true });

  // iconset requires specific filenames
  const iconsetSizes = [
    [16, 'icon_16x16.png'],
    [32, 'icon_16x16@2x.png'],
    [32, 'icon_32x32.png'],
    [64, 'icon_32x32@2x.png'],
    [128, 'icon_128x128.png'],
    [256, 'icon_128x128@2x.png'],
    [256, 'icon_256x256.png'],
    [512, 'icon_256x256@2x.png'],
    [512, 'icon_512x512.png'],
    [1024, 'icon_512x512@2x.png'],
  ];

  const svgBuffer = fs.readFileSync(SVG_SOURCE);
  for (const [size, name] of iconsetSizes) {
    await sharp(svgBuffer)
      .resize(size, size)
      .png()
      .toFile(path.join(iconsetDir, name));
  }

  const icnsOut = path.join(ICONS_DIR, 'icon.icns');
  execSync(`iconutil -c icns "${iconsetDir}" -o "${icnsOut}"`);
  fs.rmSync(iconsetDir, { recursive: true });
  console.log('  ✓ icons/icon.icns');
}

async function generateICO() {
  let pngToIco;
  try {
    pngToIco = require('png-to-ico');
  } catch {
    console.log('  ⚠  Skipping .ico — install png-to-ico: npm install --save-dev png-to-ico');
    return;
  }

  const sizes = [16, 32, 48, 64, 128, 256];
  const svgBuffer = fs.readFileSync(SVG_SOURCE);
  const pngBuffers = await Promise.all(
    sizes.map((s) => sharp(svgBuffer).resize(s, s).png().toBuffer())
  );

  const icoBuffer = await pngToIco(pngBuffers);
  fs.writeFileSync(path.join(ICONS_DIR, 'icon.ico'), icoBuffer);
  console.log('  ✓ icons/icon.ico');
}

(async () => {
  console.log('Generating icons from icons/icon.svg …\n');
  await generatePNGs();
  await generateICNS();
  await generateICO();
  console.log('\nDone.');
})();
