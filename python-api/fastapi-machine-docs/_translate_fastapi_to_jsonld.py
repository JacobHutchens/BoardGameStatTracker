"""
Translation script: extract FastAPI modules and emit JSON-LD per vocabulary.
Outputs a manifest JSON (filename -> content) for Generation to write to disk.
"""
from __future__ import annotations

import ast
import json
import os
import re
from pathlib import Path

FASTAPI_ROOT = Path(r"c:\Users\jacob\Documents\Personal_Github_Repos\fastapi\fastapi")
OUTPUT_DIR = Path(r"c:\Users\jacob\Documents\Personal_Github_Repos\BoardGameStatTracker\python-api\fastapi-machine-docs")
FASTAPI_VERSION = "0.128.2"


def module_path_to_output_filename(module_path: str) -> str:
    """e.g. fastapi.applications -> fastapi-applications.jsonld"""
    return module_path.replace(".", "-").replace("_", "-") + ".jsonld"


def get_module_path(rel_path: Path) -> str:
    """e.g. fastapi\\applications.py -> fastapi.applications"""
    parts = rel_path.with_suffix("").parts
    return "fastapi." + ".".join(parts)


def is_internal(module_path: str) -> bool:
    return "_compat" in module_path or module_path.split(".")[-1].startswith("_")


def extract_docstring(node: ast.AST) -> str:
    if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) and ast.get_docstring(node):
        return ast.get_docstring(node).strip()[:500]
    return ""


def extract_re_exports(tree: ast.AST, module_path: str) -> list[dict]:
    re_exports = []
    base = module_path.rsplit(".", 1)[0] if "." in module_path else "fastapi"
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if "fastapi" in node.module or node.module.startswith("."):
                mod = node.module if not node.module.startswith(".") else (base + "." + node.module.lstrip("."))
                for alias in node.names:
                    re_exports.append({
                        "name": alias.asname or alias.name,
                        "sourceModule": mod,
                        "sourceSymbol": alias.name
                    })
    return re_exports


def extract_imports(tree: ast.AST) -> list[dict]:
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            mod = node.module
            if "fastapi" in mod or (mod.startswith(".") and "fastapi" in str(mod)):
                symbols = [a.asname or a.name for a in node.names]
                imports.append({"module": mod, "symbols": symbols})
    return imports[:20]  # cap for size


def extract_classes_and_functions(tree: ast.AST, module_path: str) -> tuple[list[dict], list[dict]]:
    classes = []
    functions = []
    if not isinstance(tree, ast.Module):
        return classes, functions
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            bases = [ast.unparse(b) if hasattr(ast, "unparse") else "" for b in node.bases][:3]
            classes.append({
                "@id": f"fastapi:class/{module_path}/{node.name}",
                "name": node.name,
                "bases": bases,
                "docstring": extract_docstring(node),
                "internal": node.name.startswith("_")
            })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append({
                "@id": f"fastapi:function/{module_path}/{node.name}",
                "name": node.name,
                "docstring": extract_docstring(node),
                "internal": node.name.startswith("_")
            })
    return classes, functions


def build_document(rel_path: Path, source: str, module_path: str, output_filename: str) -> dict:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {"@type": "Document", "modulePath": module_path, "outputFilename": output_filename, "parseError": True, "exports": [], "imports": []}

    internal = is_internal(module_path)
    role = module_path.split(".")[-1] if "." in module_path else "root"
    re_exports = extract_re_exports(tree, module_path)
    imports = extract_imports(tree)
    classes, functions = extract_classes_and_functions(tree, module_path)

    return {
        "@context": {
            "@vocab": "https://fastapi-docs.aalang.org/",
            "fastapi": "https://fastapi-docs.aalang.org/"
        },
        "@id": f"fastapi:{output_filename.replace('.jsonld','')}",
        "@type": "Document",
        "modulePath": module_path,
        "outputFilename": output_filename,
        "internal": internal,
        "role": role,
        "description": f"FastAPI module: {module_path}",
        "fastapiVersion": FASTAPI_VERSION,
        "exports": [c for c in classes if not c.get("internal")][:30] + [f for f in functions if not f.get("internal")][:20],
        "reExports": re_exports[:40],
        "imports": imports,
        "classes": classes,
        "functions": functions
    }


def main():
    manifest = {}
    failed_modules = []
    for py_path in sorted(FASTAPI_ROOT.rglob("*.py")):
        rel = py_path.relative_to(FASTAPI_ROOT)
        module_path = get_module_path(rel)
        output_filename = module_path.replace(".", "-").replace("_", "-") + ".jsonld"
        try:
            source = py_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            failed_modules.append({"module": module_path, "reason": str(e)})
            continue
        doc = build_document(rel, source, module_path, output_filename)
        if doc.get("parseError"):
            failed_modules.append({"module": module_path, "reason": "Parse error"})
            continue
        manifest[output_filename] = json.dumps(doc, indent=2, default=str)
    # Write manifest: filename -> content
    manifest_path = OUTPUT_DIR / "_translation_manifest.json"
    # Manifest as dict of filename -> content string
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=0, default=str)
    # Also write failed modules for report
    with open(OUTPUT_DIR / "_failed_modules.json", "w", encoding="utf-8") as f:
        json.dump(failed_modules, f, indent=2)
    print("Translation complete. Files:", len(manifest), "Failed:", len(failed_modules))


if __name__ == "__main__":
    main()
