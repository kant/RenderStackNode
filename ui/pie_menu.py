import os
import bpy
import rna_keymap_ui
from bpy.types import Menu
from bpy.props import *

from .icon_utils import RSN_Preview

merge_icon = RSN_Preview(image='merge.png', name='merge_icon')
simple_task_icon = RSN_Preview(image='flow.png', name='simple_task_icon')
version_icon = RSN_Preview(image='version.png', name='version_icon')
split_icon = RSN_Preview(image='split.png', name='split_icon')


class RSN_OT_SwitchTree(bpy.types.Operator):
    bl_idname = "rsn.switch_tree"
    bl_label = 'Switch Tree'

    tree_name: StringProperty()

    def execute(self, context):
        try:
            context.space_data.node_tree = bpy.data.node_groups[self.tree_name]
        except Exception as e:
            print(e)

        return {'FINISHED'}


class RSN_MT_PieMenu(Menu):
    bl_label = "RSN Helper"
    bl_idname = "RSN_MT_PieMenu"

    @classmethod
    def poll(cls, context):
        return context.area.ui_type == 'RenderStackNodeTree'

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.25
        pie = layout.menu_pie()

        ## left
        pie.separator()
        ##

        ## right
        col1 = pie.column()

        # simple_icon = preview_collections["rsn_icon"]["simple_task_icon"]

        col = col1.box().column()
        # merge_icon = preview_collections["rsn_icon"]["merge_icon"]
        col.operator("rsn.merge_selected_nodes", icon_value=merge_icon.get_image_icon_id()).make_version = 0

        col.operator("rsn.merge_selected_nodes", icon_value=version_icon.get_image_icon_id(),
                     text='Make Variants').make_version = 1

        col.operator("rsn.split_to_selected", text="Split active to selected",
                     icon_value=split_icon.get_image_icon_id())
        ##

        # bottom
        col = pie.column(align=1)

        for g in bpy.data.node_groups:
            if g.bl_idname == 'RenderStackNodeTree':
                sub = col.row(align=1)
                if context.space_data.edit_tree != bpy.data.node_groups[g.name]:
                    sub.operator('rsn.switch_tree', icon='SCREEN_BACK', text=g.name).tree_name = g.name
                else:
                    sub.label(icon='HIDE_OFF', text=g.name)
                sub.prop(bpy.data.node_groups[g.name], 'use_fake_user', icon_only=1)
        ##
        pie.separator()
        ##

        ##
        pie.separator()
        ##

        ##
        pie.separator()
        ##

        ##
        pie.separator()
        ##

        # right bottom
        pie.operator("rsn.move_node", text='Simple Task', icon_value=simple_task_icon.get_image_icon_id())

        ##
        pie.separator()
        ##


def register_icon():
    merge_icon.register()
    simple_task_icon.register()
    version_icon.register()
    split_icon.register()


def unregister_icon():
    merge_icon.unregister()
    simple_task_icon.unregister()
    version_icon.unregister()
    split_icon.unregister()


def register():
    register_icon()

    bpy.utils.register_class(RSN_MT_PieMenu)
    bpy.utils.register_class(RSN_OT_SwitchTree)


def unregister():
    unregister_icon()

    bpy.utils.unregister_class(RSN_MT_PieMenu)
    bpy.utils.unregister_class(RSN_OT_SwitchTree)
