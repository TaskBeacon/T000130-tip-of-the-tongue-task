"""Actual main.run human setup to first instruction; synthetic form data, no QA context."""
import sys,json
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import main as task
root=Path(__file__).resolve().parents[1];windows=[]
class StopAfterInstruction(Exception):pass
original_init=task.initialize_exp;original_wait=task.StimUnit.wait_and_continue
original_collect=task.SubInfo.collect
def init(settings):
 result=original_init(settings);windows.append(result[0]);return result
def instruction(unit,*args,**kwargs):
 if unit.label=='instruction':
  # Call the real human instruction draw via public show, then stop before acquisition.
  unit.show(duration=.15)
  raise StopAfterInstruction()
 return original_wait(unit,*args,**kwargs)
task.initialize_exp=init;task.SubInfo.collect=lambda self:{'subject_id':130};task.StimUnit.wait_and_continue=instruction
passed=False
try:
 task.run(SimpleNamespace(mode='human',config_path=root/'config/config.yaml'))
except StopAfterInstruction:passed=True
finally:
 task.initialize_exp=original_init;task.SubInfo.collect=original_collect;task.StimUnit.wait_and_continue=original_wait
 for win in windows:win.close()
(root/'validation/human-startup.json').write_text(json.dumps({'passed':passed,'mode':'human','window_created':bool(windows),'limitation':'Actual human main setup and instruction; synthetic numeric form input; stops before trials. Not a full human acquisition or materials pilot.'},indent=2),encoding='utf8')
assert passed
print('PASS human main setup and first instruction without QA runtime')
