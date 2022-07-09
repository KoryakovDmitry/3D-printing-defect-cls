import os
import shutil
import cv2
import os.path as osp
from glob import glob
from tqdm import tqdm

from inference import Predictor


def test():
    base_dir = os.getcwd()
    path2folder_with_w = osp.join(base_dir, "weights")
    data_dir = osp.join(base_dir, "data")
    results_dir = osp.join(base_dir, "results")

    # Real shots of the 3D printing process with and without defects
    predictor_stand_fn = Predictor(
        w_path=osp.join(path2folder_with_w, "w_model_stand_fine_tuning_15.pth")
    )

    # Real shots of 3D printed products with and without defects to test a model
    predictor_synth = Predictor(
        w_path=osp.join(path2folder_with_w, "w_model_synth_fine_tuning.pth")
    )

    imgs_to_test_stand = glob(osp.join(
        data_dir, "defects_not_augmented_dataset/valid/*/*.jpg"
    ))
    imgs_to_test_synth = glob(osp.join(data_dir, "DS_test_bin_flipped_replaced/*/*.jpg"))

    results_dir_stand = osp.join(results_dir, "defects_not_augmented_dataset_valid_res")
    os.makedirs(results_dir_stand, exist_ok=True)
    shutil.rmtree(results_dir_stand)
    os.makedirs(results_dir_stand, exist_ok=True)

    results_dir_synth = osp.join(results_dir, "DS_test_bin_flipped_replaced_res")
    os.makedirs(results_dir_synth, exist_ok=True)
    shutil.rmtree(results_dir_synth)
    os.makedirs(results_dir_synth, exist_ok=True)

    print(
        "inference stand, Real shots of the 3D printing process with and without defects"
    )
    for img_path in tqdm(imgs_to_test_stand):
        dir2save = osp.join(results_dir_stand, osp.basename(osp.dirname(img_path)))
        os.makedirs(dir2save, exist_ok=True)

        pred, probs = predictor_stand_fn.inference(
            cv2.imread(img_path), resize_to=(600, 600)
        )
        predictor_stand_fn.plot_res(
            cv2.imread(img_path),
            pred=pred,
            probs=probs,
            save_to=osp.join(dir2save, osp.basename(img_path)),
            resize_to_scale=2,
        )

    print(
        "inference synth, Real shots of 3D printed products with and without defects to test a model"
    )
    for img_path in tqdm(imgs_to_test_synth):
        dir2save = osp.join(results_dir_synth, osp.basename(osp.dirname(img_path)))
        os.makedirs(dir2save, exist_ok=True)

        pred, probs = predictor_synth.inference(
            cv2.imread(img_path), resize_to=(600, 800)
        )
        predictor_synth.plot_res(
            cv2.imread(img_path),
            pred=pred,
            probs=probs,
            save_to=osp.join(dir2save, osp.basename(img_path)),
            resize_to_scale=2,
        )


if __name__ == "__main__":
    test()
