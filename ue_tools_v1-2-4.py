# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "UE4 Tools",
    "author": "LluisGarcia3D",
    "version": (1, 2, 4),
    "blender": (2, 7, 5),
    "location": "View3D > Tools > UE4 Tools",
    "description": "Adds some tools for improve the blender to unreal engine workflow",
    "warning": "",
    "wiki_url": "http://www.lluisgarcia.es/ue-tools-addon/",
    "category": "UE4 Tools"}



import bpy
from bpy.types import Scene
from bpy.props import *
from bpy.props import FloatVectorProperty
from bpy.types import Operator, AddonPreferences, Panel, Menu
import os
from os import mkdir, listdir
from os.path import dirname, exists, join
from mathutils import Matrix
from bpy.props import BoolProperty
from bpy.props import *
from bpy.app.handlers import persistent
from math import radians

@persistent
def load_handler(dummy):
    #print("Load Handler:", bpy.data.filepath)
    
    Main_UI_Properties(bpy.context.scene)
    SetObjScale(bpy.context.scene)
    Rename_Properties(bpy.context.scene)
    FBX_Export_Properties(bpy.context.scene)
    Animation_UI_Properties(bpy.context.scene)
    
bpy.app.handlers.load_post.append(load_handler)   



#-------------------------------------------
#----------------VARIABLES------------------
#-------------------------------------------
#UI Display Var

Init = False

UE_SceneTools = False
UE_RenameTools = False
UE_ExportTools = False
UE_AnimationTools = False


#Scene Settings Var
Init = False
ObjScale = False
testvar = 0


#Batch Rename Vars
ObjBaseNameSelector = "Custom"
RenameObjects = True
RenameData = True
RenameMaterials = False
PrefixSelector  = False
PrefixObj  = True
PrefixData  = True
PrefixMat  = False
CustomRename = ""
Prefix=""
name=""
Collision= False


#Animation Vars

CustomShapesList = []
UE_IK_HeadInherit = False
UE_IK_WaistInherit = False
UE_IK_ONOFF = True
UE_IK_ArmsInherit = False
UE_IK_DeformBones = False
UE_IK_helperBones = True
UE_IK_Lock_R_hand = True
UE_IK_Lock_L_hand = True
UE_IK_Lock_R_foot = True
UE_IK_Lock_L_foot = True



UE_IK_Leg = True
UE_IK_Arm = True
UE_IK_Showbones = False
UE_IK_ShowDeformbones = False
UE_ShowAdvancedRigProp = False
UE_ShowRigProps=True
UE_ShowRigExport=False


RIG_name = "HeroTPP"
Include_hero = True
HeroLow = False
Rotate_character=False
Rotate_Armature = False
UE_Custom_RIG_Name = ""
ACT_name = "New action"    
FakeActionName=""
Steep1=False


#FBX Export Vars

FBX_name_multi  = ""
FBXBaseNameSelector = "Object"
FBX_ExportCustomPath = ""
FBXRelativeFolderSelector = True
FBX_CustomExportName=""
FBX_AssetType = "STATIC"
FBX_Format = "BIN7400"
FBX_ExportCollision= False
FBX_Global_scale = 1
FBX_Tangent=True
FBX_Bake_Anim = False
FBX_NLA = False
FBX_AllActions = False
FBX_AnimStep = 1
FBX_AnimSimplify = 1
FBX_UseAnim = False
FBX_AllActions61 = False
FBX_AxisForward='-Z'
FBX_AxisUp = 'Y'
FBX_ShowAxis = False
FBX_PivotToCenter = False
FBX_Smoothing = 0
FBX_smooth_Type= "OFF"
FBXSmoothingType = 'OFF'


#-------------------------------------------
#---------------UI Callbacks----------------
#-------------------------------------------
#scene tools Active?
def UE_Scene_Tools_Callback (scene,context):    
    
    global UE_SceneTools
    UE_SceneTools = scene.UESceneTools
    
    
#Rename tools Active?
def UE_Rename_Tools_Callback (scene,context):    
    
    global UE_RenameTools
    UE_RenameTools = scene.UERenameTools
    
    
#Export tools Active?
def UE_Export_Tools_Callback (scene,context):    
    
    global UE_ExportTools
    UE_ExportTools = scene.UEExportTools
    

#Animation tools Active?
def UE_Animation_Tools_Callback (scene,context):    
    
    global UE_AnimationTools
    UE_AnimationTools = scene.UEAnimationTools

#-------------------------------------------
#-----------------UI PROPS------------------
#-------------------------------------------
def Main_UI_Properties(scn):
    #Scene Tools    
    bpy.types.Scene.UESceneTools = BoolProperty(
        name = "Rename Data",
        default=False,
        update = UE_Scene_Tools_Callback, 
        description = "Activate the Scene tools")
    scn['UESceneTools'] = False
    
    #Rename Tools   
    bpy.types.Scene.UERenameTools = BoolProperty(
        name = "Rename Data",
        default=False,
        update = UE_Rename_Tools_Callback, 
        description = "Activate Rename tools")
    scn['UERenameTools'] = False

    #Export Tools
    bpy.types.Scene.UEExportTools = BoolProperty(
        name = "Rename Data",
        default=False,
        update = UE_Export_Tools_Callback, 
        description = "Activate Export tools")
    scn['UEExportTools'] = False
    
    #Animation Tools
    bpy.types.Scene.UEAnimationTools = BoolProperty(
        name = "Rename Data",
        default=False,
        update = UE_Animation_Tools_Callback, 
        description = "Activate Animation tools")
    scn['UEAnimationTools'] = False


#-------------------------------------------
#--------STORE SCENE SETTINGS PROPS---------
#-------------------------------------------

#---------------------
#Props Callbacks -----
#---------------------

def ObjScale_Callback (scene,context):    
    
    global ObjScale
    ObjScale = scene.UEObjScale  
    print (ObjScale)


#---------------------
#Props ---------------
#---------------------
def SetObjScale(scn): 
     
     bpy.types.Scene.UEObjScale = BoolProperty(
        name = "Scale Selected Objects",update = ObjScale_Callback,
        description = "True or False?")        
     scn['UEObjScale'] = ObjScale
     return


#-------------------------------------------
#---------SCENE SETTINGS FUNCTIONS----------
#-------------------------------------------




#-------------------------------------------
#---------BATCH RENAME CALLBACKS-----------
#-------------------------------------------

#base name callback
def Obj_Base_Name_Selector_Callback (scene,context):    
    
    global ObjBaseNameSelector
    ObjBaseNameSelector = scene.naming_base  
    print ("Base name = " + str(ObjBaseNameSelector))       
        

#Rename object selector callback
def Rename_Objects_Callback (scene,context):
       
    global RenameObjects    
    RenameObjects = scene.rename_object  
    print ("Rename Objects = " + str(RenameObjects))

#Rename Data selector callback    
def Rename_Data_Callback (scene,context):
       
    global RenameData    
    RenameData = scene.rename_data 
    print ("Rename Data = " + str(RenameData))

#Rename Materials selector callback        
def Rename_materials_Callback (scene,context):
       
    global RenameMaterials   
    RenameMaterials = scene.rename_material 
    print ("Rename Materials = " + str(RenameMaterials))

#Add Prefix selector callback

def Prefix_selector_Callback (scene,context):
       
    global PrefixSelector   
    PrefixSelector = scene.rename_use_prefix 
    print ("Add Prefix = " + str(PrefixSelector)) 

#Add Prefix to objects callback
def Prefix_objects_Callback (scene,context):
       
    global PrefixObj   
    PrefixObj = scene.prefix_object
    print ("Add Prefix to objects = " + str(PrefixObj)) 

#Add Prefix to Data callback
def Prefix_data_Callback (scene,context):
       
    global PrefixData   
    PrefixData  = scene.prefix_data 
    print ("Add Prefix to data = " + str(PrefixData)) 
    
#Add Prefix to Materials callback
def Prefix_materials_Callback (scene,context):
       
    global PrefixMat   
    PrefixMat = scene.prefix_material 
    print ("Add Prefix to materials = " + str(PrefixMat))
    


#Is Collision callback
def Collision_Callback (scene,context):
       
    global Collision   
    Collision = scene.IsCollision 
    print ("is a collisoin object = " + str(Collision))



#-------------------------------------------
#---------BATCH RENAME PROPERTIES-----------
#-------------------------------------------

def Rename_Properties(scn):
    
    #name origins
    name_origins = [
                    ('Custom', 'Custom', 'Custom'),
                    ('Object', 'Object', 'Object'),
                    ('Mesh', 'Mesh', 'Mesh'),
                    ('Material', 'Material', 'Material')
                    ]
    
    #naming base
    bpy.types.Scene.naming_base = EnumProperty(
        items = name_origins,                      
        name = "Name Used:",
        default = "Custom",
        update = Obj_Base_Name_Selector_Callback,
        description='Base name for rename')
    scn['naming_base'] = 0
    
    #custom name
    bpy.types.Scene.rename_custom = StringProperty(
        name = "Custom Name",
        default='New Name',
        description='Rename all with this String')
    scn['rename_custom'] = ""
    
    #Data to rename
    
    #objects?    
    bpy.types.Scene.rename_object = BoolProperty(
        name = "Rename Objects",
        default=True,
        update = Rename_Objects_Callback, 
        description = "Rename Objects")
    scn['rename_object'] = True
    
    #objects data?    
    bpy.types.Scene.rename_data = BoolProperty(
        name = "Rename Data",
        default=True,
        update = Rename_Data_Callback, 
        description = "Rename Object\'s Data")
    scn['rename_data'] = True
    
    #materials?    
    bpy.types.Scene.rename_material = BoolProperty(
        name = "Rename Materials",
        default=False,
        update = Rename_materials_Callback, 
        description = "Rename Objects\' Materials")
    scn['rename_material'] = False
    
    
    #Prefix selector
    bpy.types.Scene.rename_use_prefix = BoolProperty(
        name = "Add Prefix",
        default=False,
        update = Prefix_selector_Callback, 
        description = "Prefix Object,data or material names")
    scn['rename_use_prefix'] = False
    
    #Custom Prefix
    bpy.types.Scene.rename_prefix = StringProperty(
        name = "Prefix",
        default='',
        description='Prefix name with this string')
    scn['rename_prefix'] = ""
    
    #Prefix on Objects?
    bpy.types.Scene.prefix_object = BoolProperty(
        name = "Object",
        default=True,
        update = Prefix_objects_Callback, 
        description = "Prefix Objects names")
    scn['prefix_object'] = True
    
    #Prefix on Data?
    bpy.types.Scene.prefix_data = BoolProperty(
        name = "Data",
        default=True,
        update = Prefix_data_Callback, 
        description = "Prefix Data Names")
    scn['prefix_data'] = True
    
    #Prefix on Materials?
    bpy.types.Scene.prefix_material = BoolProperty(
        name = "Material",
        default=False,
        update = Prefix_materials_Callback, 
        description = "Prefix Material Names")
    scn['prefix_material'] = False
    
    #Is collision?
    bpy.types.Scene.IsCollision = BoolProperty(
        name = "Is Collision",
        default=False,
        update = Collision_Callback, 
        description = "If Checked, add the collision prefix")
    scn['IsCollision'] = False
    

     




#-------------------------------------------
#---------BATCH RENAME FUNCTIONS------------
#-------------------------------------------

