from numpy import genfromtxt
import numpy
import math

speed_factor = 0.5
dist_threshold =4
drug_load = [200,200]
number_of_drugs = 2

class Settlement:
#this is to define the settlement object
#sindex - index number of the settlement
#xcd and ycd - xcoordinate and ycoordinate of the settlement
#time - time horizon to correspond to drug demand
#drugindex - refers to the drug type/index
#drug_demand - refers to the demand of the drug for that index
#SSI - the stockout severity index 

	def __init__ (self, sindex, xcd, ycd, drug_demand, SSI):
		self.sindex = sindex
		self.xcd = xcd
		self.ycd = ycd
		self.drug_demand = drug_demand
		self.SSI = SSI
		self.total_supply = [0,0]
		#round brackets above becuase this is a tuple initiated with 0 for each medicine type and not a list.


	def get_distance (self,settlement):
		return (math.sqrt(((self.xcd-settlement.xcd)**2)+((self.ycd-settlement.ycd)**2)))


#x = Settlement(1,10,10,1,1,15,0.2)


#print x.sindex, x.xcd,x.ycd,x.time,x.drugindex,x.drug_demand,x.SSI

class Graph:

	nodes = {}
	def __init__ (self, settlements,dist_threshold):
		for i in range (len(settlements)):
			self.nodes[settlements[i].sindex] = []
			#here we are assigning the key
			for j in range(len(settlements)):
				distance=settlements[i].get_distance(settlements[j])
				#I have used math.ceil to round up the distance value
				if distance<=dist_threshold:
					time = int(math.ceil(distance*speed_factor))
					self.nodes[settlements[i].sindex].append((j,time))
						#Here we are assigning the value of the tuple to the key
						#two round brackets in the line above after append indicates a tuple.

	def get_neighbors(self,settlement):
		return self.nodes[settlement.sindex]

	

	#def next_settlement(self,settlement):
	#	neighbors = self.get_neighbors(settlement)
		#Biplab remember, you need to call a member function on an object of the class hence we've used self.get_neighbors
	#	return neighbors
		#use return instead of print when you are calling a function from outside to print a result

class Greedy_dist:

	current_sindex = 0
	settlements={}
	current_time = 0
	#collection of all settlements which will contain the whole object as defined in class Settlement

	def __init__ (self):
		self.settlements[0]=(Settlement(0,0,0,[],0.0))
		self.settlements[1]=(Settlement(1,1,1,[[12,10,22,11,23,1],[11,22,1,4,5]],0.5))
		self.settlements[2]=(Settlement(2,2,2,[[50,40,12,5,33,2],[5,12,1,4,6,7]],0.7))
		self.graph = Graph(self.settlements,dist_threshold)
		#we have used self.settlement in the self.graph line because we're talking about the settlement in this class Pharma_dist
		#__innit__ fucntion is called a constructor, it constructs the object, it creates an instance and returns the value
		#create a member of another class in this class. Or creating a member of vehicle in class distribution
		self.vehicle = Vehicle(0)

	def get_depot_time(self,settlement):
			depot_dist = self.settlements[0].get_distance(settlement)
			depot_time = int(math.ceil(depot_dist*speed_factor))
			return depot_time

	def go_next(self):
		neighbors = self.graph.get_neighbors(self.settlements[self.current_sindex])

		selected_next_settlement = 0
		max_SSI = 0
		max_SSI_sindex = 0
		travel_time = 0
		for i in range(len(neighbors)):
			next_settlement = self.settlements[neighbors[i][0]]
			next_time = neighbors[i][1]
			if next_settlement.SSI > max_SSI:
				for drug in range(len(next_settlement.drug_demand)):
					forecast_time = self.current_time+next_time
					if self.current_time+next_time>len(next_settlement.drug_demand[drug]):
						forecast_time = len(drug_demand[drug])
					if sum(next_settlement.drug_demand[drug][:(forecast_time)])-next_settlement.total_supply[drug]>0 and self.vehicle.drug_load[drug]>0:
						travel_time = next_time
						selected_next_settlement = next_settlement
						max_SSI = next_settlement.SSI
						max_SSI_sindex = next_settlement.sindex
		if selected_next_settlement == 0:
			self.current_time += self.get_depot_time(self.settlements[self.current_sindex])
			self.current_sindex = 0


		else:
			self.current_time = self.current_time+travel_time
			self.current_sindex = max_SSI_sindex
			for drug in range(len(selected_next_settlement.drug_demand)):
				if self.current_time<=len(selected_next_settlement.drug_demand[drug]):
					drug_required = sum(selected_next_settlement.drug_demand[drug][:self.current_time])-selected_next_settlement.total_supply[drug]
					if (self.vehicle.drug_load[drug]-drug_required)>=0:
						next_settlement.total_supply[drug] += drug_required
						self.vehicle.drug_load[drug] -= drug_required
					else:
						next_settlement.total_supply[drug] += self.vehicle.drug_load[drug]
						self.vehicle.drug_load[drug] = 0
				else:
					drug_required = sum(selected_next_settlement.drug_demand[drug][:-1])-selected_next_settlement.total_supply[drug]
					if (self.vehicle.drug_load[drug]- drug_required)>=0:
						# (-1 takes you to the last point in the length)
						next_settlement.total_supply[drug] += drug_required
						self.vehicle.drug_load[drug] -= drug_required
					else:
						next_settlement.total_supply[drug] += self.vehicle.drug_load[drug]
						self.vehicle.drug_load[drug] = 0
		print next_settlement.total_supply
		print (self.current_time)
		print (self.current_sindex)
		return max_SSI_sindex

class Vehicle:

#add capacity to the below line later
	def __init__ (self,vindex):
		self.vindex = vindex
		self.drug_load = drug_load


buffalopharmadist=Greedy_dist()

for i in range (10):
	print buffalopharmadist.go_next()


#print [x.sindex for x in buffalopharmadist.settlements]

# for every x in the collection of buffalopharmadist.settlements, which is the collection of settlements, print the index
#print buffalopharmadist.graph.nodes




#print g.nodes
#print x.sindex,x.xcd,x.ycd,x.drug_demand,x.SSI		

#print g.next_settlement(x)

#class Depot( object ):
#this is to define the nodes object


#class Drug(object):
#here we have define a drug class