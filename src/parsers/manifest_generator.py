"""
Archive manifest generator.

Walks corpus directory and generates manifest.json with file metadata.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def compute_hash(file_path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def detect_file_type(file_path: Path) -> str:
    """Detect file type from extension."""
    suffix = file_path.suffix.lower()
    type_map = {
        '.txt': 'text',
        '.md': 'markdown',
        '.pdf': 'pdf',
        '.json': 'json',
        '.zip': 'archive',
        '.py': 'python',
        '.lean': 'lean',
    }
    return type_map.get(suffix, 'unknown')


def extract_metadata(file_path: Path) -> Dict[str, Any]:
    """
    Extract metadata from a file.

    TODO: Implement content analysis:
    - Extract headings from Markdown/text
    - Parse PDF metadata
    - Detect topic tags
    - Extract canon receipts
    """
    stat = file_path.stat()

    return {
        "path": str(file_path),
        "name": file_path.name,
        "size": stat.st_size,
        "type": detect_file_type(file_path),
        "hash": compute_hash(file_path),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "tags": [],  # TODO: Implement tag detection
        "headings": [],  # TODO: Extract headings
        "canon_references": []  # TODO: Detect canon mentions
    }


def generate_manifest(corpus_path: Path, output_path: Path = None) -> Dict[str, Any]:
    """
    Generate manifest.json for all files in corpus.

    Args:
        corpus_path: Path to corpus directory
        output_path: Optional output path for manifest.json

    Returns:
        Manifest dictionary
    """
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus path not found: {corpus_path}")

    files = []
    for file_path in corpus_path.rglob('*'):
        if file_path.is_file() and not file_path.name.startswith('.'):
            try:
                metadata = extract_metadata(file_path)
                files.append(metadata)
            except Exception as e:
                print(f"Warning: Failed to process {file_path}: {e}")

    manifest = {
        "generated": datetime.now().isoformat(),
        "corpus_path": str(corpus_path),
        "file_count": len(files),
        "files": files
    }

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

    return manifest


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python manifest_generator.py <corpus_path> [output_path]")
        sys.exit(1)

    corpus = Path(sys.argv[1])
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else corpus / "manifest.json"

    manifest = generate_manifest(corpus, output)
    print(f"✓ Generated manifest with {manifest['file_count']} files")
    print(f"  Output: {output}")
