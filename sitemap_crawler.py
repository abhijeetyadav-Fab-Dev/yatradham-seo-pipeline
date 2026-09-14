import re
import gzip
import logging
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# System, utility, and non-content paths to exclude from crawling
EXCLUDE_PATH_PATTERNS = [
    r'\.(jpg|jpeg|png|gif|webp|svg|ico|pdf|css|js|woff|woff2|ttf|eot|mp4|avi|mov|zip|tar|gz)$',
    r'/(wp-admin|wp-content|wp-includes|wp-json|cart|checkout|my-account|feed|tag|author|comments)/',
    r'/(customers_otp|account/login|account/register|account/forgotpassword|customer/account)/',
    r'/(privacy-policy|terms-and-conditions|user-agreement|disclaimer|cookie-restriction)/',
    r'/(contacts?|about-us|about|careers|jobs|why-choose-us|group-inquiry|travel-agents)/',
    r'/(listing/add-property|customer-reviews)/',
    r'/cdn-cgi/',
]

EXCLUDE_DOMAINS = {
    'facebook.com', 'www.facebook.com',
    'twitter.com', 'www.twitter.com',
    'x.com', 'www.x.com',
    'instagram.com', 'www.instagram.com',
    'pinterest.com', 'in.pinterest.com', 'www.pinterest.com',
    'youtube.com', 'www.youtube.com',
    'linkedin.com', 'www.linkedin.com',
    'whatsapp.com', 'api.whatsapp.com', 'web.whatsapp.com',
}

