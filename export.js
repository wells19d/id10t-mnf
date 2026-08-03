const fs = require('fs');
const path = require('path');

const ROOT_DIR = __dirname;
const COMPONENT_DIR = path.join(ROOT_DIR); // Start at project root
const OUTPUT_STRUCTURE_FILE = path.join(ROOT_DIR, 'z-sandbox', 'structure.txt');
const OUTPUT_CODE_FILE = path.join(ROOT_DIR, 'z-sandbox', 'export.txt');

const codeExtensions = [
  '.js',
  '.jsx',
  '.ts',
  '.tsx',
  '.json',
  '.html',
  '.css',
  '.py',
];
const structureExtensions = [...codeExtensions, '.png']; // for structure

const ignoreFolders = [
  '__pycache__',
  '.venv',
  '.vscode',
  '.git',
  'node_modules',
  'z-sandbox',
];

const ignoreFiles = [
  '.DS_Store',
  '.gitignore',
  'structure.txt', // na
  'export.txt', // na
  'export.js', //na
];

function walk(dir, validExtensions) {
  let results = [];

  fs.readdirSync(dir).forEach((file) => {
    const filepath = path.join(dir, file);
    const relativePath = path.relative(ROOT_DIR, filepath);
    const stat = fs.statSync(filepath);

    if (
      stat.isDirectory() &&
      !ignoreFolders.includes(path.basename(filepath))
    ) {
      results = results.concat(walk(filepath, validExtensions));
    } else if (
      stat.isFile() &&
      !ignoreFiles.includes(path.basename(filepath)) &&
      validExtensions.includes(path.extname(file))
    ) {
      results.push(filepath);
    }
  });

  return results;
}

// 📁 Build file list for structure
const structureFiles = walk(COMPONENT_DIR, structureExtensions);
const structureList = structureFiles.map((file) =>
  path.relative(ROOT_DIR, file),
);
fs.writeFileSync(OUTPUT_STRUCTURE_FILE, structureList.join('\n'), 'utf8');

// 📄 Build file list for code dump
const codeFiles = walk(COMPONENT_DIR, codeExtensions);
let bundle = '';
codeFiles.forEach((file) => {
  const relativePath = path.relative(ROOT_DIR, file);
  const code = fs.readFileSync(file, 'utf8');
  bundle += `\n\n--- FILE: ${relativePath} ---\n\n${code}`;
});
fs.writeFileSync(OUTPUT_CODE_FILE, bundle, 'utf8');
