import bpy
from bpy.props import *
from ...nodes.BASE.node_base import RenderNodeBase


def update_node(self, context):
    self.execute_tree()


class RSNodeEeveeRenderSettingsNode(RenderNodeBase):
    """A simple input node"""
    bl_idname = 'RSNodeEeveeRenderSettingsNode'
    bl_label = 'Eevee Settings'

    samples: IntProperty(default=64, min=1, name="Eevee Samples", update=update_node)


    def init(self, context):
        self.outputs.new('RSNodeSocketRenderSettings', "Render Settings")

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        col.prop(self, "samples", text='Samples')

        row = col.row(align=1)
        half = row.operator("rsn.change_samples", text="Half")
        half.node_name = self.name
        half.scale = 0.5

        double = row.operator("rsn.change_samples", text="Double")
        double.node_name = self.name
        double.scale = 2

    def process(self, context, id, path):
        task_data = self.get_data()

        engines = ['BLENDER_EEVEE', 'BLENDER_WORKBENCH'] + [engine.bl_idname for engine in
                                                            bpy.types.RenderEngine.__subclasses__()]

        # engine settings
        if 'engine' in task_data:
            if task_data['engine'] in engines:
                self.compare(bpy.context.scene.render, 'engine', task_data['engine'])

        if task_data['engine'] == "BLENDER_EEVEE":
            self.compare(bpy.context.scene.eevee, 'taa_render_samples', task_data['samples'])

    def get_data(self):
        task_data = {}
        task_data['engine'] = "BLENDER_EEVEE"
        task_data['samples'] = self.samples
        return task_data


def register():
    bpy.utils.register_class(RSNodeEeveeRenderSettingsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeEeveeRenderSettingsNode)