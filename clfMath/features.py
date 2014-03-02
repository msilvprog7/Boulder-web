import math, numpy, csv
from scipy.integrate import simps
import scipy.signal
from sklearn import svm

current_window, next_window = [], []

class DataWindow:
	current_window = []
	next_window = []
	window_size = 100
	clf = {}

	def setClf(self, newClf):
		self.clf = newClf

	def push(self, data):
		if len(self.current_window) < self.window_size:
			self.current_window.append(data)
		else:
			self.next_window.append(data)
			if len(self.next_window) == ( self.window_size / 2 ):
				self.current_window = self.current_window[( self.window_size / 2 ):] + self.next_window
				self.next_window = []

	def predict(self):
		features = get_features(self.current_window + [(0, 0, 0, 0, 2)])
		# print features
		return self.clf.predict([list(features[0])])

def get_features(lines):
	current_rep = 0
	x_sum, y_sum, z_sum = 0, 0, 0
	x_max, y_max, z_max = -100000, -100000, -100000
	x_array, y_array, z_array, time_array, features = [], [], [], [], []
	for line in lines:
		x_sum += int(line[0])
		y_sum += int(line[1])
		z_sum += int(line[2])
		x_array.append(int(line[0]))
		y_array.append(int(line[1]))
		z_array.append(int(line[2]))
		if int(line[0]) > x_max:
			x_max = int(line[0])
		if int(line[1]) > y_max:
			y_max = int(line[1])
		if int(line[2]) > z_max:
			z_max = int(line[2])
		time_array.append(int(line[3]))
		if current_rep != int(line[4]):
			current_rep = int(line[4])
			RMS = math.sqrt(x_sum * x_sum + y_sum * y_sum + z_sum * z_sum)
			# x_integral = simps(x_array, time_array)
			# y_integral = simps(y_array, time_array)
			# z_integral = simps(z_array, time_array)
			x_average = x_sum / len(x_array)
			y_average = y_sum / len(y_array)
			z_average = z_sum / len(z_array)
			x_std = numpy.std(x_array)
			y_std = numpy.std(y_array)
			z_std = numpy.std(z_array)
			feature = (RMS, x_max, y_max, z_max, x_average, y_average, z_average, x_std, y_std, z_std)
			# feature = (RMS, x_integral, y_integral, z_integral, x_average, y_average, z_average, x_std, y_std, z_std)
			features.append(feature)
			x_sum, y_sum, z_sum = 0, 0, 0
			x_max, y_max, z_max = -100000, -100000, -100000
			x_array, y_array, z_array, time_array = [], [], [], []
	return features

def train():
	features = []
	numDumbell, numShoulder, numShoulderPush, numNothing = 0, 0, 0, 0
	clf = svm.LinearSVC()
	with open('clfMath/data/dumbell.csv', 'rU') as csvfile:
		reader = csv.reader(csvfile)
		dTest = get_features(reader)
		numDumbell = len(dTest)
		features += dTest
		
	with open('clfMath/data/shoulder.csv', 'rU') as csvfile:
		reader = csv.reader(csvfile)
		sTest = get_features(reader)
		numShoulder = len(sTest)
		features += sTest
		
	with open('clfMath/data/shoulder_push.csv', 'rU') as csvfile:
		reader = csv.reader(csvfile)
		spTest = get_features(reader)
		numShoulderPush = len(spTest)
		features += spTest

	with open('clfMath/data/nothing.csv', 'rU') as csvfile:
		reader = csv.reader(csvfile)
		nTest = get_features(reader)
		numNothing = len(nTest)
		features += nTest

	trainingCategories = [2 for i in range(numDumbell)] + [1 for i in range(numShoulder)] + [3 for i in range(numShoulderPush)] + [0 for i in range(numNothing)]
	clf.fit(features, trainingCategories)
	return clf

if __name__ == "__main__":
	print "Training CLF"
	clf = train()
	test_features = []
	print "Testing Nothing (should return [0])"
	with open('data/nothing_test.csv', 'rU') as csvfile:
		reader = csv.reader(csvfile)
		test_features += get_features(reader)

	print clf.predict([list(test_features[0])])

# with open('nothing_test.csv', 'rU') as csvfile:
# 	reader = csv.reader(csvfile)
# 	test_features += get_features(reader)
# 	if test_null(reader):
# 		print "No action"
# 	else:
# 		print clf.predict([list(test_features[0])])


# b, a = scipy.signal.butter(4, 1, 'lowpass')
# output_signal_low = scipy.signal.filtfilt(b, a, current_window)

# d, c = scipy.signal.butter(4, 1, 'highpass')
# output_signal_low = scipy.signal.filtfilt(d, c, current_window)