#!/usr/bin/env python3
"""
Whitelist filtering utility for blocklist processing.

This module provides functionality to filter blocklist entries against a whitelist,
supporting various host file formats and subdomain matching.
"""

import os
from typing import List, Set, Optional


class WhitelistFilter:
    """
    A utility class for filtering blocklist entries against a whitelist.

    Supports standard host file formats:
    - 0.0.0.0 domain.com
    - 127.0.0.1 domain.com
    - domain.com (plain)

    Features subdomain matching where subdomains are filtered if parent domain is whitelisted.
    """

    def __init__(self):
        self.exact_domains: Set[str] = set()
        self.wildcard_domains: Set[str] = set()
        # Keep original whitelist for backward compatibility
        self.whitelist: Set[str] = set()
        
    def load_whitelist(self, path: str) -> bool:
        """
        Load whitelist domains from file.

        Args:
            path: Path to whitelist file

        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.exact_domains = set()
                self.wildcard_domains = set()
                self.whitelist = set()

                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Clean up domain entry
                        domain = line.strip('"').lower()
                        if domain:
                            self.whitelist.add(domain)
                            if domain.startswith('*.'):
                                # Wildcard domain - store the base domain
                                base_domain = domain[2:]
                                if base_domain:
                                    self.wildcard_domains.add(base_domain)
                            else:
                                # Exact domain
                                self.exact_domains.add(domain)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False
    
    def should_filter_domain(self, domain: str) -> bool:
        """
        Check if domain should be filtered based on whitelist.

        Performs exact match and wildcard matching against whitelist entries.

        Args:
            domain: Domain to check

        Returns:
            True if domain should be filtered (is whitelisted), False otherwise
        """
        if not domain or (not self.exact_domains and not self.wildcard_domains):
            return False

        domain = domain.lower()

        # Check exact match - O(1) lookup
        if domain in self.exact_domains:
            return True

        # Check wildcard matching - O(k) where k = number of domain parts
        if self.wildcard_domains:
            # Check if the domain itself is a wildcard base domain
            if domain in self.wildcard_domains:
                return True

            # Check parent domains for wildcard matches
            # For "sub.example.com", check "example.com", "com"
            parts = domain.split('.')
            for i in range(1, len(parts)):
                parent_domain = '.'.join(parts[i:])
                if parent_domain in self.wildcard_domains:
                    return True

        return False
    
    def filter_blocklist_line(self, line: str) -> Optional[str]:
        """
        Parse and filter a single blocklist line.
        
        Args:
            line: Raw line from blocklist
            
        Returns:
            Original line if not filtered, None if filtered out
        """
        line = line.strip()
        
        # Keep empty lines and comments
        if not line or line.startswith('#'):
            return line
            
        # Extract domain from various formats
        domain = self._extract_domain(line)
        
        # Filter if domain is whitelisted
        if domain and self.should_filter_domain(domain):
            return None
            
        return line
    
    def _extract_domain(self, line: str) -> str:
        """
        Extract domain from various host file formats.
        
        Args:
            line: Line from blocklist
            
        Returns:
            Extracted domain, empty string if not found
        """
        line = line.strip()
        domain = ""
        
        # Handle uBlock Origin format: ||domain.com^ or ||domain.com^$options
        if line.startswith("||"):
            # Find the end of the domain part
            end_pos = line.find("^", 2)  # Start search after ||
            if end_pos != -1:
                domain = line[2:end_pos]  # Extract between || and ^
            else:
                domain = line[2:]  # No ^ found, take everything after ||
        else:
            # Handle standard host file formats
            parts = line.split()
            
            if len(parts) >= 2:
                # Format: "0.0.0.0 domain.com" or "127.0.0.1 domain.com"
                domain = parts[1]
            elif len(parts) == 1:
                # Format: "domain.com"
                domain = parts[0]
                
        # Clean up domain
        domain = domain.strip().lower()
        
        # Remove common prefixes/suffixes
        if domain.startswith("*."):
            domain = domain[2:]
            
        return domain
    
    def filter_blocklist_file(self, input_path: str, output_path: Optional[str] = None) -> tuple[int, int]:
        """
        Filter an entire blocklist file.
        
        Args:
            input_path: Path to input blocklist file
            output_path: Path to output filtered file (defaults to input_path)
            
        Returns:
            Tuple of (original_count, filtered_count)
        """
        if output_path is None:
            output_path = input_path
            
        filtered_lines = []
        original_count = 0
        filtered_count = 0
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                for line in f:
                    original_count += 1
                    filtered_line = self.filter_blocklist_line(line)
                    
                    if filtered_line is None:
                        filtered_count += 1
                    else:
                        filtered_lines.append(filtered_line + '\n' if filtered_line else '\n')
                        
            # Write filtered content
            with open(output_path, 'w', encoding='utf-8') as f:
                for line in filtered_lines:
                    f.write(line)
                    
            return original_count, filtered_count
            
        except Exception:
            return 0, 0


if __name__ == "__main__":
    import unittest
    import tempfile
    import os
    
    class TestWhitelistFilter(unittest.TestCase):
        """Test cases for WhitelistFilter functionality."""
        
        def setUp(self):
            """Set up test fixtures."""
            self.filter = WhitelistFilter()
            
            # Test whitelist
            self.test_whitelist = [
                "adapty.io",
                "example.com", 
                "google.com",
                "*.blokada.org"
            ]
            
            # Create temporary whitelist file
            self.whitelist_fd, self.whitelist_path = tempfile.mkstemp()
            with os.fdopen(self.whitelist_fd, 'w') as f:
                for domain in self.test_whitelist:
                    f.write(f"{domain}\n")
                    
        def tearDown(self):
            """Clean up test fixtures."""
            if os.path.exists(self.whitelist_path):
                os.unlink(self.whitelist_path)
                
        def test_load_whitelist(self):
            """Test whitelist loading."""
            self.assertTrue(self.filter.load_whitelist(self.whitelist_path))
            self.assertEqual(len(self.filter.whitelist), 4)
            self.assertIn("adapty.io", self.filter.whitelist)
            self.assertIn("example.com", self.filter.whitelist)
            self.assertIn("*.blokada.org", self.filter.whitelist)
            
        def test_load_nonexistent_whitelist(self):
            """Test loading nonexistent whitelist file."""
            self.assertFalse(self.filter.load_whitelist("/nonexistent/path"))
            
        def test_domain_extraction(self):
            """Test domain extraction from various formats."""
            test_cases = [
                ("0.0.0.0 track.adapty.io", "track.adapty.io"),
                ("127.0.0.1 example.com", "example.com"),
                ("google.com", "google.com"),
                ("   malware.site   ", "malware.site"),
                ("*.wildcard.com", "wildcard.com"),
                # uBlock Origin format tests (should fail initially)
                ("||adapty.io^", "adapty.io"),
                ("||track.adapty.io^", "track.adapty.io"),
                ("||example.com^$third-party", "example.com"),
            ]
            
            for line, expected in test_cases:
                with self.subTest(line=line):
                    domain = self.filter._extract_domain(line)
                    self.assertEqual(domain, expected)
                    
        def test_should_filter_domain_exact_match(self):
            """Test exact domain matching."""
            self.filter.load_whitelist(self.whitelist_path)
            
            self.assertTrue(self.filter.should_filter_domain("adapty.io"))
            self.assertTrue(self.filter.should_filter_domain("ADAPTY.IO"))  # Case insensitive
            self.assertFalse(self.filter.should_filter_domain("malware.com"))
            
        def test_should_filter_domain_exact_match_only(self):
            """Test exact domain matching (no subdomain matching by default)."""
            self.filter.load_whitelist(self.whitelist_path)
            
            # Subdomains should NOT match parent domain (exact matching)
            self.assertFalse(self.filter.should_filter_domain("track.adapty.io"))
            self.assertFalse(self.filter.should_filter_domain("api.example.com"))
            self.assertFalse(self.filter.should_filter_domain("www.google.com"))
            self.assertFalse(self.filter.should_filter_domain("subdomain.test.google.com"))
            
            # Non-matching domains
            self.assertFalse(self.filter.should_filter_domain("notgoogle.com"))
            self.assertFalse(self.filter.should_filter_domain("example.net"))
            
        def test_should_filter_domain_wildcard_match(self):
            """Test wildcard domain matching."""
            self.filter.load_whitelist(self.whitelist_path)
            
            # Wildcard matching should work for *.blokada.org
            self.assertTrue(self.filter.should_filter_domain("blokada.org"))  # Exact match
            self.assertTrue(self.filter.should_filter_domain("api.blokada.org"))  # Subdomain
            self.assertTrue(self.filter.should_filter_domain("www.blokada.org"))  # Subdomain
            self.assertTrue(self.filter.should_filter_domain("sub.domain.blokada.org"))  # Deep subdomain
            
            # Should not match different domains
            self.assertFalse(self.filter.should_filter_domain("notblokada.org"))
            self.assertFalse(self.filter.should_filter_domain("blokada.com"))
            
        def test_filter_blocklist_line(self):
            """Test filtering individual lines."""
            self.filter.load_whitelist(self.whitelist_path)
            
            # Lines that should be filtered (return None)
            self.assertIsNone(self.filter.filter_blocklist_line("0.0.0.0 adapty.io"))
            self.assertIsNone(self.filter.filter_blocklist_line("google.com"))  # Exact match
            # uBlock format should be filtered
            self.assertIsNone(self.filter.filter_blocklist_line("||adapty.io^"))
            
            # Lines that should pass through (exact domain matching)
            self.assertEqual(self.filter.filter_blocklist_line("track.adapty.io"), "track.adapty.io")  # subdomain should NOT be filtered
            self.assertEqual(self.filter.filter_blocklist_line("0.0.0.0 malware.com"), "0.0.0.0 malware.com")
            self.assertEqual(self.filter.filter_blocklist_line("# Comment"), "# Comment")
            self.assertEqual(self.filter.filter_blocklist_line(""), "")
            
        def test_filter_blocklist_file(self):
            """Test filtering entire blocklist file."""
            self.filter.load_whitelist(self.whitelist_path)
            
            # Create test blocklist
            test_blocklist = [
                "# Test blocklist",
                "0.0.0.0 adapty.io",
                "127.0.0.1 track.adapty.io", 
                "0.0.0.0 malware.com",
                "badsite.net",
                "google.com",  # Exact match - will be filtered
                "",
                "# End of file"
            ]
            
            # Write test file
            input_fd, input_path = tempfile.mkstemp()
            try:
                with os.fdopen(input_fd, 'w') as f:
                    for line in test_blocklist:
                        f.write(f"{line}\n")
                        
                # Filter the file
                original_count, filtered_count = self.filter.filter_blocklist_file(input_path)
                
                # Verify counts
                self.assertEqual(original_count, 8)  # Total lines
                self.assertEqual(filtered_count, 2)  # adapty.io, google.com (track.adapty.io NOT filtered)
                
                # Verify filtered content
                with open(input_path, 'r') as f:
                    filtered_lines = f.readlines()
                    
                # Should contain: comment, track.adapty.io, malware.com, badsite.net, empty line, end comment
                self.assertEqual(len(filtered_lines), 6)
                self.assertIn("malware.com", ''.join(filtered_lines))
                self.assertIn("badsite.net", ''.join(filtered_lines))
                self.assertIn("track.adapty.io", ''.join(filtered_lines))  # Should NOT be filtered
                self.assertNotIn("0.0.0.0 adapty.io", ''.join(filtered_lines))  # Should be filtered
                self.assertNotIn("google.com", ''.join(filtered_lines))  # Should be filtered
                
            finally:
                if os.path.exists(input_path):
                    os.unlink(input_path)
                    
        def test_edge_cases(self):
            """Test edge cases and malformed input."""
            self.filter.load_whitelist(self.whitelist_path)
            
            # Empty/whitespace lines
            self.assertEqual(self.filter.filter_blocklist_line("   "), "")
            self.assertEqual(self.filter.filter_blocklist_line("\t"), "")
            
            # Malformed lines
            self.assertEqual(self.filter.filter_blocklist_line("invalid line format"), "invalid line format")
            
            # Empty domain extraction
            self.assertEqual(self.filter._extract_domain(""), "")
            self.assertEqual(self.filter._extract_domain("   "), "")

    class TestManualWhitelistEntries(unittest.TestCase):
        """Regression guards for individual whitelist-manual entries.

        Loads the real whitelist-manual, so a dropped line fails `make test`,
        which `make sync` runs before regenerating the mirrors.
        """

        def setUp(self):
            self.filter = WhitelistFilter()
            manual = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "whitelist-manual"
            )
            self.assertTrue(self.filter.load_whitelist(manual), f"missing {manual}")

        def test_google_cloud_monitoring_is_whitelisted(self):
            """blocklist/tracking sinkholes the Cloud Monitoring API frontend."""
            self.assertTrue(
                self.filter.should_filter_domain("monitoring.clients6.google.com")
            )

        def test_google_ad_endpoints_stay_blocked(self):
            """A wildcard entry would unblock these too, so keep it exact."""
            for domain in (
                "ogads-pa.clients6.google.com",
                "adsmarketingfrontend-pa.clients6.google.com",
                "googleads.g.doubleclick.net",
            ):
                with self.subTest(domain=domain):
                    self.assertFalse(self.filter.should_filter_domain(domain))

    # Run tests
    unittest.main()