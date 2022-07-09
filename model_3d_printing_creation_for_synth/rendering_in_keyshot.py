"""
Special Scripting Console

https://manual.keyshot.com/manual/scripting-2/
https://media.keyshot.com/scripting/doc/9.0/quickstart.html
"""

import sys

input_path = sys.argv[1]
output_path = sys.argv[2]
camera_position_x = int(sys.argv[3])
camera_position_y = int(sys.argv[4])
camera_position_z = int(sys.argv[5])
camera_direction_x = float(sys.argv[6])
camera_direction_y = float(sys.argv[7])
camera_direction_z = float(sys.argv[8])
brightness_list = sys.argv[9].split(",")
lux.importFile(input_path)
lux.setRenderEngine(lux.RENDER_ENGINE_PRODUCT_GPU)
env = lux.getActiveEnvironment()
env.setLightingEnvironment(
    "C:/Users/oopps/Documents/KeyShot10/Environments/Studio/Basic/All White 4K.hdz"
)
env.setLightingEnvironment("C:/Users/oopps/Documents/KeyShot 10/HDRI/base.hdr")
lux.setCameraPosition([camera_position_x, camera_position_y, camera_position_z])
lux.setCameraDirection([camera_direction_x, camera_direction_y, camera_direction_z])
lux.setCameraUp([0, 1, 0])
scene_tree = lux.getSceneTree()
model_node = scene_tree.find(types=lux.NODE_TYPE_MODEL)[0]
model_node.setMaterial("Hard Rough Plastic Black #1")
for brightness in brightness_list:
    env.setBrightness(brightness)
    lux.renderImage(f"{output_path}_{brightness}.png")
exit()
