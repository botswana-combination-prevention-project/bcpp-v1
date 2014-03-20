see README.rst in folder bhp066 

convert coordinates
-ve south
+ve east
def decodedeg2dm(dd):
	dd = abs(dd)
	degrees, minutes = divmod(dd*60,60)
	return degrees. minutes
