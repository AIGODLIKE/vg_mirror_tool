# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import os

import bpy
from .ops import *
from .prop import *
from bpy.props import PointerProperty
import bpy.utils.previews
bl_info = {
    "name" : "顶点组助手",
    "author" : "幻之境_cupcko",
    "description" : "镜像顶点组，清理顶点组",
    "blender" : (3, 0, 0),
    "version" : (1, 0, 0),
    "location" : "顶点组",
    "warning" : "",
    "doc_url": "",
    "tracker_url": "",
    "category" : "Mesh"
}


def sna_add_to_data_pt_vertex_groups_9E3D8(self, context):
    if not (False):
        layout = self.layout
        col_CCEC4 = layout.column(heading='', align=False)
        col_CCEC4.alert = False
        col_CCEC4.enabled = True
        col_CCEC4.active = True
        col_CCEC4.use_property_split = False
        col_CCEC4.use_property_decorate = False
        col_CCEC4.scale_x = 1.0
        col_CCEC4.scale_y = 1.0
        col_CCEC4.alignment = 'Left'.upper()
        if not True: col_CCEC4.operator_context = "EXEC_DEFAULT"

        obj_prop = context.object.mirror_settings
        row = layout.row(heading='', align=True)
        row_BCED0=row.row(heading='', align=True)
        row_BCED0.alert = False
        row_BCED0.enabled = True
        row_BCED0.active = True
        row_BCED0.use_property_split = False
        row_BCED0.use_property_decorate = False
        row_BCED0.scale_x = 1.0
        row_BCED0.scale_y = 1.0
        row_BCED0.alignment = 'Expand'.upper()
        if not True: row_BCED0.operator_context = "EXEC_DEFAULT"

        op = row_BCED0.prop(obj_prop,'left_right', expand=True,text='',  )

        button = row.row(heading='', align=True)

        op = button.prop(obj_prop,'is_center', text='', toggle=True, icon_value=446, emboss=True, )
        row_BCED0.enabled = obj_prop.is_center or obj_prop.is_multiple
        op = button.operator('vg.vg_mirror_weight', text='镜像顶点组', icon_value=0, emboss=True, depress=False)
        pcoll = preview_collections["main"]
        op = button.prop(obj_prop, 'is_multiple', text='', toggle=True, icon_value=pcoll['duo_icon'].icon_id, emboss=True, )
        op = button.prop(obj_prop, 'is_selected', text='', toggle=True, icon_value=pcoll['xuan_icon'].icon_id, emboss=True, )

        op = button.prop(obj_prop, 'mirror_method', text='', icon_value=30, emboss=True, expand=False, slider=True,
                       toggle=False, invert_checkbox=False,
                       index=0)
        split_68BC6 = col_CCEC4.split(factor=0.0, align=True)
        split_68BC6.alert = False
        split_68BC6.enabled = True
        split_68BC6.active = True
        split_68BC6.use_property_split = False
        split_68BC6.use_property_decorate = False
        split_68BC6.scale_x = 1.0
        split_68BC6.scale_y = 1.0
        split_68BC6.alignment = 'Expand'.upper()
        if not True: split_68BC6.operator_context = "EXEC_DEFAULT"
        op = split_68BC6.operator('vg.vg_clear_unused', text='删除没有使用', icon_value=0, emboss=True, depress=False)
        op = split_68BC6.operator('vg.vg_remove_zero', text='删除权重为零', icon_value=0, emboss=True, depress=False)
def load_icon(icon_name, icon_path, pcoll):
    """ 加载并注册一个图标 """
    pcoll.load(icon_name, icon_path, 'IMAGE')
classes=[
Mirror_Settings,
Vg_clear_unused,
Vg_remove_zero,
Vg_mirror_weight,
Vg_mirror_multiple_weights,


]
#脚本目录
script_dir=os.path.dirname(os.path.realpath(__file__))
#图标目录
icons_dir=os.path.join(script_dir, "icons")
preview_collections = {}
def register():
    from bpy.utils import register_class
    for c in classes:
        register_class(c)
    #icon
    global preview_collections
    pcoll = bpy.utils.previews.new()
    # 加载多个图标
    load_icon("duo_icon", os.path.join(icons_dir, "duo.png"), pcoll)
    load_icon("xuan_icon", os.path.join(icons_dir, "xuan.png"), pcoll)
    load_icon("multiple_icon", os.path.join(icons_dir, "multiple.png"), pcoll)
    load_icon("selected_icon", os.path.join(icons_dir, "selected.png"), pcoll)

    preview_collections["main"] = pcoll
    bpy.types.DATA_PT_vertex_groups.append(sna_add_to_data_pt_vertex_groups_9E3D8)
    bpy.types.Object.mirror_settings = PointerProperty(type=Mirror_Settings)

def unregister():
    from bpy.utils import unregister_class
    for c in reversed(classes):
        unregister_class(c)
    # icon
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
    bpy.types.DATA_PT_vertex_groups.remove(sna_add_to_data_pt_vertex_groups_9E3D8)
    del bpy.types.Object.mirror_settings