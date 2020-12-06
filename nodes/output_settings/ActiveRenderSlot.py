import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeActiveRenderSlotNode(RenderStackNode):
    bl_idname = "RSNodeActiveRenderSlotNode"
    bl_label = 'Render Slot'

    active_slot_index: IntProperty(default=0, min=0, soft_max=7)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'active_slot_index', text="Render Slot")


def register():
    bpy.utils.register_class(RSNodeActiveRenderSlotNode)


def unregister():
    bpy.utils.unregister_class(RSNodeActiveRenderSlotNode)

# images['Render Result'].render_slots.active_index