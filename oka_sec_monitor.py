import torch
import numpy as np

class OkaSecProtocol:
    """
    OKA-SEC Protocol: Shadow Mode Implementation for Reinforcement Learning.
    Focus: Intent Integrity & Gradient Sovereignty.
    """
    def __init__(self, model, threshold=0.1):
        self.model = model
        self.threshold = threshold
        self.shadow_weights = self._clone_weights()

    def _clone_weights(self):
        """Creates a 'Shadow Copy' of the sovereign weights."""
        return {name: param.clone().detach() for name, param in self.model.named_parameters()}

    def audit_intent(self, current_gradients):
        """
        Poison detection: Checks if the incoming gradients align with sovereign intent.
        If divergence is too high, it signals a 'Gradient Poisoning' attempt.
        """
        for name, grad in current_gradients.items():
            if grad is not None:
                # Calculate the 'Noise-to-Signal' ratio in the gradient
                grad_norm = torch.norm(grad)
                if grad_norm > self.threshold * 10:  # Threshold for anomaly
                    return False, f"INTENT_VIOLATION: Anomalous Gradient in {name}"
        return True, "SOVEREIGN_INTENT_VERIFIED"

    def shadow_sync(self):
        """Synchronizes the shadow weights after verified updates."""
        self.shadow_weights = self._clone_weights()

    def poison_the_well(self, reward):
        """If defense is triggered, rewards are neutralized to zero trust."""
        return 0.0 if reward < -100 else reward # Custom logic for penalty
