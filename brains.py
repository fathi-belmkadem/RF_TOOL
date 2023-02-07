from math import sin, cos, sqrt, pi, radians, degrees
import cmath
import matplotlib.image as mpimg
import numpy as np
#.append(component("", categ="", config="", value=, unit=unit))
class component:
    def __init__(self, name=None, categ=None, config=None, value=None, unit=None):
        self.name = name
        self.categ = categ
        self.config = config
        self.value = value
        self.unit = unit


def calcFromZL(f, z0, rl, xl):
    """Used to calculate results if the user uses complex load"""
    w = 2 * pi * f 
    units ={0:'', -3:'m', -6:'μ', -9:'n', -12:'p', -15:'f'}
    res = {"sol1": [], "sol2": []}
    
    # Case 1: ZL/z0 is inside the 1+jx circuit on the smithchart
    if rl > z0:
        B1 = (xl + sqrt(rl / z0) * sqrt(rl**2 + xl**2 - z0 * rl)) / (rl**2 + xl**2)
        B2 = (xl - sqrt(rl / z0) * sqrt(rl**2 + xl**2 - z0 * rl)) / (rl**2 + xl**2)
        X1 = 1/B1 + (xl * z0) / rl - z0 / (B1 * rl)
        X2 = 1/B2 + (xl * z0) / rl - z0 / (B2 * rl)
        # creating components of 1st solution
        ccounter = lcounter = 1   #those are used to keep track of the number of component of the same type
        if X1 > 0:
            L, exp = scientificNotation( abs(X1/w) )
            unit = "{}H".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"L{lcounter}", categ="inductor", config="series", value=L, unit=unit) )
            lcounter += 1
        elif X1 < 0:
            C, exp = scientificNotation( abs(1/(X1*w)) )
            unit = "{}F".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"C{ccounter}", categ="capacitor", config="series", value=C, unit=unit) )
            ccounter += 1

        if B1 > 0:
            C, exp = scientificNotation( abs(B1/w) )
            unit = "{}F".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"C{ccounter}", categ="capacitor", config="parallel", value=C, unit=unit) )
            ccounter += 1
        elif B1 < 0:
            L, exp = scientificNotation( abs(1/(B1*w)) )
            unit = "{}H".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"L{lcounter}", categ="inductor", config="parallel", value=L, unit=unit) )
            lcounter += 1

        # creating components of 2nd solution
        ccounter = lcounter = 1   #those are used to keep track of the number of component of the same type
        if X2 > 0:
            L, exp = scientificNotation( abs(X2/w) )
            unit = "{}H".format(units.get(exp, "undefined"))
            res['sol2'].append( component(f"L{lcounter}", categ="inductor", config="series", value=L, unit=unit) )
            lcounter += 1
        elif X2 < 0:
            C, exp = scientificNotation( abs(1/(X2*w)) )
            unit = "{}F".format(units.get(exp, "undefined"))
            res['sol2'].append( component(f"C{ccounter}", categ="capacitor", config="series", value=C, unit=unit) )
            ccounter += 1

        if B2 > 0:
            C, exp = scientificNotation( abs(B2/w) )
            unit = "{}F".format(units.get(exp, "undefined"))
            res['sol2'].append( component(f"C{ccounter}", categ="capacitor", config="parallel", value=C, unit=unit) )
            ccounter += 1
        elif B2 < 0:
            L, exp = scientificNotation( abs(1/(B2*w)) )
            unit = "{}H".format(units.get(exp, "undefined"))
            res['sol2'].append( component(f"L{lcounter}", categ="inductor", config="parallel", value=L, unit=unit) )
            lcounter += 1
        
    #case 2: ZL/z0 is outside the 1+jx circuit on the smithchart
    elif rl < z0:
        B1 = sqrt((z0 - rl) / rl) / z0
        B2 = -sqrt((z0 - rl) / rl) / z0
        X1 = B1 * z0 * rl - xl
        X2 = B2 * z0 * rl - xl
        # creating components of 1st solution
        ccounter = lcounter = 1   #those are used to keep track of the number of component of the same type
        if B1 > 0:
            C, exp = scientificNotation( abs(B1/w) )
            unit = "{}F".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"C{ccounter}", categ="capacitor", config="parallel", value=C, unit=unit) )
            ccounter += 1
        elif B1 < 0:
            L, exp = scientificNotation( abs(1/(B1*w)) )
            unit = "{}H".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"L{lcounter}", categ="inductor", config="parallel", value=L, unit=unit) )
            lcounter += 1
        
        if X1 > 0:
            L, exp = scientificNotation( abs(X1/w) )
            unit = "{}H".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"L{lcounter}", categ="inductor", config="series", value=L, unit=unit) )
            lcounter += 1
        elif X1 < 0:
            C, exp = scientificNotation( abs(1/(X1*w)) )
            unit = "{}F".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"C{ccounter}", categ="capacitor", config="series", value=C, unit=unit) )
            ccounter += 1

        # creating components of 2nd solution
        ccounter = lcounter = 1   #those are used to keep track of the number of component of the same type
        if B2 > 0:
            C, exp = scientificNotation( abs(B2/w) )
            unit = "{}F".format(units.get(exp, "undefined"))
            res['sol2'].append( component(f"C{ccounter}", categ="capacitor", config="parallel", value=C, unit=unit) )
            ccounter += 1
        elif B2 < 0:
            L, exp = scientificNotation( abs(1/(B2*w)) )
            unit = "{}H".format(units.get(exp, "undefined"))
            res['sol2'].append( component(f"L{lcounter}", categ="inductor", config="parallel", value=L, unit=unit) )
            lcounter += 1
        
        if X2 > 0:
            L, exp = scientificNotation( abs(X2/w) )
            unit = "{}H".format(units.get(exp, "undefined"))
            res['sol2'].append( component(f"L{lcounter}", categ="inductor", config="series", value=L, unit=unit) )
            lcounter += 1
        elif X2 < 0:
            C, exp = scientificNotation( abs(1/(X2*w)) )
            unit = "{}F".format(units.get(exp, "undefined"))
            res['sol2'].append( component(f"C{ccounter}", categ="capacitor", config="series", value=C, unit=unit) )
            ccounter += 1
    
    # Case 3: rl == z0  >===> zl/z0 on the circle
    elif rl == z0 and xl != 0:
        if xl > 0:
            B1 = (xl + sqrt(rl / z0) * sqrt(rl**2 + xl**2 - z0 * rl)) / (rl**2 + xl**2)
        else:
            B1 = (xl - sqrt(rl / z0) * sqrt(rl**2 + xl**2 - z0 * rl)) / (rl**2 + xl**2)
        B2 = 0
        X1 = 1/B1 + (xl * z0) / rl - z0 / (B1 * rl)
        X2 = -xl
        # creating components of 1st solution
        ccounter = lcounter = 1   #those are used to keep track of the number of component of the same type
        if X1 > 0:
            L, exp = scientificNotation( abs(X1/w) )
            unit = "{}H".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"L{lcounter}", categ="inductor", config="series", value=L, unit=unit) )
            lcounter += 1
        elif X1 < 0:
            C, exp = scientificNotation( abs(1/(X1*w)) )
            unit = "{}F".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"C{ccounter}", categ="capacitor", config="series", value=C, unit=unit) )
            ccounter += 1

        if B1 > 0:
            C, exp = scientificNotation( abs(B1/w) )
            unit = "{}F".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"C{ccounter}", categ="capacitor", config="parallel", value=C, unit=unit) )
            ccounter += 1
        elif B1 < 0:
            L, exp = scientificNotation( abs(1/(B1*w)) )
            unit = "{}H".format(units.get(exp, "undefined"))
            res['sol1'].append( component(f"L{lcounter}", categ="inductor", config="parallel", value=L, unit=unit) )
            lcounter += 1

        # creating components of 2nd solution
        ccounter = lcounter = 1   #those are used to keep track of the number of component of the same type
        if X2 > 0:
            L, exp = scientificNotation( abs(X2/w) )
            unit = "{}H".format(units.get(exp, "undefined"))
            res['sol2'].append( component(f"L{lcounter}", categ="inductor", config="series", value=L, unit=unit) )
            lcounter += 1
        elif X2 < 0:
            C, exp = scientificNotation( abs(1/(X2*w)) )
            unit = "{}F".format(units.get(exp, "undefined"))
            res['sol2'].append( component(f"C{ccounter}", categ="capacitor", config="series", value=C, unit=unit) )
            ccounter += 1

    return res


