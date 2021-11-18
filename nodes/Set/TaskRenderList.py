import json

from bpy.props import *
from ...utility import *
from ...nodes.BASE.node_base import RenderNodeBase
from ...ui.icon_utils import RSN_Preview

from ..BASE._runtime import cache_node_dependants


def update_active_task(self, context):
    if self.is_active_list:
        for node in self.id_data.nodes:
            if node.bl_idname == 'RenderNodeTaskRenderListNode' and node != self:
                node.is_active_list = False
    bpy.context.window_manager.rsn_active_list = self.name
    bpy.context.scene.rsn_bind_tree = self.id_data  # bind tree
    self.execute_tree()


def update_mode(self, context):
    if self.mode == 'DYNAMIC':
        for i, input in enumerate(self.inputs):
            if i != 0:
                self.inputs.remove(input)
    else:
        self.auto_update_inputs('RenderNodeSocketTask', "Task")


class RenderNodeTaskRenderListNode(RenderNodeBase):
    """Render List Node"""
    bl_idname = 'RenderNodeTaskRenderListNode'
    bl_label = 'Task Render List'

    mode: EnumProperty(name='Mode', items=[
        ('STATIC', 'Static', ''),
        ('DYNAMIC', 'Dynamic', ''),
    ], update=update_mode)

    active_index: IntProperty(name="Active Index", min=0, update=update_active_task)
    is_active_list: BoolProperty(name="Active List")

    show_task_info:BoolProperty(name = 'Task Info',default=False)
    task_info: StringProperty(name='Task Info')

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname in {'RenderStackNodeTree'}

    def draw_buttons(self, context, layout):
        layout.box().prop(self, 'is_active_list')
        if not self.is_active_list: return

        layout.prop(self, 'mode')
        layout.prop(self, 'active_index')

        # draw task info
        col = layout.box().column(align=True)
        col.prop(self,'show_task_info',text='Active Task', icon='TRIA_DOWN' if self.show_task_info else 'TRIA_RIGHT',emboss = False)

        if self.show_task_info:
            col = col.box().split().column()
            if self.task_info != '':
                for s in self.task_info.split('$$$'):
                    col.label(text=s)

    def update(self):
        if self.mode == 'STATIC':
            self.auto_update_inputs('RenderNodeSocketTask', "task")

    def get_dependant_nodes(self):
        '''returns the nodes connected to the inputs of this node'''
        dep_tree = cache_node_dependants.setdefault(self.id_data, {})
        nodes = []

        if self.mode == 'STATIC':
            for index, input in enumerate(self.inputs):
                if index == self.active_index:
                    connected_socket = input.connected_socket
                    if connected_socket and connected_socket not in nodes:
                        nodes.append(connected_socket.node)
                    break

            dep_tree[self] = nodes

        else:
            connected_socket = self.inputs[0].connected_socket
            if connected_socket and connected_socket not in nodes:
                nodes.append(connected_socket.node)

        return nodes

    def process(self, context, id, path):
        value = self.process_task(index=self.active_index if self.mode == 'STATIC' else 0)

        if not value:
            self.task_info = 'No Task is linked'
            return
        data = json.loads(value)

        context.scene.frame_start = data.get('frame_start')
        context.scene.frame_end = data.get('frame_end')
        context.scene.frame_step = data.get('frame_step')

        context.scene.render.filepath = data.get('filepath')

        # set to ui
        self.task_info = '$$$'.join([f"{key.title().replace('_',' ')}: {value}" for key, value in data.items()])


def register():
    bpy.utils.register_class(RenderNodeTaskRenderListNode)


def unregister():
    bpy.utils.unregister_class(RenderNodeTaskRenderListNode)
