import json
import cv2

colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0],
          [0, 255, 0], \
          [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255],
          [85, 0, 255], \
          [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]

def get_viable(joints_data):
	joints = []
	jind = []

	for i, ele in enumerate(joints_data):
		joints.append((ele[0], ele[1]))
		if(ele[2]>0.1):
			jind.append(i)

	limbs = [0,0,1,2, 0,17,17,5,7,6, 8,17,17,11,13,12,14]
	limbe = [1,2,3,4,17, 5, 6,7,9,8,10,11,12,13,15,14,16]

	nwlimbs = []
	nwlimbe = []

	for a, b in zip(limbs, limbe):
		if(a in jind and b in jind):
			nwlimbs.append(a)
			nwlimbe.append(b)

	return joints, jind, nwlimbs, nwlimbe



with open('output/alphapose-results.json') as f:
	data = json.load(f)

for ele in data:
	img = cv2.imread('output/' + ele['image_id'])
	array = ele['keypoints']
	joints_data = []
	for i in range(len(array)//3):
		joints_data.append((int(array[3*i]), int(array[3*i+1]), array[3*i+2]))

	x = (joints_data[5][0] + joints_data[6][0])/2
	y = (joints_data[5][1] + joints_data[6][1])/2
	sc = (joints_data[5][2] + joints_data[6][2])/2
	joints_data.append((int(x), int(y), sc))

	joints, jind, limbs, limbe = get_viable(joints_data)

	for i in jind:
		cv2.circle(img, joints[i], 6, colors[i], thickness=-1)

	for i in range(len(limbs)):
		cv2.line(img, (joints[limbs[i]][0], joints[limbs[i]][1]), (joints[limbe[i]][0], joints[limbe[i]][1]), colors[i], thickness=3)

	cv2.imwrite('output/' + ele['image_id'], img)