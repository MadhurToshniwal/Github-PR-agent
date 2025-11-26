import pytest
from app.services.github_service import DiffParser


def test_diff_parser_initialization():
    """Test DiffParser initialization"""
    parser = DiffParser()
    assert parser is not None


def test_parse_simple_diff():
    """Test parsing a simple diff"""
    diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1,3 +1,3 @@
 def hello():
-    print("Hello")
+    print("Hello World")
     return
"""
    
    parser = DiffParser()
    changes = parser.parse_diff(diff)
    
    assert len(changes) > 0
    assert 'filename' in changes[0]
    assert changes[0]['filename'] == 'test.py'


def test_detect_language_python():
    """Test Python language detection"""
    assert DiffParser._detect_language("test.py") == "python"
    assert DiffParser._detect_language("module/__init__.py") == "python"


def test_detect_language_javascript():
    """Test JavaScript language detection"""
    assert DiffParser._detect_language("app.js") == "javascript"
    assert DiffParser._detect_language("component.jsx") == "javascript"


def test_detect_language_typescript():
    """Test TypeScript language detection"""
    assert DiffParser._detect_language("app.ts") == "typescript"
    assert DiffParser._detect_language("component.tsx") == "typescript"


def test_detect_language_unknown():
    """Test unknown language detection"""
    result = DiffParser._detect_language("file.xyz")
    assert result is None


def test_extract_changed_lines():
    """Test extracting changed lines from patch"""
    patch = """@@ -10,6 +10,7 @@ def function():
     line1
     line2
+    new_line
     line3
-    old_line
     line4
"""
    
    parser = DiffParser()
    lines = parser.extract_changed_lines_with_context(patch)
    
    assert len(lines) > 0
    
    # Check for added line
    added = [l for l in lines if l[1] == 'added']
    assert len(added) > 0
    
    # Check for removed line
    removed = [l for l in lines if l[1] == 'removed']
    assert len(removed) > 0
