# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| elicitation | task.items |12 original Chinese definitions | BROWN1966 | pp326–327 definition procedure | adapted | No source item copying or claimed frequency norm |
| states | task.judgment_keys | know / TOT / don't know | BROWN1966 | p327 Procedure2–3 | adapted | Missing retained separately |
| partial | stimuli | initial sound,character count,related words | BROWN1966 | p327 response sheet | adapted | Mandarin initial replaces English letter; character count replaces syllables |
| timing | timing | judgment20,known15,initial10,count8,related10,resolution15,verify10,alternative10 seconds | BROWN1966 | Source is self-paced group work | inferred | Bounded individual digital adaptation |
| verification | task.verification_keys | sought/different/unfamiliar-or-unsure | BROWN1966 | p327 Procedure5 | adapted | intended-target confirmation, alternatives retained but manually coded |
| resolution | task.resolved_key | F4 during partial;F2 in final entry | BROWN1966 | p327 Procedure8 stops partial reports | adapted | earliest resolution report plus high-resolution software clocks |
| scheduler | task.overall_seed |130031;12 unique labels | BROWN1966 | p326 item list | inferred | Built-in even BlockUnit; no adaptive controller |
| display | window / stimuli |1280x800 white,SimHei | BROWN1966 | auditory English group source | inferred | Individual visual Chinese; explicit layout |
