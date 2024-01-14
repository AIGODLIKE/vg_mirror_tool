import bpy


class Vg_clear_unused(bpy.types.Operator):
    """删除没有使用的顶点组（形变骨骼，修改器），不包括被其他物体使用的顶点组"""

    bl_idname = "vg.vg_clear_unused"
    bl_label = "删除没有使用的顶点组"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.object is not None

    def execute(self, context):
        '''遍历当前激活骨骼修改器中的骨骼，加入列表，遍历修改器使用的顶点组'''
        obj = bpy.context.object
        used_vg = []
        armature = []
        # 检查所有修改器
        for mod in obj.modifiers:
            # 这里我们检查几个常见的修改器属性
            if hasattr(mod, 'vertex_group') and mod.vertex_group is not None:
                used_vg.append(mod.vertex_group)
            # 需要骨骼激活状态
            if mod.type == 'ARMATURE' and mod.object is not None and mod.show_viewport:
                armature.append(mod.object)
        # 检查形变骨骼
        for a in armature:
            for b in a.data.bones:
                if b.use_deform:
                    used_vg.append(b.name)
        # 检查顶点组
        for vg in obj.vertex_groups:
            if vg.name not in used_vg:
                obj.vertex_groups.remove(vg)
        return {'FINISHED'}


class Vg_remove_zero(bpy.types.Operator):
    """删除权重为0的顶点组"""

    bl_idname = "vg.vg_remove_zero"
    bl_label = "删除权重为0的顶点组"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.object is not None

    def execute(self, context):
        '''遍历所有顶点组，大于0的跳过'''
        obj = bpy.context.object
        unused_vg = []

        # 确保物体是一个网格
        if obj.type == 'MESH':
            # 遍历所有顶点组
            for v_group in obj.vertex_groups:
                used = False  # 假设顶点组未被使用

                # 遍历所有顶点检查是否属于当前顶点组
                for vertex in obj.data.vertices:
                    for group in vertex.groups:
                        if group.group == v_group.index and group.weight != 0:
                            used = True  # 顶点分配给顶点组
                            break

                    if used:
                        break  # 退出顶点循环

                # 输出顶点组及其使用状态
                if not used:
                    unused_vg.append(v_group.name)
            for vg_name in unused_vg:
                obj.vertex_groups.remove(obj.vertex_groups[vg_name])

        return {'FINISHED'}


import re

sides = [
    {"left": "_L_", "right": "_R_"},
    {"left": "_l_", "right": "_r_"},
    {"left": "Left", "right": "Right"},
    {"left": "left", "right": "right"},
    {"left": "_l", "right": "_r"},
    {"left": "_L", "right": "_R"},
    {"left": ".l", "right": ".r"},
    {"left": ".L", "right": ".R"},

]