#Get custom rename
def Get_custom_rename(label, key, scn):        
    global CustomRename     
    CustomRename = scn["rename_custom"]
    
#Get custom Prefix
def Get_custom_prefix(label, key, scn):        
    global Prefix     
    Prefix = scn["rename_prefix"]
    

#Get firts Material
def get_first_material_name(ob):    
    for m_slot in ob.material_slots:
        if m_slot.material:
            material_name = m_slot.material.name
            return material_name
        


    
#main Function for rename    
def Rename_detablocks(self, context):
    
    obs = bpy.context.selected_objects
    sufix = 0
    global PrefixSelector
    global Prefix
    
    scn = context.scene
    
    Get_custom_prefix("String:   ", 'rename_prefix', scn)
    
    
        
    for ob in obs:
        
        #Get Base Names         
        if ObjBaseNameSelector == 'Object':
            name = ob.name
        
        if ObjBaseNameSelector == 'Mesh':
            if ob.data:
                name = ob.data.name            
            else:
                name = ob.name
            
        if ObjBaseNameSelector == 'Material':        
            material_name = get_first_material_name(ob)               
            if not material_name:
                name = ob.name
            else:
                name = material_name
        
        if ObjBaseNameSelector == 'Custom':        
            name = CustomRename
            
        if Collision == True:
            Prefix = "UCX"
            PrefixSelector = True
            
        if PrefixSelector == True:
            print (Prefix)                  
       
       
        #Rename objects Names
        if RenameObjects == True:
            if (PrefixSelector == True
            and PrefixObj == True):                
                ob.name = Prefix +"_"+ name
                print (ob.name)                        
            else:
                ob.name = name
            if (PrefixSelector == True
            and PrefixObj == True
            and Collision == True):
                ob.name = Prefix +"_"+ name +"_"+ str(sufix)
                
            #else:
                #ob.name = name
                  
                
                
        #Rename objects data Names        
        if RenameData == True:
            if (ob.data
            and ob.data.users == 1):                
                if (PrefixSelector == True
                and PrefixData == True):
                    ob.data.name = Prefix +"_"+ name
                else:
                    ob.data.name = name
                    
                if (PrefixSelector == True
                and PrefixData == True
                and Collision == True):
                    ob.data.name = Prefix +"_"+ name +"_"+ str(sufix)
                #else:
                    #ob.data.name = name                   
        
        
        #Rename material Names             
        if RenameMaterials == True:
            if ob.material_slots:
                for m_slot in ob.material_slots:
                    if m_slot.material:
                        if m_slot.material.users == 1:
                            if (PrefixSelector == True
                            and PrefixMat == True):
                                m_slot.material.name = Prefix +"_"+ name
                            #else:
                                #m_slot.material.name = name
        sufix = sufix + 1
                
        
#-------------------------------------------
#------------FBX EXPORT CALLBACKS-----------
#-------------------------------------------

def FBX_Show_Axis_Callback (scene,context):
        
    global FBX_ShowAxis
    FBX_ShowAxis = scene.FBX_Show_Axis
    print ("Base name = " + str(FBX_ShowAxis))
    

def FBX_Axis_Forward_Callback (scene,context):
        
    global FBX_AxisForward
    FBX_AxisForward = scene.FBX_Axis_Forward
    print(FBX_AxisForward)
      
def FBX_Axis_Up_Callback (scene,context):
        
    global FBX_AxisUp
    FBX_AxisUp = scene.FBX_Axis_Up
    print(FBX_AxisUp)

def FBX_Smoothing_Selector_Callback (scene,context):
    
    global FBXSmoothingType
    FBXSmoothingType = scene.FBX_Smoothing
    print (str(FBXSmoothingType))
    
def FBX_Base_Name_Selector_Callback (scene,context):
        
    global FBXBaseNameSelector
    FBXBaseNameSelector = scene.FBX_base_name  
    print ("Base name = " + str(FBXBaseNameSelector)) 
    
def FBX_Relative_Assets_Folder_Callback (scene,context):    
    
    global FBXRelativeFolderSelector
    FBXRelativeFolderSelector = scene.FBX_Relative_Assets_Folder 
    print ("Base name = " + str(FBXRelativeFolderSelector))
    
    
def FBX_Export_Collision_Callback  (scene,context):    
    
    global FBX_ExportCollision
    FBX_ExportCollision = scene.FBX_Export_Collision_Obj
    print ("Base name = " + str(FBX_ExportCollision))
    
    
def FBX_TangentSpace_Callback (scene,context):    
    
    global FBX_Tangent
    FBX_Tangent = scene.FBX_TangentSpace
    print ("Base name = " + str(FBX_Tangent))
    
    
def FBX_BakeAnim_Callback (scene,context):    
    
    global FBX_Bake_Anim
    FBX_Bake_Anim = scene.FBX_BakeAnim
    print ("Base name = " + str(FBX_Bake_Anim))
    
def FBX_NLA_Callback (scene,context):    
    
    global FBX_NLA
    FBX_NLA = scene.FBX_Use_NLA
    print ("Base name = " + str(FBX_NLA))

def FBX_All_Actions_Callback (scene,context):    
    
    global FBX_AllActions
    FBX_AllActions = scene.FBX_All_Actions
    print ("Base name = " + str(FBX_AllActions))
    
def FBX_Anim_Steep_Callback (scene,context):    
    
    global FBX_AnimStep
    FBX_AnimStep = scene.FBX_Anim_Step
    print ("Base name = " + str(FBX_AnimStep))
    
def FBX_Anim_Simplify_Callback (scene,context):    
    
    global FBX_AnimSimplify
    FBX_AnimSimplify = scene.FBX_Anim_Simplify
    print ("Base name = " + str(FBX_AnimSimplify))
    
def FBX_Use_Anim_Callback (scene,context):    
    
    global FBX_UseAnim
    FBX_UseAnim = scene.FBX_Use_Anim
    print ("Base name = " + str(FBX_UseAnim))
    
def FBX_All_Actions_61_Callback (scene,context):    
    
    global FBX_AllActions61
    FBX_AllActions61 = scene.FBX_All_Actions_61
    print ("Base name = " + str(FBX_AllActions61))
    
def FBX_Pivot_To_Center_Callback (scene,context):    
    
    global FBX_PivotToCenter
    FBX_PivotToCenter = scene.FBX_Pivot_to_Center
    print ("Base name = " + str(FBX_PivotToCenter))  
    

    

#-------------------------------------------
#-----------FBX EXPORT PROPERTIES-----------
#-------------------------------------------
def FBX_Export_Properties(scn):
    
    #Use Smoothing faces?
    
    #Smoothing items
    FBX_smooth_Type = [
                    ('OFF', 'OFF', 'OFF'),
                    ('FACE', 'FACE', 'FACE'),
                    ('EDGE', 'EDGE' ,'EDGE')
                    ]
    
    #Smoothing
    bpy.types.Scene.FBX_Smoothing = EnumProperty(
        items = FBX_smooth_Type,                      
        name = "FBX Smooth type used:",
        default = 'OFF',
        update = FBX_Smoothing_Selector_Callback,
        description='Smoothing type for the objects')
    scn['FBX_Smoothing'] = 0    

    #Pivot To center
    bpy.types.Scene.FBX_Pivot_to_Center = BoolProperty(
        name = "Pivot To Center",
        default=False,
        update = FBX_Pivot_To_Center_Callback, 
        description = "Allow to Export objects with the correct pivot point without have the object at the center of the scene")
    scn['FBX_Pivot_to_Center'] = False 
    
    
    #name origins
    FBX_name_origins = [
                    ('Object', 'Object', 'Object'),
                    ('Custom', 'Custom', 'Custom')
                    ]
    
    #naming base
    bpy.types.Scene.FBX_base_name = EnumProperty(
        items = FBX_name_origins,                      
        name = "FBX Export Name Used:",
        default = "Object",
        update = FBX_Base_Name_Selector_Callback,
        description='Base name for Export as FBX')
    scn['FBX_base_name'] = 0
    
    #Show Axis?
    bpy.types.Scene.FBX_Show_Axis = BoolProperty(
        name = "Show Axis",
        default=False,
        update = FBX_Show_Axis_Callback, 
        description = "Check for show Axis Orientation")
    scn['FBX_Show_Axis'] = False
    
    
    
    #Axis_Forward inputs
    FBX_Axis_ForwardList = [
                        ('X', "X Forward", ""),
                        ('Y', "Y Forward", ""),
                        ('Z', "Z Forward", ""),
                        ('-X', "-X Forward", ""),
                        ('-Y', "-Y Forward", ""),
                        ('-Z', "-Z Forward", "")
                        ]
    
    #Axis Fordware
    bpy.types.Scene.FBX_Axis_Forward = EnumProperty(
        items = FBX_Axis_ForwardList,                      
        name = "Forward",
        default = '-Z',
        update = FBX_Axis_Forward_Callback,
        description='Set the Forward Axis')
    scn['FBX_Axis_Forward'] = 5
    
    #Axis_Up inputs
    FBX_Axis_UpList = [
                        ('X', "X Up", ""),
                        ('Y', "Y Up", ""),
                        ('Z', "Z Up", ""),
                        ('-X', "-X Up", ""),
                        ('-Y', "-Y Up", ""),
                        ('-Z', "-Z Up", "")
                        ]
    
    #Axis Up
    bpy.types.Scene.FBX_Axis_Up = EnumProperty(
        items = FBX_Axis_UpList,                      
        name = "Up",
        default = 'Y',
        update = FBX_Axis_Up_Callback,
        description='Set the Up Axis')
    scn['FBX_Axis_Up'] = 1
    
    
    
    
    
    #custom name
    bpy.types.Scene.FBX_Export_Custom_Name = StringProperty(
        name = "FBX Custom Name",
        default='', #New Name
        description='Export Objects with a custom name')
    scn['FBX_Export_Custom_Name'] = ""
    
    #Export To relative path: UE ASsets
    bpy.types.Scene.FBX_Relative_Assets_Folder = BoolProperty(
        name = "UE Assets Folder",
        default=True,
        update = FBX_Relative_Assets_Folder_Callback, 
        description = "Export into relative folder called: UE Assets")
    scn['FBX_Relative_Assets_Folder'] = True    
    
    
    #custom Path
    bpy.types.Scene.FBX_Custom_Export_Path = StringProperty(
        name = "FBX Custom Folder",
        default='', #Custom Export Folder
        description='Export Objects To a custom Path',
        subtype = 'DIR_PATH')
    scn['FBX_Custom_Export_Path'] = ""
    


    
    #Export Collision Objects too
    bpy.types.Scene.FBX_Export_Collision_Obj = BoolProperty(
        name = "Export Collision Objects",
        default=False,
        update = FBX_Export_Collision_Callback, 
        description = "Export Collision Objects along selected objects")
    scn['FBX_Export_Collision_Obj'] = False   
    

    
    #Use Tangent Space ?
    bpy.types.Scene.FBX_TangentSpace = BoolProperty(
        name = "Export Collision Objects",
        default=True,
        update = FBX_TangentSpace_Callback, 
        description = "Add binormal and tangent vectors, together with normal they form the tangent space (will only work correctly with tris/quads only meshes!")
    scn['FBX_TangentSpace'] = True
    
    #Use Bake anim ?
    bpy.types.Scene.FBX_BakeAnim = BoolProperty(
        name = "Use Bake",
        default=False,
        update = FBX_BakeAnim_Callback, 
        description = "Export baked keyframe animation")
    scn['FBX_BakeAnim'] = False
    
    #Use NLA ?
    bpy.types.Scene.FBX_Use_NLA = BoolProperty(
        name = "Use NLA",
        default=False,
        update = FBX_NLA_Callback, 
        description = "Export each non-muted NLA strip as a separated FBX’s AnimStack, if any, instead of global scene animation")
    scn['FBX_Use_NLA'] = False
    
    #Use All Actions ?
    bpy.types.Scene.FBX_All_Actions = BoolProperty(
        name = "Use All actions",
        default=True,
        update = FBX_All_Actions_Callback, 
        description = "Export each action as a separated FBX’s AnimStack, instead of global scene animation")
    scn['FBX_All_Actions'] = True
    
    
    #Sampling Rate (anim_step)
    bpy.types.Scene.FBX_Anim_Step = FloatProperty(
        name = "Sampling Rate",
        default=1,
        min=0.01,
        max=100,
        update= FBX_Anim_Steep_Callback)
    scn['FBX_Anim_Step'] = 1 
    
    #Anim Simplify 
    bpy.types.Scene.FBX_Anim_Simplify = FloatProperty(
        name = "Simplify",
        default=1,
        min=0,
        max=10,
        update= FBX_Anim_Simplify_Callback)
    scn['FBX_Anim_Simplify'] = 1
    

    
                 
  
    

