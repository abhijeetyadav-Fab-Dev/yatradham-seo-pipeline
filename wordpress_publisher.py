import base64
import json
import logging
from typing import Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)

class WordPressPublisher:
    def __init__(self, site_url: str, username: str, app_password: str):
        self.site_url = site_url.rstrip('/')
        if not self.site_url.startswith('http://') and not self.site_url.startswith('https://'):
            self.site_url = f'https://{self.site_url}'
        
        self.username = username.strip()
        self.app_password = app_password.replace(' ', '').strip()
        auth_bytes = f'{self.username}:{self.app_password}'.encode('utf-8')
        self.auth_header = f'Basic {base64.b64encode(auth_bytes).decode("utf-8")}'

    def get_headers(self) -> Dict[str, str]:
        return {
            'Authorization': self.auth_header,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def verify_connection(self) -> Dict[str, Any]:
        endpoint = f'{self.site_url}/wp-json/wp/v2/users/me'
        try:
            res = requests.get(endpoint, headers=self.get_headers(), timeout=15)
            if res.status_code == 200:
                data = res.json()
                return {
                    'success': True,
                    'user_id': data.get('id'),
                    'name': data.get('name'),
                    'roles': data.get('roles', [])
                }
            else:
                return {
                    'success': False,
                    'status_code': res.status_code,
                    'error': res.text or 'Authentication failed. Check your WordPress username and Application Password.'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to connect to WordPress site at {self.site_url}: {str(e)}'
            }

    def publish_post(
        self,
        title: str,
        content_html: str,
        meta_description: str = '',
        status: str = 'draft',
        post_type: str = 'posts',
        slug: Optional[str] = None,
        categories: Optional[list] = None,
        tags: Optional[list] = None
    ) -> Dict[str, Any]:
        # Hard QA Gate: Block publication if unresolved template variables exist in content or title
        combined_text = f"{title} {content_html} {meta_description}"
        leaks = re.findall(r"\{[a-zA-Z0-9_\-]+\}", combined_text)
        if leaks:
            return {
                'success': False,
                'error': f'Publishing Blocked: Unresolved template placeholders found in content: {list(set(leaks))}. Please edit before publishing.'
            }

        endpoint = f'{self.site_url}/wp-json/wp/v2/{post_type}'
        
        payload: Dict[str, Any] = {
            'title': title,
            'content': content_html,
            'status': status,
            'excerpt': meta_description
        }

        
        if slug:
            payload['slug'] = slug
        if categories:
            payload['categories'] = categories
        if tags:
            payload['tags'] = tags

        meta_dict = {}
        if meta_description:
            meta_dict['_yoast_wpseo_metadesc'] = meta_description
            meta_dict['rank_math_description'] = meta_description
        if title:
            meta_dict['_yoast_wpseo_title'] = title
            meta_dict['rank_math_title'] = title
        
        if meta_dict:
            payload['meta'] = meta_dict

        try:
            res = requests.post(endpoint, headers=self.get_headers(), json=payload, timeout=30)
            if res.status_code in [200, 201]:
                data = res.json()
                return {
                    'success': True,
                    'post_id': data.get('id'),
                    'link': data.get('link'),
                    'status': data.get('status'),
                    'title': title
                }
            else:
                return {
                    'success': False,
                    'status_code': res.status_code,
                    'error': res.text or 'WordPress publishing failed.'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error communicating with WordPress: {str(e)}'
            }

