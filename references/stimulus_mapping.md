# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `tot01` | judgment/partial/resolution | definition | 古人利用太阳照出的指针影子， 在刻有时刻的盘面上读出时间的器具。 → 日晷 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial r;2 characters; not normed |
| `tot02` | judgment/partial/resolution | definition | 木构件连接时，一端凸出、另一端凹入， 彼此嵌合而不靠钉子的连接结构。 → 榫卯 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial s;2 characters; not normed |
| `tot03` | judgment/partial/resolution | definition | 端午节常和艾草一起挂起、叶片像剑， 全株有香气、常生长在水边的植物。 → 菖蒲 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial ch;2 characters; not normed |
| `tot04` | judgment/partial/resolution | definition | 把蚕茧放进热水，再抽出长丝并合， 制作生丝的加工过程。 → 缫丝 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial s;2 characters; not normed |
| `tot05` | judgment/partial/resolution | definition | 古汉语中泛指八九十岁高龄的说法， 常用于祝贺老人长寿。 → 耄耋 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial m;2 characters; not normed |
| `tot06` | judgment/partial/resolution | definition | 中国古代用天然磁石制成的辨向器具， 常见复原形状为盘上的一把勺子。 → 司南 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial s;2 characters; not normed |
| `tot07` | judgment/partial/resolution | definition | 横截面呈三角形的透明光学器件， 可以把白光分解成不同颜色。 → 三棱镜 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial s;3 characters; not normed |
| `tot08` | judgment/partial/resolution | definition | 一种传统彩灯，内部转动的轮轴带着剪影， 使外罩上出现人物或动物循环移动的影像。 → 走马灯 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial z;3 characters; not normed |
| `tot09` | judgment/partial/resolution | definition | 围绕轴心转动的多片叶片装置， 把旋转动力变为推动船只或飞机的力。 → 螺旋桨 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial l;3 characters; not normed |
| `tot10` | judgment/partial/resolution | definition | 远处景物的光线经过空气折射， 使海面或沙漠上出现虚幻景象的自然现象。 → 海市蜃楼 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial h;4 characters; not normed |
| `tot11` | judgment/partial/resolution | definition | 花朵很大、白色，常在夜间开放， 而且开花时间很短的仙人掌科植物。 → 昙花 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial t;2 characters; not normed |
| `tot12` | judgment/partial/resolution | definition | 日式房间中铺在地板上、 可供坐卧的长方形草编席垫。 → 榻榻米 (only revealed at verification) | BROWN1966 | pp326–327 definition elicitation | adapted original Chinese | config/config.yaml | Initial t;3 characters; not normed |
| all | ready/fixation | ready/fixation | 下一题; + | BROWN1966 | individual computerized implementation | inferred | config/config.yaml | self-paced ready;0.5s fixation |
| all | judgment | judgment_prompt/options | 已经想起 / 确信知道快想起来却说不出 / 不知道 | BROWN1966 | p327 Procedure2–3 | adapted | config/config.yaml |20s |
| TOT | initial_sound/character_count/related_words | phase prompts/editor/count_options | 声母;字数;近音词和近义词 | BROWN1966 | p327 response sheet | adapted | config/config.yaml |10/8/10s;F4 stops reports |
| know/TOT | known_answer/resolution | editor/entry_hint | 输入完整词语;F2提交 | BROWN1966 | p327 Procedure8 | adapted | config/config.yaml |15s;no target revealed |
| all | verification/alternative_target | verification_target/options/editor | 预设词语;是/不是/不熟悉或不能确定;另一个词 | BROWN1966 | p327 Procedure5 | adapted | config/config.yaml |10s each;alternative only after different |
| all | saved/good_bye | saved/good_bye | 本题已保存;任务完成;无常模说明 | BROWN1966 | digital implementation | inferred | config/config.yaml |no correctness or personal assessment |
