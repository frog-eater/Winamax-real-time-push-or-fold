import jpype

jpype.startJVM(jpype.getDefaultJVMPath(), '-ea', '-Djava.classpath.path=.')

_cr = jpype.JPackage("pokerai").game.icm.CalcRanges()

def _list_to_jarray(jtype, plist):
    jarray = jpype.JArray(jtype)(len(plist))

    for i, val in enumerate(plist):
        jarray[i] = jtype(val)

    return jarray 

def calc(players, stacks, raiser, bb, ante, nosb, evthreshold, payouts):
    jplayers = jpype.JInt(players)
    jstacks = _list_to_jarray(jpype.JInt, stacks)
    jranges = jpype.JArray(jpype.JInt)(players)
    jraisor = jpype.JInt(raisor)
    jBB = jpype.JInt(bb)
    jante = jpype.JInt(ante)
    jnoSmallBlind = jpype.JBoolean(noSmallBlind)
    jevTreshold = jpype.JDouble(evTreshold)
    jpayouts = _list_to_jarray(jpype.JDouble, payouts)

    _cr.calc(jplayers, jstacks, jraisor, jBB, jante, jnoSmallBlind, jevTreshold, jpayouts, jranges);
    return [r for r in jranges]

if __name__ == "__main__":
    # Example 1
    players = 5;
    payouts = [0.333, 0.333, 0.333, 0, 0]
    stacks = [1610, 1275, 1765, 1360, 2990]
    raisor = 4  # my position when there is no raised before me
    BB = 200;
    ante = 10;
    noSmallBlind = False;
    evTreshold = 0;
    ranges = calc(players, stacks, raisor, BB, ante, noSmallBlind, evTreshold, payouts);

    print(ranges)
    print ("Push Example (#1):")
    for i, r in enumerate(ranges):
        print ("#%i: %i%%" % (i, r))
    print  

    # Example 2
    players = 4
    payouts = [0.333, 0.333, 0.333, 0]
    stacks = [2080, 3890, 1800, 1230]
    raisor = 2  # my position when there is no raised before me
    BB = 400
    ante = 50
    noSmallBlind = False
    evTreshold = -0.5
    ranges = calc(players, stacks, raisor, BB, ante, noSmallBlind, evTreshold, payouts)

    print ("Call Example (#2):")
    for i, r in enumerate(ranges):
        print ("#%i: %i%%" % (i, r))
    print  

# vim: filetype=python syntax=python expandtab shiftwidth=4 softtabstop=4
