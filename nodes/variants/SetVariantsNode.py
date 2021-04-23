import bpy
from bpy.props import *
from ..BASE.node_tree import RenderStackNode
from ...utility import *


def update_node(self, context):
    if self.use:
        nt = context.space_data.edit_tree
        node = nt.nodes[self.name]
        node.active = self.active


class VariantsNodeProperty(bpy.types.PropertyGroup):
    name: StringProperty(name="The name of the variants node")
    active: IntProperty(default=0, min=0)
    use: BoolProperty(default=True)


# for visualization add or delete
class RSN_UL_VarCollectNodeList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.label(text=item.name)
        row.prop(item, "active", text="Active")
        row.prop(item, "use", text="Use")


class RSN_OT_UpdateVarCollect(bpy.types.Operator):
    """ADD/REMOVE List item"""
    bl_idname = "rsn.update_var_collect"
    bl_label = "Update Collect"

    action: EnumProperty(name="Edit", items=[('ADD', 'Add', ''), ('REMOVE', 'Remove', '')])

    node_name: StringProperty(default='')
    node = None

    def execute(self, context):
        self.node = context.space_data.edit_tree.nodes[self.node_name]
        if self.action == "ADD":
            self.get_var_nodes()
            self.node.node_collect_index = len(self.node.node_collect) - 1

        else:

            self.node.node_collect.remove(self.node.node_collect_index)
            self.node.node_collect_index -= 1 if self.node.node_collect_index != 0 else 0


        return {"FINISHED"}

    def get_var_nodes(self):
        nt = bpy.context.space_data.edit_tree

        RSN = RSN_Nodes(node_tree=nt, root_node_name=self.node.name)
        nodes = RSN.get_children_from_node(root_node=self.node)
        node_list = ','.join(
            [node_name for node_name in nodes if nt.nodes[node_name].bl_idname == "RSNodeVariantsNode"])

        print(node_list)

        for i, src_node in enumerate(self.node.node_collect.keys()):
            if src_node not in node_list.split(','):
                self.node.node_collect.remove(i)
                self.node.node_collect_index -= 1 if self.node.node_collect_index != 0 else 0

        for node_name in node_list.split(','):
            if node_name != '' and node_name not in self.node.node_collect.keys():
                prop = self.node.node_collect.add()
                prop.name = node_name
                prop.active = 0


class RSNodeSetVariantsNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeSetVariantsNode'
    bl_label = 'Set Variants'

    node_list = None

    node_collect: CollectionProperty(name="Node Property", type=VariantsNodeProperty)
    node_collect_index: IntProperty(default=0)

    def init(self, context):
        self.width = 220
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")

    def draw_buttons(self, context, layout):
        row = layout.row(align=1)
        row.template_list(
            "RSN_UL_VarCollectNodeList", "The list",
            self, "node_collect",
            self, "node_collect_index", )

        edit = layout.operator("rsn.update_var_collect", icon="FILE_REFRESH")
        edit.action = "ADD"
        edit.node_name = self.name

    def get_data(self):
        pass
        # for item in self.node_collect:
        #     if item.use:
        #         node = bpy.context.space_data.edit_tree.nodes[item.name]
        #         if node.active != item.active: node.active = item.active


def register():
    bpy.utils.register_class(VariantsNodeProperty)
    bpy.utils.register_class(RSN_UL_VarCollectNodeList)

    bpy.utils.register_class(RSN_OT_UpdateVarCollect)

    bpy.utils.register_class(RSNodeSetVariantsNode)


def unregister():
    bpy.utils.unregister_class(VariantsNodeProperty)
    bpy.utils.unregister_class(RSN_UL_VarCollectNodeList)

    bpy.utils.unregister_class(RSN_OT_UpdateVarCollect)

    bpy.utils.unregister_class(RSNodeSetVariantsNode)