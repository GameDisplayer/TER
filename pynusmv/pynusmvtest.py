import pynusmv
pynusmv.init.init_nusmv()
pynusmv.glob.load_from_file("mucusOperon.smv")
pynusmv.glob.compute_model()
fsm = pynusmv.glob.prop_database().master.bddFsm
print(fsm)

prop = pynusmv.glob.prop_database()[0]
print(prop)

spec = prop.expr
print(spec)

bdd = pynusmv.mc.eval_ctl_spec(fsm, spec) & fsm.reachable_states
bdd

print("BDD Manipulation\n")

print("reachable states from initial states :")
#init
print(fsm.count_states(fsm.init))
for state in fsm.pick_all_states(fsm.init):
	print(state.get_str_values())

print("\ntransition relations pre or post-images :")
#transition relation
for state in fsm.pick_all_states(fsm.post(fsm.init)):
	print(state.get_str_values())

print("\nspecial case of transition relations co-exist :")
#next
from pynusmv.fsm import BddTrans
trans = BddTrans.from_string(fsm.bddEnc.symbTable,"next(F_operon) = 0")
for state in fsm.pick_all_states(trans.post(fsm.init)):
	print(state.get_str_values())

print("\nFrom the BDD-encoded FSM fsm and the specification spec, we call the eval_ctl_spec function to get all the states of fsm satisfying spec. Conjuncted with the set of reachables states of the model, we get bdd, a BDD representing all the reachable states of fsm satisfying spec. Finally, from this BDD we extract all the single states and display them, that is, we display, for each of them, the value of each state variable of the model :")
satstates = fsm.pick_all_states(bdd)
for state in satstates:
	print(state.get_str_values())
