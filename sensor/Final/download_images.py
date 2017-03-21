#uses python3
import urllib.request
import cv2
import numpy as np
import os

def store_raw_images():
	#neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152'
	#neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'
	neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n02735688'
	#neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n04105893'
	neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()

	pic_num = 4000

	for i in neg_image_urls.split('\n'):
		try:
			print(i)
			urllib.request.urlretrieve(i, "neg/" + str(pic_num) + '.jpg')
			img = cv2.imread("neg/" + str(pic_num) + '.jpg', cv2.IMREAD_GRAYSCALE)
			resized_image = cv2.resize(img, (300,300))
			cv2.imwrite("neg/"+str(pic_num) + '.jpg', resized_image)
			pic_num += 1

		except Exception as e:
			print(str(e))


def find_rejects():
	for file_type in ['neg']:
		for img in os.listdir(file_type):
			for rjc in os.listdir('reject'):
				try:
					current_image_path = str(file_type)+'/'+str(img)
					rjc = cv2.imread('reject/'+str(rjc))
					question = cv2.imread(current_image_path)

					if rjc.shape == question.shape and not (np.bitwise_xor(rjc, question).any()):
						print('deleted')
						print(current_image_path)
						os.remove(current_image_path)
				except Exception as e:
					print(str(e))

def create_pos_neg():
	for file_type in ['neg']:
		for img in os.listdir(file_type):
			if file_type == 'neg':
				line = file_type+'/'+img+'\n'
				with open('bg.txt', 'a') as f:
					f.write(line)
			elif file_type == 'pos':
				line = file_type+'/'+img+ ' 1 0 0 50 50\n'
				with open('info.dat', 'a') as f:
					f.write(line)



create_pos_neg()
#store_raw_images()
#find_rejects()
