import PyBoolNet
import os, sys
import tempfile
import subprocess
import networkx
import itertools
import random
import operator
import functools
import networkx

def project_attractors(Attractors, Names):
	result = set()
	for space in Attractors:
		projection = tuple((k,v) for k,v in sorted(space.items()) if k in Names)
		result.add(projection)

	result = [dict(x) for x in result]

	return result

def lift_attractors(Attractors, Projection):
	return [x for x in Attractors for y in Projection if PyBoolNet.Utility.Misc.dicts_are_consistent(x,y)]


def cartesian_product(Diagrams, Factor, EdgeData):
	"""
	creates the cartesian product of *Diagrams*.
	"""

	result = networkx.DiGraph()

	# create nodes
	nodes = [x.nodes(data=True) for x in Diagrams]

	for product in itertools.product(*nodes):
		data = {}
		data["size"] = functools.reduce(operator.mul,[x["size"] for _,x in product]) * Factor
		data["formula"] = " & ".join("(%s)"%x["formula"] for _,x in product)

		attrs = [x["attractors"] for _,x in product]
		attrs = list(itertools.product(*attrs))
		attrs = [PyBoolNet.Utility.Misc.merge_dicts(x) for x in attrs]
		data["attractors"] = attrs

		node = tuple(x for x,_ in product)

		result.add_node(node)
		for key, value in data.items():
			result.node[node][key] = value

	# create edges
	for source in result.nodes():
		for s, diagram in zip(source, Diagrams):
			factor = result.node[source]["size"] / diagram.node[s]["size"]
			for _, t, data in diagram.out_edges(s,data=True):

				data = {}
				basic_formula = ["(%s)"%g.node[x]["formula"] for x,g in zip(source,Diagrams) if not g==diagram]
				data["EX_size"]	= factor * diagram.adj[s][t]["EX_size"]
				formula = basic_formula + ["(%s)"%diagram.adj[s][t]["EX_formula"]]
				data["EX_formula"]  = " & ".join(formula)

				if EdgeData:
					data["EF_size"]	 = factor * diagram.adj[s][t]["EF_size"]
					formula = basic_formula + ["(%s)"%diagram.adj[s][t]["EF_formula"]]
					data["EF_formula"]  = " & ".join(formula)

				target = tuple(x if not g==diagram else t for x,g in zip(source,Diagrams))

				result.add_edge(source, target)
				for key, value in data.items():
					result.edges[source, target][key] = value

	# relabel nodes
	result = networkx.convert_node_labels_to_integers(result)

	return result


def diagrams_are_equal(Diagram1, Diagram2):
	"""
	removes for formulas, which are different for naive / product diagrams.
	"""

	g1 = Diagram1.copy()
	g2 = Diagram2.copy()

	for g in [g1,g2]:
		for x in g.nodes():
			g.node[x].pop("formula")
		for x,y in g.edges():
			if "border_formula" in g.adj[x][y]:
				g.adj[x][y].pop("border_formula")
				g.adj[x][y].pop("finally_formula")

	em = lambda x,y:x==y

	return networkx.is_isomorphic(g1,g2,edge_match=em)