def calcFromGamma(f, z0, mag, phi):
    """Used to calculate results if user uses S-parameters"""
    rl, xl = calcZlFromGamma(mag, phi)
    rl = rl*z0
    xl = xl*z0
    return calcFromZL(f, z0, rl, xl)
    
def calcZlFromGamma(mag, phi):
    p = mag*cos(radians(phi))
    q = mag*sin(radians(phi))
    rl = (1 - p**2 - q**2)/((1 - p)**2 + q**2)
    xl = (2*q)/((1 - p)**2 + q**2)
    #rl = z0 * (1 - mag ** 2) / ( 1 + mag ** 2 - 2 * mag * cos( radians(phi) ) )
    #xl = z0 * ( 2 * mag * sin(radians(phi)) ) / ( 1 + mag ** 2 - 2 * mag * cos(radians(phi)) )
    return rl, xl

def calcXYFromZl(zl):
    """calculates cartisien coordenates based on Zl(normalized)"""
    gamma = (zl - 1)/(zl + 1)
    mag = abs(gamma)
    phi = cmath.phase(gamma)
    x = mag * cos(phi)
    y = mag * sin(phi)
    return x, y

def caclZlfromXY(x, y):
    gamma = x + y*1j
    mag = abs(gamma)
    phi = cmath.phase(gamma)
    return calcZlFromGamma(mag, phi)


