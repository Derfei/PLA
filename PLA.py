#-*- coding: utf-8 -*-
####################################
#PLA的基本思路：
#每个特征都有权重wi，表示该特征的重要
#程度，当综合所有的特征和权重计算一个
#最终的分数，当这个分数超过某个阈值的
#时候，表示成功，否则表示失败。
####################################

####################################
#PLA的算法步骤:
#step1： 随便找一条直线，即随便找一个
#n维向量W0，赋初值w = w0
#step2： 如果这条直线正好把训练数据正
#确切分，训练结束。
#step3： 如果有任意一个样本没有被正确
#切分，即在权值计算中不等于正确的y值，
#此时我们就要对权值做一点简单的修正，
#令w(t+1) = w(t) + y'x'
#step4: 跳转到step2
####################################
import numpy as np
import matplotlib.pyplot as plt
import xlwt
import xlrd
import random

#生成数据函数，并将数据写入csv文件
def born_data():
	workbook = xlwt.Workbook("pla_data.xls")
	sheet = workbook.add_sheet("sheet1", cell_overwrite_ok=True)

	sheet.write(0, 0, "age")
	sheet.write(0, 1, "price")
	sheet.write(0, 2, "click")

	for i in range(1, 400):
		price = random.randint(50, 1000)
		age = random.randint(13, 60)
		if age * 3.14 + price * 2.3 >= 1000:
			click = 1
		else:
			click = -1
		sheet.write(i, 0, age)
		sheet.write(i, 1, price)
		sheet.write(i, 2, click)


	workbook.save("pla_data.xls")

#读取数据，返回一个列表
def get_data(filepath='pla_data.xls', sheet_name="sheet1"):
	lines = []
	workbook = xlrd.open_workbook(filepath)
	table = workbook.sheet_by_name(sheet_name)

	row = table.nrows

	for i in range(1, row):
		lines.append(table.row_values(i))

	return lines
#初始化三维列表，进行随机赋值。
def init_weight():
	vector = np.random.uniform(0, 10, size=3)
	return list(vector)

#判断数据被切分的正确率
def cut_dot(currucy=1.0, weight_vector=[], data_list=[], learning_rate=0.8):
	right = 0.0
	for i, data in enumerate(data_list):
		if weight_vector[0] + weight_vector[1]*data[0] + weight_vector[2]*data[1] > 0:
			if data[2] == 1:
				right = right + 1.0
			else:
				weight_vector[0] = weight_vector[0] - learning_rate*2*random.randrange(1, 10)
				weight_vector[1] = weight_vector[1] - learning_rate*2*data[0]
				weight_vector[2] = weight_vector[2] - learning_rate*2*data[1]
		else:
			if data[2] == -1:
				right = right + 1.0
			else:
				weight_vector[0] = weight_vector[0] + learning_rate*2*random.randrange(1, 10)
				weight_vector[1] = weight_vector[1] + learning_rate*2*data[0]
				weight_vector[2] = weight_vector[2] + learning_rate*2*data[1]
	print("The curracy is {}".format(right/len(data_list)))

	if right/len(data_list) >= currucy:
		return True
	else:
		return False

#生成数据
born_data()

#读取数据
data_list = get_data()
print("This is the data_list {}".format(data_list))
#在图形中表示数据
x_negative = []
y_negative = []
x_positive = []
y_positive = []
for data in data_list:
	if data[2] == -1:
		x_negative.append(data[0])
		y_negative.append(data[1])
	else:
		x_positive.append(data[0])
		y_positive.append(data[1])

plt.scatter(x_negative, y_negative, c='grey', marker='o')
#print("This is the x_negative {}".format(x_negative))
#print("This is the y_negative {}".format(y_negative))

plt.scatter(x_positive, y_positive, c='red', marker='x')
plt.xlabel("age")
plt.ylabel("price")
plt.ion()
plt.show()


#初始化权重
weight = init_weight()

#pla分类
while cut_dot(0.999, weight, data_list, learning_rate=0.2) == False:
	cut_dot(0.999, weight, data_list, learning_rate=0.2)

print("This is the weight: {}".format(weight))
#划线
x1 = []
y1 = []
for i in range(60):
	x = i
	y = (weight[1]*x - weight[0])/weight[2]
	x1.append(x)
	y1.append(y)

plt.plot(x1, y1)

print("The pla get successed!")
plt.pause(1000)