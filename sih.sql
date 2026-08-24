
CREATE DATABASE IF NOT EXISTS noticeguard
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE noticeguard;

CREATE TABLE IF NOT EXISTS scam_categories (
  id INT UNSIGNED NOT NULL,
  category_name VARCHAR(150) NOT NULL,
  description TEXT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_scam_categories_name (category_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS scam_patterns (
  id INT UNSIGNED NOT NULL,
  pattern_name VARCHAR(150) NOT NULL,
  description TEXT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_scam_patterns_name (pattern_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS threat_messages (
  id INT UNSIGNED NOT NULL,
  message_text VARCHAR(500) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_threat_messages_text (message_text)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS scam_payment_methods (
  id INT UNSIGNED NOT NULL,
  method_name VARCHAR(150) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_scam_payment_methods_name (method_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS malicious_content_types (
  id INT UNSIGNED NOT NULL,
  content_type VARCHAR(150) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_malicious_content_types_name (content_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS official_domains (
  id INT UNSIGNED NOT NULL,
  domain_type VARCHAR(100) NOT NULL,
  example_domain VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_official_domains_example (example_domain)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS verification_red_flags (
  id INT UNSIGNED NOT NULL,
  red_flag VARCHAR(500) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_verification_red_flags_text (red_flag)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO scam_categories (id, category_name, description) VALUES
  (1, 'Fake GST/DGGI Summons', 'Scammers create official-looking GST summons using CBIC logos and fake DIN numbers.'),
  (2, 'Fake Digital Arrest Notices', 'Criminals impersonate law enforcement or regulatory agencies and demand money.'),
  (3, 'Fake Recruitment Notices', 'Fraudulent government recruitment advertisements designed to collect money or personal data.')
ON DUPLICATE KEY UPDATE
  category_name = VALUES(category_name),
  description = VALUES(description);

INSERT INTO scam_patterns (id, pattern_name, description) VALUES
  (1, 'Official Logo Misuse', 'Use of government logos, seals, or branding to appear legitimate.'),
  (2, 'Fake Reference Number', 'Use of fabricated DINs, complaint numbers, warrant IDs, or case numbers.'),
  (3, 'Threat and Urgency', 'Threats of arrest, account suspension, legal action, or deadlines.'),
  (4, 'Payment Demand', 'Requests for money via UPI, wallets, or personal bank accounts.'),
  (5, 'Malicious Links or Attachments', 'Links, PDFs, or APK files intended to steal credentials or install malware.'),
  (6, 'Fake Verification Mechanism', 'Providing scammer-controlled phone numbers, emails, or websites for verification.')
ON DUPLICATE KEY UPDATE
  pattern_name = VALUES(pattern_name),
  description = VALUES(description);

INSERT INTO threat_messages (id, message_text) VALUES
  (1, 'Pay immediately'),
  (2, 'Arrest warrant issued'),
  (3, 'Your account will be blocked'),
  (4, 'Legal action will be taken'),
  (5, 'Respond within 24 hours')
ON DUPLICATE KEY UPDATE message_text = VALUES(message_text);

INSERT INTO scam_payment_methods (id, method_name) VALUES
  (1, 'Personal Bank Account'),
  (2, 'UPI ID'),
  (3, 'Digital Wallet'),
  (4, 'Unofficial Payment Gateway')
ON DUPLICATE KEY UPDATE method_name = VALUES(method_name);

INSERT INTO malicious_content_types (id, content_type) VALUES
  (1, 'PDF Attachment'),
  (2, 'APK File'),
  (3, 'Phishing Link'),
  (4, 'Credential Harvesting Website')
ON DUPLICATE KEY UPDATE content_type = VALUES(content_type);

INSERT INTO official_domains (id, domain_type, example_domain, description) VALUES
  (1, 'Central Government', 'meity.gov.in', 'Official ministry or department domain under .gov.in'),
  (2, 'NIC', 'nic.gov.in', 'Official National Informatics Centre domain'),
  (3, 'Government Email', 'secretary@meity.gov.in', 'Official government email address'),
  (4, 'NIC Email', 'helpdesk-nic@nic.in', 'Official NIC helpdesk email address'),
  (5, 'State Government', 'up.gov.in', 'Official state government domain')
ON DUPLICATE KEY UPDATE
  domain_type = VALUES(domain_type),
  example_domain = VALUES(example_domain),
  description = VALUES(description);

INSERT INTO verification_red_flags (id, red_flag) VALUES
  (1, 'Reference number cannot be independently verified'),
  (2, 'Verification contact belongs to sender'),
  (3, 'Notice demands immediate payment'),
  (4, 'Notice contains suspicious links'),
  (5, 'Notice threatens arrest or legal action without due process'),
  (6, 'Notice requests installation of an APK or unknown application')
ON DUPLICATE KEY UPDATE red_flag = VALUES(red_flag);
