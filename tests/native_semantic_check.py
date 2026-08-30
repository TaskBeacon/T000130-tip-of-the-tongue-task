"""Real PsychoPy/PsyFlow run_trial with synthetic responder + backend edits; not OS IME."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pyglet.window import key
from psyflow import TaskSettings,StimBank,StimUnit,initialize_exp,initialize_triggers,load_config,context_from_config,runtime_context
from psyflow.sim.contracts import Action
from src.run_trial import run_trial
from src.utils import summarize
root=Path(__file__).resolve().parents[1];out=root/'validation';out.mkdir(exist_ok=True)
cfg=load_config(str(root/'config/config_qa.yaml'))
cfg['raw']['qa']['output_dir']='outputs/native_semantic'
ctx=context_from_config(task_dir=root,config=cfg,mode='qa')
cases=[
 dict(name='know_correct',judgment='1',verification='1',text={'known_answer':'日晷错误'},edit=True),
 dict(name='know_wrong',judgment='1',verification='2',text={'known_answer':'月亮','alternative_target':'月亮'}),
 dict(name='tot_typed',judgment='2',verification='1',text={'initial_sound':'r','resolution':'日晷'},count='2'),
 dict(name='tot_recognition_only',judgment='2',verification='1',text={'initial_sound':'m','resolution':'错误'},count='3'),
 dict(name='tot_different',judgment='2',verification='2',text={'resolution':'错误'}),
 dict(name='tot_unfamiliar',judgment='2',verification='3',text={}),
 dict(name='tot_unverified',judgment='2',verification=None,text={}),
 dict(name='tot_f4_early',judgment='2',verification='1',text={'initial_sound':'r','resolution':'日晷'},f4='initial_sound'),
 dict(name='dont_know',judgment='3',verification='3',text={}),
 dict(name='judgment_missing',judgment=None,verification='3',text={}),
 dict(name='tot_f4_count',judgment='2',verification='1',text={'initial_sound':'r','resolution':'日晷'},f4='character_count'),
 dict(name='tot_f4_related_wrong',judgment='2',verification='3',text={'initial_sound':'r','resolution':'错误'},count='2',f4='related_words'),
 dict(name='tot_typed_denied',judgment='2',verification='2',text={'resolution':'日晷'}),
 dict(name='tot_unsubmitted_target',judgment='2',verification='3',resolution=None,text={'resolution':'日晷'})]
active={};before=[];entered=[];phases=[]
class Responder:
 def act(self,obs):
  p=obs.phase
  k=active.get(p, '0' if p=='character_count' else obs.valid_keys[0] if obs.valid_keys else None)
  if p=='character_count': k=active.get('count','0')
  if active.get('f4')==p:k='f4'
  return Action(key=k,rt_s=.10 if k else None)
 def start_session(self,*args):pass
 def end_session(self):pass
 def on_feedback(self,*args):pass
ctx.responder=Responder()
with runtime_context(ctx):
 settings=TaskSettings.from_dict(cfg['task_config']);settings.add_subinfo({'subject_id':130});settings.triggers=cfg['trigger_config']
 for p in ['fixation','judgment','known_answer','initial_sound','character_count','related_words','resolution','verification','alternative_target','saved']:setattr(settings,p+'_duration',.28)
 win,kb=initialize_exp(settings);bank=StimBank(win,cfg['stim_config']).preload_all();bank.get('editor').editable=False;trigger=initialize_triggers(mock=True)
 bank.get('instruction').draw();win.getMovieFrame(buffer='back');win.saveMovieFrames(str(out/'native_instruction.png'));win.flip()
 original=StimUnit.capture_response
 def capture(unit,*args,**kwargs):
  phases.append(unit.label)
  if unit.label in ['known_answer','initial_sound','related_words','resolution','alternative_target']:
   editor=bank.get('editor');before.append(editor.getText())
   def enter():
    win.winHandle.dispatch_event('on_text',active['text'].get(unit.label,''))
    if active.get('edit') and unit.label=='known_answer':
     win.winHandle.dispatch_event('on_text_motion',key.MOTION_BACKSPACE);win.winHandle.dispatch_event('on_text_motion',key.MOTION_BACKSPACE)
   win.callOnFlip(enter)
  result=original(unit,*args,**kwargs)
  if unit.label in ['known_answer','initial_sound','related_words','resolution','alternative_target']:entered.append(bank.get('editor').getText())
  return result
 StimUnit.capture_response=capture;rows=[];case_phases=[]
 try:
  for case in cases:
   active.clear();active.update(case);phases.clear()
   row=run_trial(win,kb,settings,'tot01',bank,trigger,block_id='synthetic_native',block_idx=0)
   row['case']=case['name'];rows.append(row);case_phases.append(list(phases))
 finally:StimUnit.capture_response=original
 bank.rebuild('editor',update_cache=True,text='日晷',editable=False)
 for stim in [bank.get_and_format('definition',definition=settings.items['tot01']['definition']),bank.get('resolution_prompt'),bank.get('editor'),bank.get('entry_hint')]:stim.draw()
 win.getMovieFrame(buffer='back');win.saveMovieFrames(str(out/'native_resolution.png'));win.close();trigger.close()
checks={
 'blank_reset':all(x=='' for x in before),'unicode_edit':entered[0]=='日晷',
 'known_correct':rows[0]['known_correct'],'known_wrong':not rows[1]['known_correct'],
 'typed_both':rows[2]['confirmation_basis']=='both' and rows[2]['spontaneous_resolved'],
 'partial_correct':rows[2]['initial_sound_correct'] and rows[2]['character_count_correct'],
 'recognition_only_wrong':rows[3]['confirmation_basis']=='recognition' and not rows[3]['spontaneous_resolved'] and rows[3]['initial_sound_correct'] is False,
 'different':rows[4]['tot_class']=='different_target','unknown':rows[5]['tot_class']=='unfamiliar_or_unsure',
 'unverified':rows[6]['tot_class']=='unverified','f4_skip':'character_count' not in case_phases[7] and 'related_words' not in case_phases[7],
 'f4_contamination_excluded':rows[7]['initial_sound_correct'] is None and rows[7]['spontaneous_resolved'],
 'latency_finite':0<rows[2]['resolution_latency_s']<5 and 0<rows[7]['resolution_latency_s']<5,
 'dontknow':rows[8]['judgment']=='dont_know' and not rows[8]['reported_tot'],
 'missing':rows[9]['judgment']=='missing' and not rows[9]['reported_tot'],
 'f4_count_skip':'related_words' not in case_phases[10] and rows[10]['character_count_guess'] is None,
 'f4_wrong_not_resolved':not rows[11]['spontaneous_resolved'] and rows[11]['resolution_latency_s'] is None,
 'typed_denied_preserved':rows[12]['confirmation_basis']=='typed' and rows[12]['verification']=='2',
 'unsubmitted_target':not rows[13]['spontaneous_resolved'] and rows[13]['resolution_response_text']=='日晷',
 'alternative_retained':rows[1]['alternative_target_response_text']=='月亮',
 'summary_separation':summarize(rows)['recognition_only_confirmed_n']==1}
report=dict(passed=all(checks.values()),checks=checks,before=before,entered=entered,phases=case_phases,rows=rows,summary=summarize(rows),limitation='Actual native run_trial and rebuilt TextBox2 with synthetic Pyglet Unicode/Backspace events and simulated keys;0.28s diagnostic deadlines;not human12-trial acquisition or OS IME/pilot.')
(out/'native_semantic.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(checks,ensure_ascii=False));assert report['passed'],checks
