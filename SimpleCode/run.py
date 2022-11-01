# Prism formulae:
# Probabilities: Pmax=?[ G !fail]
# Rewards:       R{"time"}min=?[F done]
# Idling: 		 

# ---------- Problem Parameters
numberOfjointtasks = 12
numberOfrobots_jointtasks = 2 #do NOT exceed 5
totaltime = 24


import sys
import pandas as pd
import random
import math




# ------------Travel cost--------------------
def travelcost(loc1,loc2):
	print("y2 {} y1 {} x2 {} x1 {}".format(loc2[1],loc1[1],loc2[0],loc1[0]))
	return round(math.sqrt( (loc2[1]-loc1[1])**2 + (loc2[0]-loc1[0])**2 ))

# ------------Module: robot --------------------
def robotModule(r,r_tasks,atomictasks,f):
	f.write("  {}Time:[0..TT] init 0;\n".format(r))
	f.write("  {}Loc:[0..{}] init 0;\n".format(r,len(r_tasks[r])))
	f.write("  {}Fail:[0..1] init 0;\n".format(r))
	#transitions
	count=0;
	for at in r_tasks[r]:
		# action
		if type(at.robot)==list:
			f.write("  [DO{}]".format(at.id))
		else:
			f.write("  [{}DO{}]".format(r,at.id))
		#guard
		f.write("  {}TimeOk_{} -> ".format(r,at.id))
		#update normal
		f.write("{}{}prob:".format(r,at.id))
		count+=1
		newstate = "({}Time'={}Time+{}{}Time+{}travelTO{}) & ({}Loc'={})".format(r,r,r,at.id,r,at.id,r,count)
		
		f.write(newstate)
		# update fail
		f.write("+ (1-{}{}prob):".format(r,at.id) )
		f.write(newstate + "& ({}Fail'=1)".format(r))
		
		f.write(";\n")
	return

# ------------Robot class--------------------
class Robot:
	def __init__(self,descr,id,location,prob):
		self.id = id
		self.loc = location
		self.prob = prob
# ------------Atomic task class--------------------
class AT:
	def __init__(self,descr,id,robot,num_robots,location,time):
		self.id = id
		self.robot = robot
		self.num_robots = num_robots
		self.loc = location
		self.time = time
# ------------Compound class--------------------
class CT:
	def __init__(self,id,subtasks,ordered):
		self.id = id
		self.subtasks = subtasks
		self.ordered = ordered



# ------------Main--------------------
# ------- Robots
r1 = Robot('move','r1',[0,0],0.999)
r2 = Robot('move','r2',[1,1],0.99)
r3 = Robot('move','r3',[1,3],0.98)
r4 = Robot('move','r4',[1,1],0.999)
r5 = Robot('move','r5',[1,1],0.995)

r6 = Robot('pickup','r3',[1,3],0.98)
r7 = Robot('pickup','r4',[1,1],0.999)
r8 = Robot('pickup','r5',[1,1],0.995)


# ---- READ how many robots per task  (numberOfrobots_jointtasks)
rr = []
for r in range(1,numberOfrobots_jointtasks+1):
	rr.append(eval("r{}".format(r)))

# -------- Tasks (allocation already done)
# Joint tasks
at1_room1 = AT("moveObj","at1_1", rr, 2, [2,2], 2)
at1_room2 = AT("moveObj","at1_2", rr, 2, [5,1], 2)
at1_room3 = AT("moveObj","at1_3", rr, 2, [5,1], 2)
at1_room4 = AT("moveObj","at1_4", rr, 2, [5,1], 2)
at1_room5 = AT("moveObj","at1_5", rr, 2, [5,1], 2)
at1_room6 = AT("moveObj","at1_6", rr, 2, [3,6], 2)
at1_room7 = AT("moveObj","at1_7", rr, 2, [2,2], 2)
at1_room8 = AT("moveObj","at1_8", rr, 2, [5,1], 2)
at1_room9 = AT("moveObj","at1_9", rr, 2, [5,1], 2)
at1_room10 = AT("moveObj","at1_10", rr, 2, [8,1], 2)
at1_room11 = AT("moveObj","at1_11", rr, 2, [5,1], 2)
at1_room12 = AT("moveObj","at1_12", rr, 2, [5,9], 2)


# ---- READ INPUTS
# --- numberOfrobots_jointtasks = YY #do NOT exceed 5
rr = [] # eg. rr = [r1,r2]
for r in range(1,numberOfrobots_jointtasks+1):
	rr.append(eval("r{}".format(r)))
# --- numberOfjointtasks = XX
atomictasks = []
for i in range(1,numberOfjointtasks+1):
	atomictasks.append( eval("at1_room{}".format(i) ))
print(atomictasks)


