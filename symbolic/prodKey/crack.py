import angr
import claripy
from pwn import *

TARGET = 0x400deb

chars = [claripy.BVS(f"c_{i}", size=8) for i in range(32)]
flag = claripy.Concat(*chars)

proj = angr.Project("./prodkey")
initial_state = proj.factory.entry_state(stdin=flag)

#constraint the symbolic chars to be printable characters
for char in chars:
	initial_state.solver.add(char >= 0x20)
	initial_state.solver.add(char <= 0x7e)

simgr = proj.factory.simulation_manager(initial_state)

solution = ""
while len(simgr.active) > 0:
	print(simgr, simgr.active)
	simgr.explore(find=TARGET, n=1, num_find=1)
	if len(simgr.found) > 0:
		solution = simgr.found[0].solver.eval(flag)
		print(solution)
		proj.terminate_execution()
		break