#-------------------------------------------
#-----------FBX EXPORT FUNCTIONS------------
#-------------------------------------------    

# Grab values From Custom Path
def Get_Custom_Path(label, key, scn):        
    global FBX_ExportCustomPath     
    FBX_ExportCustomPath = scn["FBX_Custom_Export_Path"] 
    
def Get_Custom_ExportName(label, key, scn):        
    global FBX_CustomExportName    
    FBX_CustomExportName = scn["FBX_Export_Custom_Name"]
    

def FBX_SelectCollsionObjects (self,context):
    
        name = bpy.context.object.name
               
        obj = bpy.data.objects[name]
        activeLayer = bpy.context.scene.active_layer
        
        # Make visile all layers
        scn = bpy.context.scene        
        for n in range(0,20):
            scn.layers[n] = True
        
        
        if FBX_PivotToCenter == False:
            obs = bpy.context.selected_objects
            for ob in obs:
                name = ob.name
                bpy.ops.object.select_pattern(extend=True, pattern="UCX_"+name+"_"+"*", case_sensitive=True)
                
        if FBX_PivotToCenter == True:
            #Extend the selection with  All Collisio Objects        
            bpy.ops.object.select_pattern(extend=True, pattern="UCX_"+name+"_"+"*", case_sensitive=True)             
        
            
     
def FBX_Make_Only_selectedObjLayer_visible (self,context):
    
    # Make visile only the active object layer
    name = bpy.context.object.name               
    obj = bpy.data.objects[name]
    activeLayer = bpy.context.scene.active_layer    
    
    objectLayer = [i for i in range(len(obj.layers)) if obj.layers[i] == True]
    for i in range(len(bpy.context.scene.layers)):
        if i not in objectLayer:       
            bpy.context.scene.layers[i] = False
        else:
            bpy.context.scene.layers[i] = True                
    if activeLayer not in objectLayer:
        bpy.context.scene.layers[activeLayer] = False
    
    


def FBX_Export(self,context): 
    
    global FBX_ExportCustomPath
    global FBX_name_multi
    
    scn = context.scene       
        
    Get_Custom_Path("String:   ", 'FBX_Custom_Export_Path', scn)
    Get_Custom_ExportName("String:   ", 'FBX_Custom_Export_Path', scn) 
        
    #Get Name 
    
    if FBX_PivotToCenter == True:
        
        FBX_name = FBX_name_multi       
                
    if FBX_PivotToCenter == False:
        
        if FBXBaseNameSelector == "Object":
            FBX_name = bpy.context.object.name
            #print(FBX_name)
        if  FBXBaseNameSelector == "Custom":
            FBX_name = FBX_CustomExportName
            #print(FBX_name)    
        
    #Paths
    #FBX_ExportRelativePath = bpy.path.relpath("//UE Assets")
    FBX_ExportRelativePath = bpy.path.abspath("//UE4 Assets")        
    FBX_ExportCustom = bpy.path.abspath(FBX_ExportCustomPath)         
                      
    if FBXRelativeFolderSelector == True:
        Folder = FBX_ExportRelativePath
        if not exists(FBX_ExportRelativePath):
            mkdir(FBX_ExportRelativePath)
    if FBXRelativeFolderSelector == False:
        Folder = FBX_ExportCustom
        
    #Profiles:
    
    
    if FBX_PivotToCenter == False and FBX_ExportCollision == True:
        FBX_SelectCollsionObjects (self,context)    
    else:
        print("no collision exported")               
                
    #Export FBX
    bpy.ops.export_scene.fbx(check_existing=True,
                             filepath= Folder + '/'+ FBX_name +'.fbx',
                             filter_glob="*.fbx",
                             version='BIN7400',
                             use_selection=True, 
                             apply_unit_scale=True,
                             axis_forward=FBX_AxisForward,
                             axis_up=FBX_AxisUp,
                             bake_space_transform=True,
                             object_types= {'MESH'},
                             use_mesh_modifiers=True,
                             mesh_smooth_type=FBXSmoothingType, 
                             use_mesh_edges=False, 
                             use_tspace=True,
                             use_custom_props=True,                             
                             path_mode='AUTO',
                             embed_textures=False, 
                             batch_mode='OFF', 
                             use_batch_own_dir=False,
                             use_metadata=True)   
       
    if FBX_PivotToCenter == False and FBX_ExportCollision == True:
        bpy.ops.object.select_all(action='DESELECT')
        FBX_Make_Only_selectedObjLayer_visible (self,context)    
    else:
        print("no collision exported") 
        
    FBX_ExportCustomPath = ""
    
    
    
    print ("Export OK")    



#-------------------------------------------
#-----------------RIG FUNCTIONS-----------------
#-------------------------------------------

#Rig Properties


def Animation_UI_Properties(scn):  
      
    #Show Rig Options
    bpy.types.Scene.UE_Show_Rig_Props= BoolProperty(
        name = "Show Rig Options",
        default=True,
        update = UE_Show_Rig_Props_Callback, 
        description = "Show The options for the RIG")
    scn['UE_Show_Rig_Props'] = True 
    
    #Show Rig Export Options
    bpy.types.Scene.UE_Show_Export_options= BoolProperty(
        name = "Show Export Options",
        default=False,
        update = UE_Show_Export_option_Callback, 
        description = "Show Export Options for customize the fbx name,folder and scale")
    scn['UE_Show_Export_options'] = False

     
   
#Rig Callbacks  UE_ShowAdvanced_Rig_Prop_Callback 

def RIG_Name_Callback (scene,context):    
    
    global UE_Custom_RIG_Name
    UE_Custom_RIG_Name= scene.Custom_RIG_name
    
def UE_Show_Rig_Props_Callback (scene,context):    
    
    global UE_ShowRigProps
    UE_ShowRigProps= scene.UE_Show_Rig_Props
    
def UE_Show_Export_option_Callback (scene,context):    
    
    global UE_ShowRigExport
    UE_ShowRigExport= scene.UE_Show_Export_options   
    
    
def ACT_Name_Callback (scene,context):    
    
    global UE_Custom_ACT_Name
    UE_Custom_ACT_Name= scene.Custom_ACT_name
    

#-------------------------------------------
#-----------------RIG EXPORT-------------------
#-------------------------------------------



def FBX_Export_Character(self,context):    
    
    scn = context.scene       
        
    Get_Custom_Path("String:   ", 'FBX_Custom_Export_Path', scn)
    Get_Custom_ExportName("String:   ", 'FBX_Custom_Export_Path', scn) 
        
    #Get Name 
         
    if FBXBaseNameSelector == "Object":
        FBX_name = bpy.context.object.name
            
    if  FBXBaseNameSelector == "Custom":
        FBX_name = FBX_CustomExportName
    
    objName=bpy.context.scene.objects.active.name
             
        
    #Paths
    #FBX_ExportRelativePath = bpy.path.relpath("//UE Assets")
    FBX_ExportRelativePath = bpy.path.abspath("//UE4 Assets/")
    FBX_Character_Path =  FBX_ExportRelativePath + objName+"_Character"       
    FBX_ExportCustom = bpy.path.abspath(FBX_ExportCustomPath)
                      
    if FBXRelativeFolderSelector == True:
        Folder = FBX_Character_Path
        if not exists(FBX_ExportRelativePath):
            mkdir(FBX_ExportRelativePath)
        if not exists(FBX_Character_Path):
            mkdir(FBX_Character_Path)
    if FBXRelativeFolderSelector == False:
        Folder = FBX_ExportCustom
              
    #Export FBX
    bpy.ops.export_scene.fbx(check_existing=True,
                             filepath= Folder + '/'+ FBX_name +'.fbx',
                             filter_glob="*.fbx",
                             version='BIN7400',
                             use_selection=True, 
                             axis_forward=FBX_AxisForward,
                             axis_up=FBX_AxisUp,
                             bake_space_transform=False,
                             apply_unit_scale=True,
                             object_types={'ARMATURE', 'MESH'},
                             use_mesh_modifiers=True,
                             mesh_smooth_type=FBXSmoothingType,
                             use_mesh_edges=False, 
                             use_tspace=True,
                             use_custom_props=False,
                             add_leaf_bones=False,
                             primary_bone_axis='Y',
                             secondary_bone_axis='X',
                             use_armature_deform_only=True,
                             path_mode='AUTO',
                             embed_textures=False, 
                             batch_mode='OFF', 
                             use_batch_own_dir=False,
                             use_metadata=True)   
        
    
    print ("Export OK")    



def FBX_Export_BakedAnimation(self,context):    
    
    scn = context.scene       
        
    Get_Custom_Path("String:   ", 'FBX_Custom_Export_Path', scn)
    Get_Custom_ExportName("String:   ", 'FBX_Custom_Export_Path', scn) 
        
    #Get Name
    
    ActionName=bpy.context.active_object.animation_data.action.name 
    objName=bpy.context.scene.objects.active.name
    
         
    if FBXBaseNameSelector == "Object":
        FBX_name = bpy.context.object.name + "_" +ActionName
            
    if  FBXBaseNameSelector == "Custom":
        FBX_name = FBX_CustomExportName+ "_" +ActionName
            
        
    #Paths
    #FBX_ExportRelativePath = bpy.path.relpath("//UE Assets")
    FBX_ExportRelativePath = bpy.path.abspath("//UE4 Assets/")
    FBX_Character_Path =  FBX_ExportRelativePath + objName+"_Character"
    FBX_Animation_Path =  FBX_Character_Path+"/Animations"     
    FBX_ExportCustom = bpy.path.abspath(FBX_ExportCustomPath)      
                      
    if FBXRelativeFolderSelector == True:
        Folder = FBX_Animation_Path
        if not exists(FBX_ExportRelativePath):
            mkdir(FBX_ExportRelativePath)
        if not exists(FBX_Character_Path):
            mkdir(FBX_Character_Path)
        if not exists(FBX_Animation_Path):
            mkdir(FBX_Animation_Path)
    if FBXRelativeFolderSelector == False:
        Folder = FBX_ExportCustom
    
                
    #Export FBX
    bpy.ops.export_scene.fbx(check_existing=True,
                             filepath= Folder + '/'+ FBX_name +'.fbx',
                             filter_glob="*.fbx",
                             version='BIN7400',
                             use_selection=True, 
                             apply_unit_scale=True,
                             axis_forward=FBX_AxisForward,
                             axis_up=FBX_AxisUp,
                             bake_space_transform=False,
                             object_types={'ARMATURE'},
                             add_leaf_bones=False,
                             primary_bone_axis='Y',
                             secondary_bone_axis='X',
                             use_armature_deform_only=True,
                             bake_anim=True,
                             bake_anim_use_all_bones =True,
                             bake_anim_use_nla_strips=False,
                             bake_anim_use_all_actions=False,
                             bake_anim_step=FBX_AnimStep,
                             bake_anim_simplify_factor=FBX_AnimSimplify,
                             use_anim=True,
                             use_anim_action_all=False,
                             use_default_take=False,
                             use_anim_optimize=False,
                             anim_optimize_precision=6.0,
                             path_mode='AUTO',
                             embed_textures=False, 
                             batch_mode='OFF', 
                             use_batch_own_dir=False,
                             use_metadata=True)   
    
    print ("Export OK")    