# Compound taks
#3
room3 = [0,1]
at4_3 = AT("notify", "at4_3", r1, 1, room3, 2)
at2_3 = AT("floor",	 "at2_3", r1, 1, room3, 2)
at3_3 = AT("desinfect", "at3_3", r1, 1, room3, 2)
ct1_3 = CT("cleanRroom", [at2_3,at3_3], True)
ct2_3 = CT("cleanPatient",[at4_3,ct1_3], False)
#4
room4 = [0,1]
at4_4 = AT("notify", "at4_4", r1, 1, room4, 2)
at2_4 = AT("floor",	 "at2_4", r1, 1, room4, 2)
at3_4 = AT("desinfect","at3_4", r1, 1, room4, 2)
ct1_4 = CT("cleanRroom",  [at2_4,at3_4], True)
ct2_4 = CT("cleanPatient", [at4_4,ct1_4], False)
#5
room5 = [0,1]
at4_5 = AT("notify", "at4_5", r1, 1, room5, 2)
at2_5 = AT("floor",	"at2_5", r1, 1, room5, 2)
at3_5 = AT("desinfect", "at3_5", r1, 1, room5, 2)
ct1_5 = CT("cleanRroom", [at2_5,at3_5], True)
ct2_5 = CT("cleanPatient", [at4_5,ct1_5], False)
#6
room6 = [0,1]
at4_6 = AT("notify", "at4_6", r1, 1, room6, 2)
at2_6 = AT("floor",	"at2_6", r1, 1, room6, 2)
at3_6 = AT("desinfect","at3_6", r1, 1, room6, 2)
ct1_6 = CT("cleanRroom", [at2_5,at3_5], True)
ct2_6 = CT("cleanPatient",[at4_5,ct1_5], False)



# ---------- Problem Parameters
#totaltime = 24
#atomictasks = [at1_room1,at1_room2,at1_room3,at1_room4,at1_room5]

# -----------Calculate Problem features




# -------- MDP creation
# File
f = open("mdp.txt", "w")
f.write("mdp\n")
f.write("const int TT={};\n".format(totaltime))
# AT time
for at in atomictasks:
	if type(at.robot)==list: # joint tasks
		for r in at.robot:
			f.write("const int {}{}Time ={};\n".format(r.id , at.id , at.time))
	else:
		f.write("const int {}{}Time ={};\n".format(at.robot.id , at.id , at.time))
#AT Probab
for at in atomictasks:
	if type(at.robot)==list: # joint tasks
		for r in at.robot:
			f.write("const double {}{}prob ={};\n".format(r.id , at.id , r.prob))
	else:
		f.write("const double {}{}prob ={};\n".format(at.robot.id , at.id , at.robot.prob))

#Robots in allocation
at_robots= []
for at in atomictasks:
	if type(at.robot)==list:
		at_robots.extend(at.robot)
	else:
		at_robots.append(at.robot)
#print(at_robots)
r_ids=[]
for r in at_robots:
	r_ids.append(r.id)
r_ids = list(set(r_ids))
print('Robots in allocation: ',r_ids)

#Tasks assigned to each robot
r_tasks = {}
for at in atomictasks:
	if type(at.robot)==list:
		for r in at.robot:
			try:
				r_tasks[r.id].append(at)
			except:
				r_tasks[r.id] = [at]
	else:
		try:
			r_tasks[r.id].append(at)
		except:
			r_tasks[r.id] = [at]

print(r_tasks)


#Travel cost
for r in r_tasks.keys():
	for at in r_tasks[r]:
		cost = travelcost(eval(r).loc,at.loc)
		f.write("const int {}travel_0_to_{}={};\n".format(r,at.id,cost))

		for at2 in r_tasks[r]:
			if at!=at2:
				cost = travelcost(at.loc,at2.loc)
				f.write("const int {}travel_{}_to_{}={};\n".format(r,at.id,at2.id,cost))

# Travel from any location
f.write("\n//travel cost from any location\n")
for r in r_tasks.keys():
	for at in r_tasks[r]:
		f.write("formula {}travelTO{} ".format(r,at.id))
		loc = 0
		f.write("= ({}Loc={} ? {}travel_0_to_{} : ".format(r,loc,r,at.id))
		string1 = ""
		string2 = ""
		for at_init in r_tasks[r]:
			if at != at_init:
				loc+=1
				string1 += "({}Loc={} ? {}travel_{}_to_{} : ".format(r,loc,r,at_init.id,at.id)
				string2 += ")"
		
		string1 += "0)"
		f.write(string1 + string2 + ";\n")

# Done and fail
f.write("formula done = end;\n")
f.write("formula fail = ")
s = "("
for r in r_tasks.keys():
	s+= "{}Fail=1 |".format(r)
f.write(s[:-2]+");\n")

# Time constraints
for r in r_tasks.keys():
	for at in r_tasks[r]:
		f.write("formula {}TimeOk_{} = TT>={}Time+{}{}Time+{}travelTO{};\n".format(r,at.id,r,r,at.id,r,at.id))

# Scheduler
f.write("\nmodule scheduler\n");
for at in atomictasks:
	f.write("  {}:bool;\n".format(at.id))
f.write("  end:bool;//endmission\n")
# Scheduler transitions
for at in atomictasks:
	if type(at.robot)==list:
		f.write("  [DO{}] !{} -> ({}'=true);\n".format(at.id,at.id,at.id))
#Get time
f.write("  [getTime] ")
for at in atomictasks:
	f.write("{} & ".format(at.id))
f.write("!end->(end'=true);\n")
f.write("endmodule\n")

#robot modules
for r in r_tasks.keys():
	f.write("\nmodule {}\n".format(r))
	robotModule(r,r_tasks,atomictasks,f)
	f.write("endmodule\n")

#rewards
f.write("rewards \"time\"\n")
f.write("  [getTime] true: ".format(at.id))
s=""
for r in r_tasks.keys():
	s+="{}Time + ".format(r)
f.write(s[:-3]+";\n")
f.write("endrewards")

f.close()

