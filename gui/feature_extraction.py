# import pandas as pd
import re
from urllib.parse import urlparse, parse_qs
import tldextract
from  tldextract import  extract
import pandas as pd
import ipaddress
import math
from fuzzywuzzy import fuzz
from collections import Counter
import socket
import time




# Entropi Hesaplama Fonksiyonu
def calculate_entropy(data):
    if not data:
        return 0
    probabilities = [data.count(c) / len(data) for c in set(data)]
    return round(-sum(p * math.log2(p) for p in probabilities), 6)


legitimate_domains = [
    'google.com', 'facebook.com', 'amazon.com', 'twitter.com', 'microsoft.com', 'apple.com',
    'youtube.com', 'instagram.com', 'linkedin.com', 'wikipedia.org', 'reddit.com', 'pinterest.com',
    'tumblr.com', 'ebay.com', 'paypal.com', 'net1flix.com', 'yahoo.com', 'spotify.com', 'github.com',
    'whatsapp.com', 'dropbox.com', 'slack.com', 'airbnb.com', 'zoom.us', 'merriam-webster.com',
    'cnn.com', 'bbc.com', 'bbc.co.uk', 'nytimes.com', 'forbes.com', 'businessinsider.com', 'dell.com',
    'adobe.com', 'etsy.com', 'paypal.com', 'etsy.com', 'bloomberg.com', 'chase.com', 'bankofamerica.com',
    'hulu.com', 'salesforce.com', 'twitch.tv', 'square.com', 'vimeo.com', 'messenger.com', 'snapchat.com',
    'cnn.com', 'theguardian.com', 'theverge.com', 'techcrunch.com', 'wired.com', 'nytimes.com', 'bbc.co.uk',
    'cnbc.com', 'zoom.com', 'samsung.com', 'intel.com', 'oracle.com', 'samsung.com', 't-mobile.com',
    'att.com', 'verizon.com', 'airbnb.com', 'paypal.com', 'spotify.com', 'yelp.com', 'google.co.uk',
    'bbc.co.uk', 'sainsburys.co.uk', 'guardian.co.uk', 'walmart.com', 'target.com', 'bestbuy.com', 'costco.com',
    'alibaba.com', 'wish.com', 'etsy.com', 'snapdeal.com', 'craigslist.org', 'flickr.com', 'tripadvisor.com',
    'expedia.com', 'hotels.com', 'booking.com', 'trivago.com', 'skyscanner.com', 'airasia.com', 'ryanair.com'
]
legitimate_brands = {
    'apple', 'google', 'microsoft', 'amazon', 'facebook', 'twitter', 'paypal',
    'samsung', 'sony', 'instagram', 'linkedin', 'netflix', 'youtube', 'whatsapp',
    'tesla', 'spotify', 'airbnb', 'pinterest', 'dropbox', 'uber', 'aircanada',
    'walmart', 'bestbuy', 'target', 'mcdonalds', 'nike', 'adidas', 'wellsfargo',
    'chase', 'bankofamerica', 'hsbc', 'citibank', 'barclays', 'goldman', 'americanexpress',
    'visa', 'mastercard', 'paypal', 'square', 'shopify', 'etoro', 'robinhood', 'deutschebank',
    'goldman', 'coca-cola', 'pepsi', 'loreal', 'procterandgamble', 'colgate', 'nestle',
    'unilever', 'ford', 'chevrolet', 'toyota', 'honda', 'bmw', 'mercedes', 'audi',
    'volkswagen', 'hyundai', 'kia', 'bose', 'boeing', 'nike', 'newbalance', 'reebok',
    'underarmour', 'puma', 'gucci', 'prada', 'louisvuitton', 'chanel', 'michaelkors',
    'tiffany', 'cartier', 'burberry', 'ralphlauren', 'loreal', 'nike', 'puma', 'lacoste',
    'asics', 'skype', 'viber', 'slack', 'zoom', 'discord', 'snapchat', 'telegram', 'wechat',
    'vimeo', 'yahoo', 'reddit', 'ebay', 'etsy', 'alibaba', 'taobao', 'mercadolibre',
    'shopify', 'zara', 'h&m', 'uniqlo', 'gap', 'mango', 'asos', 'nike', 'adidas', 'puma',
    'reebok', 'newbalance', 'vans', 'converse', 'skechers', 'keds', 'ugg', 'louisvuitton',
    'chanel', 'prada', 'gucci', 'fendi', 'balenciaga', 'versace', 'hermes', 'louisvuitton',
    'bally', 'salvatoreferragamo', 'tiffany', 'cartier', 'jacobcohen', 'montblanc', 'omega',
    'tagheuer', 'calvinklein', 'tommyhilfiger', 'ralphlauren', 'lindor', 'nutella', 'dove',
    'sainsburys', 'tesco', 'costco', 'aldi', 'lidl', 'bmw', 'mercedes', 'audi', 'toyota',
    'ford', 'volvo', 'mazda', 'peugeot', 'renault', 'citroen', 'kia', 'hyundai', 'honda',
    'mitsubishi', 'nissan', 'subaru', 'chrysler', 'gmc', 'chevrolet', 'buick', 'cadillac',
    'jeep', 'ram', 'dodge', 'ferrari', 'lamborghini', 'porsche', 'rollsroyce', 'bentley',
    'astonmartin', 'mclaren', 'bugatti', 'koenigsegg', 'pagani', 'chanel', 'gucci', 'hermes'
}