def FBX_Export_CameraAnimation(self,context):    
    
    scn = context.scene       
        
    Get_Custom_Path("String:   ", 'FBX_Custom_Export_Path', scn)
    Get_Custom_ExportName("String:   ", 'FBX_Custom_Export_Path', scn) 
        
    #Get Name
    
    #ActionName=bpy.context.active_object.animation_data.action.name 
    objName=bpy.context.scene.objects.active.name
    
         
    if FBXBaseNameSelector == "Object":
        FBX_name = bpy.context.object.name #+ "_" +ActionName
            
    if  FBXBaseNameSelector == "Custom":
        FBX_name = FBX_CustomExportName #+ "_" +ActionName
            
        
    #Paths
    #FBX_ExportRelativePath = bpy.path.relpath("//UE Assets")
    FBX_ExportRelativePath = bpy.path.abspath("//UE4 Assets/")
    FBX_Animation_Path =  FBX_ExportRelativePath+"/Camera_Animations"     
    FBX_ExportCustom = bpy.path.abspath(FBX_ExportCustomPath)      
                      
    if FBXRelativeFolderSelector == True:
        Folder = FBX_Animation_Path
        if not exists(FBX_ExportRelativePath):
            mkdir(FBX_ExportRelativePath)
        if not exists(FBX_Animation_Path):
            mkdir(FBX_Animation_Path)
    if FBXRelativeFolderSelector == False:
        Folder = FBX_ExportCustom
    
                
    #Export FBX    
    
    bpy.ops.export_scene.fbx(check_existing=True,
                             filepath= Folder + '/'+ FBX_name +'.fbx',
                             filter_glob="*.fbx",
                             version='BIN7400',
                             use_selection=True, 
                             apply_unit_scale=True,
                             axis_forward=FBX_AxisForward,
                             axis_up=FBX_AxisUp,
                             bake_space_transform=False,
                             object_types = {'CAMERA'},
                             add_leaf_bones=False,
                             bake_anim=True,
                             bake_anim_use_all_bones =False,
                             bake_anim_use_nla_strips=False,
                             bake_anim_use_all_actions=False,
                             bake_anim_step=FBX_AnimStep,
                             bake_anim_simplify_factor=FBX_AnimSimplify,
                             use_anim=True,
                             path_mode='AUTO',
                             embed_textures=False, 
                             batch_mode='OFF', 
                             use_batch_own_dir=False,
                             use_metadata=True)    
        
    
    print ("Export OK") 
      


def UE_Export_Animation(self,context):
    
    #Get A list of objects parented to the selected armature
    ArmChildrenList = bpy.context.object.children
            
            
    BonesList = bpy.context.object.pose.bones
    BonesListEdit = bpy.context.object.data.edit_bones
    ob = bpy.context.object        
    armature = ob.data
    objProps = bpy.context.object
              
    FakeAction=bpy.context.object.animation_data.action
    ArmatureGroups = bpy.context.active_object.pose.bone_groups 
    
    Armature_Rotated=False
    
        
    animationFrames= bpy.context.object.animation_data.action.frame_range[1] 
    bpy.context.scene.frame_end = animationFrames
             
   #Store bones with groups for export
    if  bpy.context.active_object.type == 'ARMATURE':             
        bpy.ops.object.mode_set( mode='POSE' )
        bpy.ops.pose.select_all(action='DESELECT')

              
        DeformBonesList=[]
        EpicExtraBonesList=[]
        
        if "DeformBones" in ArmatureGroups:
             pb_group = ob.pose.bone_groups['DeformBones'] # the pose bone group we wanna select
             for bone in BonesList:
                 if bone.bone_group == pb_group:
                     DeformBonesList.append(bone.name)
                     
        if "EpicExtra" in ArmatureGroups:
            pbe_group = ob.pose.bone_groups['EpicExtra'] # the pose bone group we wanna select
            for bone in BonesList:
                 if bone.bone_group == pbe_group:
                     EpicExtraBonesList.append(bone.name)
      
         #Separate Bones              
        bpy.ops.object.mode_set( mode='EDIT' )
        bpy.ops.armature.select_all(action='DESELECT')  
        
        for bone in  BonesListEdit:          
            if bone.name in DeformBonesList:
                bone.use_deform = True
            elif bone.name in EpicExtraBonesList:
                bone.use_deform = True
            else:
                bone.use_deform = False
        
        bpy.ops.object.mode_set( mode='OBJECT' )
                 
        #Export Armature Animation    
        FBX_Export_BakedAnimation(self,context)
        
        #for bone in BonesListEdit:
                #bone.use_deform = True

       
        
        del DeformBonesList[:]
        del EpicExtraBonesList[:]
    
    
def hideIKArmsOFF(): 
    
    BonesList = bpy.context.object.pose.bones
    ob = bpy.context.object
          
   
    for bone in BonesList:            
        if bone.bone_group_index == 3:
            bonename = ob.data.bones[bone.name]
            ob.data.bones[bone.name].hide = False
        if bone.bone_group_index == 5:
            bonename = ob.data.bones[bone.name]
            ob.data.bones[bone.name].hide = False
            
def hideIKArmsON():
    
    BonesList = bpy.context.object.pose.bones
    ob = bpy.context.object
          
  
    for bone in BonesList:            
        if bone.bone_group_index == 3:
            bonename = ob.data.bones[bone.name]
            ob.data.bones[bone.name].hide = True
        if bone.bone_group_index == 5:
            bonename = ob.data.bones[bone.name]
            ob.data.bones[bone.name].hide = True
            
def hideIKlegOFF():
    
    BonesList = bpy.context.object.pose.bones
    ob = bpy.context.object
    
   
    for bone in BonesList:            
        if bone.bone_group_index == 2:
            bonename = ob.data.bones[bone.name]
            ob.data.bones[bone.name].hide = False
        if bone.bone_group_index == 4:
            bonename = ob.data.bones[bone.name]
            ob.data.bones[bone.name].hide = False
            
            
def hideIKlegON():
    
    BonesList = bpy.context.object.pose.bones
    ob = bpy.context.object
    
   
    for bone in BonesList:            
        if bone.bone_group_index == 2:
            bonename = ob.data.bones[bone.name]
            ob.data.bones[bone.name].hide = True
        if bone.bone_group_index == 4:
            bonename = ob.data.bones[bone.name]
            ob.data.bones[bone.name].hide = True
            
            
#-------------------------------------------
#-----------------BUTTONS-------------------
#-------------------------------------------

#Export Camera Animation

class UEExportCamera(bpy.types.Operator):
    """UE Export Camera Button"""
    bl_idname = "ue.export_camera"
    bl_label = "Export Camera Animation"
    
    def execute (self, context):
        
        bpy.ops.transform.rotate(value=1.5708,
                                 axis=(-0.143126, -0.0365628, 0.989029),
                                 constraint_axis=(False, True, False), 
                                 constraint_orientation='LOCAL', 
                                 mirror=False, proportional='DISABLED', 
                                 proportional_edit_falloff='SMOOTH', 
                                 proportional_size=1)
                                 
        
        FBX_Export_CameraAnimation(self,context)
        
        bpy.ops.transform.rotate(value=-1.5708,
                                 axis=(-0.143126, -0.0365625, 0.989029),
                                 constraint_axis=(False, True, False), 
                                 constraint_orientation='LOCAL', 
                                 mirror=False, proportional='DISABLED', 
                                 proportional_edit_falloff='SMOOTH', 
                                 proportional_size=1)
        
        return {'FINISHED'}
    
    
#Set UE Scale button

class UEScaleOperator(bpy.types.Operator):
    """UE Scale Operator Button"""
    bl_idname = "ue.scale_operator"
    bl_label = "Set UE Scale"
    
    def execute (self, context):
        
        scn = context.scene 
        
             
        unit = context.scene.unit_settings 
        
           
        
        #Set unit and scale lenght      
        unit.system = 'METRIC'
        unit.scale_length = 0.01
        
        context.space_data.clip_start = 0.1
        context.space_data.clip_end = 1000000.0
        
        print (unit.system)
        print (unit.scale_length)
        
        #Scale objects if selected      
        if ObjScale == True:
            
            bpy.ops.view3d.snap_cursor_to_center()
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(100, 100, 100))
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.context.space_data.pivot_point = 'MEDIAN_POINT'           
                                       
        else:
            print ("scale objects is not selected,only will be set the scene scale")         
              
        return {'FINISHED'}

#Set Collision Pivots button    
class SetCollisionPivots_Button(bpy.types.Operator):
    """Button Set the pivot poit on collision objects"""
    bl_idname = "ue.setcollpivots_button"
    bl_label = "Set Collision Pivots"    
            
    def execute (self, context):
        
        #Create group
        
        
            
        group = "CollisionPivotgroup"
        
        if group in bpy.data.groups:
            print ("Group already created,will be removed and created again")
            bpy.data.groups["CollisionPivotgroup"].user_clear()        
            bpy.data.groups.remove(bpy.data.groups["CollisionPivotgroup"])
            bpy.ops.group.create(name="CollisionPivotgroup")   
        else:
            bpy.ops.group.create(name="CollisionPivotgroup")        
        
        ActionGroup = bpy.data.groups["CollisionPivotgroup"]
            
        bpy.ops.object.select_all(action='DESELECT')
            
        #Group Operation
            
        for ob in ActionGroup.objects:
                                                           
            print (ob.name)              
            ob.select = True
            bpy.context.scene.objects.active = ob
            bpy.ops.view3d.snap_cursor_to_selected()
            FBX_SelectCollsionObjects (self,context)
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            ob.select = False
            bpy.ops.object.select_all(action='DESELECT')
            FBX_Make_Only_selectedObjLayer_visible (self,context)
            
        bpy.data.groups["CollisionPivotgroup"].user_clear()        
        bpy.data.groups.remove(bpy.data.groups["CollisionPivotgroup"])        
        
        return {'FINISHED'}   
 
 
#Rename Button

