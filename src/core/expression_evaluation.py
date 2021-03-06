"""
Define EquationNode class, that holds the reference to variables in the ExpressionTrees.

Define the ExpressionTree class, that holds capabilities to process arbitrary operations among Quantity objects through the arrengement of EquationNodes in ExpressionTrees, and the later processment of them.
"""

from anytree import NodeMixin, RenderTree, PreOrderIter
import error_definitions as errors
import math_functions 

class base_(object):

    """
    Included for new-style class compability purposes only
    """

    pass

class ExpressionTree(base_, NodeMixin):

    """

    ExpressionTree definition, used for representation of the equations through almost-wirting syntax
    Eg: a() + b()*Exp(c()*Constant(1.,c.units**-1))

    Each Quantity object (eg: a,b,c) when called returns an ExpressionTree object containing appropriate EquationNode objects. When the expression trees are summed, they are merged accordingly to precedence orders.

    """

    def __init__(self, object_, parent=None):

        """
        Initial definitions

        :param EquationNode object_:
        Object contained in the current node of ExpressionTree

        :parent ExpressionTree parent:
        Parent node of ExpressionTree for the current node

        """

        super(self.__class__,self).__init__() # NodeMixin class instantiation

        self.object = object_

        self.parent = parent

    def __str__(self):

        """

        Print informations about current ExpressionTree for easy visualization

        """

        for pre,fill,node in RenderTree(self):

            print("%s%s" % (pre,node.object.name))

        return ""

    def __getitem__(self,item_name):

        """

        Return the EquationNode with name equivalent to 'item_name'

        TODO: Prevent for cases with name duplicity

        :param str item_name:
        Name of the EquationNode to be returned

        """


        if isinstance(item_name,str) != True:

            raise(errors.UnexpectedValueError("string"))

        else:

            for _1,_2, node in RenderTree(self):

                if node.object.name == item_name:

                    return(node.object)

    def _info_(self, verbosity_level = 2 ):

        #TODO: Change function to return specific atributes supplied by one list by the user

        for pre,fill,node in RenderTree(self):

            #1 - Only names
            #2 - Base_objects values
            #3 - Full dicts

            if verbosity_level == 3:

                try:

                    print("%s%s\n%s\n%s\n" % (pre,node.object.name, node.object__dict__,node.object.base_object.__dict__))

                except:

                    print("%s%s\n%s\n%s\n" % (pre,node.object.name,node.object.__dict__,"None"))   
            
            elif verbosity_level == 2:

                try:

                    print "%s%s\n%s%s" % (pre,node.object.name,fill,node.object.base_object.value)

                except:

                    print "%s%s\n%s%s" % (pre,node.object.name,fill,None)          

            elif verbosity_level == 1:

                print("%s%s" % (pre,node.object.name))

    
    def _sweep_(self):

        """

        Search the current ExpressionTree to search for the leaf-nodes, which contains the variables declared. 

        :rtype dict sweeped_objects:
        Dict sorted by key-names of the 'base_objects' contained in homonymous EquationNode objects.

        """

        sweeped_objects = {}

        for _1,_2,node in RenderTree(self):

            if node.is_leaf == True:

                sweeped_objects[node.object.name] = node.object

        return(sweeped_objects)


    def _evalExpressionTree_(self):

        """

        Evaluates equation residual using equation previously provided.

        """
        #List nodes from the last to the top

        list_of_nodes = list(PreOrderIter(self))

        list_of_nodes.reverse()

        for node_i in list_of_nodes:

            if node_i.is_leaf: #Leaf-node, just pass

                pass
            
            else: #Branch-root node, evaluate according to 'object.base_operation'

                node_i.object.base_operation(
                                             node_i.object, \
                                             [ child_i.object for child_i in node_i.children ]
                                            )

    def __add__(self, other_object):

        """
        
        Overloaded function for summation of two ExpressionTree objects. Returns a ExpressionTree object containing the current tree extended to include the 'other_object' argument.

        Four cases arises:

        1 - Both objects ('self','other_object') are orphan nodes:

            E.g: a()+ b() = |a + |b = ExpTree(+,|a,|b)
        
        2 - 'self' is a branch-root node and 'other_object' is not:

            E.g: (a()+b())+c() = ExpTree(+,|a,|b) + |c = ExpTree(+,ExpTree(+,|a,|b),|c)

        3 - 'other_object' is a branch-root node and 'self' is not:

            E.g: |c + ExpTree(+,|a,|b) = ExpTree(+,|c,ExpTree(+,|a,|b))

        4 - Both objects ('self','other_object') are branch-root nodes:

            E.g: ExpTree(+,|a,|b) + ExpTree(+,|c,|d) = ExpTree(+,ExpTree(+,|a,|b),ExpTree(+,|c,|d))    

        All are resumed into: ExpTree(+,<A object>, <B object>)

        """

        if isinstance(other_object, self.__class__) == False:

            raise(errors.UnexpectedValueError("ExpressionTree"))

        else:


            branch_root_node =  EquationNode( 
                                name = " + ".join([self.object.name, other_object.object.name]), \
                                base_object = None, \
                                base_operation = EquationNode.summation, \
                                base_operation_name = 'add', \
                                latex_text = self.object.latex_text+" + "+other_object.object.latex_text
                              )

            branch_root = self.__class__(
                              object_ = branch_root_node
                            )

            self.parent = branch_root

            other_object.parent = branch_root

            return(branch_root)


    def __sub__(self, other_object):

        """
        
        Overloaded function for subtraction of two ExpressionTree objects. Returns a ExpressionTree object containing the current tree extended to include the 'other_object' argument.

        """

        if isinstance(other_object, self.__class__) == False:

            raise(errors.UnexpectedValueError("ExpressionTree"))

        else:


            branch_root_node =  EquationNode( 
                                name = " - ".join([self.object.name, other_object.object.name]), \
                                base_object = None, \
                                base_operation = EquationNode.subtraction, \
                                base_operation_name = 'sub', \
                                latex_text = self.object.latex_text+" - "+other_object.object.latex_text
                              )

            branch_root = self.__class__(
                              object_ = branch_root_node
                            )

            self.parent = branch_root

            other_object.parent = branch_root

            return(branch_root)


    def __mul__(self, other_object):

        """
        
        Overloaded function for multiplication of two ExpressionTree objects. Returns a ExpressionTree object containing the current tree extended to include the 'other_object' argument.

        """

        if isinstance(other_object, self.__class__) == False:

            raise(errors.UnexpectedValueError("ExpressionTree"))

        else:


            branch_root_node =  EquationNode( 
                                name = " * ".join([self.object.name, other_object.object.name]), \
                                base_object = None, \
                                base_operation = EquationNode.multiply, \
                                base_operation_name = 'mul', \
                                latex_text = self.object.latex_text+"\times"+other_object.object.latex_text
                              )

            branch_root = self.__class__(
                              object_ = branch_root_node
                            )

            self.parent = branch_root

            other_object.parent = branch_root

            return(branch_root)


    def __div__(self, other_object):

        """
        
        Overloaded function for division of two ExpressionTree objects. Returns a ExpressionTree object containing the current tree extended to include the 'other_object' argument.

        """

        if isinstance(other_object, self.__class__) == False:

            raise(errors.UnexpectedValueError("ExpressionTree"))

        else:


            branch_root_node =  EquationNode( 
                                name = " / ".join([self.object.name, other_object.object.name]), \
                                base_object = None, \
                                base_operation = EquationNode.divide, \
                                base_operation_name = 'div', \
                                latex_text = "\frac{"+self.object.latex_text+"}{"+other_object.object.latex_text+"}"
                              )

            branch_root = self.__class__(
                              object_ = branch_root_node
                            )

            self.parent = branch_root

            other_object.parent = branch_root

            return(branch_root)


    def __pow__(self, other_object):

        """
        
        Overloaded function for exponentiation of one ExpressionTree object. Returns a ExpressionTree object containing the current tree extended to include the 'other_object' argument.

        """

        if isinstance(other_object, self.__class__) == False:

            raise(errors.UnexpectedValueError("ExpressionTree"))

        else:

            branch_root_node =  EquationNode( 
                                name = " ** ".join([self.object.name, other_object.object.name]), \
                                base_object = None, \
                                base_operation = EquationNode.power, \
                                base_operation_name = 'pow', \
                                latex_text = self.object.latex_text+"^{"+other_object.object.latex_text+"}"
                              )

            branch_root = self.__class__(
                              object_ = branch_root_node
                            )

            self.parent = branch_root

            other_object.parent = branch_root

            return(branch_root)

