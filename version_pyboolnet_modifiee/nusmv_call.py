import PyBoolNet
import os, sys
import tempfile
import subprocess

def check_primes_with_acceptingstates(Primes, Update, InitialStates, CTLSpec, DynamicReorder=True, ConeOfInfluence=True, Silent=True):
	"""
	Calls :ref:`installation_nusmv` to check whether the *CTLSpec* is true or false in the transition system defined by *Primes*,
	the *InitialStates* and *Update*.
	The remaining arguments are :ref:`installation_nusmv` options, see the manual at http://nusmv.fbk.eu for details.
	See :ref:`primes2smv` and :ref:`Sec. 3.4 <sec:model_checking>` for details on model checking with |Software|.
	The accepting states are a dictionary with the following keywords:
		* `INIT`: a Boolean expression for the initial states, or `None`, see note below
		* `INIT_SIZE`: integer number of initial states, or `None`, see note below
		* `ACCEPTING`: a Boolean expression for the accepting states
		* `ACCEPTING_SIZE`: integer number of accepting states
		* `INITACCEPTING`: a Boolean expression for the intersection of initial and accepting states, or `None`, see note below
		* `INITACCEPTING_SIZE`: integer number of states in the intersection of initial and accepting states, or `None`, see note below
	.. note::
		*DisableReachableStates* is enforced as the accepting states are otherwise over-approximated.
	.. note::
		If the *CTLSpec* is equivalent to either `TRUE` or `FALSE` then NuSMV will not compute the initial states,
		because it does not have to to find out what the *Answer* to the query is.
		In that case the four values that involve the initial states are set to `None`.
	**arguments**:
		* *Primes*: prime implicants
		* *Update* (str): the update strategy, either *"synchronous"*, *"asynchronous"* or *"mixed"*
		* *InitialStates* (str): a :ref:`installation_nusmv` expression for the initial states, including the keyword *INIT*
		* *CTLSpec* (str): a :ref:`installation_nusmv` formula, including the keyword *CTLSPEC*
		* *DynamicReorder* (bool): enables dynamic reordering of variables (*-dynamic*)
		* *ConeOfInfluence* (bool): enables cone of influence reduction using *-coi*
		* *Silent* (bool): print infos to screen
	**returns**:
		* *Answer, AcceptingStates* (bool, dict): result of query with accepting states
	**example**::
		>>> init = "INIT TRUE"
		>>> update = "asynchronous"
		>>> spec = "CTLSPEC AF(EG(v1&!v2))"
		>>> answer, accepting = check_primes_with_acceptingstates(primes, update, init, spec)
		>>> accepting["INITACCEPTING"]
		'v1 | v3'
	"""

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


# basic model checking
primes = PyBoolNet.Repository.get_primes("remy_tumorigenesis")
init = "INIT TRUE"
spec = "CTLSPEC DNA_damage -> AG(EF(Apoptosis_medium))"

# model checking with accepting states
answer, accepting = check_primes_with_acceptingstates(primes, "asynchronous", init, spec, Silent=False)
#print(answer, accepting)
for key, value in accepting.items():
    print("{} = {}".format(key, value))
