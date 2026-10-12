from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ASSETS = Path(__file__).resolve().parents[1] / 'skills/internet-diagnostics/assets'


class ReportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.links = []
        self.ids = set()
        self.policies = []
        self.resources = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if 'src' in attrs:
            self.resources.append(attrs['src'])
        if tag == 'link':
            self.resources.append(attrs.get('href', ''))
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'content-security-policy':
            self.policies.append(attrs['content'])
        if any(key.startswith('on') for key in attrs):
            raise AssertionError('Report cannot have executable event attributes')


class ReportTests(unittest.TestCase):
    def test_static_offline_html(self):
        for name in ['report.html', 'report-example.html']:
            text = (ASSETS / name).read_text(encoding='utf-8')
            parsed = ReportParser()
            parsed.feed(text)
            self.assertFalse(set(parsed.tags) & {'script', 'iframe', 'object', 'embed', 'form'})
            self.assertFalse(parsed.resources)
            self.assertEqual(parsed.tags.count('h1'), 1)
            self.assertIn("default-src 'none'", parsed.policies[0])
            self.assertIn("font-src data:", parsed.policies[0])
            self.assertNotIn('@import', text)
            self.assertTrue(all(url.startswith('data:font/woff2;base64,') for url in re.findall(r'url\((.*?)\)', text)))
            self.assertIn('SIL OPEN FONT LICENSE', text)
            for link in parsed.links:
                if link.startswith('#'):
                    self.assertIn(link[1:], parsed.ids)
                else:
                    self.assertTrue(link.startswith('https://'))

    def test_preview_has_no_template_markers(self):
        for name in ['report-example.html', 'report-example.md']:
            text = (ASSETS / name).read_text(encoding='utf-8')
            self.assertNotRegex(text, r'\{\{[^}]+\}\}')
            self.assertIn('fictional readings', text)


if __name__ == '__main__':
    unittest.main()
