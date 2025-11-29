#!/usr/bin/env python3
"""
Test Edge Cases for LJPW Analyzer
Tests boundary conditions, error handling, and unusual inputs
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ljpw.ljpw_standalone import analyze_file, analyze_quick, analyze_directory


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_empty_code(self):
        """Test analyzing empty code string"""
        result = analyze_quick("")
        assert result['lines'] == 0
        assert result['health'] == 0
        assert 'Empty file' in result['insights'][0]
    
    def test_none_input(self):
        """Test analyzing None input"""
        result = analyze_quick(None)
        assert 'error' in result
        assert result['error'] == 'None input'
    
    def test_invalid_type(self):
        """Test analyzing non-string input"""
        result = analyze_quick(123)
        assert 'error' in result
        assert 'Invalid type' in result['error']
    
    def test_only_comments(self):
        """Test file with only comments, no code"""
        code = """
# This is a comment
# Another comment
# More comments
"""
        result = analyze_quick(code)
        assert result['lines'] == 0
        assert 'Empty file' in result['insights'][0]
    
    def test_only_whitespace(self):
        """Test file with only whitespace"""
        code = "\n\n   \n\t\t\n   "
        result = analyze_quick(code)
        assert result['lines'] == 0
    
    def test_very_long_line(self):
        """Test code with extremely long lines"""
        code = "x = " + "1 + " * 10000 + "1"
        result = analyze_quick(code)
        assert 'ljpw' in result
        assert result['lines'] > 0
    
    def test_unicode_characters(self):
        """Test code with unicode characters"""
        code = """
def greet():
    print("Hello 世界 🌍")
    return "Success ✓"
"""
        result = analyze_quick(code)
        assert 'ljpw' in result
        assert result['lines'] > 0
    
    def test_mixed_line_endings(self):
        """Test code with mixed line endings (CRLF/LF)"""
        code = "def foo():\r\n    pass\nreturn 1"
        result = analyze_quick(code)
        assert 'ljpw' in result
        assert result['lines'] > 0
    
    def test_nested_strings(self):
        """Test code with heavily nested strings and quotes"""
        code = '''
def test():
    s1 = "He said \\"hello\\""
    s2 = 'She said "hi"'
    s3 = """triple
    quote"""
'''
        result = analyze_quick(code)
        assert 'ljpw' in result
        assert result['lines'] > 0


class TestFileEdgeCases:
    """Test file-related edge cases"""
    
    def test_nonexistent_file(self):
        """Test analyzing non-existent file"""
        result = analyze_file("/nonexistent/file.py")
        assert 'error' in result
        assert result['error'] == 'File not found'
    
    def test_directory_not_file(self, tmp_path):
        """Test analyzing directory path instead of file"""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        
        result = analyze_file(str(test_dir))
        assert 'error' in result
        assert result['error'] == 'Not a file'
    
    def test_empty_file(self, tmp_path):
        """Test analyzing empty file"""
        empty_file = tmp_path / "empty.py"
        empty_file.write_text("")
        
        result = analyze_file(str(empty_file))
        assert result['lines'] == 0
        assert result['health'] == 0
    
    def test_file_with_only_newlines(self, tmp_path):
        """Test file with only newline characters"""
        newline_file = tmp_path / "newlines.py"
        newline_file.write_text("\n\n\n\n\n")
        
        result = analyze_file(str(newline_file))
        assert result['lines'] == 0


class TestDirectoryEdgeCases:
    """Test directory analysis edge cases"""
    
    def test_empty_directory(self, tmp_path):
        """Test analyzing empty directory"""
        results = analyze_directory(str(tmp_path), show_progress=False)
        assert len(results) == 0
    
    def test_directory_with_no_code_files(self, tmp_path):
        """Test directory with only non-code files"""
        (tmp_path / "test.txt").write_text("Not code")
        (tmp_path / "data.json").write_text("{}")
        
        results = analyze_directory(str(tmp_path), show_progress=False)
        assert len(results) == 0
    
    def test_nested_directories(self, tmp_path):
        """Test analyzing nested directory structure"""
        # Create nested structure
        (tmp_path / "level1").mkdir()
        (tmp_path / "level1" / "level2").mkdir()
        (tmp_path / "level1" / "level2" / "test.py").write_text("def foo(): pass")
        
        results = analyze_directory(str(tmp_path), show_progress=False)
        assert len(results) == 1
        assert results[0]['lines'] > 0
    
    def test_nonexistent_directory(self):
        """Test analyzing non-existent directory"""
        results = analyze_directory("/nonexistent/directory", show_progress=False)
        assert len(results) == 0


class TestBoundaryValues:
    """Test boundary values and limits"""
    
    def test_minimal_code(self):
        """Test minimal valid code"""
        result = analyze_quick("x=1")
        assert 'ljpw' in result
        assert result['lines'] == 1
    
    def test_single_character(self):
        """Test single character"""
        result = analyze_quick("#")
        assert result['lines'] == 0  # Comment only
    
    def test_maximum_nesting(self):
        """Test deeply nested code"""
        code = "if True:\n" + ("    if True:\n" * 50) + "    " * 50 + "pass"
        result = analyze_quick(code)
        assert 'ljpw' in result
        assert result['lines'] > 0
    
    def test_many_functions(self):
        """Test file with many functions"""
        code = "\n".join([f"def func{i}(): pass" for i in range(1000)])
        result = analyze_quick(code)
        assert 'ljpw' in result
        assert result['health'] > 0  # Should have some wisdom score


class TestSpecialCharacters:
    """Test handling of special characters"""
    
    def test_tabs_vs_spaces(self):
        """Test code with tabs vs spaces"""
        code_spaces = "def foo():\n    pass"
        code_tabs = "def foo():\n\tpass"
        
        result_spaces = analyze_quick(code_spaces)
        result_tabs = analyze_quick(code_tabs)
        
        # Should analyze both successfully
        assert 'ljpw' in result_spaces
        assert 'ljpw' in result_tabs
    
    def test_special_regex_characters(self):
        """Test code that might break regex patterns"""
        code = """
def test():
    pattern = r"(test.*[abc]+)"
    text = "test{123}"
    if re.match(pattern, text):
        return True
"""
        result = analyze_quick(code)
        assert 'ljpw' in result
        assert result['lines'] > 0


class TestRealWorldScenarios:
    """Test realistic edge cases from actual usage"""
    
    def test_code_with_todos(self):
        """Test code with TODO comments"""
        code = """
def process():
    # TODO: Add error handling
    # FIXME: This is broken
    # HACK: Temporary solution
    pass
"""
        result = analyze_quick(code)
        assert 'ljpw' in result
        # Should have low safety score (no error handling)
        assert result['ljpw']['L'] < 0.3
    
    def test_generated_code(self):
        """Test auto-generated code patterns"""
        code = """
# Auto-generated by tool v1.0
# DO NOT EDIT

def getter_0(): return field_0
def getter_1(): return field_1
def getter_2(): return field_2
"""
        result = analyze_quick(code)
        assert 'ljpw' in result
    
    def test_minified_code(self):
        """Test minified/compressed code"""
        code = "def f(x):return x*2 if x>0 else 0"
        result = analyze_quick(code)
        assert 'ljpw' in result
        assert result['lines'] == 1


def test_all_edge_cases():
    """Run all edge case tests"""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    test_all_edge_cases()
