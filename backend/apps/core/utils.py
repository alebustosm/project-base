def normalize_text(txt, codif='utf-8'):
	normalize('NFKD', bytes(txt, codif).decode(codif)).encode('ASCII', 'ignore')