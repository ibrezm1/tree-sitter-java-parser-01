
from tree_sitter import Language, Parser, Node
from typing import Dict, Any, Optional

# Language-specific imports
import tree_sitter_java as tsjava
# import tree_sitter_c_sharp as tscs  # Uncomment when c# is needed

LANGUAGES = {
    "java": Language(tsjava.language()),
    # "csharp": Language(tscs.language()), # Uncomment when c# is needed
}

def init_parser(language: str) -> Parser:
    """Initialize tree-sitter parser for a given language."""
    if language not in LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")
    
    parser = Parser(LANGUAGES[language])
    return parser

def parse_source(source: str, language: str) -> Dict[str, Any]:
    """
    Parse source code with tree-sitter and extract elements based on the language.
    """
    parser = init_parser(language)
    tree = parser.parse(bytes(source, "utf8"))
    root_node = tree.root_node
    
    elements = {
        "classes": [],
        "methods": [],
        "imports": [],
        "method_calls": []
    }
    
    # Language-specific extraction logic can be added here
    if language == "java":
        extract_imports(root_node, source, elements)
        extract_classes_and_methods(root_node, source, elements)
        extract_method_calls(root_node, source, elements)
    # Add elif for other languages like csharp
    
    return elements

def extract_imports(node: Node, source: str, elements: Dict[str, Any]) -> None:
    """Extract import statements from the AST."""
    for child in node.children:
        if child.type == "import_declaration":
            import_text = get_node_text(child, source)
            import_path = import_text.replace("import", "").replace(";", "").strip()
            if import_path.startswith("static "):
                import_path = import_path.replace("static ", "").strip()
            elements["imports"].append(import_path)
        
        extract_imports(child, source, elements)

def extract_classes_and_methods(node: Node, source: str, elements: Dict[str, Any]) -> None:
    """Extract class and interface declarations along with their methods."""
    if node.type in ["class_declaration", "interface_declaration", "enum_declaration"]:
        cls_name = None
        
        for child in node.children:
            if child.type == "identifier":
                cls_name = get_node_text(child, source)
                break
        
        if cls_name:
            cls_code = get_node_text(node, source)
            elements["classes"].append({
                "name": cls_name,
                "code": cls_code,
                "node": node
            })
            
            extract_methods_from_class(node, cls_name, source, elements)
    
    for child in node.children:
        extract_classes_and_methods(child, source, elements)

def extract_methods_from_class(class_node: Node, cls_name: str, source: str, elements: Dict[str, Any]) -> None:
    """Extract method declarations from a class or interface."""
    for child in class_node.children:
        if child.type in ["class_body", "interface_body", "enum_body"]:
            for member in child.children:
                if member.type == "method_declaration":
                    method_name = None
                    
                    for mchild in member.children:
                        if mchild.type == "identifier":
                            method_name = get_node_text(mchild, source)
                            break
                    
                    if method_name:
                        method_code = get_node_text(member, source)
                        full_method_id = f"{cls_name}.{method_name}"
                        elements["methods"].append({
                            "class": cls_name,
                            "name": method_name,
                            "id": full_method_id,
                            "code": method_code,
                            "node": member
                        })
                elif member.type == "constructor_declaration":
                    method_name = None
                    for mchild in member.children:
                        if mchild.type == "identifier":
                            method_name = get_node_text(mchild, source)
                            break
                    
                    if method_name:
                        method_code = get_node_text(member, source)
                        full_method_id = f"{cls_name}.{method_name}"
                        elements["methods"].append({
                            "class": cls_name,
                            "name": method_name,
                            "id": full_method_id,
                            "code": method_code,
                            "node": member
                        })

def extract_method_calls(node: Node, source: str, elements: Dict[str, Any]) -> None:
    """Extract method invocations (method calls) from the AST."""
    if node.type == "method_invocation":
        method_name = None
        qualifier = None
        
        for child in node.children:
            if child.type == "identifier":
                method_name = get_node_text(child, source)
            elif child.type == "field_access":
                qualifier = get_node_text(child, source)
            elif child.type in ["this", "super"]:
                qualifier = child.type
        
        if not method_name:
            for child in node.children:
                if child.type == "identifier":
                    method_name = get_node_text(child, source)
                    break
        
        if method_name:
            caller = find_enclosing_method_or_class(node, source)
            
            elements["method_calls"].append({
                "caller": caller,
                "call": method_name,
                "qualifier": qualifier,
                "node": node
            })
    
    for child in node.children:
        extract_method_calls(child, source, elements)

def get_node_text(node: Node, source: str) -> str:
    """Extract the source text for a given node."""
    return source[node.start_byte:node.end_byte]

def find_enclosing_method_or_class(node: Node, source: str) -> Optional[str]:
    """
    Find the name of the enclosing method or class for a given node.
    Traverses up the tree to find the nearest method or class declaration.
    """
    current = node.parent
    
    while current is not None:
        if current.type in ["method_declaration", "constructor_declaration"]:
            for child in current.children:
                if child.type == "identifier":
                    text = child.text
                    return text.decode("utf8") if isinstance(text, bytes) else text
        
        elif current.type in ["class_declaration", "interface_declaration", "enum_declaration"]:
            for child in current.children:
                if child.type == "identifier":
                    text = child.text
                    return text.decode("utf8") if isinstance(text, bytes) else text
        
        current = current.parent
    
    return None
