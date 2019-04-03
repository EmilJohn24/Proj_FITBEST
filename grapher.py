from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph.output import GraphvizOutput
from pycallgraph import GlobbingFilter
import main

config = Config(max_depth=5)
graphviz = GraphvizOutput(output_file='filter_max_depth.png')
config.trace_filter = GlobbingFilter(exclude=[
    'pycallgraph.*',
    '*.secret_function',
    'open',
    'print',
    '*.append',
    '*.keys',
    '*.items',
    '*.close',
    '_find_and_load',
    '*._find_and_load'
    
])

graphviz = GraphvizOutput(output_file='filter_exclude.png')

with PyCallGraph(output=graphviz, config=config):
    main.main()
