import bpy
class Mirror_Settings(bpy.types.PropertyGroup):
    mirror_method: bpy.props.EnumProperty(
        name="镜像方法",
        description="左右对称时最近点效果好，不对称时面插值",
        items=(("NEAREST", "最近点", "最近的顶点"),
               ("POLYINTERP_NEAREST", "面插值", "最近的面插值"),
               ))
    left_right: bpy.props.EnumProperty(
            name="镜像方向",
            description="选择镜像方向",
            items=(("-x", "", "(-x箭头<-)使用右边权重+x->-x",'BACK', 1),
                   ("+x", "", "(+x箭头->)使用左边权重-x->+x",'FORWARD', 2),
                   )

    )
            # 此处图标名'FILE_TICK'和'FILE_NEW'应替换为有效的Blender图标名称
    is_center: bpy.props.BoolProperty(name='对称',
                                                  description="开启时使中间骨骼对称权重，关闭时使左右两边的骨骼镜像权重")

    is_multiple:bpy.props.BoolProperty(name='多个顶点组',
                                                  description="镜像或者对称多个顶点组")
    is_selected:bpy.props.BoolProperty(name='选中的',
                                              description="镜像或者对称选中的顶点组(选中的骨骼，需要在权重绘制模式)")
