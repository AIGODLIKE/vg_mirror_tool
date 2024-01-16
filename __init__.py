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

import bpy.utils.previews
from bpy.props import PointerProperty

from . import ui
from .ops import *
from .prop import *

bl_info = {
    "name": "VertexGroupsMirrorTool",
    "author": "AIGODLIKE Community(cupcko)",
    "description": "Mirror vertex groups weights, clean vertex groups",
    "blender": (3, 0, 0),
    "version": (1, 0, 0),
    "location": "vertex group",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Mesh"
}


def load_icon(icon_name, icon_path, pcoll):
    """ 加载并注册一个图标 """
    pcoll.load(icon_name, icon_path, 'IMAGE')


classes = [
    Mirror_Settings,
    Vg_clear_unused,
    Vg_remove_zero,
    Vg_mirror_weight,

]


class TranslationHelper():
    def __init__(self, name: str, data: dict, lang='zh_CN'):
        self.name = name
        self.translations_dict = dict()

        for src, src_trans in data.items():
            key = ("Operator", src)
            self.translations_dict.setdefault(lang, {})[key] = src_trans
            key = ("*", src)
            self.translations_dict.setdefault(lang, {})[key] = src_trans

    def register(self):
        try:
            bpy.app.translations.register(self.name, self.translations_dict)
        except(ValueError):
            pass

    def unregister(self):
        bpy.app.translations.unregister(self.name)


# Set
############
from . import zh_CN

vg_mirror_tool_zh_CN = TranslationHelper('vg_mirror_tool_zh_CN', zh_CN.data)
vg_mirror_tool_zh_HANS = TranslationHelper('vg_mirror_tool_zh_HANS', zh_CN.data, lang='zh_HANS')
# 脚本目录
script_dir = os.path.dirname(os.path.realpath(__file__))
# 图标目录
icons_dir = os.path.join(script_dir, "icons")
preview_collections = {}


def register():
    from bpy.utils import register_class
    for c in classes:
        register_class(c)
    # icon
    global preview_collections
    pcoll = bpy.utils.previews.new()
    # 加载多个图标
    load_icon("duo_icon", os.path.join(icons_dir, "duo.png"), pcoll)
    load_icon("xuan_icon", os.path.join(icons_dir, "xuan.png"), pcoll)
    load_icon("multiple_icon", os.path.join(icons_dir, "multiple.png"), pcoll)
    load_icon("selected_icon", os.path.join(icons_dir, "selected.png"), pcoll)

    ui.register()
    preview_collections["main"] = pcoll
    bpy.types.Object.mirror_settings = PointerProperty(type=Mirror_Settings)
    # 翻译
    if bpy.app.version < (4, 0, 0):
        vg_mirror_tool_zh_CN.register()
    else:
        vg_mirror_tool_zh_CN.register()
        vg_mirror_tool_zh_HANS.register()


def unregister():
    from bpy.utils import unregister_class
    for c in reversed(classes):
        unregister_class(c)
    ui.unregister()
    # icon
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
    del bpy.types.Object.mirror_settings
    # 翻译
    if bpy.app.version < (4, 0, 0):
        vg_mirror_tool_zh_CN.unregister()
    else:
        vg_mirror_tool_zh_CN.unregister()
        vg_mirror_tool_zh_HANS.unregister()
