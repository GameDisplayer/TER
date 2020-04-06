blocks = """-> State: 1.1 <-
    semaphore = FALSE
    proc1.state = idle
    proc2.state = idle
  -> Input: 1.2 <-
    _process_selector_ = proc1
    running = FALSE
    proc2.running = FALSE
    proc1.running = TRUE
  -- Loop starts here
  -> State: 1.2 <-
    proc1.state = entering
  -> Input: 1.3 <-
    _process_selector_ = proc2
    proc2.running = TRUE
    proc1.running = FALSE
  -- Loop starts here
  -> State: 1.3 <-
  -> Input: 1.4 <-
  -> State: 1.4 <-
    proc2.state = entering
  -> Input: 1.5 <-
  -> State: 1.5 <-
    semaphore = TRUE
    proc2.state = critical
  -> Input: 1.6 <-
    _process_selector_ = proc1
    proc2.running = FALSE
    proc1.running = TRUE
  -> State: 1.6 <-
  -> Input: 1.7 <-
    _process_selector_ = proc2
    proc2.running = TRUE
    proc1.running = FALSE
  -> State: 1.7 <-
    proc2.state = exiting
  -> Input: 1.8 <-
  -> State: 1.8 <-
    semaphore = FALSE
    proc2.state = idle
	"""



counterexample = []
last_state = False


blocks = blocks.split('-> ')
for block in blocks:
	lines = block.split('\n')
	lines = [x.strip() for x in lines]
	lines = [x for x in lines if '=' in x]
	lines = [x for x in lines if '_IMAGE' not in x]
	lines = [x for x in lines if '_STEADY' not in x]
	lines = [x for x in lines if not x.startswith('SUCCESSORS')]
	lines = [x for x in lines if not x.startswith('STEADYSTATE')]
	lines = [x for x in lines if x!=[]]

	if lines:
		if last_state:
			state = last_state.copy()
		else:
			state = {}

		for line in lines:
			name, value = line.split(' = ')
			print("La ligne qui provoque l'erreur est : ", line)
			assert(value in ['TRUE','FALSE'])
			state[name] = 1 if value== 'TRUE' else 0

		counterexample.append(state)
		last_state = state

print(tuple(counterexample))
