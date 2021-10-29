import os

# Substance 3D Painter modules
import substance_painter.ui
import substance_painter.export
import substance_painter.project
import substance_painter.textureset

# PySide module to build custom UI
from PySide2 import QtWidgets


plugin_widgets = []

class ExportMapConfig:
	def __init__(self, baseColor = True, roughmetalao = True, normal = True, emission = True):
		self.baseColor = baseColor
		self.roughmetalao = roughmetalao
		self.normal = normal
		self.emission = emission

def export_textures(suffix = "") :
	# Verify if a project is open before trying to export something
	if not substance_painter.project.is_open() :
		return

	# Base export path
	path = substance_painter.project.file_path()
	path = os.path.dirname(path) + "/Export/"

	# List all the Texture Sets:
	for texture_set in substance_painter.textureset.all_texture_sets():
		for stack in texture_set.all_stacks():
			# Get stack name
			stack_name = str(stack)
            
			# Get stack resolution (in powers of 2)
			material = stack.material()
			resolution = material.get_resolution()
			sizeLog2 = int(math.log2(resolution.width))
                        
			# Export
			exportList = [{ "rootPath" : stack_name }] 

			# You can also use a suffix to only export variations on a basecolor map           
			full_export = len(suffix) == 0
			export_map_config = ExportMapConfig(True, full_export, full_export, full_export)
			export(exportList, path, "", suffix, sizeLog2, "$mesh", export_map_config)

def export(exportList, basePath, subFolder = "", suffix = "", sizeLog2 = 12, meshName = "$mesh", export_map_config: ExportMapConfig = ExportMapConfig()):

	config = {
		"exportShaderParams" 	: False,
		"exportPath" 			: basePath,
		"exportList"			: exportList,
		"exportPresets" 		: [getExportPreset("defaultPreset", subFolder, suffix, meshName, export_map_config)],
		"defaultExportPreset" 	: "defaultPreset",
		"exportParameters" 		: [
			{
				"parameters"	: { "paddingAlgorithm": "infinite", "sizeLog2" :  sizeLog2, "fileFormat" : "png" },
			}
		]
	}

	substance_painter.export.export_project_textures( config )

	return