def compute_diagram(AttrJson, FnameImage=None, FnameJson=None, EdgeData=False, Silent=False):

	Primes = AttrJson["primes"]
	Update = AttrJson["update"]

	Subspaces = []
	for x in AttrJson["attractors"]:
		if x["mintrapspace"]["is_univocal"] and x["mintrapspace"]["is_faithful"]:
			Subspaces.append(x["mintrapspace"]["dict"])
		else:
			Subspaces.append(x["state"]["dict"])

	if not Silent:
		print("Commitment.compute_diagram(..)")

	size_total = PyBoolNet.StateTransitionGraphs.size_state_space(Primes)

	if len(Subspaces)==1:
		if not Silent:
			print(" single attractor, trivial case.")
		diagram = networkx.DiGraph()
		counter_mc = 0

		diagram.add_node("0")
		diagram.node["0"]["attractors"]	= Subspaces
		diagram.node["0"]["size"]		= size_total
		diagram.node["0"]["formula"]	= "TRUE"

	else:

		igraph = PyBoolNet.InteractionGraphs.primes2igraph(Primes)
		outdags = PyBoolNet.InteractionGraphs.find_outdag(igraph)

		attractor_nodes = [x for A in Subspaces for x in A]
		critical_nodes = PyBoolNet.Utility.DiGraphs.ancestors(igraph, attractor_nodes)
		outdags = [x for x in outdags if not x in critical_nodes]

		igraph.remove_nodes_from(outdags)
		if not Silent:
			print(" excluding the non-critical out-dag nodes %s"%outdags)

		components = networkx.connected_components(igraph.to_undirected())
		components = [list(x) for x in components]
		if not Silent:
			print(" working on %i connected component(s)"%len(components))

		counter_mc = 0
		diagrams = []
		for component in components:
			subprimes = PyBoolNet.PrimeImplicants.copy(Primes)
			PyBoolNet.PrimeImplicants.remove_all_variables_except(subprimes, component)

			attrs_projected = project_attractors(Subspaces, component)

			diagram, count = _compute_diagram_component(subprimes, Update, attrs_projected, EdgeData, Silent)
			counter_mc+=count

			diagrams.append(diagram)

		factor = 2**len(outdags)
		diagram = cartesian_product(diagrams, factor, EdgeData)

		for x in AttrJson:
			diagram.graph[x] = PyBoolNet.Utility.Misc.copy_json_data(AttrJson[x])


		nodes_sum = 0
		for x in diagram.nodes():
			projection = diagram.node[x]["attractors"]
			diagram.node[x]["attractors"] = lift_attractors(Subspaces, projection)
			nodes_sum+= diagram.node[x]["size"]

		if not nodes_sum==size_total:
			print("WARNING: commitment diagram does not partition the state space, this may be due to rounding of large numbers.")

		sorted_ids = sorted(diagram, key=lambda x: diagram.node[x]["formula"])
		mapping = {x:str(sorted_ids.index(x)) for x in diagram}
		networkx.relabel_nodes(diagram,mapping,copy=False)

	if not Silent:
		print(" total executions of NuSMV: %i"%counter_mc)


	if FnameImage:
		diagram2image(diagram, FnameImage=FnameImage, StyleInputs=True, StyleSplines="curved", StyleEdges=EdgeData, StyleRanks=True, FirstIndex=1)

	if FnameJson:
		save_diagram(diagram, FnameJson)

	return diagram

def check_primes_with_acceptingstates(Primes, Update, InitialStates, CTLSpec, DynamicReorder=True, ConeOfInfluence=True, Silent=False):
	assert(CTLSpec[:7] == "CTLSPEC")

	#print_warning_accstates_bug(Primes, CTLSpec)

	cmd = ["NuSMV"]
	cmd+= ['-dcx']
	cmd+= ['-a','print']

	if DynamicReorder:
		cmd+= ['-dynamic']
	if ConeOfInfluence:
		cmd+= ['-coi']

	# enforced to ensure accepting states are correct
	cmd+= ['-df']

	tmpfile = tempfile.NamedTemporaryFile(delete=False, prefix="pyboolnet_")
	tmpfname = tmpfile.name
	if not Silent:
		print("created %s"%tmpfname)
	tmpfile.close()
	smvfile = PyBoolNet.ModelChecking.primes2smv(Primes, Update, InitialStates, CTLSpec, FnameSMV=tmpfname, Silent=True)

	cmd+= [tmpfname]

	print("CMD", cmd)
	try:
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print(proc)
	except Exception:
		print("could not start process for nusmv")
		print("cmd: %s"%' '.join(cmd))
		raise Exception

	out, err = proc.communicate()
	out = out.decode()

	return PyBoolNet.ModelChecking.nusmv_handle(cmd, proc, out, err, DisableCounterExamples=True, AcceptingStates=True)

