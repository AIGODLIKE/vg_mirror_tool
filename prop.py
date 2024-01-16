import bpy
from bpy.app.translations import pgettext as _


class Mirror_Settings(bpy.types.PropertyGroup):
    mirror_method: bpy.props.EnumProperty(
        name=_("Mirror method"),
        description=_(
            "When left and right are symmetrical, the nearest point effect is better; when they are not symmetrical, use face interpolation."),
        items=(("NEAREST", "Nearest", "Nearest vertex"),
               ("POLYINTERP_NEAREST", "Polyinterp", "Nearest face interpolation"),
               ))
    left_right: bpy.props.EnumProperty(
        name="Mirror direction",
        description="Select mirror direction",
        items=(("-x", "", "(-x arrow<-) Use the weight on the right side +x -> -x", 'BACK', 1),
               ("+x", "", "(+x arrow->) Use the weight on the left side -x -> +x", 'FORWARD', 2),
               )

    )
    # 此处图标名'FILE_TICK'和'FILE_NEW'应替换为有效的Blender图标名称
    is_center: bpy.props.BoolProperty(name='Symmetric',
                                      description="When enabled, make the middle bone symmetrical weight; when disabled, mirror the weight between the left and right bones.")

    is_multiple: bpy.props.BoolProperty(name='Multiple vertex groups',
                                        description="Mirror or symmetrize multiple vertex groups.")
    is_selected: bpy.props.BoolProperty(name='Selected',default=False,
                                        description="Mirror or symmetrize selected vertex groups (selected bones, in weight paint mode)")
