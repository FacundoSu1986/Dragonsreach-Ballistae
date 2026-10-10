.function CaptureMatrices
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp24 Bool
						.local ::temp25 ObjectReference
						.local ::temp26 Bool
						.local ::temp27 Float[]
						.local ::temp28 Bool
					.endLocalTable
					.code
						CallMethod Is3DLoaded self ::temp24                      ;@line 148
						Not ::temp24 ::temp24                                    ;@line 148
						Cast ::temp24 ::temp24                                   ;@line 148
						JumpT ::temp24 _label0                                   ;@line 148
						Cast ::temp25 self                                       ;@line 148
						CallStatic netimmerse HasNode ::temp26 ::temp25 ::YawNode_var False  ;@line 148
						Not ::temp26 ::temp26                                    ;@line 148
						Cast ::temp24 ::temp26                                   ;@line 148
					_label0:
						Cast ::temp24 ::temp24                                   ;@line 148
						JumpT ::temp24 _label1                                   ;@line 148
						Cast ::temp25 self                                       ;@line 148
						CallStatic netimmerse HasNode ::temp26 ::temp25 ::PitchNode_var False  ;@line 148
						Not ::temp26 ::temp26                                    ;@line 148
						Cast ::temp24 ::temp26                                   ;@line 148
					_label1:
						Cast ::temp24 ::temp24                                   ;@line 148
						JumpT ::temp24 _label2                                   ;@line 148
						Cast ::temp25 self                                       ;@line 148
						CallStatic netimmerse HasNode ::temp26 ::temp25 ::VisualBoltNode_var False  ;@line 148
						Not ::temp26 ::temp26                                    ;@line 148
						Cast ::temp24 ::temp26                                   ;@line 148
					_label2:
						JumpF ::temp24 _label3                                   ;@line 148
						Return False                                             ;@line 149
						Jump _label3                                             ;@line 149
					_label3:
						Cast ::temp27 None                                       ;@line 152
						CompareEQ ::temp26 yawBase ::temp27                      ;@line 152
						JumpF ::temp26 _label4                                   ;@line 152
						ArrayCreate ::temp27 9                                   ;@line 153
						Assign yawBase ::temp27                                  ;@line 153
						ArrayCreate ::temp27 9                                   ;@line 154
						Assign pitchBase ::temp27                                ;@line 154
						ArrayCreate ::temp27 9                                   ;@line 155
						Assign yawMatrix ::temp27                                ;@line 155
						ArrayCreate ::temp27 9                                   ;@line 156
						Assign pitchMatrix ::temp27                              ;@line 156
						ArrayCreate ::temp27 9                                   ;@line 157
						Assign rootWorldMatrix ::temp27                          ;@line 157
						ArrayCreate ::temp27 9                                   ;@line 158
						Assign muzzleWorldMatrix ::temp27                        ;@line 158
						ArrayCreate ::temp27 3                                   ;@line 159
						Assign rootPosition ::temp27                             ;@line 159
						ArrayCreate ::temp27 3                                   ;@line 160
						Assign muzzlePosition ::temp27                           ;@line 160
						Cast ::temp25 self                                       ;@line 161
						CallStatic netimmerse GetNodeLocalRotationMatrix ::temp24 ::temp25 ::YawNode_var yawBase False  ;@line 161
						Not ::temp24 ::temp24                                    ;@line 161
						Cast ::temp24 ::temp24                                   ;@line 161
						JumpT ::temp24 _label5                                   ;@line 161
						Cast ::temp25 self                                       ;@line 161
						CallStatic netimmerse GetNodeLocalRotationMatrix ::temp28 ::temp25 ::PitchNode_var pitchBase False  ;@line 161
						Not ::temp28 ::temp28                                    ;@line 161
						Cast ::temp24 ::temp28                                   ;@line 161
					_label5:
						JumpF ::temp24 _label6                                   ;@line 161
						Cast ::temp27 None                                       ;@line 162
						Assign yawBase ::temp27                                  ;@line 162
						Return False                                             ;@line 163
						Jump _label6                                             ;@line 163
					_label6:
						Jump _label4                                             ;@line 163
					_label4:
						Return True                                              ;@line 166
					.endCode
				.endFunction