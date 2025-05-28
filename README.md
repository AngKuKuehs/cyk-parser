# CYK-Parser
Python Implementation of error-correcting CYK parsers with items and error metrics.

## Parsers
### CYK Parser
A CYK parser that returns a symbol chart and an item chart.

Parse trees associated with each symbol can be found alongside the symbol in the symbol chart.

To use the parser:
<ol>
<li>Instatiate a config object for the parser.</li>
<li>Load initial items and productions from relevant grammar.</li>
<li>Load file and convert file into a string of tokens OR instantiate sentence.</li>
<li>Call `parse` from cyk_parser.py with relevant arguments.</li>
<li>Save parse tree from symbol chart.</li>
</ol>

Example of usage: examples/parse_basic_api

To run example: `python -m examples.parse_basic_api`

### Error-Correcting CYK Parser
An error-correcting CYK parser that returns either a parse tree or `None`.

To use the parser:
<ol>
<li>Instatiate a config object for the parser with relevant error limits.</li>
<li>Load initial items and productions from relevant grammar.</li>
<li>Load file and convert file into a string of tokens OR instantiate sentence.</li>
<li>Call `ec_parse` from error_parser.py with relevant arguments.</li>
<li>Save parse tree.</li>
</ol>

Example of usage: examples/correct_hello_world.py

To run example: `python -m examples.correct_hello_world`

### Patience Error-Correcting Parser
An alternate error-correcting CYK parser loosely inspired by patience diff. Returns a tuple of a list of parse trees, original sentence, and parse status.

To use the parser:
<ol>
<li>Instatiate a config object for the parser with relevant error limits.</li>
<li>Load initial items and productions from relevant grammar.</li>
<li>Load file and convert file into a string of tokens OR instantiate sentence.</li>
<li>Call `patience_parse` from patience_parser.py with relevant arguments.</li>
<li>Save parse trees.</li>
</ol>

Example of usage: examples/feedback_bracket_correction.py

To run example: `python -m examples.feedback_bracket_correction`
