import bpy
import json
import logging
from itertools import groupby

from mathutils import Color, Vector


# LOG_FORMAT = "%(asctime)s - RSN-%(levelname)s - %(message)s"
# logging.basicConfig(format=LOG_FORMAT)
# logger = logging.getLogger('mylogger')


def source_attr(src_obj, scr_data_path):
    def get_obj_and_attr(obj, data_path):
        path = data_path.split('.')
        if len(path) == 1:
            return obj, path[0]
        else:
            back_obj = getattr(obj, path[0])
            back_path = '.'.join(path[1:])
            return get_obj_and_attr(back_obj, back_path)

    return get_obj_and_attr(src_obj, scr_data_path)


class RSN_NodeTree:
    """To store context node tree for getting data in renderstack"""

    def get_context_tree(self, return_name=False):
        try:
            name = bpy.context.space_data.edit_tree.name
            return bpy.context.space_data.edit_tree.name if return_name else bpy.data.node_groups[name]
        except:
            return None

    def set_wm_node_tree(self, node_tree_name):
        bpy.context.window_manager.rsn_cur_tree_name = node_tree_name

    def get_wm_node_tree(self, get_name=False):
        name = bpy.context.window_manager.rsn_cur_tree_name
        if get_name:
            return name
        else:
            return bpy.data.node_groups[name]

    def set_context_tree_as_wm_tree(self):
        tree_name = self.get_context_tree(return_name=1)
        if tree_name:
            self.set_wm_node_tree(tree_name)


class RSN_Task:
    """Tree method"""

    def __init__(self, node_tree, root_node_name):
        self.nt = node_tree
        self.root_node = self.get_node_from_name(root_node_name)

    def get_node_from_name(self, name):
        try:
            node = self.nt.nodes[name]
            return node
        except KeyError:
            return None

    def get_root_node(self):
        return self.root_node

    def get_sub_node_from_node(self, root_node):
        """Depth first search"""
        node_list = []

        def append_node_to_list(node):
            """Skip the reroute node"""
            if node.bl_idname != 'NodeReroute':
                if len(node_list) == 0 or (len(node_list) != 0 and node.name != node_list[-1]):
                    node_list.append(node.name)

        def get_sub_node(node):
            """Skip the mute node"""
            for input in node.inputs:
                if input.is_linked:
                    sub_node = input.links[0].from_node
                    if sub_node.mute:
                        continue
                    else:
                        get_sub_node(sub_node)
                else:
                    continue
            append_node_to_list(node)

        get_sub_node(root_node)

        return node_list

    def get_sub_node_dict_from_node_list(self, node_list, parent_node_type, black_list=None):
        """Use Task node as separator to get sub nodes in this task"""
        node_list_dict = {}
        if not black_list: black_list = ['RSNodeTaskListNode', 'RSNodeRenderListNode']

        node_list[:] = [node for node in node_list if
                        self.nt.nodes[node].bl_idname not in black_list]
        children_node_list = [list(g) for k, g in
                              groupby(node_list, lambda name: self.nt.nodes[name].bl_idname == parent_node_type) if
                              not k]
        parent_node_list = [node for node in node_list if self.nt.nodes[node].bl_idname == parent_node_type]

        for i in range(len(parent_node_list)):
            try:
                node_list_dict[parent_node_list[i]] = children_node_list[i]
            # release the node behind the parent
            except IndexError:
                pass
        return node_list_dict

    def get_sub_node_from_task(self, task_name, return_dict=False, type='RSNodeTaskNode'):
        """pack method for task node"""
        task = self.get_node_from_name(task_name)
        try:
            node_list = self.get_sub_node_from_node(task)
            if not return_dict:
                return node_list
            else:
                return self.get_sub_node_dict_from_node_list(node_list=node_list,
                                                             parent_node_type=type)
        except AttributeError:
            pass

    def get_sub_node_from_render_list(self, return_dict=False, type='RSNodeTaskNode'):
        """pack method for render list node(get all task)"""
        render_list = self.get_node_from_name(self.root_node.name)
        node_list = self.get_sub_node_from_node(render_list)
        if not return_dict:
            return node_list
        else:
            return self.get_sub_node_dict_from_node_list(node_list=node_list,
                                                         parent_node_type=type)

    def get_task_data(self, task_name, task_dict):
        """transfer nodes to data"""
        task_data = {}
        for node_name in task_dict[task_name]:
            node = self.nt.nodes[node_name]
            node.debug()
            # label
            task_data['label'] = self.nt.nodes[task_name].label

            # Object select Nodes
            if node.bl_idname == 'RSNodeObjectDataNode':
                if 'object_data' not in task_data:
                    task_data['object_data'] = {}
                task_data['object_data'].update(node.get_data())

            if node.bl_idname == 'RSNodeObjectModifierNode':
                if 'object_modifier' not in task_data:
                    task_data['object_modifier'] = {}
                task_data['object_modifier'].update(node.get_data())

            elif node.bl_idname == 'RSNodeObjectDisplayNode':
                if 'object_display' not in task_data:
                    task_data['object_display'] = {}
                task_data['object_display'].update(node.get_data())

            elif node.bl_idname == 'RSNodeObjectMaterialNode':
                if 'object_material' not in task_data:
                    task_data['object_material'] = {}
                task_data['object_material'].update(node.get_data())

            elif node.bl_idname == 'RSNodeObjectPSRNode':
                if 'object_psr' not in task_data:
                    task_data['object_psr'] = {}
                task_data['object_psr'].update(node.get_data())

            elif node.bl_idname == 'RSNodeViewLayerPassesNode':
                if 'view_layer_passes' not in task_data:
                    task_data['view_layer_passes'] = {}
                task_data['view_layer_passes'].update(node.get_data())

            elif node.bl_idname == 'RSNodeSmtpEmailNode':
                if 'email' not in task_data:
                    task_data['email'] = {}
                task_data['email'].update(node.get_data())

            elif node.bl_idname == 'RSNodeScriptsNode':
                if node.type == 'SINGLE':
                    if 'scripts' not in task_data:
                        task_data['scripts'] = {}
                    task_data['scripts'].update(node.get_data())
                else:
                    if 'scripts_file' not in task_data:
                        task_data['scripts_file'] = {}
                    task_data['scripts_file'].update(node.get_data())
            # Single node
            else:
                try:
                    task_data.update(node.get_data())
                except TypeError:
                    pass

        return task_data
