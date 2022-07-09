import bpy
import mathutils
from g_code_parser import Parser


class IMPORT_OT_gcode(bpy.types.Operator, Parser):
    filepath = bpy.props.StringProperty(name="File Path", maxlen=1024, default="")

    def __init__(self):
        self.ySquash = 0.5
        self.xOoze = 1.15
        super(IMPORT_OT_gcode, self).__init__()

    def draw(self, context):
        pass

    def execute(self, context):
        self.build(self.filepath)
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def build(self, fileName):
        self.parse(fileName)
        count = 0
        radius = 0
        for key in sorted(self.thickness.keys()):
            if self.thickness[key] > count:
                count = self.thickness[key]
                radius = key

        profileName = self.obName + "_profile"
        profileData = bpy.data.curves.new(profileName, type="CURVE")
        profileData.dimensions = "3D"
        profilePoly = profileData.splines.new("POLY")
        profilePoly.points.add(7)
        angRad = radius * 0.70711
        profilePoly.points[7].co = (radius * self.xOoze, 0.0, 0.0, 1)
        profilePoly.points[6].co = (angRad * self.xOoze, angRad * self.ySquash, 0.0, 1)
        profilePoly.points[5].co = (0.0, radius * self.ySquash, 0.0, 1)
        profilePoly.points[4].co = (-angRad * self.xOoze, angRad * self.ySquash, 0.0, 1)
        profilePoly.points[3].co = (-radius * self.xOoze, 0.0, 0.0, 1)
        profilePoly.points[2].co = (
            -angRad * self.xOoze,
            -angRad * self.ySquash,
            0.0,
            1,
        )
        profilePoly.points[1].co = (0.0, -radius * self.ySquash, 0.0, 1)
        profilePoly.points[0].co = (angRad * self.xOoze, -angRad * self.ySquash, 0.0, 1)
        profilePoly.use_cyclic_u = True
        profileObject = bpy.data.objects.new(profileName, profileData)
        scn = bpy.context.view_layer
        scn.update()
        bpy.context.collection.objects.link(profileObject)
        scn.objects.active = profileObject
        for layerNum, layer in enumerate(self.layers):
            layerName = self.obName + "_slice_%d" % layerNum
            curveData = bpy.data.curves.new(layerName, type="CURVE")
            curveData.dimensions = "3D"
            curveData.bevel_object = profileObject
            for poly in self.layers[layer]:
                pointNum = 0
                for point in poly:
                    if pointNum == 0:
                        x, y, z = point
                        oldPt = mathutils.Vector((x, y, z, 1))
                        pointNum = 1
                    else:
                        polyline = curveData.splines.new("POLY")
                        polyline.points.add(1)
                        x, y, z = point
                        newPt = mathutils.Vector((x, y, z, 1))
                        polyline.points[0].co = oldPt
                        polyline.points[1].co = newPt
                        oldPt = newPt
        layerObject = bpy.data.objects.new(layerName, curveData)
        bpy.context.collection.objects.link(layerObject)
        scn.objects.active = layerObject

def menu_func(self, context):
    self.layout.operator(
        IMPORT_OT_gcode.bl_idname, text="Slic3r GCode(.gcode)", icon="PLUGIN"
    )

def register():
    classes = (IMPORT_OT_gcode,)
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)


def unregister():
    classes = (IMPORT_OT_gcode,)
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)


if __name__ == "__main__":
    register()
