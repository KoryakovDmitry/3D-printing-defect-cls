import copy


class Parser:
    def __init__(self):
        self.pos = {"X": 0.0, "Y": 0.0, "Z": 0.0, "E": 0.0}
        self.points = []
        self.polys = []
        self.layers = {}
        self.thickness = {}
        self.Prusa = False

    def parse(self, fileName):
        self.points = []
        f = open(fileName)
        for line in f.readlines():
            if "PrusaSlicer" in line:
                self.Prusa = True
            line = line.split(";", 1)[0].strip()
            if len(line) < 1:
                continue
            tokens = line.split()
            self.dispatch(tokens)

        f.close()
        self.newLayer(-1.0, -1.0)

    def dispatch(self, tokens):
        if tokens[0] in dir(self):
            eval("self." + tokens[0] + "(" + str(tokens[1:]) + ")")
        else:
            print("unknown command:" + str(tokens[0]))

    def newPoly(self):
        if len(self.points) > 0:
            self.polys.append(self.points[:])
            self.points = []

    def newLayer(self, delta, zetta):
        self.newPoly()
        if len(self.polys) > 0:
            if zetta in self.layers:
                t = self.layers[zetta]
                t.extend(self.polys[:])
                self.layers[zetta] = t
            else:
                self.layers[zetta] = self.polys[:]
            self.polys = []
            if delta > 0.0 and delta < 1.0:
                if delta in self.thickness.keys():
                    self.thickness[delta] = self.thickness[delta] + 1
                else:
                    self.thickness[delta] = 1

    def moveTo(self, newPos):
        if newPos["Z"] != self.pos["Z"]:
            delta = newPos["Z"] - self.pos["Z"]

            zetta = self.pos["Z"]
            self.newLayer(delta, zetta)

        if self.Prusa:
            if newPos["E"] is None or newPos["E"] <= 0.0:
                self.newPoly()
        else:
            if (
                newPos["E"] is None
                or newPos["E"] <= 0.0
                or newPos["E"] <= self.pos["E"]
            ):
                self.newPoly()
        if newPos["E"] is not None and newPos["E"] > 0:
            if newPos["Z"] is None:
                newPos["Z"] = self.pos["Z"]

            if newPos["X"] is None:
                newPos["X"] = self.pos["X"]

            if newPos["Y"] is None:
                newPos["Y"] = self.pos["Y"]

            self.points.append([newPos["X"], newPos["Y"], newPos["Z"]])
        self.pos = copy.deepcopy(newPos)

    def parseCoords(self, tokens):
        npos = {}
        for tok in tokens:
            axis = tok[0]
            if axis in ["X", "Y", "Z", "E"]:
                npos[axis] = float(tok[1:])
        return npos

    def parseCoordsUpdate(self, tokens):
        npos = self.parseCoords(tokens)
        for axis in ["X", "Y", "Z", "E"]:
            if axis not in npos.keys():
                npos[axis] = self.pos[axis]
        return npos

    def N(self, tokens):
        self.dispatch(tokens[1:])

    def G0(self, tokens):
        newPos = self.parseCoordsUpdate(tokens)
        self.moveTo(newPos)

    def G1(self, tokens):
        self.G0(tokens)

    def G4(self, tokens):
        pass

    def G21(self, tokens):
        pass

    def G28(self, tokens):
        npos = self.pos
        for tok in tokens:
            axis = tok[0]
            if axis in ["X", "Y", "Z", "E"]:
                npos[axis] = 0.0
        npos["E"] = 0.0
        self.moveTo(npos)

    def G80(self, tokens):
        pass

    def G90(self, tokens):
        pass

    def G92(self, tokens):
        newPos = self.parseCoordsUpdate(tokens)
        if newPos["E"] == 0:
            self.newPoly()
        self.pos = newPos

    def M73(self, tokens):
        pass

    def M82(self, tokens):
        pass

    def M83(self, tokens):
        pass

    def M84(self, tokens):
        pass

    def M104(self, tokens):
        pass

    def M106(self, tokens):
        pass

    def M107(self, tokens):
        pass

    def M109(self, tokens):
        pass

    def M115(self, tokens):
        pass

    def M140(self, tokens):
        pass

    def M190(self, tokens):
        pass

    def M201(self, tokens):
        pass

    def M203(self, tokens):
        pass

    def M204(self, tokens):
        pass

    def M205(self, tokens):
        pass

    def M221(self, tokens):
        pass

    def M900(self, tokens):
        pass

    def M907(self, tokens):
        pass

    def M862(self, tokens):
        pass


if __name__ == "__main__":
    p = Parser()
    p.parse(r"gcode\2.gcode")