def determine_and_convert(vertex_group_name, LR=None):
    '''参数：顶点组名，顶点组位置
        只有顶点组名时，返回左右转换后的顶点组名，中间顶点组不变
        传入顶点组位置时，返回 顶点组位置是否匹配'''
    # 定义左右边的标识符及其转换规则

    if LR:
        if LR == 'center':
            # 创建正则表达式模式，将所有左右标识符组合成一个正则表达式
            pattern = "|".join([re.escape(side["left"]) + "|" + re.escape(side["right"]) for side in sides])

            # 使用正则表达式查找左右标识符
            matches = re.findall(pattern, vertex_group_name)

            # 如果没有找到任何匹配项，返回True；否则返回False
            return not bool(matches)

        # 对每一组左右标识符进行检查
        for side in sides:
            if sides.index(side)>3:#使用末尾查找
                # 定义左右标识符的组合正则表达式
                combined_pattern = "|".join(
                    [re.escape(side["left"]) + "|" + re.escape(side["right"]) for side in sides])

                # 使用负向预查来确保左右标识符后面不是其他左右标识符
                pattern = f"(?:(?!{combined_pattern}).)*$"
                left_pattern = re.escape(side["left"]) + pattern
                right_pattern = re.escape(side["right"]) + pattern
            else:
                left_pattern = re.escape(side["left"])
                right_pattern = re.escape(side["right"])

            # 查找L
            if re.search(left_pattern, vertex_group_name, ) and LR == '-x':
                return True
            # 查找R
            elif re.search(right_pattern, vertex_group_name, ) and LR == '+x':
                return True

        return False
    else:
        # 对每一组左右标识符进行检查和转换
        for side in sides:
            if sides.index(side)>3:#使用末尾查找
                # 定义左右标识符的组合正则表达式
                combined_pattern = "|".join(
                    [re.escape(side["left"]) + "|" + re.escape(side["right"]) for side in sides])

                # 使用负向预查来确保左右标识符后面不是其他左右标识符
                pattern = f"(?:(?!{combined_pattern}).)*$"
                left_pattern = re.escape(side["left"]) + pattern
                right_pattern = re.escape(side["right"]) + pattern
            else:
                left_pattern = re.escape(side["left"])
                right_pattern = re.escape(side["right"])

            # 检查并替换左边标识符为右边标识符
            if re.search(left_pattern, vertex_group_name, ):
                return re.sub(left_pattern, side["right"], vertex_group_name, )
            # 检查并替换右边标识符为左边标识符
            elif re.search(right_pattern, vertex_group_name, ):
                return re.sub(right_pattern, side["left"], vertex_group_name, )

        # 如果没有找到任何匹配的标识符，返回原名称
        print(vertex_group_name)
        return vertex_group_name


def clean_vertex_groups(obj, keep_groups):
    """
    删除不在 keep_groups 列表中的顶点组。

    :param obj: 要处理的Blender对象。
    :param keep_groups: 要保留的顶点组名称列表。
    """
    # 确保对象有顶点组
    if not hasattr(obj, 'vertex_groups'):
        print("对象没有顶点组")
        return

    # 循环遍历顶点组
    for vg in obj.vertex_groups[:]:
        if vg.name not in keep_groups:
            # 删除不在列表中的顶点组
            obj.vertex_groups.remove(vg)


def check_for_matching_pairs(string_list, sides):
    # 对于每对标识符，检查是否在列表中的某个字符串中出现
    for side in sides:
        left_pattern = re.compile(re.escape(side['left']))
        right_pattern = re.compile(re.escape(side['right']))

        left_exists = any(left_pattern.search(string) for string in string_list)
        right_exists = any(right_pattern.search(string) for string in string_list)

        if left_exists and right_exists:
            return True  # 找到至少一对匹配的标识符

    return False