def scientificNotation(value):
    parts = str(value).split('e')
    if len(parts) == 2:
        exp = int(parts[1])
        x = value * 10 ** (-exp + exp % 3)
        x = round(x, 3)
        exp -= exp % 3
        return (float(str(x).rstrip('0')), exp)
    else:
        parts = parts[0].split('.')
        # if value is an integer: no decimal part
        if len(parts) == 1:
            return(value, 0)
        # else value has a decimal part
        n = int(parts[0])
        decimals = parts[1]
        if n != 0:
            return ( float(str(round(value, 3)).rstrip('0')), 0)
        else:
            exp = -1 - (len(decimals) - len(decimals.lstrip('0')))
            x = value * 10 ** (-exp + exp % 3)
            x = round(x, 3)
            exp -= exp % 3
            return (float(str(x).rstrip('0')), exp)


def buildCircuit(assetList):
    load = mpimg.imread("resources/components/load.png")[:,:,0]
    description = []
    circuit = np.ndarray((154, 0))
    for i, comp in enumerate(assetList):
        description.append("<p style=\"color:blue;\"<b>Component {0}</b></p>Name........... : {1}<br>Category...... : {2}<br>Configuration : {3}<br>Value........... : <b>{4} {5}</b>".format(i+1, comp.name, comp.categ, comp.config, comp.value, comp.unit))
        comSymb = mpimg.imread("resources/components/{} {}.png".format(comp.config, comp.categ))[:,:,0]
        circuit = np.concatenate([circuit, comSymb], axis = 1)
    circuit = np.concatenate([circuit, load], axis = 1)
    return description, circuit

def makeErrMsg(expression, inf=None, sup=None):
        errMsg = ""
        if expression != "":
            try:
                value = float(expression)
            except ValueError:
                errMsg = "Only reals allowed"
            else:
                if inf is not None and sup is not None and value > sup and value < inf:
                    errMsg = f"Invalid: {inf} ≤ value ≤ {sup}"
                if inf is not None and value <= inf:
                    errMsg = f"Value must be ≥ {inf}"
                if sup is not None and value > sup:
                    errMsg = f"Value must be ≤ {sup}"
        else:
            errMsg = "Value required"
        return errMsg


""" def runTest(f, z0, rl, xl, amp, phi):
    res1 = calcFromZL(f, z0, rl, xl)
    res2 = calcFromGamma(f, z0, amp, phi)
    for k, v in res1.items():
        print("{}:  ".format(k))
        for c in v:
            print("          name   = {}".format(c.name))
            print("          categ  = {}".format(c.categ))
            print("          config = {}".format(c.config))
            print("          value  = {}{}".format(c.value, c.unit))
            print("=====================================")
        print("\n######################################\n")

runTest(10e6, 50, 150, 50, 0.4, 45)

load = mpimg.imread("resources/components/load.png")[:,:,0]
series_capacitor = mpimg.imread("resources/components/series capacitor.png")[:,:,0]
series_inductor = mpimg.imread("resources/components/series inductor.png")[:,:,0]
parallel_inductor = mpimg.imread("resources/components/parallel inductor.png")[:,:,0]
parallel_capacitor = mpimg.imread("resources/components/parallel capacitor.png")[:,:,0]
print(f"load ==>shape:  {load.shape}")
print(f"series capacitor ==>shape:  {series_capacitor.shape}")
print(f"series inductor ==>shape:  {series_inductor.shape}")
print(f"parallel insuctor ==>shape:  {parallel_inductor.shape}")
print(f"parallel capacitor ==>shape:  {parallel_capacitor.shape}")

res = calcFromZL(10e6, 50, 150, 50)
circuit = buildCircuit(res['sol1'])
print(circuit[0][1]) """