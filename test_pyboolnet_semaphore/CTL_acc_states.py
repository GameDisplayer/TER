import PyBoolNet.ModelChecking as pm

def check_smv(FnameSMV):

    print("Test sur le fichier :", FnameSMV, "\n")
    #if (pm.check_smv(FnameSMV)):
    print(pm.check_smv_with_acceptingstates(FnameSMV))

    print(pm.check_smv_with_counterexample(FnameSMV))

print(check_smv("semaphoreCTL1.smv"))
print(check_smv("semaphoreCTL2.smv"))
