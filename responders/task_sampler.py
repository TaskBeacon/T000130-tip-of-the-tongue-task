from dataclasses import dataclass
from psyflow.sim.contracts import Action

@dataclass
class TaskSamplerResponder:
    rt_s: float=.15
    def start_session(self,session,rng): self.rng=rng
    def act(self,obs):
        keys=list(obs.valid_keys or [])
        return Action(key=keys[0],rt_s=self.rt_s*(.8+.4*self.rng.random())) if keys else Action(key=None,rt_s=None)
    def on_feedback(self,feedback): pass
    def end_session(self): pass
