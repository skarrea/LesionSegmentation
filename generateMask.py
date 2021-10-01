import SimpleITK as sitk
import numpy as np
from itertools import product

def generateSphericalMask(image : sitk.Image, VOIOriginCoordinates : list, diameter : float=10, label : int=1) -> sitk.Image:
	"""Generate a spherical mask in the image at the specified coordinates and of the specified radius.

	Parameters
	----------
	image : sitk.Image
		image to create the mask in
	VOIOriginCoordinates : list
		coordinates of centre of VOI
	diameter : float, optional
		Radius of sphere in mm, by default 10.
	label : int, optional
		positive label in mask
	Returns
	-------
	sitk.Image
		VOI mask. Will be an image of the same dimensions as the input image.
	"""
	spacing = image.GetSpacing()
	originIndex = image.TransformPhysicalPointToIndex(VOIOriginCoordinates)
	size = image.GetSize()

	# Making an index grid of one quadrant so we don't have to work with 
	# negative indices yet.
	# The spherical VOI can be inscribed in a cube with lenghts equal to 
	# the diameter of the sphere.
	x = np.arange(0, diameter/2, spacing[0])
	y = np.arange(0, diameter/2, spacing[1])
	z = np.arange(0, diameter/2, spacing[2])
	xx, yy, zz = np.meshgrid(x, y, z)

	# Get a matrix containing the distance from each index (x,y,z) to the origin
	rMatr = np.sqrt(xx**2 + yy**2 + zz**2)
	# Extracting the coords
	coordsQuadrant = [(x,y,z) for x, y, z, r in zip(xx.reshape(-1), yy.reshape(-1), zz.reshape(-1), rMatr.reshape(-1)) if r<=diameter/2]

	quadrantSigns = product([1, -1], repeat=3)
	coords = []

	for signs in quadrantSigns:
		coords += list(np.multiply(np.array(coordsQuadrant), np.array(signs)).astype(float))

	# Remove duplicates
	coords = np.unique(coords, axis=0)

	coordsInImageSpace = np.array(coords)+np.array(VOIOriginCoordinates)

	maskImage = sitk.Image(size[0], size[1], size[2], sitk.sitkInt8)
	maskImage.CopyInformation(image)
	indices = np.apply_along_axis(image.TransformPhysicalPointToIndex, 1, coordsInImageSpace)
	keepIndices = np.all(indices > 1, axis = 1)
	indices = indices[keepIndices]
	for index in indices:
		if index[0] < size[0] and index[1] < size[1] and index[2] < size[2]:
			maskImage[[int(elem) for elem in index]] = label

	return maskImage