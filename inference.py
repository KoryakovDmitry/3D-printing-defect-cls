import os
import torch
import torch.nn as nn
import cv2
import numpy as np
from torchvision import datasets, models, transforms
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


class Predictor:
    def __init__(self, w_path, resize=(600, 600)):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        num_features = 9216
        self.model = models.alexnet(pretrained=False)

        self.model.classifier = nn.Sequential(
            nn.Dropout(p=0.5, inplace=False),
            nn.Linear(num_features, 2, bias=True),
            nn.Softmax(),
        )

        self.model = self.model.to(self.device)
        self.model.load_state_dict(torch.load(w_path, map_location=self.device))
        self.model.eval()
        self.to_tensor = transforms.ToTensor()
        self.to_norm = transforms.Normalize(
            [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
        )
        self.classes = ["NoDefects", "YesDefects"]

    def inference(self, img: np.array, resize_to=(600, 600)):
        img = cv2.resize(img, resize_to)

        tensor = self.to_tensor(img)
        tensor = self.to_norm(tensor)
        tensor = tensor.unsqueeze(0)
        tensor = tensor.to(self.device)
        probs = self.model(tensor)
        probs = probs.cpu().detach()
        _, prediction = torch.max(probs, 1)
        prediction = prediction.numpy()
        probs = probs.numpy()
        return prediction[0], probs[0]

    def plot_res(self, img: np.array, pred, probs, save_to, resize_to_scale=2):
        plt.figure(figsize=(26, 14))
        img = cv2.resize(
            img, (img.shape[1] // resize_to_scale, img.shape[0] // resize_to_scale)
        )
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        p = np.round(probs[pred], decimals=2)
        pred_prob = f"{self.classes[pred]} with prob: {str(p)}"
        pred_patch = mpatches.Patch(
            color="green" if pred == 0 else "red", label=pred_prob
        )
        p = np.round(probs[1 - pred], decimals=2)
        pred_prob_another = f"{self.classes[1 - pred]} with prob: {str(p)}"
        pred_patch_another = mpatches.Patch(
            color="green" if pred == 1 else "red", label=pred_prob_another
        )
        plt.legend(handles=[pred_patch, pred_patch_another], prop={"size": 30})
        plt.axis("off")
        # plt.show()
        plt.savefig(save_to)


if __name__ == "__name":
    import os
    import os.path as osp

    pred = Predictor(osp.join(os.getcwd(), "weights/w_model_stand_fine_tuning_15.pth"))


