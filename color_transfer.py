import numpy as np
import cv2
import os

def get_mean_and_std(x):
	x_mean, x_std = cv2.meanStdDev(x)
	x_mean = np.hstack(np.around(x_mean,2))
	x_std = np.hstack(np.around(x_std,2))
	return x_mean, x_std

sf = []
tf = []
cotr=0

for root, ds, fs in os.walk("./source"):
    for f in fs:
        if (f.endswith('.bmp'))or(f.endswith('.jpg'))or(f.endswith('.png')):
            fullname = os.path.join(root, f)
            sf.append(fullname)

for root, ds, fs in os.walk("./target"):
    for f in fs:
        if (f.endswith('.bmp'))or(f.endswith('.jpg'))or(f.endswith('.png')):
            fullname = os.path.join(root, f)
            tf.append(fullname)

for cots in range (len(sf)):
	for cott in range (len(tf)):

		s = cv2.imread(sf[cots])
		s = cv2.cvtColor(s,cv2.COLOR_BGR2LAB)
		t = cv2.imread(tf[cott])
		t = cv2.cvtColor(t,cv2.COLOR_BGR2LAB)

		print("Converting picture "+sf[cots]+" -> "+tf[cott])
		s_mean, s_std = get_mean_and_std(s)
		t_mean, t_std = get_mean_and_std(t)

		height, width, channel = s.shape
		for i in range(0,height):
			for j in range(0,width):
				for k in range(0,channel):
					x = s[i,j,k]
					x = ((x-s_mean[k])*(t_std[k]/s_std[k]))+t_mean[k]
					# round or +0.5
					if x == x:
						x = round(x)
					else:
						x = 0
					# boundary check
					x = 0 if x<0 else x
					x = 255 if x>255 else x
					s[i,j,k] = x

		s = cv2.cvtColor(s,cv2.COLOR_LAB2BGR)
		cv2.imwrite('result/r'+str(cotr)+'.png',s)
		cotr +=1