class SitemapCrawler:
    @staticmethod
    def fetch_urls(source_url: str, max_urls: int = 100) -> Dict[str, Any]:
        """
        Crawls an XML Sitemap (single or index, including .gz) or an HTML Category Hub.
        Extracts, classifies, and ranks high-value package, stay, puja, and wellness links.
        """
        source_url = source_url.strip()
        if not source_url.startswith('http://') and not source_url.startswith('https://'):
            source_url = f'https://{source_url}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
        }

        try:
            res = requests.get(source_url, headers=headers, timeout=25, allow_redirects=True)
            if res.status_code != 200:
                return {
                    'success': False,
                    'error': f'Failed to fetch {source_url} (HTTP {res.status_code})',
                    'items': []
                }

            # Decompress gzip payload if present
            if res.content[:2] == b'\x1f\x8b':
                try:
                    text = gzip.decompress(res.content).decode('utf-8', errors='replace')
                except Exception:
                    text = res.text
            else:
                text = res.text

            content_type = res.headers.get('content-type', '').lower()
            is_xml = (
                'xml' in content_type 
                or source_url.endswith('.xml') 
                or source_url.endswith('.xml.gz')
                or text.strip().startswith('<?xml') 
                or '<urlset' in text 
                or '<sitemapindex' in text
            )

            if is_xml:
                raw_items = SitemapCrawler._parse_xml_sitemap(text, source_url)
            else:
                raw_items = SitemapCrawler._parse_html_links(text, source_url)

            parsed_src = urlparse(source_url)
            src_norm = f"{parsed_src.scheme}://{parsed_src.netloc}{parsed_src.path.rstrip('/')}"

            clean_urls = []
            seen = set()

            for item in raw_items:
                u = item['url'].strip()
                if not u:
                    continue

                # Strip anchor hashes
                u = u.split('#')[0]

                p = urlparse(u)
                if not p.scheme or not p.netloc:
                    continue

                domain = p.netloc.lower()
                if domain in EXCLUDE_DOMAINS:
                    continue

                # Ignore root homepages with no path
                if p.path in ('', '/'):
                    continue

                norm_u = f"{p.scheme}://{p.netloc}{p.path.rstrip('/')}"
                # Ignore the crawled source URL itself
                if norm_u == src_norm:
                    continue

                if norm_u in seen:
                    continue

                if any(re.search(pat, u, re.IGNORECASE) for pat in EXCLUDE_PATH_PATTERNS):
                    continue

                seen.add(norm_u)

                category = SitemapCrawler._infer_category(u, item.get('anchor_text', ''))
                suggested_name = item.get('anchor_text') or SitemapCrawler._generate_title_from_url(u)
                score = SitemapCrawler._calculate_relevance_score(u)

                clean_urls.append({
                    'url': u,
                    'suggested_name': suggested_name,
                    'category': category,
                    '_score': score
                })

            # Sort by relevance score descending so best package & stay links appear first
            clean_urls.sort(key=lambda x: x['_score'], reverse=True)

            final_items = []
            for item in clean_urls[:max_urls]:
                del item['_score']
                final_items.append(item)

            return {
                'success': True,
                'source_url': source_url,
                'total_found': len(final_items),
                'items': final_items
            }

        except Exception as e:
            logger.error(f'Sitemap crawler error on {source_url}: {e}', exc_info=True)
            return {
                'success': False,
                'error': f'Crawler error: {str(e)}',
                'items': []
            }

    @staticmethod
    def _calculate_relevance_score(url: str) -> int:
        """Prioritizes bookable pilgrimage packages, destination stays, pujas, and retreats."""
        u = url.lower()
        score = 0
        if '/package/' in u or 'chardham-package' in u or '-tour-package' in u:
            score += 50
        if '/yatradham-destinations/' in u:
            score += 45
        if any(w in u for w in ['dharamshala', 'hotel', 'ashram', 'bhavan', 'room']):
            score += 40
        if '/puja' in u or '/pandit' in u:
            score += 35
        if any(w in u for w in ['wellness', 'retreat', 'yoga', 'ayurveda']):
            score += 35
        if any(w in u for w in ['travel.yatradham.org', 'temple.yatradham.org', 'wellness.yatradham.org']):
            score += 20
        if 'blog.yatradham.org' in u or '/blog/' in u:
            score += 5
        return score

    @staticmethod
    def _infer_category(url: str, text: str = "") -> str:
        """Accurately classifies discovered links into stay, tour, wellness, or puja."""
        try:
            from scraper import detect_url_category
            cat = detect_url_category(url, text)
            if cat in ('wellness', 'tour', 'stay', 'puja'):
                if 'yatradham-destinations' in url.lower() and cat == 'tour':
                    return 'stay'
                return cat
        except Exception:
            pass

        u = url.lower()
        if 'wellness.' in u or any(w in u for w in ['yoga', 'ayurveda', 'retreat', 'naturopathy', 'detox']):
            return 'wellness'
        if 'temple.' in u or any(w in u for w in ['puja', 'pandit', 'aarti', 'darshan']):
            return 'puja'
        if 'yatradham-destinations' in u or any(w in u for w in ['dharamshala', 'hotel', 'room', 'ashram', 'bhavan', 'guest-house', 'trh', 'gmvn']):
            return 'stay'
        if 'travel.' in u or any(w in u for w in ['package', 'tour', 'yatra', 'chardham']):
            return 'tour'
        return 'tour'

    @staticmethod
    def _generate_title_from_url(url: str) -> str:
        """Derives a clean human-readable title from URL segments when anchor text is absent."""
        p = urlparse(url)
        path = p.path.strip('/')
        if not path:
            return 'Package'
        
        # Remove file extensions
        path = re.sub(r'\.(html?|php|aspx?)$', '', path, flags=re.IGNORECASE)
        parts = [part for part in path.split('/') if part]
        if not parts:
            return 'Package'
        
        # Format destinations: /yatradham-destinations/{state}/{city}
        if len(parts) >= 3 and parts[0] == 'yatradham-destinations':
            state = parts[1].replace('-', ' ').title()
            city = parts[2].replace('-', ' ').title()
            return f"{city}, {state}"
        elif len(parts) == 2 and parts[0] == 'yatradham-destinations':
            return f"{parts[1].replace('-', ' ').title()} Dharamshala & Stays"
        
        last_seg = parts[-1].replace('-', ' ').title()
        return last_seg

    @staticmethod
    def _parse_xml_sitemap(xml_text: str, source_url: str, max_depth: int = 2) -> List[Dict[str, str]]:
        """Parses XML sitemaps with namespace stripping, index recursing, and regex fallback."""
        discovered = []
        is_index = ('<sitemapindex' in xml_text or '<sitemap>' in xml_text)

        # Strip XML namespaces for robust ElementTree parsing
        clean_xml = re.sub(r'\s+xmlns(?::[a-zA-Z0-9_-]+)?=[\'"][^\'"]*[\'"]', '', xml_text)
        
        et_urls = []
        try:
            root = ET.fromstring(clean_xml)
            for loc in root.findall('.//loc'):
                if loc.text and loc.text.strip():
                    et_urls.append(loc.text.strip())
        except Exception as e:
            logger.debug(f"ElementTree parse error, falling back to regex: {e}")

        # Regex fallback if ElementTree returned 0 locs
        if not et_urls:
            matches = re.findall(r'<loc>\s*(https?://[^\s<]+)\s*</loc>', xml_text, re.IGNORECASE)
            et_urls.extend(matches)

        # Recursively explore child sitemaps in sitemap indexes
        child_sitemaps = [u for u in et_urls if u.endswith('.xml') or u.endswith('.xml.gz') or 'sitemap' in u.lower()]
        
        if is_index and child_sitemaps and max_depth > 0:
            nested_items = []
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            for child_url in child_sitemaps[:8]:
                try:
                    resp = requests.get(child_url, headers=headers, timeout=15)
                    if resp.status_code == 200:
                        child_text = resp.text
                        if resp.content[:2] == b'\x1f\x8b':
                            try:
                                child_text = gzip.decompress(resp.content).decode('utf-8', errors='replace')
                            except Exception:
                                pass
                        child_res = SitemapCrawler._parse_xml_sitemap(child_text, child_url, max_depth=max_depth - 1)
                        nested_items.extend(child_res)
                except Exception as ex:
                    logger.warning(f"Failed to fetch child sitemap {child_url}: {ex}")
            if nested_items:
                return nested_items

        for u in et_urls:
            discovered.append({'url': u, 'anchor_text': ''})

        return discovered

    @staticmethod
    def _parse_html_links(html_text: str, base_url: str) -> List[Dict[str, str]]:
        """Parses HTML category pages, capturing clean anchor titles and canonical URLs."""
        items = []
        parsed_base = urlparse(base_url)
        base_domain = parsed_base.netloc.lower()
        root_domain = '.'.join(base_domain.split('.')[-2:]) if len(base_domain.split('.')) >= 2 else base_domain

        soup = BeautifulSoup(html_text, 'html.parser')
        for a in soup.find_all('a', href=True):
            raw_href = a['href'].strip()
            if not raw_href or raw_href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                continue

            abs_url = urljoin(base_url, raw_href)
            p = urlparse(abs_url)
            if not p.scheme.startswith('http'):
                continue

            link_domain = p.netloc.lower()
            if link_domain == base_domain or link_domain.endswith('.' + root_domain):
                anchor_text = a.get_text(separator=' ', strip=True)
                anchor_text = re.sub(r'\s+', ' ', anchor_text).strip()
                # Ignore generic button/action labels
                if re.match(r'^(book now|view details|know more|click here|read more|view more|view all|explore|explore more|details|view|more|\d+)$', anchor_text, re.IGNORECASE):
                    anchor_text = ''
                if len(anchor_text) > 80:
                    anchor_text = anchor_text[:80].rsplit(' ', 1)[0]

                items.append({
                    'url': abs_url,
                    'anchor_text': anchor_text
                })

        return items
