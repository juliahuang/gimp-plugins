import os
from gimpfu import *

def batch_apply_filter(image, layer, inputFolder, outputFolder, r, color, op, prefix):
	fb_filter = pdb.file_png_load("/home/julia/Pictures/smite-pf/final-fb-ult.png", "/home/julia/Pictures/smite-pf/final-fb-ult.png")
	orig_fb_layer = fb_filter.layers[0]
	for file in os.listdir(inputFolder):
		try:
			#full file paths
			inputPath = inputFolder + "/" + file
			newInputPath = outputFolder + " - pre filter" + "/" + file
			outputPath = outputFolder + "/" + prefix + file

			# open file
			image = pdb.file_jpeg_load(inputPath, inputPath)

			if image:
				layer = image.layers[0]
				
				#duplicate the layer
				new_layer = layer.copy(True)
				new_layer.name = "bwlayer"
				image.add_layer(new_layer,-1)
			
				#change layer to black white
				new_layer.mode = SATURATION_MODE
				#pdb.gimp_hue_saturation(new_layer, ALL_HUES, 0, 0, -100) 

				#add filter
				fb_layer = pdb.gimp_layer_new_from_drawable(orig_fb_layer, image)
				fb_layer.name = "fblayer"
				image.add_layer(fb_layer, -1)		
				
				#scale and center filter
				gimp.context_push()
				pdb.gimp_context_set_interpolation(INTERPOLATION_CUBIC)
				pdb.gimp_layer_scale(fb_layer, r*image.width, r*image.height, TRUE)
				fb_layer.set_offsets((image.width-fb_layer.width)/2, (image.height-fb_layer.height)/2)
				gimp.displays_flush()
				gimp.context_pop()
				
				#select mask
				pdb.gimp_selection_layer_alpha(fb_layer)
				#pdb.gimp_selection_invert(image)
				#pdb.gimp_layer_add_mask(new_layer, pdb.gimp_layer_create_mask(new_layer, ADD_SELECTION_MASK))				
				
				#edit final filter
				gimp.set_foreground(color)
				pdb.gimp_edit_fill(fb_layer, FG_BUCKET_FILL)
				pdb.gimp_layer_set_opacity(fb_layer, op)

				#save file
				temp = image.duplicate()
				temp.merge_visible_layers(0)
				pdb.file_jpeg_save(temp, temp.layers[0], outputPath, outputPath, 0.9, 0, 0, 0, "Creating with GIMP", 0, 0, 0, 0)

			#move file to new directory
			os.rename(inputPath, newInputPath)
		except Exception as err:
			gimp.message("Unexpected error: " + str(err))

register(
	"python_fu_test_batch_fb_filter",
	"Batch FB filter",
	"Applies fb filter to all jpeg images of folder",
	"Julia Huang",
	"Open Source",	
	"2015",
	"<Image>/Scripts/Batch FB filter",
	"*",
	[
		(PF_DIRNAME, "inputFolder", "Input directory", "/home/julia/Dropbox (MIT)/File requests/Ultimate Profile Pictures"),
		(PF_DIRNAME, "outputFolder", "Output directory", "/home/julia/Dropbox (MIT)/[2015] Ultimate pubbing"),
		(PF_FLOAT, "r", "Radius", .95),
		(PF_COLOR, "color", "Color", (255,255,255)),
		(PF_INT, "op", "Opacity", 60),
		(PF_STRING, "prefix", "Prefix", "")
	],
	[],
	batch_apply_filter)

main()
