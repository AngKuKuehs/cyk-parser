# CYK-Parser
Python Implementation of error-correcting CYK parsers with items and error metrics.

## Parsers
General steps to use parsers:
<ol>
<li>Instatiate a config object for the parser.</li>
<li>Load initial items and productions from relevant grammar.</li>
<li>Load file and convert file into a string of tokens OR instantiate sentence.</li>
<li>Call relevant `parse` function.</li>
<li>Save parse tree from symbol chart OR save parse tree.</li>
</ol>

### CYK Parser
A CYK parser that returns a symbol chart and an item chart.

Parse trees associated with each symbol can be found alongside the symbol in the symbol chart.

Example of usage: examples/parse_basic_api

To run example: `python -m examples.parse_basic_api`

### Error-Correcting CYK Parser
An error-correcting CYK parser that returns either a parse tree or `None`.

Example of usage: examples/correct_hello_world.py

To run example: `python -m examples.correct_hello_world`

### Patience Error-Correcting Parser
An alternate error-correcting CYK parser loosely inspired by patience diff. Returns a tuple of a list of parse trees, original sentence, and parse status.

Example of usage: examples/feedback_bracket_correction.py

To run example: `python -m examples.feedback_bracket_correction`
