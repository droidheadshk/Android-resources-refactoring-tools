#!/usr/bin/python

import os
import re
import sys
import xml.dom.minidom

def is_valid_file(filename, extension_name):
    return filename.lower().endswith(extension_name)

# Replace pattern from search_pattern to target_text in a file
def replace_file(filepath, search_pattern, exclude_pattern, target_text):
    # run only when pattern matches
    with open(filepath) as f:
        if not any(re.search(search_pattern, line) for line in f):
            return

    with open(filepath) as f:
        # create tmp file to save our modified file
        out_filename = filepath + ".tmp"
        out = open(out_filename, "w")
        for line in f:
            m = re.search(search_pattern, line)
            # if current line matches, run it
            if m:
                # print fullname
                patched = re.search(exclude_pattern, line)
                # if file is not patched before
                if not patched:
                    print re.sub(search_pattern, target_text, line)
                    out.write(re.sub(search_pattern, target_text, line))
                else:
                    out.write(line)
            else:
                out.write(line)
                    
        out.close()
        os.rename(out_filename, filepath)

# Replace pattern from search_pattern to target_text, on all files in a directory
def patch_files(dir_name, extension_name, search_text, exclude_text, target_text):
    search_pattern = re.compile(search_text)
    exclude_pattern = re.compile(exclude_text)
    for dirpath, dirnames, filenames in os.walk(dir_name):
        for filename in filenames:
            # patch the files with correct file extension only
            if is_valid_file(filename, extension_name):
                fullname = os.path.join(dirpath, filename)
                replace_file(fullname, search_pattern, exclude_pattern, target_text)
                #print fullname

# rename all xml name attribute's value
def patch_attribute_name(dir_name, extension_name, resource_prefix):
    for dirpath, dirnames, filenames in os.walk(dir_name):
        for filename in filenames:
            if is_valid_file(filename, extension_name):
                fullname = os.path.join(dirpath, filename)
                try:
                    xml_dom = xml.dom.minidom.parse(fullname)
                    resources_nodes = xml_dom.getElementsByTagName("resources")[0]
                    for x in resources_nodes.childNodes:
                        if (x.nodeType == 1 and x.hasAttribute("name")):
                            name = x.getAttribute("name")
                            if (not name.startswith(resource_prefix)):
                                name = resource_prefix + name
                                x.setAttribute("name", name)
                            
                    f = open(fullname, "w")
                    f.write(xml_dom.toxml())
                    f.close()
                except Exception as err:
                    #print "Error: %s" % err
                    print "skip %s"%fullname

# rename resources file
def rename_res_files(dir_name, resource_prefix):
    res_dir = dir_name + "/res"
    exclude_folder = dir_name + "/res/values"
    for dirpath, dirnames, filenames in os.walk(res_dir):
        for filename in filenames:
            if (not filename.startswith(resource_prefix)):
                fullname = os.path.join(dirpath, filename)
                if (not fullname.startswith(exclude_folder)):
                    targetname = os.path.join(dirpath, resource_prefix + filename)
                    os.rename(fullname,targetname)

# rename asset files
def rename_asset_files(dir_name, resource_prefix):
    assets_dir = dir_name + "/assets"
    for dirpath, dirnames, filenames in os.walk(assets_dir):
        for filename in filenames:
            if not filename.startswith(resource_prefix):
                fullname = os.path.join(dirpath, filename)
                new_fullname = os.path.join(dirpath, resource_prefix + filename)
                os.rename(fullname, new_fullname)
                
                asset_str = fullname[len(assets_dir)+1:]
                new_asset_str = new_fullname[len(assets_dir)+1:]
                
                search_for_java_text = '\"%s\"'%asset_str
                exclude_java_text = '\"%s\"'%new_asset_str
                target_java_text = '\"%s\"'%new_asset_str

                print "xxx"
                print search_for_java_text
                print exclude_java_text
                print target_java_text
                
                # patch .java files, change R.something.some_name to R.something.RESOURCES_PREFIXsome_name
                patch_files(dir_name + "/src", ".java", search_for_java_text, exclude_java_text, target_java_text)

if __name__ == "__main__":
    argc = len(sys.argv)
    if not (argc == 3):
        print "Usage: add_prefix.py <my_prject_folder_name> <resources_prefix>"
        print ""
        print "Description: rename all your android resources by adding a prefix"
        print "Tips: put add_prefix.py to your workspace directory, and run add_prefix.py <my_prject_folder_name> <resources_prefix>"
        print ""
    else:
        # commit shared variables
        target_dir = sys.argv[1]
        resource_prefix = sys.argv[2]

        search_for_java_text = '( |=|\\()(R\\.(([a-z]|_)*)\\.)(([a-z]|_)*)'
        exclude_java_text = '( |=|\\()(R\\.(([a-z]|_)*)\\.)%s(([a-z]|_)*)'%resource_prefix
        target_java_text = r'\1\2%s\5'%resource_prefix

        # patch .java files, change R.something.some_name to R.something.RESOURCES_PREFIXsome_name
        patch_files(target_dir, ".java", search_for_java_text, exclude_java_text, target_java_text)

        # patch .xml files, change name attributes from some_name to RESOURCES_PREFIXsome_name
        patch_attribute_name(target_dir, ".xml", resource_prefix)

        # patch .xml files, change @sometype/some_name to @sometype/RESOURCES_PREFIXsome_name
        search_for_java_text = '([^a-z]@[a-z^(android:)\+][a-z]*/)(([a-z]|_)*)'
        exclude_java_text = '([^a-z]@[a-z^(android:)\+][a-z]*/)%s(([a-z]|_)*)'%resource_prefix
        target_java_text = r'\1%s\2'%resource_prefix
        patch_files(target_dir, ".xml", search_for_java_text, exclude_java_text, target_java_text)

        # patch .xml file, rename files from some_name.xml to RESOURCES_PREFIXsome_name.xml
        rename_res_files(target_dir, resource_prefix)
        
        rename_asset_files(target_dir, resource_prefix)