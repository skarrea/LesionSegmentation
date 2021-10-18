# LesionSegmentation
This is a simple repository that contains code to segment PET lesions based
on their coordinates in the image coordinate system. Specifically the LPS
coordinates used by dicom images.

## Example usage
Assuming we have an image `TestImage.mha` that has a lesion located at
`(10, 20, 10)` we can generate a boolean image with a 10 mm spherical mask
around the specified lesion coordinates as follow. 

```python
import SimpleITK as sitk
from generateMask import generateSphericalMask

image = sitk.ReadImage('TestImage.mha')
lesionMask = generateSphericalMask(image, [10, 20, 10])
sitk.WriteImage(lesionMask, 'LesionMask.nii.gz')
```

The results can be verified by opening the image and the segmentation in a
medical image viewer like
[itk-SNAP](http://www.itksnap.org/pmwiki/pmwiki.php). 