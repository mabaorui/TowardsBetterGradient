# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 19:22:12 2023

@author: Admin
"""

# pytorch version
sdf_nn_output = sdf_network(pts)
sdf = sdf_nn_output[:, :1]
gradients = sdf_network.gradient(pts).squeeze()
gradient_norm = F.normalize(gradients, dim=-1)
pts_moved = pts + gradient_norm * sdf

sdf_moved = sdf_network(pts_moved)[:, :1]
gradient_moved = sdf_network.gradient(pts_moved).squeeze()
gradient_moved_norm = F.normalize(gradient_moved, dim=-1)
consis_constraint = 1 - F.cosine_similarity(gradient_moved_norm, gradient_norm, dim=-1)
weight_moved = torch.exp(-self.conf.get_float('train.sharp') * torch.abs(sdf)).reshape(-1,consis_constraint.shape[-1]) 
consis_constraint = consis_constraint * weight_moved

# tensorflow version
gradient_norm = F.normalize(gradient, dim=-1)
coords_moved = coords + gradient_norm * pred_sdf
model_moved_input = {'coords':coords_moved}
model_output_moved = model(model_moved_input)
coords_moved = model_output_moved['model_in']
pred_sdf_moved = model_output_moved['model_out']
gradient_moved = diff_operators.gradient(pred_sdf_moved, coords_moved)
gradient_moved_norm = F.normalize(gradient_moved, dim=-1)
consis_constraint = 1 - F.cosine_similarity(gradient_moved_norm, gradient_norm, dim=-1)
weight_moved = torch.exp(-self.conf.get_float('train.sharp') * torch.abs(sdf)).reshape(-1,consis_constraint.shape[-1])
consis_constraint = consis_constraint * weight_moved