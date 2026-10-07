"""Apply only the KTX retrieval fixes to an existing API image."""
import sys
from pathlib import Path

path = Path(sys.argv[1])
source = path.read_text(encoding='utf-8')
replacements = [
    ('return electricity_question(query) and not any(term in value for term in ("trom cap", "hanh lang", "duong day"))',
     "return (electricity_question(query) and 'student_housing' not in question_categories(query)\n"
     '            and not any(term in value for term in ("trom cap", "hanh lang", "duong day")))'),
    ("if rental and 'ky tuc xa' in value and 'ky tuc xa' not in question and 'nguoi thue nha' not in value:",
     "if rental and 'ky tuc xa' in value and 'student_housing' not in categories and 'nguoi thue nha' not in value:"),
    ("collective_query = any(term in question for term in ('ky tuc xa', 'khu tap trung', 'co so tap trung', 'dang ky tap the'))",
     "collective_query = ('student_housing' in categories or any(term in question for term in ('ky tuc xa', 'khu tap trung', 'co so tap trung', 'dang ky tap the')))"),
]
for old, new in replacements:
    if old not in source:
        raise ValueError('Unexpected base image: retrieval patch does not match')
    source = source.replace(old, new, 1)
compile(source, str(path), 'exec')
path.write_text(source, encoding='utf-8')
