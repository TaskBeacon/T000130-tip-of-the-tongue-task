"""Pure intended-target scoring; no norms, timing or scheduling infrastructure."""
import re
import unicodedata

def normalize(text):
    return re.sub(r'[\s，。！？、,.!?；;：:]+','',unicodedata.normalize('NFKC',str(text or '')).lower())

def text_attempt(text, submitted, rt, accepted):
    value=normalize(text)
    return dict(response_text=str(text or ''),normalized_text=value,submitted=bool(submitted),
                correct=bool(submitted and value and value in [normalize(x) for x in accepted]),
                submit_rt_s=float(rt) if submitted and rt is not None else None)

def score_trial(judgment, known, resolution, verification, initial, count, item, latency):
    reported=judgment=='tot'
    typed=bool(reported and resolution and resolution['correct'])
    recognition=bool(reported and verification=='1')
    confirmed=typed or recognition
    basis='both' if typed and recognition else 'typed' if typed else 'recognition' if recognition else 'none'
    initial_guess=normalize(initial['response_text']) if initial and initial['submitted'] else ''
    # Pinyin initials are complete consonant graphemes (zh/ch/sh indivisible).
    # 0 means zero onset; y/w are spelling carriers, not consonant initials.
    valid_initials={'b','p','m','f','d','t','n','l','g','k','h','j','q','x','zh','ch','sh','r','z','c','s','0'}
    return dict(judgment=judgment,reported_tot=reported,confirmed_tot=confirmed,confirmation_basis=basis,
      recognition_confirmed=recognition,typed_confirmed=typed,
      tot_class='not_tot' if not reported else 'confirmed_intended' if confirmed else 'different_target' if verification=='2' else 'unfamiliar_or_unsure' if verification=='3' else 'unverified',
      known_correct=bool(judgment=='know' and known and known['correct']),
      spontaneous_resolved=typed,resolution_latency_s=latency if typed else None,
      verification=verification,
      initial_sound_guess=initial_guess or None,
      initial_sound_usable=bool(confirmed and initial_guess in valid_initials),
      initial_sound_correct=(initial_guess==item['initial_sound']) if confirmed and initial_guess in valid_initials else None,
      character_count_guess=int(count) if count in ['1','2','3','4'] else None,
      character_count_correct=(int(count)==item['character_count']) if confirmed and count in ['1','2','3','4'] else None)

def summarize(rows):
    total=len(rows); tots=[r for r in rows if r['reported_tot']]; confirmed=[r for r in tots if r['confirmed_tot']]
    def mean(values): return sum(values)/len(values) if values else None
    return dict(trials=total,reported_tot_n=len(tots),confirmed_intended_tot_n=len(confirmed),
      reported_tot_rate=len(tots)/total if total else None,
      confirmed_intended_tot_rate=len(confirmed)/total if total else None,
      typed_confirmed_n=sum(r['typed_confirmed'] for r in tots),
      recognition_only_confirmed_n=sum(r['confirmation_basis']=='recognition' for r in tots),
      different_target_tot_n=sum(r['tot_class']=='different_target' for r in tots),
      unfamiliar_or_unsure_tot_n=sum(r['tot_class']=='unfamiliar_or_unsure' for r in tots),
      unverified_tot_n=sum(r['tot_class']=='unverified' for r in tots),
      judgment_missing_n=sum(r['judgment']=='missing' for r in rows),
      spontaneous_resolution_rate_of_reported_tot=mean([int(r['spontaneous_resolved']) for r in tots]),
      resolution_latency_mean_s=mean([r['resolution_latency_s'] for r in tots if r['resolution_latency_s'] is not None]),
      initial_sound_accuracy=mean([int(r['initial_sound_correct']) for r in confirmed if r['initial_sound_correct'] is not None]),
      initial_sound_denominator=sum(r['initial_sound_correct'] is not None for r in confirmed),
      character_count_accuracy=mean([int(r['character_count_correct']) for r in confirmed if r['character_count_correct'] is not None]),
      character_count_denominator=sum(r['character_count_correct'] is not None for r in confirmed),
      interpretation='Descriptive intended-target measures only; recognition-only confirmation is subjective; original Chinese materials unpiloted; no norms.')
