# Copyright (c) OpenMMLab. All rights reserved.
import pytest
import torch

from mmpose.models.backbones.vit import VisionTransformer


def test_vit_backbone():

    with pytest.raises(TypeError):
        # img_size must be int or tuple
        model = VisionTransformer(img_size=512.0)

    with pytest.raises(TypeError):
        # out_indices must be int ,list or tuple
        model = VisionTransformer(out_indices=1.)

    with pytest.raises(AssertionError):
        # The length of img_size tuple must be lower than 3.
        VisionTransformer(img_size=(224, 224, 224))

    with pytest.raises(TypeError):
        # Pretrained must be None or Str.
        VisionTransformer().init_weights(pretrained=123)

    # Test the initialization
    model = VisionTransformer()
    model.init_weights()
    model.train()

    # Test img_size isinstance tuple
    imgs = torch.randn(1, 3, 224, 224)
    model = VisionTransformer(img_size=(224, ))
    model.init_weights()
    model(imgs)

    # Test img_size isinstance tuple
    imgs = torch.randn(1, 3, 224, 224)
    model = VisionTransformer(img_size=(224, 224))
    model(imgs)

    # Test various input resolutions
    imgs = torch.randn(1, 3, 256, 256)
    model = VisionTransformer(img_size=(224, 224))
    model(imgs)

    # Test out_indices = list
    model = VisionTransformer(out_indices=[2, 4, 8, 12])
    model.train()

    # Test image size = (224, 224)
    imgs = torch.randn(1, 3, 224, 224)
    feat = model(imgs)
    assert feat[-1].shape == (1, 768, 14, 14)

    # Test ViT backbone with input size of 256 and patch size of 16
    model = VisionTransformer(img_size=(256, 256))
    model.init_weights()
    model.train()
    imgs = torch.randn(1, 3, 256, 256)
    feat = model(imgs)
    assert feat.shape == (1, 768, 16, 16)

    # Test ViT backbone with input size of 32 and patch size of 16
    model = VisionTransformer(img_size=(32, 32))
    model.init_weights()
    model.train()
    imgs = torch.randn(1, 3, 32, 32)
    feat = model(imgs)
    assert feat.shape == (1, 768, 2, 2)

    # Test unbalanced size input image
    model = VisionTransformer(img_size=(112, 224))
    model.init_weights()
    model.train()
    imgs = torch.randn(1, 3, 112, 224)
    feat = model(imgs)
    assert feat.shape == (1, 768, 7, 14)

    # Test final norm
    model = VisionTransformer(final_norm=True)
    imgs = torch.randn(1, 3, 224, 224)
    feat = model(imgs)
    assert feat.shape == (1, 768, 14, 14)