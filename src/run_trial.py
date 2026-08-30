from psyflow import StimUnit, next_trial_id, set_trial_context
from .utils import text_attempt, score_trial

def run_trial(win,kb,settings,condition,stim_bank,trigger_runtime,block_id=None,block_idx=None):
    trial_id=next_trial_id(); item=settings.items[condition]
    row=dict(trial_id=trial_id,block_id=block_id,block_idx=block_idx,condition=condition,item_id=condition,
             material_version=settings.material_version,definition=item['definition'],target=item['target'],
             resolution_clock='psychopy_flip_time_plus_rt',
             synthetic_fixture=bool(getattr(settings,'synthetic_fixture',False)))
    def unit(phase,*stimuli,keys=(),duration=None):
        u=StimUnit(phase,win,kb,runtime=trigger_runtime).add_stim(*stimuli)
        set_trial_context(u,trial_id=trial_id,phase=phase,deadline_s=duration,valid_keys=list(keys),
                          block_id=block_id,condition_id=condition,stim_id=phase,
                          task_factors={'item_id':condition,'material_version':settings.material_version})
        return u
    unit('ready',stim_bank.get('ready'),keys=[settings.continue_key]).wait_and_continue(keys=[settings.continue_key]).to_dict(row)
    unit('fixation',stim_bank.get('fixation'),duration=settings.fixation_duration).show(duration=settings.fixation_duration,onset_trigger=settings.triggers['fixation_onset']).to_dict(row)
    definition=stim_bank.get_and_format('definition',definition=item['definition'])
    judgment=unit('judgment',definition,stim_bank.get('judgment_prompt'),stim_bank.get('judgment_options'),
                  keys=settings.judgment_keys,duration=settings.judgment_duration)
    judgment.capture_response(keys=settings.judgment_keys,duration=settings.judgment_duration,terminate_on_response=True,
        onset_trigger=settings.triggers['judgment_onset'],response_trigger={'1':settings.triggers['judgment_response'],'2':settings.triggers['judgment_tot'],'3':settings.triggers['judgment_dont_know']},timeout_trigger=settings.triggers['judgment_no_response']).to_dict(row)
    state={'1':'know','2':'tot','3':'dont_know'}.get(judgment.get_state('response'),'missing')
    tot_start=judgment.get_state('flip_time')+judgment.get_state('rt') if state=='tot' else None
    attempts={}; count=None; resolved_at=None; early=False
    phases=['known_answer'] if state=='know' else ['initial_sound','character_count','related_words','resolution'] if state=='tot' else []
    for phase in phases:
        if early and phase!='resolution': continue
        partial=phase in ['initial_sound','character_count','related_words']
        duration=getattr(settings,phase+'_duration')
        keys=list(settings.count_keys) if phase=='character_count' else [settings.submit_key]
        if partial: keys.append(settings.resolved_key)
        stimuli=[definition,stim_bank.get(phase+'_prompt')]
        editor=None
        if phase=='character_count': stimuli += [stim_bank.get('count_options'),stim_bank.get('count_hint')]
        else:
            fixture=getattr(settings,'synthetic_text',{}).get(condition,{}).get(phase,'')
            editor=stim_bank.rebuild('editor',update_cache=True,text=fixture,editable=True); editor.hasFocus=True
            stimuli += [editor,stim_bank.get('partial_hint' if partial else 'entry_hint')]
        capture=unit(phase,*stimuli,keys=keys,duration=duration)
        response_map={key:settings.triggers[phase+'_response'] for key in keys}
        if partial: response_map[settings.resolved_key]=settings.triggers[phase+'_resolved']
        capture.capture_response(keys=keys,duration=duration,terminate_on_response=True,onset_trigger=settings.triggers[phase+'_onset'],
            response_trigger=response_map,timeout_trigger=settings.triggers[phase+'_no_response'])
        response=capture.get_state('response'); rt=capture.get_state('rt')
        if editor:
            editor.editable=False; editor.hasFocus=False
            attempt=text_attempt(editor.getText(),response==settings.submit_key,rt,item['accepted'])
            attempts[phase]=attempt; capture.set_state(**attempt)
        if phase=='character_count' and response!=settings.resolved_key: count=response
        if partial and response==settings.resolved_key:
            resolved_at=capture.get_state('flip_time')+rt;early=True
            row['early_resolution_phase']=phase
        if phase=='resolution' and attempts[phase]['correct'] and resolved_at is None:
            resolved_at=capture.get_state('flip_time')+rt
        capture.to_dict(row)
    verify=unit('verification',stim_bank.get_and_format('verification_target',target=item['target']),
        stim_bank.get('verification_prompt'),stim_bank.get('verification_options'),keys=settings.verification_keys,duration=settings.verification_duration)
    verify.capture_response(keys=settings.verification_keys,duration=settings.verification_duration,terminate_on_response=True,
        onset_trigger=settings.triggers['verification_onset'],response_trigger={'1':settings.triggers['verification_response'],'2':settings.triggers['verification_different'],'3':settings.triggers['verification_unknown']},timeout_trigger=settings.triggers['verification_no_response']).to_dict(row)
    verification=verify.get_state('response')
    if verification=='2':
        editor=stim_bank.rebuild('editor',update_cache=True,text='',editable=True);editor.hasFocus=True
        alt=unit('alternative_target',stim_bank.get('alternative_target_prompt'),editor,stim_bank.get('entry_hint'),
            keys=[settings.submit_key],duration=settings.alternative_target_duration)
        alt.capture_response(keys=[settings.submit_key],duration=settings.alternative_target_duration,terminate_on_response=True,
            onset_trigger=settings.triggers['alternative_target_onset'],response_trigger=settings.triggers['alternative_target_response'],
            timeout_trigger=settings.triggers['alternative_target_no_response'])
        editor.editable=False;editor.hasFocus=False
        alt.set_state(response_text=editor.getText(),submitted=alt.get_state('response')==settings.submit_key).to_dict(row)
    latency=resolved_at-tot_start if resolved_at is not None and tot_start is not None else None
    row.update(score_trial(state,attempts.get('known_answer'),attempts.get('resolution'),verification,attempts.get('initial_sound'),count,item,latency))
    row.setdefault('early_resolution_phase',None)
    unit('saved',stim_bank.get('saved'),duration=settings.saved_duration).show(duration=settings.saved_duration,onset_trigger=settings.triggers['saved_onset']).to_dict(row)
    return row
