import os
import numpy as np
import efficientnet.keras as efn

from skimage.io import imread
from efficientnet.keras import center_crop_and_resize, preprocess_input
from keras.applications.imagenet_utils import decode_predictions

model = efn.EfficientNetB7(weights=weights)

image_size = model.input_shape[1]

def read_image(path):
    try:
        return preprocess_input(
            center_crop_and_resize(imread(path)[:, :, :3], image_size=image_size)
        )
    except:
        return None

from time import time

def predictor(in_paths=[], batch_size=2):
    #with multiprocessing.Pool(batch_size) as pool:
    #    in_images = pool.map(read_image, in_paths)
    #    pool.close()

    in_images = [read_image(in_path) for in_path in in_paths]
    
    bad_indices = {i for i, in_image in enumerate(in_images) if in_image is None}
    in_images = [in_image for in_image in in_images if in_image is not None]

    preds = []

    start = time()

    while len(in_images):
        batch = np.asarray(in_images[:batch_size])
        in_images = in_images[batch_size:]
        try:
            batch_preds = model.predict(batch, batch_size=batch_size)
            batch_preds = decode_predictions(batch_preds)
            batch_preds = [
                [{"pred": i[1], "prob": float(i[2])} for i in pred]
                for pred in batch_preds
            ]
        except Exception as ex:
            batch_preds = [str(ex) for _ in batch]

        while batch_preds:
            if len(preds) in bad_indices:
                preds.append("Failed to read image")
            else:
                preds.append(batch_preds[0])
                batch_preds = batch_preds[1:]

    end = time()

    return end - start


if __name__ == "__main__":
    import json
    import pickle
    import base64

    example = ["example.jpg"]

    in_images = example * 512    

    for batch_size in [1, 2, 4, 8]:
            json.dump({
            file_name: 
            for file_name in example

        json.dump({'data': {f'{i}.jpg': base64.b64encode(open("example.jpg", "rb").read()).decode("utf-8") for i in range(batch_size)}})

        print(f'batch_size: {batch_size}, total_time: {predictor(in_images, batch_size)} for 512 examples.')