class Vg_mirror_weight(bpy.types.Operator):
    """镜像顶点权重"""

    bl_idname = "vg.vg_mirror_weight"
    bl_label = "镜像顶点组权重"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        model_a = bpy.context.view_layer.objects.active
        return model_a is not None and model_a.type == 'MESH' and len(model_a.vertex_groups)

    def mirror_based_on_selection(self):
        '''返回选择的顶点组'''
        # 获取当前活动对象
        objs = bpy.context.selected_objects
        rig = next((obj for obj in objs if obj.type == 'ARMATURE'), None)
        if not rig:
            return {'CANCELLED'}

        # 获取选择顶点组
        select_vg = []
        for b in rig.data.bones:
            if b.select:
                select_vg.append(b.name)
        return select_vg

    def mirror_based_on_LR(self,ms):
        '''返回左右两边的其中一边的顶点组'''
        obj = bpy.context.object
        v_groups = []
        LR = ms.left_right
        if obj.type == 'MESH':

            for vg in obj.vertex_groups:
                if determine_and_convert(vg.name, LR):
                    v_groups.append(vg.name)
        return v_groups

    def mirror_based_on_center(self):
        '''返回处于模型中心的顶点组'''
        obj = bpy.context.object
        v_groups = []

        if obj.type == 'MESH':
            for vg in obj.vertex_groups:
                if determine_and_convert(vg.name, 'center'):
                    v_groups.append(vg.name)
        return v_groups
    def create_mirrored(self, model_a, name_weight, name_trans):
        '''创建权重模型，权重转移模型，
        返回原模型，
        权重模型，
        传输模型，
        激活顶点组名'''
        # 获取当前激活的模型A

        # 记录模型A当前激活顶点组a_g的名称
        active_vg_name = model_a.vertex_groups.active.name

        # 创建模型B和模型C为模型A的副本
        model_b = model_a.copy()
        model_b.data = model_a.data.copy()
        model_b.name = name_weight
        model_b.data.name = name_weight
        bpy.context.collection.objects.link(model_b)

        model_c = model_a.copy()
        model_c.data = model_a.data.copy()
        model_c.name = name_trans
        model_c.data.name = name_trans

        bpy.context.collection.objects.link(model_c)

        bpy.context.view_layer.objects.active = model_b
        return model_b, model_c, active_vg_name

    def symmetriy_ops(self, ms, model_b):
        '''对称中间骨权重'''
        # 激活模型B
        # 添加并应用镜像修改器
        mirror_mod = model_b.modifiers.new(name="Mirror", type='MIRROR')
        mirror_mod.use_axis[0] = True
        mirror_mod.use_bisect_axis[0] = True
        if ms.left_right == '-x':
            mirror_mod.use_bisect_flip_axis[0] = False
        else:
            mirror_mod.use_bisect_flip_axis[0] = True

        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with bpy.context.temp_override(window=window, area=area, active_object=model_b):
                        # bpy.ops.screen.screen_full_area()
                        bpy.ops.object.modifier_apply(modifier='Mirror')
                    break

        # 添加并应用切分修改器

    def transfer_vg(self, origin, source, result):
        '''转移权重，应用修改器'''
        bpy.context.view_layer.objects.active = result
        result.select_set(True)

        # 为模型C添加DataTransfer修改器，传递模型B的顶点组
        bpy.context.view_layer.objects.active = result
        result.select_set(True)
        data_transfer_mod = result.modifiers.new(name="DataTransferC", type='DATA_TRANSFER')
        data_transfer_mod.object = source
        data_transfer_mod.use_vert_data = True
        data_transfer_mod.data_types_verts = {'VGROUP_WEIGHTS'}
        if origin.mirror_settings.mirror_method == 'POLYINTERP_NEAREST':
            data_transfer_mod.vert_mapping = 'POLYINTERP_NEAREST'
        else:
            data_transfer_mod.vert_mapping = 'NEAREST'
        # 应用DataTransfer修改器到模型C
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with bpy.context.temp_override(window=window, area=area, active_object=source):
                        # bpy.ops.screen.screen_full_area()
                        bpy.ops.object.datalayout_transfer(modifier="DataTransferC")
                        bpy.ops.object.modifier_apply(modifier="DataTransferC")
                    break

    def execute(self, context):
        temp_mode = bpy.context.object.mode

        # 确保Blender处于对象模式
        bpy.ops.object.mode_set(mode='OBJECT')
        model_a = bpy.context.view_layer.objects.active
        model_a.select_set(True)
        ms=model_a.mirror_settings
        '''按选择骨骼镜像时，处理方式不同'''
        # 处理选择的骨骼顶点组 权重
        if ms.is_selected:
            v_groups = self.mirror_based_on_selection()
            if check_for_matching_pairs(v_groups, sides):
                self.report({"ERROR"}, "不能同时选择左右两边的骨骼！")
                bpy.ops.object.mode_set(mode=temp_mode)
                return {'CANCELLED'}
            # 对称权重
            model_b_sym, model_c_sym, active_vg_name = self.create_mirrored(model_a, 'model_b_sym', 'model_c_sym')
            self.symmetriy_ops(ms, model_b_sym)
            self.transfer_vg(model_a, model_b_sym, model_c_sym)

            # 镜像权重
            model_b_mir, model_c_mir, active_vg_name = self.create_mirrored(model_a, 'model_b_mir', 'model_c_mir')
            model_b_mir.scale.x*=-1
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            self.transfer_vg(model_a, model_b_mir, model_c_mir)


        # 处理单个顶点组
        else:
            model_b, model_c, active_vg_name = self.create_mirrored(model_a, 'model_b', 'model_c')
            if ms.is_center:
                self.symmetriy_ops(ms, model_b)
            else:
                # 在X轴上缩放模型B为-1，实现镜像
                model_b.scale.x *= -1
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            self.transfer_vg(model_a, model_b, model_c)
        # 确保变更生效
        # bpy.context.view_layer.update()

        # 单个顶点组
        if not ms.is_multiple:
            # 清理模型C的顶点组，只留下a_g
            clean_vertex_groups(model_c,[active_vg_name])

            # 更改镜像后的顶点组名称
            if ms.is_center:
                mirrored = model_c.vertex_groups.active.name
            else:
                mirrored = determine_and_convert(model_c.vertex_groups.active.name)
            model_c.vertex_groups.active.name = mirrored
            # 为模型A添加DataTransfer修改器，传递模型C的a_g顶点组
            self.transfer_vg(model_a, model_c, model_a)

        # 多个顶点组
        else:
            
            # 按中间镜像
            if ms.is_center and not ms.is_selected:
                v_groups = self.mirror_based_on_center()
                for vg in model_c.vertex_groups[:]:
                    if vg.name not in v_groups:
                        model_c.vertex_groups.remove(vg)
                print(v_groups)
                self.transfer_vg(model_a, model_c, model_a)
            # 按左右镜像
            elif not ms.is_center and not ms.is_selected:
                v_groups=self.mirror_based_on_LR(ms)
                print(v_groups)
                for vg in model_c.vertex_groups[:]:
                    if vg.name not in v_groups:
                        model_c.vertex_groups.remove(vg)
                for vg in model_c.vertex_groups[:]:
                    vg.name=determine_and_convert(vg.name)
                self.transfer_vg(model_a, model_c, model_a)
            # 按选择镜像
            elif ms.is_selected:
                v_groups=self.mirror_based_on_selection()
                print(f'选择的{v_groups}')
                #留下中间的顶点组
                for vg in model_c_sym.vertex_groups[:]:
                    # print(vg.name)
                    if not determine_and_convert(vg.name,'center'):
                        # print(f'shanchu{vg.name}')
                        model_c_sym.vertex_groups.remove(vg)
                clean_vertex_groups(model_c_sym,v_groups)
                #留下对应的左右边顶点组
                for vg in model_c_mir.vertex_groups[:]:
                    if determine_and_convert(vg.name,'center'):
                        model_c_mir.vertex_groups.remove(vg)
                for vg in model_c_mir.vertex_groups[:]:
                    print(vg.name)
                clean_vertex_groups(model_c_mir, v_groups)
                for vg in model_c_mir.vertex_groups[:]:
                    vg.name=determine_and_convert(vg.name)
                self.transfer_vg(model_a, model_c_sym, model_a)
                self.transfer_vg(model_a, model_c_mir, model_a)

            #激活顶点组
            mirrored = active_vg_name
        try:
            bpy.data.meshes.remove(model_b.data)
            bpy.data.meshes.remove(model_c.data)

        except:
            bpy.data.meshes.remove(model_b_mir.data)
            bpy.data.meshes.remove(model_b_sym.data)
            bpy.data.meshes.remove(model_c_mir.data)
            bpy.data.meshes.remove(model_c_sym.data)

        model_a.vertex_groups.active_index = model_a.vertex_groups.find(mirrored)
        bpy.context.view_layer.objects.active = model_a
        bpy.ops.object.mode_set(mode=temp_mode)
        return {'FINISHED'}


class Vg_mirror_multiple_weights(bpy.types.Operator):
    """对称顶点权重，适用于居中的顶点组"""

    bl_idname = "vg.vg_symmetry_weight"
    bl_label = "对称顶点权重"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.object is not None

    def execute(self, context):
        temp_mode = bpy.context.object.mode
        # 确保Blender处于对象模式
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}
