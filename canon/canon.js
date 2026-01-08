/**
 * Seven Living Magicks Canon Definition
 * Single source of truth for the 7-color sequence and adjacency rules.
 *
 * DO NOT modify this file directly.
 * The canonical definition is in canon/canon.json.
 */

const fs = require('fs');
const path = require('path');

// Load canonical definition
const canonPath = path.join(__dirname, 'canon.json');
const CANON = JSON.parse(fs.readFileSync(canonPath, 'utf-8'));

// Canonical sequence
const COLORS = CANON.canon.colors.ordered_sequence;
const COLOR_COUNT = COLORS.length;

// Adjacency rule
const ADJACENCY_RULE = CANON.canon.adjacency.rule;
const MODULUS = CANON.canon.adjacency.modulus;
const VALID_DELTAS = CANON.canon.adjacency.valid_deltas;

// Meta tokens
const VIOLET = CANON.canon.meta_tokens.violet;
const GRAY = CANON.canon.meta_tokens.gray;

// Symbol mappings
const SYMBOL_TO_INDEX = Object.fromEntries(
  COLORS.map(color => [color.symbol, color.index])
);

const NAME_TO_INDEX = Object.fromEntries(
  COLORS.map(color => [color.name.toLowerCase(), color.index])
);

const INDEX_TO_SYMBOL = Object.fromEntries(
  COLORS.map(color => [color.index, color.symbol])
);

const INDEX_TO_NAME = Object.fromEntries(
  COLORS.map(color => [color.index, color.name])
);

// Color enum
const Color = {
  BLACK: 0,
  WHITE: 1,
  YELLOW: 2,
  BROWN: 3,
  RED: 4,
  GREEN: 5,
  BLUE: 6,
};

/**
 * Get color definition by index
 * @param {number} index - Color index (0-6)
 * @returns {object} Color definition
 */
function getColorByIndex(index) {
  return COLORS[index % MODULUS];
}

/**
 * Get color definition by name (case-insensitive)
 * @param {string} name - Color name
 * @returns {object} Color definition
 */
function getColorByName(name) {
  const index = NAME_TO_INDEX[name.toLowerCase()];
  if (index === undefined) {
    throw new Error(`Unknown color name: ${name}`);
  }
  return COLORS[index];
}

/**
 * Get color definition by symbol
 * @param {string} symbol - Color symbol (emoji)
 * @returns {object} Color definition
 */
function getColorBySymbol(symbol) {
  const index = SYMBOL_TO_INDEX[symbol];
  if (index === undefined) {
    throw new Error(`Unknown color symbol: ${symbol}`);
  }
  return COLORS[index];
}

/**
 * Check if transition respects adjacency law (±1 mod 7)
 * @param {number} fromIndex - Starting color index
 * @param {number} toIndex - Target color index
 * @returns {boolean} True if legal transition
 */
function isAdjacent(fromIndex, toIndex) {
  const delta = (toIndex - fromIndex + MODULUS) % MODULUS;
  return VALID_DELTAS.includes(delta);
}

/**
 * Validate a sequence of color indices
 * @param {number[]} sequence - Array of color indices
 * @returns {{isValid: boolean, violations: object[]}} Validation result
 */
function validateSequence(sequence) {
  const violations = [];

  for (let i = 0; i < sequence.length - 1; i++) {
    const fromIdx = sequence[i];
    const toIdx = sequence[i + 1];

    if (!isAdjacent(fromIdx, toIdx)) {
      const delta = (toIdx - fromIdx + MODULUS) % MODULUS;
      violations.push({
        type: 'adjacency_violation',
        index: i,
        from: fromIdx,
        to: toIdx,
        delta,
        reason: `Illegal jump: delta ${delta} not in [${VALID_DELTAS.join(', ')}]`,
      });
    }
  }

  return {
    isValid: violations.length === 0,
    violations,
  };
}

/**
 * Get canon definition version
 * @returns {string} Version string
 */
function getCanonVersion() {
  return CANON.version;
}

// Exports
module.exports = {
  Color,
  COLORS,
  COLOR_COUNT,
  ADJACENCY_RULE,
  MODULUS,
  VALID_DELTAS,
  VIOLET,
  GRAY,
  SYMBOL_TO_INDEX,
  NAME_TO_INDEX,
  INDEX_TO_SYMBOL,
  INDEX_TO_NAME,
  getColorByIndex,
  getColorByName,
  getColorBySymbol,
  isAdjacent,
  validateSequence,
  getCanonVersion,
};
