import torch
import numpy as np

from transformers import pipeline
from diffusers.utils import load_image

from diffusers import KandinskyV22PriorPipeline, KandinskyV22ControlnetPipeline
from diffusers import DiffusionPipeline

from PIL import Image, ImageFilter
from IPython.display import display

class KandyControlnet:
    def __init__(self, seed=42):
        self.pipe_prior = KandinskyV22PriorPipeline.from_pretrained(
            "kandinsky-community/kandinsky-2-2-prior", torch_dtype=torch.float16
        ).to("cuda")

        # self.controlnet_pipe = KandinskyV22ControlnetPipeline.from_pretrained(
        #     "kandinsky-community/kandinsky-2-2-controlnet-depth", torch_dtype=torch.float16
        # ).to("cuda")

        self.pipe = DiffusionPipeline.from_pretrained("kandinsky-community/kandinsky-2-2-decoder", torch_dtype=torch.float16).to("cuda")
        self.generator = torch.Generator(device="cuda").manual_seed(seed)
    
    def make_hint(self, image):
        image = np.array(image)
        detected_map = torch.from_numpy(image).float() / 255.0
        hint = detected_map.permute(2, 0, 1)
        return hint

    def color_mask(self, array, r_lim, g_lim, b_lim):
        """
        array : m x n x 3 array of colors
        *_lim are 2-element tuples, where the first element is expected to be <= the second.
        """
        r_mask = ((array[..., 0] >= r_lim[0]) & (array[..., 0] <= r_lim[1]))
        g_mask = ((array[..., 1] >= g_lim[0]) & (array[..., 1] <= g_lim[1]))
        b_mask = ((array[..., 2] >= b_lim[0]) & (array[..., 2] <= b_lim[1]))
        return r_mask & g_mask & b_mask

    def generate_mask(self, path2image, r=(220, 255), g=(220, 255), b=(220, 255), height=768, width=1024):
        img = Image.open(path2image).convert('RGB').resize((width, height))
        mask = self.color_mask(np.array(img), r, g, b)
        mask = np.expand_dims(mask, axis=-1)
        mask = np.concatenate([mask, mask, mask], axis=-1) 
        return mask
    
    def generate_image(self, prompt, negative_prompt, mask:np.array=None, height=768, width=1024):
        # assert mask.shape[:2] == (height, width)
        # print(mask.shape)
        # We pass the prompt and negative prompt through the prior to generate image embeddings
        prompt = prompt
        negative_prior_prompt = negative_prompt


        image_emb, zero_image_emb = self.pipe_prior(
            prompt=prompt, negative_prompt=negative_prior_prompt, generator=self.generator,
        ).to_tuple()

        # Now we can pass the image embeddings and the depth image we extracted to the controlnet pipeline. With Kandinsky 2.2, only prior pipelines accept `prompt` input. You do not need to pass the prompt to the controlnet pipeline.
        kwargs = dict(
            image_embeds=image_emb,
            negative_image_embeds=zero_image_emb,
            num_inference_steps=50,
            generator=self.generator,
            num_images_per_prompt=1,
            height=768,
            width=1024,
        )
        
        if mask is not None: 
            hint = self.make_hint(mask.astype(np.float32)).unsqueeze(0).half().to("cuda")
            kwargs.update(dict(hint=hint))
            image = self.controlnet_pipe(**kwargs).images[0]
        else:
            image = self.pipe(**kwargs).images[0]
        
        return image
    
    def generate_background(self, path2image, prompt, negative_prompt="", image_size=(1600, 900)):
        mask = self.generate_mask(path2image)
        image = self.generate_image(prompt, negative_prompt, mask=mask)
        return image.resize((image_size))
                          
    def generate_foreground(self, path2image, prompt, negative_prompt="", image_size=(1600, 900)):
        mask = self.generate_mask(path2image)
        mask = np.logical_not(mask)
        image = self.generate_image(prompt, negative_prompt, mask=mask)
        return image.resize((image_size))
    
    def imagine(self, prompt, path2image=None, negative_prompt="", image_size=(1600, 900)):
        
        if path2image:
            image = np.array(Image.open(path2image).convert('RGB').resize(image_size)).astype(np.uint8)
            mask = Image.fromarray(self.generate_mask(path2image).astype(np.uint8)).resize(image_size)
            background_mask = mask 
            foreground_mask = np.logical_not(mask)
            gen_1 = self.generate_background(path2image, prompt, negative_prompt, image_size)
            gen_1, mask = [np.array(x) for x in [gen_1, mask]]
            output = gen_1 * background_mask + image * foreground_mask 
        else:
            output = self.generate_image(prompt, negative_prompt)

        return output
    