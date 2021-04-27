import bpy
import nodeitems_utils
from bpy.props import EnumProperty


class SearchEnumOperator(bpy.types.Operator):
    bl_idname = "object.search_enum_operator"
    bl_label = "Search Enum Operator"
    bl_property = "my_search"

    my_search: EnumProperty(
        name="My Search",
        items=(
            ('RSNodeTaskNode', 'Task', ''),
            ('RSNodeNullNode', 'Null', ''),
            ('RSNodeRenderListNode', 'Render List', ''),
            ('RSNodeProcessorNode', 'Processor', ''),
            ('RSNodeViewerNode', 'Viewer', ''),
            ('RSNodeVariantsNode', 'Variants', ''),
            ('RSNodeSetVariantsNode', 'Set Variants', ''),
            ('RSNodeNullNode', 'Null', ''),
            ('RSNodeCommonSettingsNode', 'Common Settings', ''),
            ('RSNodePropertyInputNode', 'Property', ''),
            ('RSNodeCamInputNode', 'Camera', ''),
            ('RSNodeWorldInputNode', 'World', ''),
            ('RSNodeViewLayerInputNode', 'View Layer', ''),
            ('RSNodeColorManagementNode', 'Color Management', ''),
            ('RSNodeTaskInfoInputsNode', 'Task Info(Experiment)', ''),
            ('RSNodeObjectDisplayNode', 'Object Display', ''),
            ('RSNodeObjectMaterialNode', 'Object Material', ''),
            ('RSNodeObjectPSRNode', 'Object PSR', ''),
            ('RSNodeObjectDataNode', 'Object Data', ''),
            ('RSNodeObjectModifierNode', 'Object Modifier', ''),
            ('RSNodeResolutionInputNode', 'Resolution', ''),
            ('RSNodeFrameRangeInputNode', 'Frame Range', ''),
            ('RSNodeImageFormatInputNode', 'Image Format', ''),
            ('RSNodeFilePathInputNode', 'File Path', ''),
            ('RSNodeActiveRenderSlotNode', 'Render Slot', ''),
            ('RSNodeViewLayerPassesNode', 'View Layer Passes', ''),
            ('RSNodeWorkBenchRenderSettingsNode', 'WorkBench Settings', ''),
            ('RSNodeEeveeRenderSettingsNode', 'Eevee Settings', ''),
            ('RSNodeCyclesRenderSettingsNode', 'Cycles Settings', ''),
            ('RSNodeCyclesLightPathNode', 'Cycles Light Path', ''),
            ('RSNodeOctaneRenderSettingsNode', 'Octane Settings', ''),
            ('RSNodeLuxcoreRenderSettingsNode', 'Luxcore Settings', ''),
            ('RSNodeScriptsNode', 'Scripts', ''),
            ('RSNodeSmtpEmailNode', 'SMTP Email', ''),
            ('RSNodeLightStudioNode', 'SSM Light Studio', ''),
            ('RSNodeSettingsMergeNode', 'Merge', ''),
            ('RSNodeSettingsMergeNode', 'Switch', ''),
            ('RSNodeSettingsMergeNode', 'Version', ''),
        ))

    def node_enum_items(self, context):
        node_items_list = []
        for index, item in enumerate(nodeitems_utils.node_items_iter(context)):
            if isinstance(item, nodeitems_utils.NodeItem):
                node_items_list.append((item.nodetype, item.label, ''))

        print(node_items_list)
        return node_items_list

    def create_node(self, context, node_type=None):
        if node_type:
            bpy.ops.node.select_all(action='DESELECT')

            node = context.space_data.edit_tree.nodes.new(type=node_type)

            node.select = True
            context.space_data.edit_tree.nodes.active = node
            node.location = context.space_data.cursor_location
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')

            # node.location = space.cursor_location

    def execute(self, context):
        print(self.my_search)

        self.create_node(context, node_type=self.my_search)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_class(SearchEnumOperator)


def unregister():
    bpy.utils.unregister_class(SearchEnumOperator)
