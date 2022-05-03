from pdfminer.high_level import extract_text
from pprint import pp, pprint
import re

texto = extract_text(r'Requisicao.pdf')


emails = re.findall(r'((?:bom dia|boa tarde).+?visualizou)', texto, flags=re.I|re.S)

for email in emails:
    pprint(email)
