import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def active_version(self, context):
    if self.active > len(self.inputs):
        self.active = len(self.inputs)

    for input in self.inputs:
        if input.is_linked:
            node = input.links[0].from_node
            node.mute = 1

    if self.inputs[self.active - 1].is_linked:
        node = self.inputs[self.active - 1].links[0].from_node
        node.mute = 0
        nt = context.space_data.edit_tree
        nt.links.remove(self.inputs[self.active - 1].links[0])
        nt.links.new(node.outputs[0], self.inputs[self.active - 1])

    dg = context.evaluated_depsgraph_get()
    dg.update()


class RSNodeSettingsMergeNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeSettingsMergeNode'
    bl_label = 'Merge'

    node_type: EnumProperty(name='node type', items=[
        ('SWITCH', 'Switch', ''),
        ('MERGE', 'Merge', ''),
        ('VERSION', 'Version', ''),
    ], default='MERGE')

    active: IntProperty(name='Active Version', default=1, update=active_version, min=1)

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")

    def draw_buttons(self, context, layout):
        if self.node_type in {'MERGE', 'VERSION'}:
            if self.node_type == 'VERSION':
                layout.prop(self, 'active')
            try:
                if hasattr(bpy.context.space_data, 'edit_tree'):
                    if bpy.context.space_data.edit_tree.nodes.active.name == self.name:
                        row = layout.row(align=1)
                        a = row.operator("rsnode.edit_input", icon='ADD', text='Add')
                        a.socket_type = 'RSNodeSocketTaskSettings'
                        a.socket_name = "Input"
                        r = row.operator("rsnode.edit_input", icon='REMOVE', text='Del')
                        r.remove = 1

            except Exception:
                pass

        else:
            layout.operator('rsn.switch_setting').node = self.name


def register():
    bpy.utils.register_class(RSNodeSettingsMergeNode)


def unregister():
    bpy.utils.unregister_class(RSNodeSettingsMergeNode)