def _compute_diagram_component(Primes, Update, Subspaces, EdgeData, Silent):


	assert(Update in PyBoolNet.StateTransitionGraphs.UPDATE_STRATEGIES)
	assert(Primes)

	# create nodes
	counter_mc = 0
	node_id = 0
	worst_case_nodes = 0
	inputs = PyBoolNet.PrimeImplicants.find_inputs(Primes)

	states_per_case = PyBoolNet.StateTransitionGraphs.size_state_space(Primes, FixedInputs=True)

	diagram = networkx.DiGraph()

	if not Silent:
		print(" _compute_diagram_component(..)")
		print("  inputs: {x} ({y})".format(x=len(inputs), y=", ".join(inputs)))
		print("  combinations:  %i"%2**len(inputs))

	for i, combination in enumerate(PyBoolNet.PrimeImplicants.input_combinations(Primes)):

		attr = [x for x in Subspaces if PyBoolNet.StateTransitionGraphs.A_is_subspace_of_B(Primes, A=x, B=combination)]

		worst_case_nodes+= 2**len(attr)-1
		states_covered = 0
		specs = [PyBoolNet.TemporalLogic.subspace2proposition(Primes, x) for x in attr]
		vectors = len(attr)*[[0,1]]
		vectors = list(itertools.product(*vectors))
		random.shuffle(vectors)

		combination_formula = PyBoolNet.TemporalLogic.subspace2proposition(Primes, combination)

		if not Silent:
			print("  input combination %i, worst case #nodes: %i"%(i,2**len(attr)-1))

		for vector in vectors:
			if sum(vector)==0: continue
			if states_covered==states_per_case:
				if not Silent:
					print("  avoided executions of NuSMV due to state counting")
				break

			if len(vector)==1:
				data = {"attractors":   attr,
						"size":		 	states_per_case,
						"formula":	  	combination_formula}

			else:

				init = "INIT %s"%combination_formula

				reach = ["EF(%s)"%x for flag, x in zip(vector, specs) if flag]
				reach_all  = " & ".join(reach)
				reach_some = " | ".join(reach)
				spec = "CTLSPEC %s & AG(%s)"%(reach_all,reach_some)

				answer, accepting = check_primes_with_acceptingstates(Primes, Update, init, spec)
				print("Accepting States Call 1")
				counter_mc+=1

				data = {"attractors":   [x for flag,x in zip(vector, attr) if flag],
						"size":		 	accepting["INITACCEPTING_SIZE"],
						"formula":	  	accepting["INITACCEPTING"]}

			if data["size"]>0:
				diagram.add_node(node_id)
				for key, value in data.items():
					diagram.node[node_id][key] = value
				node_id+=1
				states_covered+= data["size"]

	if not Silent:
		perc = "= %.2f%%"%(100.*diagram.order()/worst_case_nodes) if worst_case_nodes else ""
		print("  worst case #nodes: %i"%worst_case_nodes)
		print("  actual nodes: %i %s"%(diagram.order(),perc))

	# list potential targets
	potential_targets = {}
	for source, source_data in diagram.nodes(data=True):
		succs = []
		for target, target_data in diagram.nodes(data=True):
			if source==target: continue
			if all(x in source_data["attractors"] for x in target_data["attractors"]):
				succs.append((target,target_data))

		potential_targets[source] = succs

	if not Silent:
		worst_case_edges = sum(len(x) for x in potential_targets.values())
		print("  worst case #edges: %i"%worst_case_edges)

	# create edges
	for source, source_data in diagram.nodes(data=True):
		for target, target_data in potential_targets[source]:

			init = "INIT %s"%source_data["formula"]
			spec = "CTLSPEC EX(%s)"%target_data["formula"]
			answer, accepting = check_primes_with_acceptingstates(Primes, Update, init, spec)
			print("Accepting States Call 2")
			counter_mc+=1

			data = {}
			data["EX_size"] = accepting["INITACCEPTING_SIZE"]
			data["EX_formula"] = accepting["INITACCEPTING"]

			if data["EX_size"]>0:

				if EdgeData:
					if len(potential_targets[source])==1:
						data["EF_size"] = source_data["size"]
						data["EF_formula"] = source_data["formula"]

					else:
						spec = "CTLSPEC E[%s U %s]"%(source_data["formula"],target_data["formula"])
						answer, accepting = check_primes_with_acceptingstates(Primes, Update, init, spec)
						print("Accepting States Call 3")
						counter_mc+=1

						data["EF_size"] = accepting["INITACCEPTING_SIZE"]
						data["EF_formula"] = accepting["INITACCEPTING"]

				diagram.add_edge(source, target)
				for key, value in data.items():
					diagram.edges[source, target][key] = value

	if not Silent:
		perc = "= %.2f%%"%(100.*diagram.size()/worst_case_edges) if worst_case_edges else ""
		print("  actual edges: %i %s"%(diagram.size(),perc))
		print("  total executions of NuSMV: %i"%counter_mc)

	return diagram, counter_mc

primes = PyBoolNet.Repository.get_primes("raf")
attrs = PyBoolNet.Attractors.compute_json(primes, "asynchronous")
diag = compute_diagram(attrs)
print(diag)
