class PriorityQueue(object): 
	def __init__(self): 
		self.heap = []
		self.count = 0 

	def push(self, item, priority):
		data = [item, priority]
		self.heap.append(data) 
		self.count = self.count + 1

	def pop(self): 
		min = 0
		for i in range(len(self.heap)): 
			if self.heap[i][1] < self.heap[min][1]: 
				min = i 
		item = self.heap[min]
		del self.heap[min]
		self.count = self.count - 1
		return item

	def isEmpty(self):
		return self.count == 0

	def getCount(self):
		return self.count	

	def update(self, item, priority):
		for i in self.heap:
			if i[0] == item:
				i[1] = priority
def PQSort(array):
	myq = PriorityQueue()
	for i in array:
		myq.push(i,i) #Each number has it's priority and it is the number it self
	sorted_array = []
	for i in range(myq.getCount()):
		sorted_array.append(myq.pop()[0]) #pop the smallest number and keeping the item(number) only
	return sorted_array	

if __name__ == "__main__":
	array = [1,4,3,7,3,8,12]
	print(array)
	array = PQSort(array)
	print(array)
	