with open("tldlist.txt", "r", encoding="utf-8") as file:
    known_tlds = {line.strip().lower() for line in file if line.strip()}

def contains_www(url):
    # Protokol kısmını (http:// veya https://) ayıklayalım
    # Eğer varsa, https:// veya http:// kısmını atlayacağız
    url = re.sub(r'^https?://', '', url)  # https:// veya http://'yi kaldır

    # URL'nin başında tam olarak 'www.' olup olmadığını kontrol et
    if url.startswith("www.") and url.count("www.") == 1:
        return True
    return False


def count_www(url):
    # Protokol kısmını (http:// veya https://) ayıklayalım
    url = re.sub(r'^https?://', '', url)  # https:// veya http://'yi kaldır

    # 'www.' alt dizisinin kaç kez geçtiğini kontrol et
    return url.count("www.")


def check_known_tld(url, known_tlds):
    match = re.search(r"\.([a-zA-Z]{2,})/?$", url)

    if match:
        tld = match.group(1).lower()
        return 1 if tld in known_tlds else 0  # True → 1, False → 0

    return 0  # TLD bulunamadıysa


# Typosquatting kontrol fonksiyonu (benzerlik)
def check_typosquatting(url, domain_list=legitimate_domains):
    url_domain = re.sub(r'http[s]?://|www\.', '', url).split('/')[0]  # URL'yi temizle

    # Eğer URL geçerli bir domain listesinde varsa, aldatmaca değildir
    if url_domain in domain_list:
        return 0  # Domain geçerli, aldatmaca yok

    # Potansiyel aldatmaca domainlerini kontrol et
    for domain in domain_list:
        similarity_score = fuzz.ratio(url_domain, domain)

        # Eğer benzerlik skoru 50'nin üzerinde ise aldatmaca olarak kabul et
        if similarity_score > 70:
            return 1  # Potansiyel aldatmaca

    return 0  # Benzerlik düşükse aldatmaca değil


