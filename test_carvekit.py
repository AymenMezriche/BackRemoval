from carvekit.api.high import HiInterface

# # Simplified initialization
# interface = HiInterface(
#     object_type="object",  # General-purpose
#     batch_size_seg=1,
#     batch_size_matting=1,
#     seg_mask_size=640,
#     matting_mask_size=2048,
#     trimap_prob_threshold=231,
#     trimap_dilation=30,
#     trimap_erosion_iters=5
# )
#
# # Test with an image
# input_image = "app_icon.png"  # Replace with the path to your test image
# result = interface([input_image])
# result[0].save("output_image.png")  # Save the result
# print("Image processing complete! Saved as output_image.png." )
import torch
from carvekit.api.high import HiInterface

# Check doc strings for more information
interface = HiInterface(object_type="hairs-like",  # Can be "object" or "hairs-like".
                        batch_size_seg=5,
                        batch_size_matting=1,
                        device='cuda' if torch.cuda.is_available() else 'cpu',
                        seg_mask_size=320,  # Use 640 for Tracer B7 and 320 for U2Net
                        matting_mask_size=2048,
                        trimap_prob_threshold=231,
                        trimap_dilation=30,
                        trimap_erosion_iters=5,
                        fp16=False)
images_without_background = interface(['app_icon.jpg'])
cat_wo_bg = images_without_background[0]
cat_wo_bg.save('2.png')
print("Image processing complete! Saved as 2.png.")

