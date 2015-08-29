#this is a gimp plug in that takes a file of text, and generates an image from each line
#the image is similar to the original, aside from having the line of text different for one layer

import os
from gimpfu import *

def create_door_signs(img, layer, inputFile, outputFolder):
	names = []
	try: 
		namesFile = open(inputFile, "r")
		for line in namesFile:
			names.append(line.rstrip('\n'))
	except Exception as err:
		print err

	for name in names:
		try:
			#full file paths
			outputPath = outputFolder + "/" + name + ".jpg"
		
			#duplicate image
			image = pdb.gimp_image_duplicate(img)

			#set visibility of first 4 layers to true, last 2 as false
			layers = image.layers
			pdb.gimp_item_set_visible(layers[0], TRUE)
			pdb.gimp_item_set_visible(layers[1], TRUE)
			pdb.gimp_item_set_visible(layers[2], TRUE)
			pdb.gimp_item_set_visible(layers[3], TRUE)
			pdb.gimp_item_set_visible(layers[4], FALSE)
			pdb.gimp_item_set_visible(layers[5], FALSE)
			
			#set name as text 
			pdb.gimp_text_layer_set_text(layers[0], name)
			
			#merge visible layers
			text = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)			
			
			#invert mask
			layers = image.layers
		
			#make other layers visible
			pdb.gimp_item_set_visible(layers[0], FALSE)
			pdb.gimp_item_set_visible(layers[1], TRUE)
			pdb.gimp_item_set_visible(layers[2], TRUE)
			
			#select alpha
			pdb.gimp_selection_layer_alpha(layers[0])	
			pdb.gimp_selection_invert(image)
			pdb.gimp_layer_add_mask(layers[1], pdb.gimp_layer_create_mask(layers[1], ADD_SELECTION_MASK))

			#save file
			final = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)			
			pdb.file_jpeg_save(image, final, outputPath, outputPath, 0.9, 0, 0, 0, "Creating with GIMP", 0, 0, 0, 0)
		except Exception as err:
			gimp.message("Unexpected error: " + str(err))

register(
	"python_fu_test_create_doorsigns",
	"Create Door Signs",
	"Creates sMITe door signs for a list of people",
	"Julia Huang",
	"Open Source",	
	"2015",
	"<Image>/Scripts/Create Door Signs",
	"*",
	[
		(PF_FILENAME, "inputFile", "Input file", "/home/julia/Pictures/smite-doors/new-smite-names.txt"),
		(PF_DIRNAME, "outputFolder", "Output directory", "/home/julia/Pictures/smite-doors/signs"),
	],
	[],
	create_door_signs)

main()