# 2. Özellik Çıkarma Fonksiyonları
def extract_url_features(url):
    features = {}
    feature_times = {}

    try:
        if not isinstance(url, str) or not url:
            return None
        # URL'nin farklı kısımlarını ayırmak
        url = url.replace("[", "").replace("]", "")  # [ ve ] karakterlerini kaldır
        parsed_url = urlparse(url)


        extracted = tldextract.extract(url)
        domain_info = f"{extracted.domain}.{extracted.suffix}"
        domain_info_netloc = extract(parsed_url.netloc)
        hostname = parsed_url.hostname if parsed_url.hostname else ""
        path = parsed_url.path if parsed_url.path else ""
        query_params = parse_qs(parsed_url.query)
        subdomain = extracted.subdomain if extracted.subdomain else ""  # Subdomain varsa al, yoksa boş string
        tld = extracted.suffix if extracted.suffix else ""  # TLD varsa al, yoksa boş string



        #1 LENGTH
        start = time.time()
        features['url_length'] = len(url)
        feature_times['url_length'] = time.time() - start

        start = time.time()
        features['domain_length'] = len(domain_info) if domain_info else 0
        feature_times['domain_length'] = time.time() - start

        start = time.time()
        features['hostname_length'] = len(parsed_url.hostname) if parsed_url.hostname else 0
        feature_times['hostname_length'] = time.time() - start

        start = time.time()
        features['path_length'] = len(parsed_url.path) if parsed_url.path else 0
        feature_times['path_length'] = time.time() - start

        start = time.time()
        features['query_length'] = len(parsed_url.query) if parsed_url.query else 0
        feature_times['query_length'] = time.time() - start

        start = time.time()
        features['fragment_length'] = len(parsed_url.fragment) if parsed_url.fragment else 0
        feature_times['fragment_length'] = time.time() - start

        start = time.time()
        cleaned_url1 = url.rstrip('/')
        words_url = re.findall(r'\w+', cleaned_url1)
        features['length_words_raw'] = sum(len(word) for word in words_url)
        feature_times['length_words_raw'] = time.time() - start

        start = time.time()
        words_url2 = re.split(r'[./\-?&=_:,;!~@#\$%\^\*\(\)\[\]\{\}<>]', cleaned_url1)
        features['longest_words_raw'] = max(len(word) for word in words_url2) if words_url else 0
        feature_times['longest_words_raw'] = time.time() - start

        start = time.time()
        words_host = re.split(r'[./\-?&=_:,;!~@#\$%\^\*\(\)\[\]\{\}<>]', hostname)
        features['longest_word_host'] = max(len(word) for word in words_host) if words_host else 0
        feature_times['longest_word_host'] = time.time() - start

        start = time.time()
        words_path = re.split(r'[./\-?&=_:,;!~@#\$%\^\*\(\)\[\]\{\}<>]', path)
        features['longest_word_path'] = max(len(word) for word in words_path) if words_path else 0
        feature_times['longest_word_path'] = time.time() - start

        start = time.time()
        path_parts = [part for part in path.split('/') if part]
        features['num_words_path'] = len(path_parts)
        feature_times['num_words_path'] = time.time() - start

        start = time.time()
        words_host = [word for word in words_host if word.isalpha()]
        features['num_words_host'] = len(words_host)
        feature_times['num_words_host'] = time.time() - start

        start = time.time()
        features['num_uppercase'] = sum(1 for char in url if char.isupper())
        feature_times['num_uppercase'] = time.time() - start

        start = time.time()
        features['num_lowercase'] = sum(1 for char in url if char.islower())
        feature_times['num_lowercase'] = time.time() - start

        start = time.time()
        features['num_queries'] = len(query_params)
        feature_times['num_queries'] = time.time() - start

        start = time.time()
        features['max_query_length'] = max(
    (len(k) + sum(len(vv) for vv in v) + 1) for k, v in query_params.items()
) if query_params else 0
        feature_times['max_query_length'] = time.time() - start

        start = time.time()
        features['path_depth'] = parsed_url.path.count('/')
        feature_times['path_depth'] = time.time() - start


        #2 TOTAL - COUNT

        start = time.time()
        features["total_tld_count"] = len(extracted.suffix.split(".")) if extracted.suffix else 0
        feature_times["total_tld_count"] = time.time() - start

        start = time.time()
        features['total_of_dot'] = url.count('.')
        feature_times['total_of_dot'] = time.time() - start

        start = time.time()
        features['total_of_hypens'] = url.count('-')
        feature_times['total_of_hypens'] = time.time() - start

        start = time.time()
        features['total_of_at'] = url.count('@')
        feature_times['total_of_at'] = time.time() - start

        start = time.time()
        features['total_of_question_mark'] = url.count('?')
        feature_times['total_of_question_mark'] = time.time() - start

        start = time.time()
        features['total_of_slash'] = url.count('/')
        feature_times['total_of_slash'] = time.time() - start

        start = time.time()
        features['total_of_percent'] = url.count('%')
        feature_times['total_of_percent'] = time.time() - start

        start = time.time()
        features['total_of_underscore'] = url.count('_')
        feature_times['total_of_underscore'] = time.time() - start

        start = time.time()
        features['total_of_https'] = len(re.findall(r'\bhttps\b', url))
        feature_times['total_of_https'] = time.time() - start

        start = time.time()
        features['total_of_http'] = len(re.findall(r'\bhttp\b', url))
        feature_times['total_of_http'] = time.time() - start

        start = time.time()
        features['path_https_count'] = len(re.findall(r'\bhttps\b', path))
        feature_times['path_https_count'] = time.time() - start

        start = time.time()
        features['path_http_count'] = len(re.findall(r'\bhttp\b', path))
        feature_times['path_http_count'] = time.time() - start

        start = time.time()
        features['host_https_count'] = len(re.findall(r'\bhttps\b', hostname))
        feature_times['host_https_count'] = time.time() - start

        start = time.time()
        features['host_http_count'] = len(re.findall(r'\bhttp\b', hostname))
        feature_times['host_http_count'] = time.time() - start

        start = time.time()
        features['percent_20_count'] = url.count('%20')
        feature_times['percent_20_count'] = time.time() - start

        start = time.time()
        special_chars = re.findall(r"[^a-zA-Z0-9]", url)
        features['total_special_chars'] = len(special_chars)
        feature_times['total_special_chars'] = time.time() - start

        start = time.time()
        specialch_count_path = len(re.findall(r"[^a-zA-Z0-9/]", path))
        features['specialch_count_path'] = specialch_count_path
        feature_times['specialch_count_path'] = time.time() - start

        start = time.time()
        features['www_count'] = count_www(url)
        feature_times['www_count'] = time.time() - start

        start = time.time()
        features['num_subdomain_hyphens'] = sum(
            sub.count('-') for sub in extracted.subdomain.split('.')) if extracted.subdomain else 0
        feature_times['num_subdomain_hyphens'] = time.time() - start

        start = time.time()
        features['path_digits_count'] = len(re.findall(r'\d', path))
        feature_times['path_digits_count'] = time.time() - start

        start = time.time()
        features['host_digits_count'] = len(re.findall(r'\d', hostname))
        feature_times['host_digits_count'] = time.time() - start


        #3 RATİO (ORT)
        start = time.time()
        features['ratio_special_chars'] = round(features['total_special_chars'] / features['url_length'] if features[
                                                                                                          'url_length'] > 0 else 0, 6)
        feature_times['ratio_special_chars'] = time.time() - start

        start = time.time()
        numeric_chars = re.findall(r'\d', url)
        features['ratio_special_to_numeric'] = round(features['total_special_chars'] / len(numeric_chars) if len(
            numeric_chars) > 0 else 0, 6)
        feature_times['ratio_special_to_numeric'] = time.time() - start

        start = time.time()
        digits_in_url = len(re.findall(r'\d', url))
        features['ratio_digits_url'] = round(digits_in_url / len(url) if len(url) > 0 else 0, 6)
        feature_times['ratio_digits_url'] = time.time() - start

        start = time.time()
        digits_in_domain = len(re.findall(r'\d', domain_info))
        features['ratio_digits_host'] = digits_in_domain / len(domain_info) if len(
            domain_info) > 0 else 0
        feature_times['ratio_digits_host'] = time.time() - start

        start = time.time()
        features['avg_query_length'] = round(features['query_length'] / features['num_queries'] if features[
                                                                                                      'num_queries'] > 0 else 0, 6)
        feature_times['avg_query_length'] = time.time() - start


        start = time.time()
        features['entropy_of_url'] = calculate_entropy(url)
        feature_times['entropy_of_url'] = time.time() - start

        # Ortalama Kelime Uzunluğu
        start = time.time()
        words2 = re.split(r'[./\-?&=_:,;!~@#\$%\^\*\(\)\[\]\{\}<>]', url)
        words2 = [word for word in words2 if word]  # Boş stringleri temizle
        features["avg_word_length"] = round(sum(len(word) for word in words2) / len(words2) if words2 else 0, 6)
        feature_times["avg_word_length"] = time.time() - start

        #4 HAS (1 veya 0)

        start = time.time()
        features['typosquatting'] = check_typosquatting(url)  # Potansiyel aldatmaca durumu
        feature_times['typosquatting'] = time.time() - start

        start = time.time()
        features['contains_fragments'] = 1 if parsed_url.fragment else 0
        feature_times['contains_fragments'] = time.time() - start

        start = time.time()
        try:
            ipaddress.ip_address(domain_info)
            features['contains_ip'] = 1
        except ValueError:
            features['contains_ip'] = 0
        feature_times['contains_ip'] = time.time() - start

        start = time.time()
        features['contains_https_token'] = 1 if url.startswith("https://") else 0
        feature_times['contains_https_token'] = time.time() - start

        start = time.time()
        features['contains_http_token'] = 1 if url.startswith("http://") else 0
        feature_times['contains_http_token'] = time.time() - start

        start = time.time()
        features['contains_legitimate_brand'] = 1 if any(brand in url.lower() for brand in legitimate_brands) else 0
        feature_times['contains_legitimate_brand'] = time.time() - start

        start = time.time()
        features["is_known_tld"] = 1 if check_known_tld(url, known_tlds) else 0
        feature_times["is_known_tld"] = time.time() - start

        start = time.time()
        features['punycode'] = 1 if re.search(r'xn--', domain_info) else 0
        feature_times['punycode'] = time.time() - start

        start = time.time()
        features['prefix_suffix'] = 1 if '-' in domain_info else 0
        feature_times['prefix_suffix'] = time.time() - start

        start = time.time()
        if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', domain_info):
            tld_in_subdomain = 0  # IP adresi durumunda TLD subdomain'de olamaz
        else:
            tld_in_subdomain = 1 if tld in subdomain.split('.') else 0  # TLD, subdomain'de varsa 1, yoksa 0
        features['tld_in_subdomain'] = tld_in_subdomain
        feature_times['tld_in_subdomain'] = time.time() - start

        start = time.time()
        features['tld_in_path'] = 1 if extracted.suffix in parsed_url.path else 0
        feature_times['tld_in_path'] = time.time() - start

        start = time.time()
        features['contains_www'] = 1 if contains_www(url) else 0
        feature_times['contains_www'] = time.time() - start

        start = time.time()
        try:
            features["contains_port"] = 1 if parsed_url.port and isinstance(parsed_url.port, int) else 0
        except ValueError:
            features["contains_port"] = 0  # Hatalı port formatı varsa yokmuş gibi kabul et
        feature_times["contains_port"] = time.time() - start

        start = time.time()
        features['contains_login'] = 1 if 'login' in url.lower() else 0
        feature_times['contains_login'] = time.time() - start

        start = time.time()
        features['contains_bank'] = 1 if 'bank' in url.lower() else 0
        feature_times['contains_bank'] = time.time() - start

        start = time.time()
        features['contains_secure'] = 1 if 'secure' in url.lower() else 0
        feature_times['contains_secure'] = time.time() - start

        start = time.time()
        features['contains_account'] = 1 if 'account' in url.lower() else 0
        feature_times['contains_account'] = time.time() - start

        start = time.time()
        features['contains_confirm'] = 1 if 'confirm' in url.lower() else 0
        feature_times['contains_confirm'] = time.time() - start

        start = time.time()
        features['contains_token'] = 1 if 'token' in url.lower() else 0
        feature_times['contains_token'] = time.time() - start

        start = time.time()
        features['contains_free'] = 1 if 'free' in url.lower() else 0
        feature_times['contains_free'] = time.time() - start

        start = time.time()
        features['contains_win'] = 1 if 'win' in url.lower() else 0
        feature_times['contains_win'] = time.time() - start

        start = time.time()
        features['is_repeated_word'] = 1 if any(count > 1 for count in Counter(words_url).values()) else 0
        feature_times['is_repeated_word'] = time.time() - start

        start = time.time()
        features['contains_redirect'] = 1 if "//" in parsed_url.path[1:] else 0
        feature_times['contains_redirect'] = time.time() - start

        start = time.time()
        features['contains_js_code'] = 1 if 'javascript:' in parsed_url.path.lower() else 0
        feature_times['contains_js_code'] = time.time() - start

        return features, feature_times
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None  # Hatalı URL'leri atla




