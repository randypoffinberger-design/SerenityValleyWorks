"""Run with python -m unittest discover -s tests. No third-party dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.tags = []
        self.ids = []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {p.resolve(): Page(p) for p in ROOT.rglob('*.html')}

    def test_local_links_assets_and_fragments(self):
        for path, page in self.pages.items():
            self.assertEqual(len(page.ids), len(set(page.ids)), str(path))
            for tag, attrs in page.tags:
                for field in ('href', 'src'):
                    raw = attrs.get(field)
                    if not raw:
                        continue
                    url = urlsplit(raw)
                    if url.scheme or url.netloc:
                        continue
                    target = ((ROOT / url.path.lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)).resolve() if url.path else path
                    if target.is_dir():
                        target /= 'index.html'
                    self.assertTrue(target.is_file(), f'{path.relative_to(ROOT)}: {raw}')
                    if url.fragment and target in self.pages:
                        self.assertIn(unquote(url.fragment), self.pages[target].ids, f'{path.name}: {raw}')

    def test_brand_share_metadata(self):
        for path, page in self.pages.items():
            metadata = {a.get('property', a.get('name')): a.get('content') for tag, a in page.tags if tag == 'meta'}
            for field in ['description', 'og:title', 'og:description', 'og:url', 'og:image', 'og:image:alt', 'twitter:image']:
                self.assertTrue(metadata.get(field), f'{path.name}: {field}')
            expected = 'mtm-icon.png' if 'morethanmeasured' in path.parts else 'sk-icon.png' if 'serenitykitchen' in path.parts else 'svw-logo.jpeg'
            self.assertTrue(metadata['og:image'].endswith('/'+expected))
            self.assertEqual(metadata['og:image'], metadata['twitter:image'])
            self.assertTrue(metadata['og:url'].startswith('https://serenityvalleyworks.com/'))

    def test_mtm_accessibility_and_static_content(self):
        pages = [p for p in self.pages.values() if 'morethanmeasured' in p.path.parts]
        self.assertEqual(len(pages), 15)
        for page in pages:
            tags = page.tags
            self.assertEqual(sum(t == 'h1' for t, a in tags), 1, page.path.name)
            self.assertEqual(sum(t == 'main' for t, a in tags), 1, page.path.name)
            self.assertEqual(sum(t == 'a' and a.get('aria-current') == 'page' for t, a in tags), 1)
            self.assertIn('main', page.ids)
            self.assertTrue(any(t == 'link' and a.get('href','').endswith('mtm-theme.css') for t, a in tags))
            self.assertFalse(any(t == 'script' and a.get('src','').endswith('/script.js') for t, a in tags))
        resources = (ROOT/'morethanmeasured/resources.html').read_text(encoding='utf-8')
        self.assertEqual(resources.count('class="article-card '), 10)
        self.assertEqual(len(list((ROOT/'morethanmeasured/articles').glob('*.html'))), 10)

    def test_released_and_prelaunch_downloads(self):
        for app in ['morethanmeasured', 'serenitykitchen']:
            page = self.pages[(ROOT/app/'index.html').resolve()]
            sections = [a for t, a in page.tags if 'data-app-downloads' in a]
            self.assertEqual(len(sections), 1)
            self.assertEqual('hidden' in sections[0], app == 'serenitykitchen')
            controls = [a for t, a in page.tags if 'data-store' in a]
            self.assertEqual({a['data-store'] for a in controls}, {'apple','google','windows'})
            for control in controls:
                if app == 'morethanmeasured' and control['data-store'] in ('windows', 'google'):
                    expected = {'windows': 'https://apps.microsoft.com/detail/9pbh50v7gsc1', 'google': 'https://play.google.com/store/apps/details?id=com.serenityvalleyworks.morethanmeasured'}
                    self.assertEqual(control.get('href'), expected[control['data-store']])
                    self.assertNotIn('hidden', control)
                    self.assertNotIn('aria-disabled', control)
                    continue
                if app == 'morethanmeasured':
                    self.assertIn('hidden', control)
                self.assertNotIn('href', control)
                self.assertEqual(control.get('aria-disabled'), 'true')

    def test_mtm_onboarding_information(self):
        text = (ROOT/'morethanmeasured/index.html').read_text(encoding='utf-8')
        for phrase in ['Try the web app', 'No automatic charge', '$12.99/month', '$99.99/year', 'Create or join a household', 'Verify your email', 'Babysitter registration is free', 'fictional test information']:
            self.assertIn(phrase, text)
        for image in ['mtm-first-task-phone.png', 'mtm-care-phone.png']:
            self.assertIn(image, text)
            self.assertTrue((ROOT/'assets'/image).is_file())
        self.assertNotIn('tail96598f', text)
        self.assertNotIn('trycloudflare', text)
        self.assertNotIn('still in development', text)
        self.assertIn("awaiting Apple's approval", text)

    def test_product_directory(self):
        page = self.pages[(ROOT/'morethanmeasured/product-links.html').resolve()]
        self.assertEqual(len({attrs['data-product-id'] for tag, attrs in page.tags if tag == 'li' and 'data-product-id' in attrs}), 147)
        self.assertEqual(sum(tag == 'section' and attrs.get('class') == 'directory-section' for tag, attrs in page.tags), 6)
        self.assertEqual(sum(tag == 'section' and attrs.get('class') == 'directory-subgroup' for tag, attrs in page.tags), 11)
        text = page.path.read_text(encoding='utf-8')
        self.assertIn('Sensory Support <span class="category-count">(78)</span>', text)
        for name in ['Swings &amp; Suspended Equipment', 'Balls &amp; Balance', 'Balance &amp; Climbing', 'Active Movement', 'Positioning &amp; Resistance', 'Tactile Exploration', 'Clothing &amp; Bedding', 'Sound &amp; Headphones', 'Visual &amp; Calm Spaces', 'Oral Care', 'Books &amp; Learning']:
            self.assertIn(name, text)
        self.assertIn('product-search', page.ids)
        for other in self.pages.values():
            if 'morethanmeasured' in other.path.parts:
                self.assertTrue(any(tag == 'a' and attrs.get('href', '').endswith('product-links.html') for tag, attrs in other.tags), str(other.path))

    def test_no_affiliate_claims_or_tags(self):
        for path in self.pages:
            text = path.read_text(encoding='utf-8')
            self.assertNotIn('As an Amazon Associate I earn', text)
            for link in re.findall(r'href="([^"]+)"', text):
                self.assertNotRegex(link, r'[?&](tag|ascsubtag|linkCode)=')
        self.assertIn('not currently an Amazon Associate or affiliate', (ROOT/'morethanmeasured/products.html').read_text(encoding='utf-8'))

if __name__ == '__main__':
    unittest.main()
