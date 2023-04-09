# A ready-to-run script for Blender Cycles Render v2.78

## A water bubble in air simulation rendered in Blender
<img src="pic04.jpg?raw=true&v=100" alt="your_alternative_text" width="100%" height="100%" loop="true" autoplay="true">

This repo demonstrates the Python scripting in Blender Cycles Render for 
blender v2.78. It shows how to create multiple materials and shade them 
differently, and render them using a Python script that can be run from 
the command line in the background. This is a ready to run code. It has 
5 .stl mesh files corresponding to a convecting water bubble. The script loops 
through these files  and creates and saves the render images. To run this code, 
do the following in the command line in this directory.

<path_to_blender_exec> --background --python BlenderCyclesTest.py

<path_to_blender_exec> will look like for eg. ./blender.app/Contents/MacOS/blender

This will create 5 images in this directory.

## How it works

The basic idea is to create a scene using the blender GUI - load a single .stl
file in the blender GUI, and set the background, camera angle and lighting for the 
scene. Make sure that the render looks the way you want. Then delete the object 
(here it is the water drop), and save the scene as a .blend file (Here it is
DropScene.blend). The Python script will load the .blend file, and the object 
(the moving water drop) will be loaded inside the for loop in the python script.


