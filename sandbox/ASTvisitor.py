#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# This class represents the visitor that will go through and parse the AST generated from the user's code. 
# There are two ways to limit functionality: I could specify the visitors' behavior for certain nodes that the user shouldn't invoke
# Or, I could limit any external function calls. I chose to go this way since the number of nodes that could be potentially dangerous is enormous.
# This pattern is extendible to eventually recognize dangerous code and just remove it instead of blocking it from running.
#    It was decided that this is was worth the time and energy it would take to make it work. If the user is attempting to do something they shouldn't, it's unlikely that they are part of our target audience. Also, there is no guarentee that the code would work with certain parts removed.

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
        file.write("node type: " + type(node).__name__)
        if (hasattr(node,'lineno')):
            file.write(" linenumber:" + str(node.lineno))
        file.write("\n")
        file.close()
        ast.NodeVisitor.generic_visit(self, node) # essentially a call to super
    def visit_Import(self, node):
        file = open("astoutput", "a")
        file.write("\nImport|LINE:"+ str(node.lineno)+ "|FROM:")
        for name in node.names:
            file.write(name.name + "|")
        file.write("\n")
        file.close()
        ast.NodeVisitor.generic_visit(self, node) # can recurse using super because it will be overriden by the above def
    def visit_ImportFrom(self, node):
        file = open("astoutput", "a")
        if not (str(node.lineno)=="2" or str(node.lineno)=="3"):
            file.write("\nImportFrom|LINE:"+ str(node.lineno))
            file.write("|FROM:"+ node.module+ "|NAMES:")
            for name in node.names:
                file.write(name.name + "|")
            file.write("\n")
        file.close()
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Name(self, node):
        file = open("tsa", "a")
        out=open("astoutput", "a")
        file.write("Name|LINE:" + str(node.lineno) + "|NAME:"+ node.id + "\n")
        out.write("|NAME:"+ node.id)
        out.close()
        file.close()
        ast.NodeVisitor.generic_visit(self, node)
        return node.id
    def visit_Call(self, node):
        file=open("tsa", "a")
        out=open("astoutput", "a")
        out.write("\nCall|LINE:" + str(node.lineno))
        file.write("Call|LINE:" + str(node.lineno)+"\n")
        file.close()
        out.close()
        ast.NodeVisitor.generic_visit(self, node)
        out=open("astoutput", "a")
        out.write("\n")
        out.close()
    def visit_Attribute(self, node):
        file = open("tsa", "a")
        out = open("astoutput", "a")
        out.write("|ATTRIBUTE:" + node.attr)
        file.write("attribute node: " + node.attr + "\n")
        out.close()
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Load(self, node):
        pass#Just because they're annoying
