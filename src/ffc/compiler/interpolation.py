__author__ = "Anders Logg (logg@tti-c.org)"
__date__ = "2005-05-16"
__copyright__ = "Copyright (c) 2005 Anders Logg"
__license__  = "GNU GPL Version 2"

# FIAT modules
from FIAT.dualbasis import *
from FIAT.shapes import *

# FFC modules
from declaration import *

class Interpolation:

    """Interpolation generates a function that can compute the
    interpolation of a given onto the a finite element basis."""

    def __init__(self, dualbasis):
        "Create Interpolation."

        print "-------------------------------------------------------------"
        print "Creating interpolation (experimental)"
        print ""

        # Get points (temporary until we can handle other types of nodes)
        points = dualbasis.pts

        # Map point to reference element (different in FFC and FIAT)
        newpoints = []
        for point in points:
            newpoints += [tuple([0.5*(x + 1.0) for x in point])]
        points = newpoints

        # Get the number of vector components
        num_components = dualbasis.num_reps

        # Iterate over the dofs
        self.declarations = []
        dof = 0
        for component in range(num_components):
            for point in points:
                x = (", ".join(["%.15e" % x for x in point]))
                if num_components > 1:
                    i = ", %d" % component
                else:
                    i = ""
                name = "c[%d]" % dof
                value = "f(map(%s)%s)" % (x, i)
                self.declarations += [Declaration(name, value)]
                dof += 1

        for declaration in self.declarations:
            print declaration.name + " = " + declaration.value
        

        print "-------------------------------------------------------------"
