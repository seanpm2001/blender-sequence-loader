import bpy
import fileseq
from .utils import *
from .importer_manager import *
import traceback

#  Codes here are mostly about the callback functions and update functions used in properties.py 



def callback_color_attribute(self, context):
    '''
    When an imported sequence selected, this function returns all the color attributes it has, such as 'id', 'velocity', etc.
    '''
    attr_items = [('None', 'None', '')]
    mytool = context.scene.my_tool
    item = mytool.imported[mytool.imported_num]
    for i in item.all_attributes:
        attr_items.append((i.name, i.name, ''))
    return attr_items


def update_color_attribute(self, context):
    '''
    When an imported sequence selected, and a new color attribute selected, it will update the importer so the color can be correctly rendered. 
    '''
    mytool = context.scene.my_tool
    idx = mytool.imported_num

    importer = importer_list[idx]
    item = mytool.imported[idx]
    if item.all_attributes_enum != "None":
        importer.set_color_attribute(item.all_attributes_enum)
        # this is used to store the used color attribute
        item.used_color_attribute.name = item.all_attributes_enum
    else:
        importer.set_color_attribute(None)
        item.used_color_attribute.name = 'None'


def callback_fileseq(self, context):
    '''
    Detects all the file sequences in the directory
    '''

    p = context.scene.my_tool.importer.path
    try:
        f = fileseq.findSequencesOnDisk(p)
    except:
        return [("None", "No sequence detected", "")]

    if not f:
        return [("None", "No sequence detected", "")]
    file_seq = []
    if len(f) >= 20:
        file_seq.append(
            ("Manual", "Manual, too much sequence detected, use pattern above", ""))
    else:      
        file_seq.append(("None", "Please select the pattern", "")) 
        for seq in f:
            file_seq.append((str(seq), seq.basename()+"@"+seq.extension(), ""))
        file_seq.append(("Manual", "Manually set the pattern, use the pattern entered above", ""))
    return file_seq


#  this function precheck and set the type of this sequence
def update_fileseq(self, context):
    '''
    When a file sequence selected, this function here do some pre-check, e.g. check if it's particle or mesh.
    '''
    file_seq_items_name = context.scene.my_tool.importer.fileseq
    if file_seq_items_name == "None":
        return
    f = None
    if file_seq_items_name == "Manual":
        try:
            p = context.scene.my_tool.importer.path
            pattern = context.scene.my_tool.importer.pattern
            f = fileseq.findSequenceOnDisk(p + "/" + pattern)
        except:
            show_message_box(
                "can't find this sequence with pattern \"" + pattern+"\"", icon="ERROR")
    else:
        f = fileseq.findSequenceOnDisk(file_seq_items_name)
    if f:
        try:
            context.scene.my_tool.importer.type = check_type(f[0])
        except Exception as e:
            show_message_box("meshio error when reading: " +
                             f[0]+",\n please check console for more details. And please don't load sequence.", icon="ERROR")
            traceback.print_exc()
            return


def update_particle_radius(self, context):
    '''
    This function here updates the radius of selected particle sequence.
    '''
    idx = context.scene.my_tool.imported_num
    r = context.scene.my_tool.imported[idx].radius
    importer = importer_list[idx]
    importer.set_radius(r)


def update_max_value(self, context):
    '''
    When max (or min) value adjusted by user, this function will update it in the importer 
    '''
    idx = context.scene.my_tool.imported_num
    max = context.scene.my_tool.imported[idx].max_value
    min = context.scene.my_tool.imported[idx].min_value
    importer = importer_list[idx]
    if max >= min:
        importer.set_max_value(max)
    else:
        show_message_box(
            "max value shoule be larger than min value", icon="ERROR")


def update_min_value(self, context):
    '''
    When max (or min) value adjusted by user, this function will update it in the importer 
    '''
    idx = context.scene.my_tool.imported_num
    max = context.scene.my_tool.imported[idx].max_value
    min = context.scene.my_tool.imported[idx].min_value
    importer = importer_list[idx]
    if min <= max:
        importer.set_min_value(min)
    else:
        show_message_box(
            "min value shoule be smaller than max value", icon="ERROR")


def update_display(self, context):
    '''
    When particles display method adjusted by user, this function will update it in the importer 
    '''
    idx = context.scene.my_tool.imported_num
    method = context.scene.my_tool.imported[idx].display
    importer = importer_list[idx]
    importer.update_display(method)


def update_start(self,context):
    idx = context.scene.my_tool.imported_num
    start = context.scene.my_tool.imported[idx].start
    end = context.scene.my_tool.imported[idx].end
    if start< end:
        importer = importer_list[idx]
        importer.start = start
    else:
        show_message_box(
            "start frame should be smaller than end frame", icon="ERROR")

def update_end(self,context):
    idx = context.scene.my_tool.imported_num
    start = context.scene.my_tool.imported[idx].start
    end = context.scene.my_tool.imported[idx].end
    if start< end:
        importer = importer_list[idx]
        importer.end = end
    else:
        show_message_box(
            "start frame should be smaller than end frame", icon="ERROR")


def update_imported_num(self,context):
    if importer_list:
        idx = context.scene.my_tool.imported_num
        bpy.ops.object.select_all(action='DESELECT')
        importer = importer_list[idx]
        importer.get_obj().select_set(True)
        bpy.context.view_layer.objects.active = importer.get_obj()


def selected_callback():
    if importer_list:
        for ind,im in enumerate(importer_list):
            if im.get_obj() == bpy.context.view_layer.objects.active:
                bpy.context.scene.my_tool.imported_num = ind
