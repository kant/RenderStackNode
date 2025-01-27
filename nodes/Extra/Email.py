from ...nodes.BASE.node_tree import RenderStackNode
from ...preferences import get_pref

import bpy
from bpy.props import *


def test_email(self, context):
    if self.test_send:
        self.process()
        self.test_send = False


class RenderNodeEmail(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RenderNodeEmail'
    bl_label = 'Email'

    test_send: BoolProperty(name="Test Send", update=test_email)

    warning: BoolProperty(name='Is warning', default=False)
    warning_msg: StringProperty(name='warning message', default='')

    def init(self, context):
        self.create_prop('RenderNodeSocketString', 'subject', 'Subject')
        self.create_prop('RenderNodeSocketString', 'content', 'Content')
        self.create_prop('RenderNodeSocketString', 'sender_name', 'Sender Name')
        self.create_prop('RenderNodeSocketString', 'email', 'Email')

        self.outputs.new('RSNodeSocketTaskSettings', "Settings")

        self.width = 150
        self.warning = False

    def draw_buttons(self, context, layout):
        layout.prop(self, 'text_send', toggle=True)

    def process(self):
        self.store_data()
        bpy.ops.rsn.send_email(subject=self.node_dict['subject'],
                               content=self.node_dict['content'],
                               sender_name=self.node_dict['sender_name'],
                               email=self.node_dict['email'])


def register():
    bpy.utils.register_class(RenderNodeEmail)


def unregister():
    bpy.utils.unregister_class(RenderNodeEmail)