def getExportPreset(name, subFolder, suffix, meshName, export_map_config: ExportMapConfig):
	maps = []
 
	if len(suffix) > 0:
		suffix = "_" + suffix

    # Blender (OpenGL)
	if export_map_config.baseColor:
		maps.append({ 
			"fileName": f"Blender/{subFolder}{meshName}{suffix}_$textureSet_BaseColor(.$udim)", 					
			"parameters": { "bitDepth": "8", "dithering": False },
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "A", "srcChannel": "L", "srcMapType": "documentMap", "srcMapName": "opacity" }
			]
		})
  
	if export_map_config.roughmetalao:
		maps.append({ 
			"fileName": f"Blender/{subFolder}{meshName}{suffix}_$textureSet_Roughness(.$udim)", 
			"parameters": { "bitDepth": "8", "dithering": False },
			"channels": [
				{ "destChannel": "G", "srcChannel": "L", "srcMapType": "documentMap", "srcMapName": "roughness" }
			] 
		}) 
		maps.append({ 
			"fileName": f"Blender/{subFolder}{meshName}{suffix}_$textureSet_Metallic(.$udim)", 
			"parameters": { "bitDepth": "8", "dithering": False },
			"channels": [
				{ "destChannel": "G", "srcChannel": "L", "srcMapType": "documentMap", "srcMapName": "metallic" }
			] 
		})
 
	if export_map_config.normal:
		maps.append({ 
			"fileName": f"Blender/{subFolder}{meshName}{suffix}_$textureSet_Normal(.$udim)", 
			"parameters": { "bitDepth": "16", "dithering": False},
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "virtualMap", "srcMapName": "Normal_OpenGL" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "virtualMap", "srcMapName": "Normal_OpenGL" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "virtualMap", "srcMapName": "Normal_OpenGL" }
			]	 
		})
 
	if export_map_config.emission:
		maps.append({ 
			"fileName": f"Blender/{subFolder}{meshName}{suffix}_$textureSet_Emissive(.$udim)", 					
			"parameters": { "bitDepth": "8", "dithering": False },
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "emissive" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "emissive" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "emissive" }
			]
		})

	# Sketchfab (DirectX)
	if export_map_config.baseColor:
		maps.append({ 
			"fileName": f"Sketchfab/{subFolder}{meshName}{suffix}_$textureSet_BaseColor(.$udim)", 					
			"parameters": { "bitDepth": "8", "dithering": False, "fileFormat" : "png" },
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "A", "srcChannel": "L", "srcMapType": "documentMap", "srcMapName": "opacity" }
			]    
		})
  
	if export_map_config.roughmetalao:
		maps.append({ 
			"fileName": f"Sketchfab/{subFolder}{meshName}{suffix}_$textureSet_Roughness(.$udim)", 
			"parameters": { "bitDepth": "8", "dithering": False, "fileFormat" : "jpg" },
			"channels": [
				{ "destChannel": "G", "srcChannel": "L", "srcMapType": "documentMap", "srcMapName": "roughness" }
			]      
		})
		maps.append({ 
			"fileName": f"Sketchfab/{subFolder}{meshName}{suffix}_$textureSet_Metallic(.$udim)", 
			"parameters": { "bitDepth": "8", "dithering": False , "fileFormat" : "jpg"},
			"channels": [
				{ "destChannel": "G", "srcChannel": "L", "srcMapType": "documentMap", "srcMapName": "metallic" }
			]      
		})
		maps.append({ 
			"fileName": f"Sketchfab/{subFolder}{meshName}{suffix}_$textureSet_AO(.$udim)", 
			"parameters": { "bitDepth": "8", "dithering": False , "fileFormat" : "jpg"},
			"channels": [
				{ "destChannel": "G", "srcChannel": "L", "srcMapType": "virtualMap", "srcMapName": "AO_Mixed" }
			]      
		})
 
 
	if export_map_config.normal:
		maps.append({ 
			"fileName": f"Sketchfab/{subFolder}{meshName}{suffix}_$textureSet_Normal(.$udim)", 
			"parameters": { "bitDepth": "16", "dithering": False},
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "virtualMap", "srcMapName": "Normal_DirectX" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "virtualMap", "srcMapName": "Normal_DirectX" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "virtualMap", "srcMapName": "Normal_DirectX" }
			]
		})
 
	if export_map_config.emission:
		maps.append({ 
			"fileName": f"Sketchfab/{subFolder}{meshName}{suffix}_$textureSet_Emissive(.$udim)", 					
			"parameters": { "bitDepth": "8", "dithering": False, "fileFormat" : "jpg" },
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "emissive" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "emissive" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "emissive" }
			]
		})
 
	# Unity
	if export_map_config.baseColor:
		maps.append({ 
			"fileName": f"Unity/{subFolder}{meshName}{suffix}_$textureSet_BaseMap(.$udim)", 					
			"parameters": { "bitDepth": "8", "dithering": False },
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "A", "srcChannel": "L", "srcMapType": "documentMap", "srcMapName": "opacity" }
			]           
		})
  	
	if export_map_config.roughmetalao:
		maps.append({ 
			"fileName": f"Unity/{subFolder}{meshName}{suffix}_$textureSet_MaskMap(.$udim)", 					
			"parameters": { "bitDepth": "8", "dithering": False},
			"channels": [
				{ "destChannel": "R", "srcChannel": "L", "srcMapType": "documentMap", "srcMapName": "metallic" },
				{ "destChannel": "G", "srcChannel": "L", "srcMapType": "virtualMap", "srcMapName": "AO_Mixed" },
				{ "destChannel": "A", "srcChannel": "L", "srcMapType": "virtualMap", "srcMapName": "glossiness" }
			]     
		})
  
	if export_map_config.emission:
		maps.append({ 
			"fileName": f"Unity/{subFolder}{meshName}{suffix}_$textureSet_Emissive(.$udim)", 					
			"parameters": { "bitDepth": "8", "dithering": False },
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "emissive" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "emissive" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "emissive" }
			] 
		})
    
	if export_map_config.normal:
		maps.append({ 
			"fileName": f"Unity/{subFolder}{meshName}{suffix}_$textureSet_Normal(.$udim)", 
			"parameters": { "bitDepth": "8", "dithering": True},
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "virtualMap", "srcMapName": "Normal_OpenGL" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "virtualMap", "srcMapName": "Normal_OpenGL" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "virtualMap", "srcMapName": "Normal_OpenGL" }
			]    
		})

	# Unreal
	if export_map_config.baseColor:
		maps.append({ 
			"fileName": f"Unreal/{subFolder}{meshName}{suffix}_$textureSet_BaseMap(.$udim)", 					
			"parameters": { "bitDepth": "8", "dithering": False },
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "baseColor" },
				{ "destChannel": "A", "srcChannel": "L", "srcMapType": "documentMap", "srcMapName": "opacity" }
			]          
		})

	if export_map_config.roughmetalao:
		maps.append({ 
			"fileName": f"Unreal/{subFolder}{meshName}{suffix}_$textureSet_OcclusionRoughnessMetallic(.$udim)", 					
			"parameters": { "bitDepth": "8", "dithering": False},
			"channels": [
				{ "destChannel": "R", "srcChannel": "L", "srcMapType": "virtualMap", "srcMapName": "AO_Mixed" },
				{ "destChannel": "G", "srcChannel": "L", "srcMapType": "documentMap", "srcMapName": "roughness" },
				{ "destChannel": "B", "srcChannel": "L", "srcMapType": "documentMap", "srcMapName": "metallic" }
			]        
		})

	if export_map_config.emission:
		maps.append({ 
			"fileName": f"Unreal/{subFolder}{meshName}{suffix}_$textureSet_Emissive(.$udim)", 					
			"parameters": { "bitDepth": "8", "dithering": False },
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "emissive" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "emissive" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "emissive" }
			]     
		})

	if export_map_config.normal:
		maps.append({ 
			"fileName": f"Unreal/{subFolder}{meshName}{suffix}_$textureSet_Normal(.$udim)", 
			"parameters": { "bitDepth": "8", "dithering": True},
			"channels": [
				{ "destChannel": "R", "srcChannel": "R", "srcMapType": "virtualMap", "srcMapName": "Normal_DirectX" },
				{ "destChannel": "G", "srcChannel": "G", "srcMapType": "virtualMap", "srcMapName": "Normal_DirectX" },
				{ "destChannel": "B", "srcChannel": "B", "srcMapType": "virtualMap", "srcMapName": "Normal_DirectX" }
			]       
		})

	return { "name" : name, "maps" : maps }

def start_plugin():
	# Create a text widget for a menu
	Action = QtWidgets.QAction("Multi-Export", 
								triggered=export_textures)

	# Add this widget to the existing File menu of the application
	substance_painter.ui.add_action(
		substance_painter.ui.ApplicationMenu.File,
		Action )

	# Store the widget for proper cleanup later when stopping the plugin
	plugin_widgets.append(Action)


def close_plugin():
	# Remove all widgets that have been added to the UI
	for widget in plugin_widgets:
		substance_painter.ui.delete_ui_element(widget)

	plugin_widgets.clear()


if __name__ == "__main__":
	start_plugin()