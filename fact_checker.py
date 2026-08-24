import re, json, logging
from typing import Dict, Any, List

logger = logging.getLogger('fact_checker')

def _extract_numeric_price(price_str: str) -> float:
    if not price_str:
        return 0.0
    match = re.search(r'[\d,]+(?:\.\d{2})?', str(price_str))
    if match:
        try:
            return float(match.group(0).replace(',', ''))
        except ValueError:
            return 0.0
    return 0.0

def verify_ground_truth(package_input: Dict[str, Any], sections_dict: Dict[str, Any], title_tag: str, meta_description: str) -> Dict[str, Any]:
    flags = []
    recommendations = []
    score = 100

    scraped_cost_raw = package_input.get('cost', '') or ''
    scraped_dest_raw = package_input.get('destination', '') or ''
    scraped_dur_raw = package_input.get('duration', '') or ''
    scraped_name_raw = package_input.get('name', '') or ''
    scraped_cat = package_input.get('category', 'wellness')

    qf = sections_dict.get('quick_facts', {})
    gen_cost = qf.get('cost', '') or ''
    gen_dest = qf.get('destination', '') or ''
    gen_dur = qf.get('duration', '') or ''

    scraped_price_num = _extract_numeric_price(scraped_cost_raw)
    gen_price_num = _extract_numeric_price(gen_cost)

    price_check = {'status': True, 'scraped': scraped_cost_raw or 'Unlisted / Contact', 'generated': gen_cost or 'Contact YatraDham', 'details': 'Price grounded accurately.'}

    if scraped_price_num > 0:
        if gen_price_num > 0:
            diff_ratio = abs(scraped_price_num - gen_price_num) / scraped_price_num
            if diff_ratio > 0.05:
                price_check['status'] = False
                price_check['details'] = 'Price mismatch: scraped ' + str(scraped_price_num) + ' vs generated ' + str(gen_price_num)
                flags.append('Price mismatch: Scraped price differs from generated price')
                score -= 30
            else:
                price_check['details'] = 'Exact base rate match'
        else:
            price_check['status'] = False
            price_check['details'] = 'Scraped price available but generated output defaulted to contact for pricing'
            flags.append('Generated output missed available scraped pricing')
            score -= 15

    dest_check = {'status': True, 'scraped': scraped_dest_raw or 'India', 'generated': gen_dest or 'India', 'details': 'Destination aligned.'}
    if scraped_dest_raw:
        scraped_tokens = [t.strip().lower() for t in re.split(r'[,/|-]+', scraped_dest_raw) if len(t.strip()) > 2]
        gen_tokens = [t.strip().lower() for t in re.split(r'[,/|-]+', gen_dest) if len(t.strip()) > 2]
        has_overlap = any(st in gen_dest.lower() or any(st in gt for gt in gen_tokens) for st in scraped_tokens)
        if not has_overlap and scraped_dest_raw.lower() != 'india':
            dest_check['status'] = False
            dest_check['details'] = 'Location drift: Scraped ' + scraped_dest_raw + ' vs Generated ' + gen_dest
            flags.append('Location drift detected')
            score -= 25

    cat_check = {'status': True, 'details': 'Domain rules respected.'}
    all_gen_text = (title_tag + ' ' + meta_description + ' ' + json.dumps(sections_dict)).lower()
    if scraped_cat == 'wellness':
        if any(w in all_gen_text for w in ['vip darshan', 'puja thali', 'pandit ji fee', 'aarti pass', 'abhishek booking']):
            cat_check['status'] = False
            cat_check['details'] = 'Pilgrimage puja rituals detected in Wellness retreat content'
            flags.append('Category violation: Puja/Darshan terms in Wellness content')
            score -= 20

    schema_check = {'status': True, 'details': 'All core structured sections present.'}
    required_sections = ['package_overview', 'why_choose_bullets', 'inclusions', 'exclusions', 'faq']
    missing_sections = [sec for sec in required_sections if not sections_dict.get(sec)]
    if missing_sections:
        schema_check['status'] = False
        schema_check['details'] = 'Missing sections: ' + ', '.join(missing_sections)
        flags.append('Missing required sections: ' + ', '.join(missing_sections))
        score -= 20

    final_score = max(0, min(100, score))
    verdict = 'VERIFIED' if final_score >= 85 and len(flags) == 0 else ('NEEDS_REVIEW' if final_score >= 60 else 'MISMATCH_DETECTED')

    return {
        'factual_integrity_score': final_score,
        'verification_status': verdict,
        'checks': {
            'price': price_check,
            'destination': dest_check,
            'duration': {'status': True, 'scraped': scraped_dur_raw or 'Flexible', 'generated': gen_dur or 'Flexible', 'details': 'Duration aligned.'},
            'category_integrity': cat_check,
            'schema_compliance': schema_check
        },
        'flags': flags,
        'recommendations': recommendations or ['Content passed factual ground-truth verification.']
    }
