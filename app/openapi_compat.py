"""Convert Pydantic v2 / OpenAPI 3.1 schemas to 3.0.3 compatible."""
from typing import Any, Dict


def _walk(node: Any) -> Any:
    """Recursively transform OpenAPI 3.1 constructs to 3.0.x."""
    if isinstance(node, list):
        return [_walk(x) for x in node]
    if not isinstance(node, dict):
        return node

    # anyOf: [X, {type: null}] -> X + nullable: true
    if "anyOf" in node and isinstance(node["anyOf"], list):
        variants = node["anyOf"]
        null_variants = [v for v in variants if isinstance(v, dict) and v.get("type") == "null"]
        non_null = [v for v in variants if not (isinstance(v, dict) and v.get("type") == "null")]
        if null_variants and non_null:
            if len(non_null) == 1:
                merged = dict(non_null[0])
                merged["nullable"] = True
                # preserve extras from parent
                for k, v in node.items():
                    if k != "anyOf":
                        merged.setdefault(k, v)
                return _walk(merged)
            else:
                node["anyOf"] = [_walk(v) for v in non_null]
                node["nullable"] = True
                return node

    # type: [X, "null"] -> type: X + nullable: true
    t = node.get("type")
    if isinstance(t, list):
        if "null" in t:
            others = [x for x in t if x != "null"]
            if len(others) == 1:
                node["type"] = others[0]
                node["nullable"] = True
            else:
                node.pop("type")
                node["nullable"] = True
                node["anyOf"] = [{"type": x} for x in others]

    # drop 3.1-only keywords
    for k in ("examples", "const", "prefixItems", "$comment"):
        node.pop(k, None)

    # Recurse
    for k, v in list(node.items()):
        node[k] = _walk(v)
    return node


def to_3_0_3(spec: Dict[str, Any]) -> Dict[str, Any]:
    spec["openapi"] = "3.0.3"
    spec.pop("servers", None)
    spec.pop("webhooks", None)
    if "jsonSchemaDialect" in spec:
        spec.pop("jsonSchemaDialect")
    return _walk(spec)
