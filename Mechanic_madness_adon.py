import bpy


bl_info = {
    "name": "Mechanic madness",
    "author": "Lebri (purcoll)",
    "version": (0, 1),
    "blender": (3, 30, 1),
    "location": "side bar > Mechanic madness",
    "description": "Add mechanics things",
    "warning": "",
    "doc_url": "",
    "category": "Helper",
}


#
def unblock(context):
    bpy.context.object.lock_location[0] = False
    bpy.context.object.lock_location[1] = False
    bpy.context.object.lock_rotation[0] = False
    bpy.context.object.lock_rotation[1] = False

    
def block(context):
    bpy.context.object.lock_location[0] = True
    bpy.context.object.lock_location[1] = True
    bpy.context.object.lock_rotation[0] = True
    bpy.context.object.lock_rotation[1] = True


def del_dup_rot(context):
    bpy.ops.constraint.delete(constraint="Копировать вращение", owner='OBJECT')

    
def dup_rot(context):
    bpy.ops.object.constraint_add(type='COPY_ROTATION')
    bpy.context.object.constraints["Копировать вращение"].use_x = False
    bpy.context.object.constraints["Копировать вращение"].use_y = False
    bpy.context.object.constraints["Копировать вращение"].use_z = True
    bpy.context.object.constraints["Копировать вращение"].invert_z = True


#===============================================================================
class UnBlockObject(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.un_block_object"
    bl_label = "Unblock object"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        unblock(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(UnBlockObject.bl_idname, text=UnBlockObject.bl_label)


#--------------------------------------------------------------------------------
class BlockObject(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.block_object"
    bl_label = "Block object"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        block(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(BlockObject.bl_idname, text=BlockObject.bl_label)

#--------------------------------------------------------------------------------
class JoinToGear(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.join_to_gear_op"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        dup_rot(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(JoinToGear.bl_idname, text=JoinToGear.bl_label)
    
#--------------------------------------------------------------------------------
class DeleteJoinToGear(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.delete_join_to_gear_op"
    bl_label = "Delete join"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        del_dup_rot(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(DeleteJoinToGear.bl_idname, text=DeleteJoinToGear.bl_label)
#===============================================================================


class MM_panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Mechanic madness"
    # bl_options = {'HIDE_HEADER'}
    bl_options = {"DEFAULT_CLOSED"}

class MM_PT_panel_1(MM_panel, bpy.types.Panel):
    bl_idname = "MM_PT_panel_1"
    bl_label = "Main"

    def draw(self, context):
        pass

class MM_PT_panel_2(MM_panel, bpy.types.Panel):
    bl_parent_id = "MM_PT_panel_1"
    bl_label = "Gears"



    def draw(self, context):
        column = self.layout.column(align = True)
        layout = self.layout
        column.operator("object.join_to_gear_op", text = "create join")
        column.operator("object.delete_join_to_gear_op", text = "delete join")
   
        
class MM_PT_panel_3(MM_panel, bpy.types.Panel):
    bl_parent_id = "MM_PT_panel_1"
    bl_label = "Other"



    def draw(self, context):
        column = self.layout.column(align = True)
        layout = self.layout
        column.operator("object.block_object", text = "Block")
        column.operator("object.un_block_object", text = "Unblock")



classes = (MM_PT_panel_1, MM_PT_panel_2, MM_PT_panel_3)

def register():
    bpy.utils.register_class(JoinToGear)
    bpy.utils.register_class(DeleteJoinToGear)
    bpy.utils.register_class(BlockObject)
    bpy.utils.register_class(UnBlockObject)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    bpy.utils.unregister_class(JoinToGear)
    bpy.utils.unregister_class(DeleteJoinToGear)
    bpy.utils.unregister_class(BlockObject)
    bpy.utils.unregister_class(UnBlockObject)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