class Rename_Button(bpy.types.Operator):
    """Button for Rename"""
    bl_idname = "rename.button"
    bl_label = "RenameButton"    
     
    
    @classmethod
    def poll(cls, context):
        return context.selected_objects != None
    
    
    def execute (self, context):
        
        scn = context.scene
    
        Get_custom_rename("String:   ", 'rename_custom', scn)
        #Get_custom_prefix("String:   ", 'rename_prefix', scn)
                  
        Rename_detablocks(self, context)     
              
        
        return {'FINISHED'}      
    

#Init button    
class InitUEToolsButton(bpy.types.Operator):
    """Init Main Properties"""
    bl_idname = "ue.init_button"
    bl_label = "InitButton"    
        
    def execute (self, context):       
        
        Main_UI_Properties(bpy.context.scene)
        SetObjScale(bpy.context.scene)
        Rename_Properties(bpy.context.scene)
        FBX_Export_Properties(bpy.context.scene)
        Animation_UI_Properties(bpy.context.scene)
        
        
        global Init
        Init = True        
        
        return {'FINISHED'}   

#FBX Export Actions

def FBX_Export_actions(self,context):
    
    if FBX_PivotToCenter == True:                  
            
        global FBX_name_multi
       
        
        scn = context.scene 
        
        sufix = 0
        
        #Create group
        
        group = "exportgroup"
    
        if group in bpy.data.groups:
            print ("Group already created")
        else:
            bpy.ops.group.create(name="exportgroup")        
    
        ActionGroup = bpy.data.groups["exportgroup"]
        
        bpy.ops.object.select_all(action='DESELECT') 
        
        Get_Custom_ExportName("String:   ", 'FBX_Custom_Export_Path', scn)
        
        #Group Operation
        
        for ob in ActionGroup.objects:
                                                       
            print(ob.name) 
                       
            ob.select = True
            bpy.context.scene.objects.active = ob
                           
            if FBXBaseNameSelector == "Object":
                FBX_name_multi = ob.name
            if FBXBaseNameSelector == "Custom":
                FBX_name_multi = FBX_CustomExportName + "_" + str(sufix)
                
            #Store initial position
            obStartPosX = ob.location[0]
            obStartPosY = ob.location[1]
            obStartPosZ = ob.location[2]
            
            if FBX_ExportCollision == False:
                print("Collision Not Exported")
            if FBX_ExportCollision == True:
                FBX_SelectCollsionObjects (self,context)  
            
            
            #move object to center
            bpy.ops.view3d.snap_cursor_to_center()
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
            #ob.location = (0,0,0) 
                           
            #Export                
            FBX_Export(self,context)
            
            #Move to initial position
            ob.location = (obStartPosX,obStartPosY,obStartPosZ)
            bpy.ops.view3d.snap_cursor_to_active()
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)               
                                
            ob.select = False
            
            if FBX_ExportCollision == False:
                print("Collision Not Exported")
            if FBX_ExportCollision == True:
                #FBX_SelectCollsionObjects (self,context)
                bpy.ops.object.select_all(action='DESELECT')
                FBX_Make_Only_selectedObjLayer_visible (self,context)               
            
            sufix = sufix +1           
                     
        bpy.data.groups["exportgroup"].user_clear()        
        bpy.data.groups.remove(bpy.data.groups["exportgroup"])       
        
        
        #print("pivotOK")
        
    if FBX_PivotToCenter == False:
        FBX_Export(self,context)
        print("Export normally")  



#FBX Export button    
class FBX_ExportButton(bpy.types.Operator):
    """Button for Fbx Export"""
    bl_idname = "ue.export_fbx_button"
    bl_label = "ExportFbxButton" 
    
      
            
    def execute (self, context):   
        
        ActualPath = dirname(bpy.data.filepath) 
        
        if FBXRelativeFolderSelector == True:            
            if ActualPath == "":
                self.report({'ERROR'}, "You need Save the file for use save automatically into a relative folder")
            else:
                FBX_Export_actions(self,context)
        else:
            FBX_Export_actions(self,context)       
         
            
        #print("test OK")
        return {'FINISHED'}




#Choose Action Buttons 
class Action_buttons(bpy.types.Operator):
    """Select Action For bake the Animations"""
    bl_idname = "ue.action_change"
    bl_label = "Actions"    
        
    act = bpy.props.StringProperty()   
    
    def execute(self, context): 
                       
        print(self.act)       
       
        bpy.context.active_object.animation_data.action = bpy.data.actions[self.act]
       
        return {'FINISHED'}   

#Delete Action Buttons 
class Delete_Action_buttons(bpy.types.Operator):
    """Delete actoin From List"""
    bl_idname = "ue.action_delete"
    bl_label = "Actions Delete"    
        
    actdel = bpy.props.StringProperty()   
    
    def execute(self, context):        
        
        #Remove the new created animation action from the RIG armature
        bpy.context.object.animation_data.action = None
   
        actions = bpy.data.actions
        
        for action in actions:
            if action.name == self.actdel:
                bpy.data.actions[self.actdel].user_clear()
                      
        for action in actions:            
            if action.users == 0 :
                bpy.data.actions.remove(action)
                           
                   
       
        return {'FINISHED'}
    
def ExportIKAnimation_proces(self,context):
    FakeAction=bpy.context.object.animation_data.action
    
                 
    if bpy.context.object.animation_data.action != None:
        
          
        UE_Export_Animation(self,context)             
     
        bpy.context.object.animation_data.action = FakeAction
      
        for action in bpy.data.actions:
            if action.users == 0 :
                action.user_clear()
                bpy.data.actions.remove(action)
    else:
        self.report({'ERROR'}, "The armature must have an action asigned")  
        
       

#Export IK Animation  
class Export_IK_animation(bpy.types.Operator):
    """Bake the animation from the helper bones to the deform bones and export animation"""
    bl_idname = "ue_export_anim.button"
    bl_label = "Export Animation" 
    
  
            
    def execute (self, context):
        
        #global Rotate_Armature
       
        if FBXRelativeFolderSelector == True:           
            ActualPath = dirname(bpy.data.filepath)
              
            if ActualPath == "":
                self.report({'ERROR'}, "You need Save the file for use save automatically into a relative folder")
            else:
                #Rotate_Armature = self.Rotate_Armature_180
                ExportIKAnimation_proces(self,context)
                
        else:
            #Rotate_Armature = self.Rotate_Armature_180
            ExportIKAnimation_proces(self,context)    
        
         
        return {'FINISHED'}
    
  
#Bake And Export All Animations

def ExportAllAnims_proces(self,context):
    
    ActionList=bpy.data.actions
    FakeAction=bpy.context.object.animation_data.action
    BonesList = bpy.context.object.pose.bones 
    

    
    #global Rotate_Armature
    
    for action in  ActionList:
        if action.use_fake_user == True:
            bpy.context.object.animation_data.action = action
            UE_Export_Animation(self,context)
                    
            bpy.context.object.animation_data.action = None
            bpy.ops.object.mode_set( mode='POSE' )
            for bone in BonesList:
                bpy.ops.pose.loc_clear()
                bpy.ops.pose.rot_clear()
            bpy.ops.object.mode_set( mode='OBJECT' )

   
    bpy.context.object.animation_data.action =  FakeAction
    
    for action in  ActionList:       
        if action.users == 0 :
            action.user_clear()
            bpy.data.actions.remove(action) 


class ExportAllAnims(bpy.types.Operator):
    """bake and export all animations with Fake User"""
    bl_idname = "ue_export_all.button"
    bl_label = "Export All Animations" 
 
    
    
    def execute (self, context):
        
      
                        
        if FBXRelativeFolderSelector == True:
                       
            ActualPath = dirname(bpy.data.filepath)
              
            if ActualPath == "":
                self.report({'ERROR'}, "You need Save the file for use save automatically into a relative folder")
            else:
               
                ExportAllAnims_proces(self,context)        
        else:
           
            ExportAllAnims_proces(self,context)            
                   
        return {'FINISHED'}
    


#Append Hero button

class AppendHeroTPP(bpy.types.Operator):
    """Append The Hero Character and the Rig"""
    bl_idname = "ue.append_hero"
    bl_label = "Append Hero"
    
    Custom_RIG_name = StringProperty(name="Custom Name",update = RIG_Name_Callback)
    Include_Hero_value = BoolProperty(name="Include Hero Mesh?")
    Include_LowRes = BoolProperty(name="Movile version?")
      
    def execute (self, context):
        
        Include_hero = self.Include_Hero_value
        RIG_name= self.Custom_RIG_name
        HeroLow = self.Include_LowRes
                
        #Grab the ctive layer before the operation       
        ActiveLayer = bpy.context.scene.layers.data.active_layer        
        
        #ScriptName = bpy.data.texts['ue_tools_v1-2.py'].name
        #ScriptPath = bpy.data.texts['ue_tools_v1-2.py'].filepath
        ScriptDirectory = os.path.dirname(os.path.realpath(__file__)) #bpy.data.texts['ue_tools_v1-2.py'].filepath.strip(ScriptName)
        BlendFileName = "UE4_Mannequinn_Template.blend"

        TemplatePath = os.path.join(ScriptDirectory, BlendFileName, "Object", "SK_MannequinMesh")
        TemplatePathLow = os.path.join(ScriptDirectory, BlendFileName, "Object", "SK_Mannequin_Mobile")
        TemplateDirectory = os.path.join(ScriptDirectory, BlendFileName, "Object", "")

        RIG_Armature_name = RIG_name
        RIG_Mesh_name = RIG_name + "_MESH"
        
        if bpy.data.objects.get(RIG_Armature_name) is not None:
            self.report({'ERROR'}, "Please Give an unique name to the New RIG you already have one "+RIG_name+" on the scene")  
            
        else:
            if Include_hero == True:                        
                if HeroLow == False:                                                   
                    bpy.ops.wm.link(filepath= TemplatePath,
                                      directory= TemplateDirectory,
                                      filename="SK_MannequinMesh",
                                      link=True,
                                      relative_path=True,
                                      autoselect=True,
                                      active_layer=True)
                                              
                    bpy.ops.object.make_local(type='ALL')
                    
                    bpy.context.scene.objects.active = bpy.data.objects["SK_MannequinMesh"]
                    bpy.data.objects['SK_MannequinMesh'].select = True
                    bpy.data.objects['SK_MannequinMesh'].name = RIG_Mesh_name
                    bpy.ops.object.select_all(action='DESELECT')
                    
                    bpy.context.scene.objects.active = bpy.data.objects["HeroTPP_Character"]
                    bpy.data.objects['HeroTPP_Character'].select = True
                    bpy.data.objects['HeroTPP_Character'].name = RIG_Armature_name 
                    bpy.ops.object.mode_set( mode='POSE' )
                   
                if HeroLow == True:                 
                    bpy.ops.wm.link(filepath= TemplatePathLow,
                                      directory= TemplateDirectory,
                                      filename="SK_Mannequin_Mobile",
                                      link=True,
                                      relative_path=True,
                                      autoselect=True,
                                      active_layer=True)
                                              
                    bpy.ops.object.make_local(type='ALL')
                    
                    bpy.context.scene.objects.active = bpy.data.objects["SK_Mannequin_Mobile"]
                    bpy.data.objects['SK_Mannequin_Mobile'].select = True
                    bpy.data.objects['SK_Mannequin_Mobile'].name = RIG_Mesh_name
                    bpy.ops.object.select_all(action='DESELECT')
                    
                    bpy.context.scene.objects.active = bpy.data.objects["HeroTPP_Character"]
                    bpy.data.objects['HeroTPP_Character'].select = True
                    bpy.ops.object.delete()
                    
                    bpy.context.scene.objects.active = bpy.data.objects["HeroTPP_Character_Mobile"]
                    bpy.data.objects['HeroTPP_Character_Mobile'].select = True
                    bpy.data.objects['HeroTPP_Character_Mobile'].name = RIG_Armature_name 
                    bpy.ops.object.mode_set( mode='POSE' )
                               
            else:
                bpy.ops.wm.link(filepath= TemplatePath,
                                      directory= TemplateDirectory,
                                      filename="SK_MannequinMesh",
                                      link=True,
                                      relative_path=True,
                                      autoselect=True,
                                      active_layer=True)
                                      
                bpy.ops.object.make_local(type='ALL')
                                      
                bpy.context.scene.objects.active = bpy.data.objects["SK_MannequinMesh"]
                bpy.data.objects['SK_MannequinMesh'].select = True
                bpy.ops.object.delete()
                
                bpy.context.scene.objects.active = bpy.data.objects["HeroTPP_Character"]
                bpy.data.objects['HeroTPP_Character'].select = True
                bpy.data.objects['HeroTPP_Character'].name = RIG_Armature_name 
                bpy.ops.object.mode_set( mode='POSE' )   
           
           
       
        return {'FINISHED'}
      
       
        
    def invoke(self, context, event):        
       
        global RIG_name, Include_hero , HeroLow      
        self.Custom_RIG_name = RIG_name
        self.Include_Hero_value = Include_hero
        self.Include_LowRes = HeroLow 
                         
        return context.window_manager.invoke_props_dialog(self)
      
       
         
        return {'FINISHED'}

