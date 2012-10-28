import compile_less
import os

compile_less.compile_less([os.path.join(os.getcwd(),"public","static")])