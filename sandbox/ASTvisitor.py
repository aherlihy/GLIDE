#!/usr/bin/python
# This class represents the visitor that will go through and parse the AST generated from the user's code. 
# There are two ways to limit functionality: I could specify the visitors' behavior for certain nodes that the user shouldn't invoke
# Or, I could specify the visitors' behavior for nodes that are allowed (since this is smaller)
    # I would also override generic visitor so that everything else would flag the code as dangerous
# Concievably, if there's time, I could modify the user's code so that anything dangerous was just removed as opposed to just throwing an error.
# But that's totally it's own nest of worms.

# NOTE: The python library pages don't have a lot of information when it comes to implementing this stuff, so I found a tutorial on the AST module at http://codemonkeytips.blogspot.com/2010/08/simple-python-nodevisitor-example.html

# @author aherlihy
import ast
import sys
class ASTvisitor(ast.NodeVisitor):
    #init doesn't need to do anything
    def __init__(self):
        pass
    # The AST module handles visitors by providing a generic_visit method that does nothing to a node and recurses on it's children.
    # Type-specific visitors can be defined by writing a function 'visit_<classname>'
    # When generic_visit is called on a node and a type-specific visitor is defined for that node, the type-specific visitor will be called instead.
    # However every visitor recurses on it's children using generic_visit, since the child's type is necessarily known by the parent.
    # Here I've override generic_visit to print out the name of the node (for debugging). Note that my generic_visit then calls the super's generic_visit to continue the recursive tree traversal
    def generic_visit(self, node):
        file = open("tsa", "a")
        file.write("node type: " + type(node).__name__ + "\n")
        file.close()
        ast.NodeVisitor.generic_visit(self, node) # essentially a call to super
    def visit_Import(self, node):
        file = open("astoutput", "a")
        file.write("Import|LINE:"+ str(node.lineno)+ "|FROM:")
#        file.write("Import:FROM:"+ node.module+ "\n")
        for name in node.names:
            file.write(name.name + "|")
        file.write("\n")
        file.close()
        ast.NodeVisitor.generic_visit(self, node) # can recurse using super because it will be overriden by the above def
    def visit_ImportFrom(self, node):
        file = open("astoutput", "a")
        file.write("ImportFrom|LINE:"+ str(node.lineno))
        file.write("|FROM:"+ node.module+ "|NAMES:")
        for name in node.names:
            file.write(name.name + "|")
        file.write("\n")
        file.close()
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Name(self, node):
        file = open("tsa", "a")
        file.write("Name|LINE:" + str(node.lineno) + "|NAME:"+ node.id + "\n")
        file.close()
        ast.NodeVisitor.generic_visit(self, node)
#    def visit_Call(self, node):
#        file=open("tsa", "a")
#        file.write("Call|LINE:" + str(node.lineno) + "|NAME:" + str(node.func.value) + "|CTX:" + str(node.func.ctx) + "\n")
#        for l in node._fields:
#           print l
#        print node.func.id
#        print node.func.ctx
#        file.close()
#        ast.NodeVisitor.generic_visit(self, node)
#print "visiting..."
#visitor = ASTvisitor()
#file = open(sys.argv[1], "r")
#usrcode = file.read()
#tree = ast.parse(usrcode)
#visitor.generic_visit(tree)
#print("dumping...")
#print ast.dump(tree, annotate_fields=True, include_attributes=False)

