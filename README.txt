# Overview

This directory contains the automata generation code for our submission "Pacemaker Requirements in Duration Calculus" (number 232).

# Installation

pip install -r requirements.txt

# Usage

Simulate conjunction of all generated automata and execute system on input signals.
```
python src/simulate_system.py
```
The above code reads input from input/url_holdoff.json and simulates the system using our method and writes the values of the all the signals at every time step in output/url_holdoff.txt. The code plots some of these signals across time.
The current setup demonstrates URL Holdoff explained in the paper. For visualizing this demonstration, we have scaled down the constants, with consultation from the domain expert such that the captured behaviour is not altered.


# Optional

If you want to generate the automata (specs/<spec_name>/auto*.py files) corresponding to each specification (specs/<spec_name>/*.dc files) execute
```
python src/spec_to_automata.py <path_to_spec_dc_file>
```

We use the "dcvalid" tool provided under ./external to generate automata from specification. To install this tool, follow the instructions in ./external/dcvalid/README. The tool is tested on Ubuntu 16.04 and 18.04 (x_86 64 bit architecture).

The above code expands macros (if used) in the dcvalid syntax, and generates the automata using the dcvalid tool.
For example, given a specification at ./specs/8/PAAR.dc, the expanded macro is written at ./specs/8/macro_expanded/PAAR.dc and the generated automata is written at ./specs/8/auto_PAAR.py.

To generate automata for all specifications, use the following script.
```bash
bash src/generate_automata_from_specs.sh
```

