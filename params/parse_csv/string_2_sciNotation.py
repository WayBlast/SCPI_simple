

def string_2_sciNotation(x = ''):
	try:
		x_unit = x[-1]
		x_val = float(x[:-1])
	except:
		return float(x)

	res = any(chr.isdigit() for chr in x_unit)

	if res:
		return float(x)

	if x_unit == 'm':
		x_val = x_val/1000
		sciNot = '{:e}'.format(x_val)
	elif x_unit == 'u':
		x_val = x_val/1000000
		sciNot = '{:e}'.format(x_val)
	elif x_unit == 'n':
		x_val = x_val/1000000000
		sciNot = '{:e}'.format(x_val)
	elif x_unit == 'p':
		x_val = x_val/1000000000000
		sciNot = '{:e}'.format(x_val)
	elif x_unit == 'f':
		x_val = x_val/1000000000000000
		sciNot = '{:e}'.format(x_val)

	return float(sciNot)