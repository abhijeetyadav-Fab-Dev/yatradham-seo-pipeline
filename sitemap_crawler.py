import re
import logging
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class SitemapCrawler:
    @staticmethod
    def fetch_urls(source_url: str, max_urls: int = 100) -> Dict[str, Any]:
        source_url = source_url.strip()
        if not source_url.startswith('http://') and not source_url.startswith('https://'):
            source_url = f'https://{source_url}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

        try:
            res = requests.get(source_url, headers=headers, timeout=25)
            if res.status_code != 200:
                return {
                    'success': False,
                    'error': f'Failed to fetch {source_url} (HTTP {res.status_code})',
                    'items': []
                }
            
            content_type = res.headers.get('content-type', '').lower()
            text = res.text

            if 'xml' in content_type or text.strip().startswith('<?xml') or '<urlset' in text or '<sitemapindex' in text:
                urls = SitemapCrawler._parse_xml_sitemap(text)
            else:
                urls = SitemapCrawler._parse_html_links(text, source_url)

            clean_urls = []
            seen = set()
            ignore_patterns = [
                r'\.(jpg|jpeg|png|gif|webp|svg|pdf|css|js)$',
                r'/(wp-admin|wp-content|wp-includes|wp-json|cart|checkout|my-account|feed|tag|author)/'
            ]

            for u in urls:
                u = u.strip()
                if not u or u in seen:
                    continue
                if any(re.search(p, u, re.IGNORECASE) for p in ignore_patterns):
                    continue
                seen.add(u)
                
                inferred_cat = 'package'
                if 'wellness.' in u or 'yoga' in u or 'ayurveda' in u or 'retreat' in u or 'ashram' in u:
                    inferred_cat = 'wellness'
                elif 'temple.' in u or 'puja' in u or 'aarti' in u or 'pandit' in u:
                    inferred_cat = 'puja'
                elif 'travel.' in u or 'tour' in u or 'chardham' in u:
                    inferred_cat = 'travel'
                elif 'dharamshala' in u or 'hotel' in u or 'room' in u:
                    inferred_cat = 'stay'

                parts = [p for p in u.rstrip('/').split('/') if p]
                slug = parts[-1].replace('-', ' ').title() if parts else 'Package'

                clean_urls.append({
                    'url': u,
                    'suggested_name': slug,
                    'category': inferred_cat
                })

                if len(clean_urls) >= max_urls:
                    break

            return {
                'success': True,
                'source_url': source_url,
                'total_found': len(clean_urls),
                'items': clean_urls
            }

        except Exception as e:
            logger.error(f'Sitemap crawler error: {e}')
            return {
                'success': False,
                'error': f'Crawler failed: {str(e)}',
                'items': []
            }


    @staticmethod
    def _parse_xml_sitemap(xml_text: str, max_depth: int = 2) -> List[str]:
        urls = []
        is_index = '<sitemapindex' in xml_text or '<sitemap>' in xml_text
        try:
            clean_xml = re.sub(' xmlns=\"[^\"]+\"', '', xml_text, count=1)
            root = ET.fromstring(clean_xml)
            for loc in root.findall('.//loc'):
                if loc.text and loc.text.strip():
                    urls.append(loc.text.strip())
        except Exception:
            matches = re.findall(r'<loc>\s*(https?://[^\s<]+)\s+</loc>', xml_text, re.IGNORECASE)
            urls.extend(matches)
        
        # If this is a sitemap index containing child sitemaps (e.g., post-sitemap.xml, page-sitemap.xml), recursively fetch child URLs
        if is_index and max_depth > 0:
            nested_urls = []
            child_sitemaps = [u for u in urls if u.endswith('.xml') or 'sitemap' in u]
            for child_url in child_sitemaps[:5]:  # Process top 5 relevant sub-sitemaps
                try:
                    resp = requests.get(child_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
                    if resp.status_code == 200:
                        child_extracted = SitemapCrawler._parse_xml_sitemap(resp.text, max_depth=max_depth - 1)
                        nested_urls.extend(child_extracted)
                except Exception as e:
                    logger.warning(f"Failed to fetch nested sitemap {child_url}: {e}")
            if nested_urls:
                return nested_urls

        return urls



    @staticmethod
    def _parse_html_links(html_text: str, base_url: str) -> List[str]:
        urls = []
        parts = base_url.split('//')
        base_domain = parts[-1].split('/')[0] if len(parts) > 1 else base_url

        try:
            from scrapling.parser import Selector
            page = Selector(html_text)
            hrefs = page.css("a::attr(href)").getall()
            for href in hrefs:
                href = href.strip()
                if href.startswith('/'):
                    scheme = 'https:' if base_url.startswith('https:') else 'http:'
                    href = f'{scheme}//{base_domain}{href}'
                if href.startswith('http') and base_domain in href:
                    urls.append(href)
            if urls:
                return urls
        except Exception:
            pass

        soup = BeautifulSoup(html_text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            if href.startswith('/'):
                scheme = 'https:' if base_url.startswith('https:') else 'http:'
                href = f'{scheme}//{base_domain}{href}'
            if href.startswith('http') and base_domain in href:
                urls.append(href)

        return urls

