import unittest
from src.utils import text_attempt,score_trial,summarize
ITEM=dict(accepted=['日晷'],initial_sound='r',character_count=2)
class Scoring(unittest.TestCase):
 def test_no_submit_not_resolution(self):
  a=text_attempt('日晷',False,None,ITEM['accepted'])
  r=score_trial('tot',None,a,'3',None,None,ITEM,1.0)
  self.assertFalse(r['confirmed_tot']);self.assertFalse(r['spontaneous_resolved'])
 def test_initial_inventory(self):
  for value,expected in [('r',True),('sh',False),('y',None),('',None),('0',False)]:
   a=text_attempt(value,True,.1,[])
   r=score_trial('tot',None,None,'1',a,'0',ITEM,None)
   self.assertEqual(r['initial_sound_correct'],expected);self.assertIsNone(r['character_count_correct'])
 def test_recognition_only_not_typed(self):
  r=score_trial('tot',None,None,'1',None,None,ITEM,None)
  self.assertEqual(r['confirmation_basis'],'recognition');self.assertFalse(r['typed_confirmed'])
  self.assertEqual(summarize([r])['recognition_only_confirmed_n'],1)
 def test_traditional_and_punctuation(self):
  self.assertTrue(text_attempt(' 繅絲。',True,.3,['缫丝','繅絲'])['correct'])
 def test_missing_not_unknown(self):
  r=score_trial('missing',None,None,None,None,None,ITEM,None)
  self.assertEqual(summarize([r])['judgment_missing_n'],1)
if __name__=='__main__':unittest.main()