def UE_ExportCharacter(self,context):
     
     #Get A list of objects parented to the selected armature
    ArmChildrenList = bpy.context.object.children
    
    
    BonesList = bpy.context.object.pose.bones
    BonesListEdit = bpy.context.object.data.edit_bones
    ob = bpy.context.object
    armature = ob.data
    objProps = bpy.context.object
    ArmatureGroups = bpy.context.active_object.pose.bone_groups
    
  
    
    #Store bones with groups for export
    if  bpy.context.active_object.type == 'ARMATURE':             
        bpy.ops.object.mode_set( mode='POSE' )
        bpy.ops.pose.select_all(action='DESELECT')

              
        DeformBonesList=[]
        EpicExtraBonesList=[]
        
        if "DeformBones" in ArmatureGroups:
             pb_group = ob.pose.bone_groups['DeformBones'] # the pose bone group we wanna select
             for bone in BonesList:
                 if bone.bone_group == pb_group:
                     DeformBonesList.append(bone.name)
                     
        if "EpicExtra" in ArmatureGroups:
            pbe_group = ob.pose.bone_groups['EpicExtra'] # the pose bone group we wanna select
            for bone in BonesList:
                 if bone.bone_group == pbe_group:
                     EpicExtraBonesList.append(bone.name)
      
         #Separate Bones              
        bpy.ops.object.mode_set( mode='EDIT' )
        bpy.ops.armature.select_all(action='DESELECT')  
        
        for bone in  BonesListEdit:          
            if bone.name in DeformBonesList:
                bone.use_deform = True
            elif bone.name in EpicExtraBonesList:
                bone.use_deform = True
            else:
                bone.use_deform = False
        
        bpy.ops.object.mode_set( mode='OBJECT' )
        
        
        #Export armature and child objects (No animation)        
        FBX_Export_Character(self,context)
          
        #for bone in BonesListEdit:
            #bone.use_deform = True
            
        del DeformBonesList[:]
        del EpicExtraBonesList[:]
    


#Export Character
class UE_Export_Character(bpy.types.Operator):
    """Export Character"""
    bl_idname = "ue_export_character.button"
    bl_label = "Export Character" 
    
  
            
    def execute (self, context):
        
       
        if FBXRelativeFolderSelector == True:           
             ActualPath = dirname(bpy.data.filepath)
              
             if ActualPath == "":
                 self.report({'ERROR'}, "You need Save the file for use save automatically into a relative folder")
             else:
               
                 UE_ExportCharacter(self,context)
        else:
           
            UE_ExportCharacter(self,context)
            
        return {'FINISHED'}
  
     
     
#Set Deform Bones Group (for no standar skeletons)

class UE_Set_Deform_Bones(bpy.types.Operator):
    """Set Deform Bones for no standar skeletons"""
    bl_idname = "ue_set_deform_bones.button"
    bl_label = "Set Deform Bones for no Hero RIG skeletons"    
            
    def execute (self, context):
        
         BoneList=bpy.context.object.data.bones
         BonesSelected = []
         
         for bone in BoneList:
             if bone.select==True:
                 BonesSelected.append(bone.name)
                
         if  BonesSelected != []:      
             bpy.ops.pose.group_assign(type=0)
             bpy.context.object.pose.bone_groups['Group'].name = "DeformBones" 
         else:
             self.report({'ERROR'}, "You need select some bones")
             print("You need select some bone")     
        
        
         return {'FINISHED'}
     
#Go to pose mode for set the deform bones (for no standar skeletons)

class UE_Set_POSE_mode(bpy.types.Operator):
    """Set pose mode for no standar skeletons"""
    bl_idname = "ue_set_podemode.button"
    bl_label = "Set Pose mode for no Hero RIG skeletons"    
            
    def execute (self, context): 
        
         global Steep1       
        
         bpy.ops.object.mode_set( mode='POSE' )
         Steep1=True
        
         return {'FINISHED'}
     
#Create Automatically DeformBones Gorup

class UE_AutomaticBoneGroup_button(bpy.types.Operator):
    """Create the "DeformBones" group automatically"""
    bl_idname = "ue.deformbone_create"
    bl_label = "Deform Bones"    
        
    
    
    def execute(self, context):
        
                 
         ArmChildrenList = bpy.context.object.children
         BonesListEdit = bpy.context.object.data.edit_bones
         BoneList = bpy.context.object.pose.bones
         armObject = bpy.context.scene.objects.active
         
         for child in ArmChildrenList:
             bpy.data.objects[child.name].select = True
         
         nonZero = []
         for child in ArmChildrenList:
             if child.type == 'MESH':           
                 for vert in child.data.vertices:
                    # Get a list of the non-zero group weightings for the vertex
                    for g in vert.groups:
                         g.weight = round(g.weight, 4)                     
                         if g.weight > .0000:
                              if g.group not in nonZero:
                                  nonZero.append(g.group) 
                              
                                                             
        
        
         nonZeroNames = []
         BonesSelected = []
         
         for child in ArmChildrenList:
             if child.type == 'MESH':
                
                 vertexGroups = bpy.data.objects[child.name].vertex_groups
                 for group in vertexGroups:                                                           
                     gName=group.name
                     gIndex=group.index
                     if gIndex in nonZero:
                         if gName not in nonZeroNames:
                            nonZeroNames.append(gName)
                      
         
         bpy.ops.object.select_all(action='DESELECT')
        
         bpy.data.objects[armObject.name].select = True
         bpy.context.scene.objects.active = bpy.data.objects[armObject.name]
         
         bpy.ops.object.mode_set( mode='POSE' )
         
         #Store visible bone layers
         Bonelayers = bpy.context.object.data.layers
         VisibleBoneLayers=[]
         for layer in Bonelayers:
             if layer == True:
                 VisibleBoneLayers.append(True)
             else:
                 VisibleBoneLayers.append(False)
         
         
         #Enable All bone layers
         for n in range(0,32):
            bpy.context.object.data.layers[n] = True

         
         #Deselect All bones
         bpy.ops.pose.select_all(action='DESELECT')
         
         
         #Reselect the bones   
         BonesSelected=[]
         
         for b in BoneList:
             if b.name in nonZeroNames:
                 b.bone.select=True
                 BonesSelected.append(b.name)
                    
                 
         #Asign The group
                
         if  BonesSelected != []:      
             bpy.ops.pose.group_assign()
             bpy.context.object.pose.bone_groups['Group'].name = "DeformBones" 
         else:
             self.report({'ERROR'}, "Any bones have vertex associated")
             
         #Restore Visible Layers
         i=0
         for n in range(0,32):
             bpy.context.object.data.layers[n] = VisibleBoneLayers[i]
             i=i+1
         
         bpy.ops.object.mode_set( mode='OBJECT' )
           
        

         return {'FINISHED'}   





    
#New action Button
class UE_New_Action_Button(bpy.types.Operator):
    """Create a new Action"""
    bl_idname = "ue.action_new_button"
    bl_label = "New Action"    
        
    Custom_ACT_name = StringProperty(name="Custom Action",update = ACT_Name_Callback)
          
    def execute (self, context):       
        
        ACT_name= self.Custom_ACT_name
        
        print(ACT_name)        
        bpy.data.actions.new(ACT_name)
        bpy.data.actions[ACT_name].use_fake_user = True 
        
        ob =  bpy.context.active_object
        
        if ob.animation_data == None:
            bpy.context.active_object.animation_data_create()
                                    
        ob.animation_data.action = bpy.data.actions[ACT_name]
      
        return {'FINISHED'}   
        
         
    def invoke(self, context, event):        
       
        global ACT_name   
        self.Custom_ACT_name = ACT_name                
        return context.window_manager.invoke_props_dialog(self)
        
        return {'FINISHED'} 
    
    
    
    
       
# RIG Props        
    
class UE_Rig_Props(bpy.types.Operator):
    """Set the value for the props on the Hero RIG"""
    bl_idname = "ue_rig_props.button"
    bl_label = "Set Propeties" 
    
    
    RigProp = bpy.props.StringProperty()    
            
    def execute (self, context):
        
        
        
        print(self.RigProp)
                
        #bpy.context.object["Constraints_ON_OFF"] = 1        
        if bpy.context.object[self.RigProp] == 0:
            bpy.context.object[self.RigProp] = 1
        else:
            bpy.context.object[self.RigProp] = 0            
        
        # "Buttos CAllbacks" for IK True     
        if self.RigProp == "IKMAIN":
            if bpy.context.object["IKMAIN"]==1:
                bpy.context.object["IKARMS"]=1
                bpy.context.object["IKLEGS"]=1
                bpy.context.object["Ik hand R Lock"]=1
                bpy.context.object["Ik Hand L Lock"]=1
                bpy.context.object["Ik Arm R"]=1.0
                bpy.context.object["IK Arm L"]=1.0
                bpy.context.object["Foot Lock L"]=1
                bpy.context.object["Foot Lock R"]=1
                bpy.context.object["Ik Leg L"]=1.0
                bpy.context.object["Ik Leg R"]=1.0
                hideIKArmsOFF()
                hideIKlegOFF() 
                 
            
            if  bpy.context.object["IKMAIN"]==0:
                bpy.context.object["IKARMS"]=0
                bpy.context.object["IKLEGS"]=0
                bpy.context.object["Ik hand R Lock"]=0
                bpy.context.object["Ik Hand L Lock"]=0
                bpy.context.object["Ik Arm R"]=0.0
                bpy.context.object["IK Arm L"]=0.0
                bpy.context.object["Foot Lock L"]=0
                bpy.context.object["Foot Lock R"]=0
                bpy.context.object["Ik Leg L"]=0.0
                bpy.context.object["Ik Leg R"]=0.0
                hideIKArmsON()
                hideIKlegON() 
        
        # "Buttos CAllbacks" for IK ARMS True          
        if self.RigProp == "IKARMS":
            if bpy.context.object["IKARMS"]==1:  
                bpy.context.object["Ik hand R Lock"]=1
                bpy.context.object["Ik Hand L Lock"]=1
                bpy.context.object["Ik Arm R"]=1.0
                bpy.context.object["IK Arm L"]=1.0                
                hideIKArmsOFF()
                        
            if bpy.context.object["IKARMS"]==0:  
                bpy.context.object["Ik hand R Lock"]=0
                bpy.context.object["Ik Hand L Lock"]=0 
                bpy.context.object["Ik Arm R"]=0.0
                bpy.context.object["IK Arm L"]=0.0
                hideIKArmsON()
                
        
         # "Buttos CAllbacks" for IK LEGS True          
        if self.RigProp == "IKLEGS":
            if bpy.context.object["IKLEGS"]==1:  
                bpy.context.object["Foot Lock L"]=1
                bpy.context.object["Foot Lock R"]=1
                bpy.context.object["Ik Leg L"]=1.0
                bpy.context.object["Ik Leg R"]=1.0
                hideIKlegOFF()
                
              
            if bpy.context.object["IKLEGS"]==0:  
                bpy.context.object["Foot Lock L"]=0
                bpy.context.object["Foot Lock R"]=0
                bpy.context.object["Ik Leg L"]=0.0
                bpy.context.object["Ik Leg R"]=0.0
                hideIKlegON()
                    
             
            
        return {'FINISHED'}
   
