## Running timeScript.py
$python timeScript.py

Ensure that both JSYN and Z3Prover are installed onto the computer. Before running the script, navigate to ../dtsynth and run the command

	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./lib/z3/bin/

The script prints the times reported by JSynth and DTSynth (total computation time only) into an excel file (data.csv) stored in the /scripts folder (the same folder that the script is in). The data is stored in the following format

	JSynth Benchmark	Time(s)			DTSynth Benchmark	Time(s)
	{Name of benchmark}	{Time reported}		{Name of benchmark}	{Time reported}
	.
	.
	.

The names of both the JSynth benchmark and DTSynth benchmark are stored because there is not a one-to-one correspondence between names (ie the JSynth box.lus benchmark is called boxGame.json for DTSynth).
