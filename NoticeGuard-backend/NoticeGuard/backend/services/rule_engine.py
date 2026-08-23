import re
from urllib.parse import urlparse

URGENT_WORDS = [
    "urgent", "immediately", "immediate", "within 24 hours",
    "within 48 hours", "act now", "last warning", "final notice",
    "failure to comply", "respond immediately",
]

PAYMENT_WORDS = [
    "payment", "pay immediately", "pay now", "transfer",
    "bank transfer", "deposit", "fee", "fine", "penalty", "upi",
    "money", "account number", "bank account",
]

THREAT_WORDS = [
    "arrest", "police", "court", "warrant", "legal action",
    "criminal case", "prosecution", "penalty", "jail",
]

SUSPICIOUS_CONTACT_WORDS = [
    "whatsapp", "telegram", "personal number", "contact me",
    "dm me", "message this number",
]

GOVERNMENT_DOMAIN_SUFFIXES = [".gov.in", ".nic.in", ".gov"]


def analyze_rules(text):
    normalized = text.lower()
    reasons = []
    score = 0

    if find_matches(normalized, URGENT_WORDS):
        score += 20
        reasons.append("Urgent or threatening language")

    if find_matches(normalized, PAYMENT_WORDS):
        score += 25
        reasons.append("Payment or money-transfer request")

    if find_matches(normalized, THREAT_WORDS):
        score += 20
        reasons.append("Threat of legal or enforcement action")

    if find_matches(normalized, SUSPICIOUS_CONTACT_WORDS):
        score += 20
        reasons.append("Suspicious contact method")

    urls = extract_urls(text)
    for url in urls:
        if not is_government_domain(url):
            score += 30
            reasons.append("Unofficial or suspicious domain")
            break

    if contains_payment_information(normalized):
        score += 20
        reasons.append("Notice contains potentially unsafe payment details")

    if contains_free_email_address(normalized):
        score += 20
        reasons.append("Notice uses a personal email provider")

    score = min(score, 100)
    verdict, confidence = determine_verdict(score)

    if not reasons:
        reasons.append("No major red flags were detected")

    reasons = list(dict.fromkeys(reasons))

    return {
        "verdict": verdict,
        "confidence": confidence,
        "reasons": reasons,
        "score": score
    }


def determine_verdict(score):
    if score >= 60:
        return ("Fake", "High")
    if score >= 30:
        return ("Suspicious", "Medium")
    return ("Likely Genuine", "Low")


def find_matches(text, patterns):
    matches = []
    for pattern in patterns:
        if pattern in text:
            matches.append(pattern)
    return matches


def extract_urls(text):
    pattern = r"https?://[^\s<>\"]+"
    return re.findall(pattern, text, flags=re.IGNORECASE)


def is_government_domain(url):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False
        hostname = hostname.lower()
        return any(
            hostname.endswith(suffix) or hostname == suffix.lstrip(".")
            for suffix in GOVERNMENT_DOMAIN_SUFFIXES
        )
    except Exception:
        return False


def contains_payment_information(text):
    patterns = [
        r"\bupi\b", r"\bupi id\b", r"\bifsc\b",
        r"\baccount number\b", r"\bbank account\b",
        r"\b\d{9,18}\b",
    ]
    return any(re.search(pattern, text) for pattern in patterns)


def contains_free_email_address(text):
    providers = [
        "@gmail.com", "@yahoo.com", "@hotmail.com",
        "@outlook.com", "@protonmail.com",
    ]
    return any(provider in text for provider in providers)