#-------------------------------------------
#------------------PANEL--------------------
#-------------------------------------------

class Mainpanel(bpy.types.Panel):
    """A Custom Panel in the Viewport Toolbar"""
    
    bl_label = "UE4 Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'        
    #bl_category = 'Tools'
    bl_category = 'UE4 Tools'
    
    @classmethod
    def poll (self,context):
        return (bpy.context.mode == 'OBJECT' or 'POSE') 
    
        

    def draw(self, context):
        
        scn = context.scene
        rs = bpy.context.scene             
        
        if Init == False:
            layout = self.layout        
            row = layout.row()
            col = row.column(align=True)
            col.operator ( "ue.init_button", text= "Open UE4 Tools",icon='VISIBLE_IPO_ON')
            
        if Init == True:
            
            #Main Buttons
            layout = self.layout        
            row = layout.row()
            col = row.column(align=True)
            #col.operator ( "tests.button", text= "Test Button")
            col.separator()      
            col.prop (scn, 'UESceneTools', text="Scene Tools",icon= 'SCENE_DATA')
            col.prop (scn, 'UERenameTools', text="Rename Tools",icon= 'GREASEPENCIL')
            col.prop (scn, 'UEAnimationTools', text="Animation Tools",icon= 'POSE_HLT')
            col.prop (scn, 'UEExportTools', text="Export Tools",icon= 'EXPORT')
            
        
        
            if (UE_SceneTools == True):                        
                #Scene Settings
                layout = self.layout     
            
                box = layout.box()
                box.label ("Scene Settings",icon="SCENE_DATA")
                              
                row = box.row()        
                col = row.column(align=True)       
                col.operator("ue.scale_operator", text="Set UE Scale", icon='ZOOM_SELECTED')
                col.prop(scn, 'UEObjScale')
                col.separator()
                col.label ("Additional Tools",icon="HELP")
                col.operator("ue.setcollpivots_button", text="Set Collision Pivots",icon='INLINK')        
        
            if (UE_RenameTools == True):       
                #Rename Settings
        
                box = layout.box()
                box.label ("Batch Rename Options",icon="SORTALPHA")
        
                box2 = box.box()
                row = box2.row() 
                row.label(text='Base Name:')
                row = box2.row() 
                row.prop(scn,'naming_base', expand=True)
        
                col = box2.column()
                col.prop(scn,'rename_custom')        
        
                box3 = box.box()
                col = box3.column()     
                col.label('Datablocks to rename:')
        
                col.prop(scn, 'rename_object')
                col.prop(scn, 'rename_data')
                col.prop(scn, 'rename_material')        
        
                box4 = box.box()
        
        
                col= box4.column()
                col.label ("Prefix?")
                col.prop (scn, 'IsCollision', text= "Collider")
                col.prop(scn, 'rename_use_prefix', text="Custom Prefix")  
                col.prop(scn, 'rename_prefix',text= "Custom")
             
        
                box4.label ("Where to add?")
                row = box4.row()
                row.prop(scn, 'prefix_object')
                row.prop(scn,'prefix_data')
                row.prop(scn, 'prefix_material')
                row = box.row(align = True)
                row.operator ("rename.button", text="Rename", icon='GREASEPENCIL')
                row = layout.row()
            
            if (UE_AnimationTools == True):
                    
                box = layout.box()
                box.label ("Animation Tools",icon="POSE_HLT")
                col = box.column()
                #Button For append The character 
                if context.mode == 'OBJECT':     
                    col.operator ( "ue.append_hero", text= "Append Hero RIG!",icon='VISIBLE_IPO_ON' )           
                
                #Check if I have selected object in context(prevent error if change layer)
                if bpy.context.selected_objects != []:                        
                    # DO all this only if active object is an ARMATURE
                    if  bpy.context.active_object.type == 'CAMERA':
                        col.operator ("ue.export_camera",text ="Export Camera Animation",icon='FORWARD')
                        row=box.row()                                
                        row.prop (scn, 'UE_Show_Export_options')
                               
                        if UE_ShowRigExport == True:                                   
                                
                            box14=box.box()
                            col=box14.column()
                            col.prop (scn,'FBX_Show_Axis')
                            col.prop (scn,'FBX_Anim_Step')
                            col.prop (scn,'FBX_Anim_Simplify')
                            
                            if FBX_ShowAxis == True:
                                col.prop (scn,'FBX_Axis_Forward')
                                col.prop (scn,'FBX_Axis_Up')   
                           
                            #name settings
                            box6 = box.box()
                            col= box6.column()
                            row=box6.row(align=True)
                            col.label(text='FBX Name:') 
                            row.prop(scn,'FBX_base_name', expand=True)                       
                            col.prop(scn,'FBX_Export_Custom_Name',text = "Custom Name")
                                                       
                            #Folder settings
                            box14 = box.box()
                            col= box14.column()
                            col.label ("Export Directory:")
                            col.prop(scn,'FBX_Relative_Assets_Folder',text= "Relative: UE Assets") 
                            col.prop(scn,"FBX_Custom_Export_Path" ,text = "Custom Path")  
                                   
                    if  bpy.context.active_object.type == 'ARMATURE':                 
                        
                        objProps = bpy.context.object
                        ArmatureGroups = bpy.context.active_object.pose.bone_groups                   
                       
                        if context.mode == 'OBJECT':                                 
                            #Tools For bake Animations       
                            box8 = box.box()                
                            col = box8.column() 
                                                      
                            col.label ("Export Anim Tools")             
                                       
                            if "DeformBones" in ArmatureGroups: 
                                col.operator ("ue_export_character.button",text = "Export  Character", icon='FORWARD')
                                col.operator ( "ue_export_anim.button", text= "Export Animation", icon='FORWARD')
                                col.operator ( "ue_export_all.button" ,text = "Export All Animations", icon='FORWARD')
                                
                                row=box.row()                                
                                row.prop (scn, 'UE_Show_Export_options')
                                
                                if UE_ShowRigExport == True:                                   
                                
                                    box14=box.box()
                                    col=box14.column()
                                    col.prop (scn, 'FBX_Smoothing')
                                    col.prop (scn,'FBX_Show_Axis')
                                    col.prop (scn,'FBX_Anim_Step')
                                    col.prop (scn,'FBX_Anim_Simplify')
                                    
                                    if FBX_ShowAxis == True:
                                        col.prop (scn,'FBX_Axis_Forward')
                                        col.prop (scn,'FBX_Axis_Up')   
                                   
                                    #name settings
                                    box6 = box.box()
                                    col= box6.column()
                                    row=box6.row(align=True)
                                    col.label(text='FBX Name:') 
                                    row.prop(scn,'FBX_base_name', expand=True)                       
                                    col.prop(scn,'FBX_Export_Custom_Name',text = "Custom Name")
                                                               
                                    #Folder settings
                                    box14 = box.box()
                                    col= box14.column()
                                    col.label ("Export Directory:")
                                    col.prop(scn,'FBX_Relative_Assets_Folder',text= "Relative: UE Assets") 
                                    col.prop(scn,"FBX_Custom_Export_Path" ,text = "Custom Path")
                               
                            else:
                                col.alignment='CENTER'
                                col.label("Steep 1:",icon='INFO')
                                col.label("For use this tools this")
                                col.label("armature must have a bone")
                                col.label("group called 'DeformBones'.")
                                col.operator( "ue_set_podemode.button", text= "Manual Creation")
                                col.operator( "ue.deformbone_create", text= "Auto Creation!")
                                
                                
                                

                        if context.mode == 'POSE':
                            if "HeroRIG" not in objProps:
                                if Steep1 == 1:
                                    if "DeformBones" not in ArmatureGroups:
                                        box8 = box.box()                
                                        col = box8.column()
                                        col.label("Steep 2:",icon='INFO')
                                        col.label("Select The bones you")
                                        col.label("want to Export and ")
                                        col.label("press the button below")                            
                                        col.operator ("ue_set_deform_bones.button", text = "Set Deform Bones")
                                    
                            if "HeroRIG" in objProps:                                
                                row=box.row()
                                #row.prop(scn,'UE_Show_Rig_Props',text="Show Rig Options")
                                if bpy.context.object["ShowRiGoptions"]==0: 
                                        row.operator("ue_rig_props.button", text="Show RIG Options",icon='CHECKBOX_DEHLT').RigProp="ShowRiGoptions"                      
                                if bpy.context.object["ShowRiGoptions"]==1:
                                        row.operator("ue_rig_props.button", text="Show RIG Options",icon='CHECKBOX_HLT').RigProp="ShowRiGoptions"  
                                
                                if bpy.context.object["ShowRiGoptions"]==1:   
                                    box9 = box.box()   
                                    box9.label("Rig Options")
                                    row=box9.row()
                                    
                                    if bpy.context.object["ShowAdvancedProps"]==0: 
                                        row.operator("ue_rig_props.button", text="Advanced Options",icon='CHECKBOX_DEHLT').RigProp="ShowAdvancedProps"                      
                                    if bpy.context.object["ShowAdvancedProps"]==1:
                                        row.operator("ue_rig_props.button", text="Advanced Options",icon='CHECKBOX_HLT').RigProp="ShowAdvancedProps"  
                                    
                                    row=box9.row()                                    
                                    if bpy.context.object.show_x_ray == True:
                                        row.prop (context.object, "show_x_ray",text="X Ray", expand=True,icon='RESTRICT_VIEW_OFF')
                                    else:
                                        row.prop (context.object, "show_x_ray",text="X Ray", expand=True,icon='RESTRICT_VIEW_ON')
                                       
                                    if bpy.context.object.data.show_names == True:
                                        row.prop (context.object.data, "show_names",text="Names", expand=True,icon='RESTRICT_VIEW_OFF')
                                    else:
                                        row.prop (context.object.data, "show_names",text="Names", expand=True,icon='RESTRICT_VIEW_ON')
                                        
                                    if bpy.context.object.data.show_axes == True:
                                        row.prop (context.object.data, "show_axes",text="Axes", expand=True,icon='RESTRICT_VIEW_OFF')
                                    else:
                                        row.prop (context.object.data, "show_axes",text="Axes", expand=True,icon='RESTRICT_VIEW_ON')
                                   
                                    row=box9.row()
                                    #row.prop(scn,'UE_ShowAdvanced_Rig_Prop',text= "Show Advanced Options?")
                                    row = box9.row(align=True)
                                    row.prop(context.active_object.data, 'layers', index=0, toggle=True, text='Deform Bones',icon='BONE_DATA')
                                    row.prop(context.active_object.data, 'layers', index=2, toggle=True, text='Helper Bones',icon='POSE_DATA')
                                    
                                    #Show Constraints Button
                                    row = box9.row()          
                                    if bpy.context.object["Constraints_ON_OFF"]==0:
                                        row.operator("ue_rig_props.button", text="Constraints ON",icon='LINKED').RigProp="Constraints_ON_OFF"                      
                                    if bpy.context.object["Constraints_ON_OFF"]==1:
                                        row.operator("ue_rig_props.button", text="Constraints OFF",icon='UNLINKED').RigProp="Constraints_ON_OFF"           
                                    
                                    #Show IK Swith Button                           
                                    row = box9.row(align=True)                    
                                    #row.prop(scn,'UEAnimationIK_ONOFF',icon= 'CONSTRAINT')                    
                                    if bpy.context.object["IKMAIN"]==0:
                                        row.operator("ue_rig_props.button", text="IK OFF",icon='UNLINKED').RigProp="IKMAIN"                      
                                    if bpy.context.object["IKMAIN"]==1:
                                        row.operator("ue_rig_props.button", text="IK ON",icon='LINKED').RigProp="IKMAIN"      
                                    
                                    #Show IK arms and legs Buttons             
                                    if bpy.context.object["IKMAIN"]==1:
                                                                      
                                        row = box9.row()
                                        #Show Buttons for arms
                                        if bpy.context.object["IKARMS"]==0:
                                            row.operator("ue_rig_props.button", text="IK Arms",icon='RESTRICT_VIEW_ON').RigProp="IKARMS"  
                                                   
                                        if bpy.context.object["IKARMS"]==1:
                                            row.operator("ue_rig_props.button", text="IK Arms",icon='RESTRICT_VIEW_OFF').RigProp="IKARMS"
                                        #Show buttons for legs    
                                        if bpy.context.object["IKLEGS"]==0:                        
                                            row.operator("ue_rig_props.button", text="IK Legs",icon='RESTRICT_VIEW_ON').RigProp="IKLEGS"                                     
                                        if bpy.context.object["IKLEGS"]==1:
                                            row.operator("ue_rig_props.button", text="IK Legs",icon='RESTRICT_VIEW_OFF').RigProp="IKLEGS" 
                                    
                                    
                                    #SHow IK value Bars
                                    if bpy.context.object["IKARMS"]==1:                                 
                                           row = box9.row()
                                           row.prop (context.object, '["Ik Arm R"]', slider = True)
                                           row = box9.row()
                                           row.prop (context.object, '["IK Arm L"]', slider = True)
                                    
                                    if bpy.context.object["IKLEGS"]==1:
                                           row = box9.row()
                                           row.prop (context.object, '["Ik Leg R"]', slider = True)
                                           row = box9.row()
                                           row.prop (context.object, '["Ik Leg L"]', slider = True)
                                                 
                                    
                                    #Show Ik Loks
                                    if bpy.context.object["IKARMS"]==1:                                        
                                        #Show button for Lock R hand 
                                        row = box9.row()                                                  
                                        if bpy.context.object["Ik hand R Lock"]==0:
                                            row.operator("ue_rig_props.button", text="Hand R",icon='UNLOCKED').RigProp="Ik hand R Lock"                      
                                        if bpy.context.object["Ik hand R Lock"]==1:
                                            row.operator("ue_rig_props.button", text="Hand R",icon='LOCKED').RigProp="Ik hand R Lock" 
                                               
                                        #Show button for Lock L hand
                                        if bpy.context.object["Ik Hand L Lock"]==0:
                                            row.operator("ue_rig_props.button", text="Hand L",icon='UNLOCKED').RigProp="Ik Hand L Lock"                      
                                        if bpy.context.object["Ik Hand L Lock"]==1:
                                            row.operator("ue_rig_props.button", text="Hand L",icon='LOCKED').RigProp="Ik Hand L Lock" 
                                        
                                        #Show Slider for animate hand lock
                                        if bpy.context.object["ShowAdvancedProps"]==1:
                                            row = box9.row()
                                            row.prop (context.object, '["Ik hand R Lock"]',text="Hand R", slider = True)
                                            row.prop (context.object, '["Ik Hand L Lock"]',text="Hand L", slider = True)
                                        
                                    if bpy.context.object["IKLEGS"]==1:
                                         #Show button for Lock R Foot
                                        row = box9.row()                         
                                        if bpy.context.object["Foot Lock R"]==0:
                                            row.operator("ue_rig_props.button", text="Foot R",icon='UNLOCKED').RigProp="Foot Lock R"                      
                                        if bpy.context.object["Foot Lock R"]==1:
                                            row.operator("ue_rig_props.button", text="Foot R",icon='LOCKED').RigProp="Foot Lock R" 
                                                
                                        #Show button for Lock L Foot
                                        if bpy.context.object["Foot Lock L"]==0:
                                            row.operator("ue_rig_props.button", text="Foot R",icon='UNLOCKED').RigProp="Foot Lock L"                      
                                        if bpy.context.object["Foot Lock L"]==1:
                                            row.operator("ue_rig_props.button", text="Foot R",icon='LOCKED').RigProp="Foot Lock L" 
                                            
                                        #Show Slider for animate hand lock
                                        if bpy.context.object["ShowAdvancedProps"]==1:
                                            row = box9.row()
                                            row.prop (context.object, '["Foot Lock R"]',text="Hand R", slider = True)
                                            row.prop (context.object, '["Foot Lock L"]',text="Hand L", slider = True) 
                                    
                                    row=box9.row()
                                    row.label("Inherit Rotation:",icon='GROUP_BONE')
                                    
                                    row=box9.row()                    
                                    if bpy.context.object["Head inherit Rotation"]==0: 
                                        row.operator("ue_rig_props.button", text="Head",icon='CHECKBOX_DEHLT',emboss=False).RigProp="Head inherit Rotation"                      
                                    if bpy.context.object["Head inherit Rotation"]==1:
                                        row.operator("ue_rig_props.button", text="Head",icon='CHECKBOX_HLT',emboss=False).RigProp="Head inherit Rotation"
                                    
                                    
                                    if bpy.context.object["Arms inherit Rotation"]==0: 
                                        row.operator("ue_rig_props.button", text="Arms",icon='CHECKBOX_DEHLT',emboss=False).RigProp="Arms inherit Rotation"                      
                                    if bpy.context.object["Arms inherit Rotation"]==1:
                                        row.operator("ue_rig_props.button", text="Arms",icon='CHECKBOX_HLT',emboss=False).RigProp="Arms inherit Rotation" 
                                    
                                        
                                    if bpy.context.object["Waist Inherit Rotation"]==0: 
                                        row.operator("ue_rig_props.button", text="Waist",icon='CHECKBOX_DEHLT',emboss=False).RigProp="Waist Inherit Rotation"                      
                                    if bpy.context.object["Waist Inherit Rotation"]==1:
                                        row.operator("ue_rig_props.button", text="Waist",icon='CHECKBOX_HLT', emboss=False).RigProp="Waist Inherit Rotation" 
                                         
                                    row=box9.row() 
                                    if bpy.context.object["ShowAdvancedProps"]==1:
                                        row.prop (context.object, '["Head inherit Rotation"]',text="Head inherit rotation", slider = True)  
                                        row.prop (context.object, '["Arms inherit Rotation"]',text="Arms inherit rotation", slider = True)  
                                        row.prop (context.object, '["Waist Inherit Rotation"]',text="Wais inherit rotation", slider = True)
                                    
                                    
   
                            
                        #DIsplay The Faked Actions stored on Data
                        actions = bpy.data.actions
                        
                        box = layout.box()
                        box.label("Available Actions", icon='ACTION')
                        row=box.row()
                        row=box.row(align=True)
                        row.alignment = 'RIGHT'
                        row.operator ("ue.action_new_button",icon='ZOOMIN')
                        box12=box.box()                        
                        row=box12.row()
                        col = row.column()
                            
                        for action in actions: 
                            if action.use_fake_user == True:                                                    
                                col.operator("ue.action_change", text=action.name,).act=action.name            
                        col = row.column()
                                                 
                        for action in actions: 
                            if action.use_fake_user == True:                                
                                col.operator("ue.action_delete",icon='X', text="").actdel=action.name  
                         
            if (UE_ExportTools == True):
                       
                #FBX Export Settings
                layout = self.layout     
            
                box = layout.box()
                box.label ("Export Tools",icon="EXPORT")
                
                #General settings
                box5 = box.box()
                col = box5.column()
                row = box5.row()
                #row.prop (scn, 'FBX_AssetTypeSelector', expand=True)
                
                row.label ("FBX Settings:")
                col = box5.column()
                col.prop (scn, 'FBX_Pivot_to_Center')
                col.prop (scn,'FBX_Export_Collision_Obj',text= "Export collision")
                
                col.prop (scn,'FBX_Show_Axis')
                if FBX_ShowAxis == True:
                    col.prop (scn,'FBX_Axis_Forward')
                    col.prop (scn,'FBX_Axis_Up')
                col.prop (scn, 'FBX_Smoothing')
                
                #name settings
                box6 = box.box()
                row = box6.row()
                row.label(text='FBX Name:')
                row = box6.row()
                row.prop(scn,'FBX_base_name', expand=True)
                col = box6.column()
                col.prop(scn,'FBX_Export_Custom_Name',text = "Custom Name")               
                
                #Folder settings
                box7 = box.box()
                col = box7.column()
                col.label ("Export Directory:")
                col.prop(scn,'FBX_Relative_Assets_Folder',text= "Relative: UE4 Assets") 
                col.prop(scn,"FBX_Custom_Export_Path" ,text = "Custom Path")  
                
                col = box.column()
                col.operator ( "ue.export_fbx_button", text= "FBX Export",icon='FORWARD')  



                
                         
#-------------------------------------------
#-----------------REGISTER------------------
#-------------------------------------------

classes = [
    SetCollisionPivots_Button,
    FBX_ExportButton,
    InitUEToolsButton,    
    Rename_Button,
    UE_Export_Character,
    UEScaleOperator,
    AppendHeroTPP,
    Mainpanel,
    Export_IK_animation,
    ExportAllAnims,
    Action_buttons,
    UE_Set_Deform_Bones,
    UE_Set_POSE_mode,
    UE_Rig_Props,
    UE_New_Action_Button,
    Delete_Action_buttons,
    UE_AutomaticBoneGroup_button,
    UEExportCamera        
    ]     
        
        
def register():    
    
    for c in classes:        
        bpy.utils.register_class(c)  

def unregister():  
    
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()












