import PyBoolNet


#_______________bnet to primes____________________
primes = PyBoolNet.Repository.get_primes("raf")

#_______________state transition graph______________________
PyBoolNet.StateTransitionGraphs.create_image(primes, "asynchronous", "stg.pdf")

#___________________________basins________________________

attrs = PyBoolNet.Attractors.compute_json(primes, "asynchronous")

PyBoolNet.Basins.compute_basins(attrs)
PyBoolNet.Attractors.save_json(attrs, "attrs.json")
PyBoolNet.Basins.create_barplot(attrs, "basin_barplot.pdf")
PyBoolNet.Basins.create_piechart(attrs, "basin_piechart.pdf")

#_____________________commitment sets and pie_________________

diag = PyBoolNet.Commitment.compute_diagram(attrs)
PyBoolNet.Commitment.diagram2image(diag, "commitment_diag.pdf")
PyBoolNet.Commitment.create_piechart(diag, "commitment_pie.pdf")