class EquationNode(object):

    """

    Definition of an EquationNode. Represent an object from which arithmetical operations can be performed. The EquationNode's are arrenged in a binary tree and later evaluated through tree renderization. Each operation returns a bigger tree, that will be later evaluated.

    *TODO
        - Include comparison operators for EquationNode objects (<,>,<=,>=,etc) as unary operation that compares values directly.
        - Include overloading of arithmetical operators for EquationNode objects
        - Include Conditional evaluation operator (IfThen) as binary operations
          Eg: IfThen(CONDITION, [THEN_CLAUSE,ELSE_CAUSE]) 

    """

    def __init__(self, name = '', base_object = None, base_operation = None, \
                args = None, base_operation_name = 'eval', was_evaluated = False, latex_text=''):

        """
    
        Initial definition.

        """
        
        self.name = name

        self.base_object = base_object

        if base_operation == None:

            base_operation = self.evalNode

        self.base_operation_name = base_operation_name

        self.base_operation = base_operation

        self.args = args

        self.was_evaluated = was_evaluated

        self.latex_text = latex_text

    def evalNode(self):

        return(self)

    def summation(self, arguments):

        node_1 = arguments[0]

        node_2 = arguments[1]

        self.base_object = node_1.base_object + node_2.base_object

    def subtraction(self, arguments):

        node_1 = arguments[0]

        node_2 = arguments[1]

        self.base_object = node_1.base_object - node_2.base_object

    def multiply(self, arguments):

        node_1 = arguments[0]

        node_2 = arguments[1]

        self.base_object = node_1.base_object * node_2.base_object

    def divide(self, arguments):

        node_1 = arguments[0]

        node_2 = arguments[1]

        self.base_object = node_1.base_object / node_2.base_object

    def power(self, arguments):

        node_1 = arguments[0]

        node_2 = arguments[1]        

        self.base_object = node_1.base_object ** node_2.base_object

    def Log(self, arguments):

        node = arguments[0]

        self.base_object = math_functions.Log( node.base_object )

    def Log10(self, arguments):

        node = arguments[0]

        self.base_object = math_functions.Log10( node.base_object )

    def Abs(self, arguments):

        node = arguments[0]

        self.base_object = math_functions.Abs( node.base_object )

    def Exp(self, arguments):

        node = arguments[0]

        self.base_object = math_functions.Exp( node.base_object )

    def Sin(self, arguments):

        node = arguments[0]

        self.base_object = math_functions.Sin( node.base_object )

    def Cos(self, arguments):

        node = arguments[0]

        self.base_object = math_functions.Cos( node.base_object )

    def Tan(self, arguments):

        node = arguments[0]

        self.base_object = math_functions.Tan( node.base_object )
