import torch
from oka_sec_monitor import OkaSecProtocol
from mujoco_shadow_env import SovereignMuJoCoEnv
import gymnasium as gym

# Setup
raw_env = gym.make("Ant-v4")
env = SovereignMuJoCoEnv(raw_env)
model = torch.nn.Sequential(torch.nn.Linear(27, 64), torch.nn.ReLU(), torch.nn.Linear(64, 8))
protocol = OkaSecProtocol(model)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

def train_step(state):
    # Forward
    action_probs = model(torch.tensor(state).float())
    # ... (RL Logic: Sampling action, getting reward)
    
    # Audit Gradients before Optimizer step
    grads = {name: param.grad for name, param in model.named_parameters()}
    is_safe, msg = protocol.audit_intent(grads)
    
    if is_safe:
        optimizer.step()
        protocol.shadow_sync()
        print(f"[*] {msg}")
    else:
        optimizer.zero_grad()
        print(f"[!] {msg} - DEFENSE_MODE_ACTIVATED")

print("OKA-SEC Protocol: RL Research Framework Online.")
