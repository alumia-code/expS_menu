"""All the menu actions necessary for interaction with the menu GUI.
Single presses have long and short actions.
Double presses have a tuple key where the order of the elements represents the order of press.
"""
menu_combinations = {
    "single": {
        "long": {
            "menu1": {
                0: "action0long",
                1: "action1long",
                2: "action2long",
                3: "action3long",
                4: "action4long",
                5: "action5long",
                6: "action6long",
                7: "action7long"
            },
            "menu2": {
                0: "action0long",
                1: "action1long",
                2: "action2long",
                3: "action3long",
                4: "action4long",
                5: "action5long",
                6: "action6long",
                7: "action7long"
            }
        },
        "short": {
            "nav": {
                "left": {
                    0: "fps_",
                    1: "blk_",
                    2: "exp_",
                    4: "up",
                    5: "down",
                    6: "left",
                    7: "right",
                },
                "right": {
                    0: "fps_",
                    1: "exp_",
                    2: "stop_0",
                    4: "up",
                    5: "down",
                    6: "left",
                    7: "right",
                },
                "up": {
                    0: "msppresetchange_current&",
                    4: "up",
                    5: "down",
                    6: "left",
                    7: "right",
                },
                "down": {
                    0: "mspwavplay_current&",
                    4: "up",
                    5: "down",
                    6: "left",
                    7: "right",
                },
                "center": {
                    0: "str_0",
                    1: "bperf_0",
                    2: "eperf_0",
                    3: "end_0",
                    4: "up",
                    5: "down",
                    6: "left",
                    7: "right",
                }
            },
            "audio": {
                "left": {
                    0: "mspcrossfreq_current&",
                    1: "mspcrossfreq_umax&",
                    2: "mspcrossfreq_umin&",
                    3: "mspcrossfreq_cycle&",
                    4: "up",
                    5: "down",
                    6: "left",
                    7: "right",
                    8: "loopr",
                    9: "loopl"
                },
                "right": {
                    0: "mspcrossfreq3_current&",
                    1: "mspcrossfreq3_umax&",
                    2: "mspcrossfreq3_umin&",
                    3: "mspcrossfreq3_cycle&",
                    4: "up",
                    5: "down",
                    6: "left",
                    7: "right",
                    8: "loopr",
                    9: "loopl"
                },
                "up": {
                    0: "mspcrossfreq2_current&",
                    1: "mspcrossfreq2_umax&",
                    2: "mspcrossfreq2_umin&",
                    3: "mspcrossfreq2_cycle&",
                    4: "up",
                    5: "down",
                    6: "left",
                    7: "right",
                    8: "loopr",
                    9: "loopl"
                },
                "down": {
                    0: "mspodlevel_current&",
                    1: "mspodlevel_umax&",
                    2: "mspodlevel_umin&",
                    3: "mspodlevel_cycle&",
                    4: "up",
                    5: "down",
                    6: "left",
                    7: "right",
                    8: "loopr",
                    9: "loopl"
                },
                "center": {
                    0: "mspmaingain_current&",
                    1: "mspmaingain_umax&",
                    2: "mspmaingain_umin&",
                    3: "mspmaingain_cycle&",
                    4: "up",
                    5: "down",
                    6: "left",
                    7: "right",
                    8: "loopr",
                    9: "loopl"
                }
            },
            "video_sel": {
                "center": {
                    0: "play",
                    1: "play",
                    6: "prevv",
                    7: "nextv"
                }
            },
            "video_play": {
                "center": {
                    0: "play_",
                    1: "blk_",
                    2: "edt_",
                    4: "up",
                    5: "down",
                }
            }
        }
    },
    "double": {#the order of the pair is the press order
            # MENU CHANGE COMBINATIONS
            (0,1): "nav",
            (0,2): "video_sel",
            (0,3): "audio",
            # -------------//--------
            # LOOP COMBINATIONS
            (4,8): "loopr",
            (4,9): "loopl",
            (5,8): "loopr",
            (5,9): "loopl",
            (6,8): "loopr",
            (6,9): "loopl",
            (7,8): "loopr",
            (7,9): "loopl"
            # -------------//--------
    }
}

# estar em stream ou nao
# ter selecionado pasta ou nao
# estar a gravar ou nao
# estar a tocar video ou nao

menu_conditions = {
    "single": {
        "long": {
            "menu1": {
                0: "action0long",
                1: "action1long",
                2: "action2long",
                3: "action3long",
                4: "action4long",
                5: "action5long",
                6: "action6long",
                7: "action7long"
            },
            "menu2": {
                0: "action0long",
                1: "action1long",
                2: "action2long",
                3: "action3long",
                4: "action4long",
                5: "action5long",
                6: "action6long",
                7: "action7long"
            }
        },
        "short": {
            "nav": {
                "left": {
                    0: {"stream": True, "sel_folder": "", "record": False, "play": "", "in_perf": ""},
                    1: {"stream": True, "sel_folder": "", "record": False, "play": "", "in_perf": ""},
                    2: {"stream": True, "sel_folder": "", "record": False, "play": "", "in_perf": ""},
                    4: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    5: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    6: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    7: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                },
                "right": {
                    0: {"stream": False, "sel_folder": True, "record": False, "play": "", "in_perf": True},
                    1: {"stream": False, "sel_folder": True, "record": False, "play": "", "in_perf": True},
                    2: {"stream": False, "sel_folder": True, "record": True, "play": "", "in_perf": True},
                    4: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    5: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    6: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    7: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                },
                "up": {
                    0: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    4: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    5: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    6: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    7: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                },
                "down": {
                    0: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    4: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    5: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    6: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    7: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                },
                "center": {
                    0: {"stream": "", "sel_folder": "", "record": False, "play": "", "in_perf": False},
                    1: {"stream": False, "sel_folder": True, "record": False, "play": False, "in_perf": False},
                    2: {"stream": False, "sel_folder": True, "record": False, "play": False, "in_perf": True},
                    3: {"stream": False, "sel_folder": "", "record": False, "play": False, "in_perf": ""},
                    4: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    5: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    6: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    7: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                }
            },
            "audio": {
                "left": {
                    0: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    1: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    2: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    3: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    4: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    5: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    6: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    7: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    8: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    9: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                },
                "right": {
                    0: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    1: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    2: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    3: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    4: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    5: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    6: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    7: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    8: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    9: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                },
                "up": {
                    0: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    1: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    2: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    3: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    4: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    5: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    6: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    7: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    8: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    9: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                },
                "down": {
                    0: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    1: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    2: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    3: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    4: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    5: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    6: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    7: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    8: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    9: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                },
                "center": {
                   0: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    1: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    2: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    3: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    4: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    5: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    6: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    7: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    8: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    9: {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                }
            },
            "video_sel": {
                "center": {
                    0:  {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    1:  {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    6:  {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                    7:  {"stream": "", "sel_folder": "", "record": "", "play": "", "in_perf": ""},
                }
            },
            "video_play": {
                "center": {
                    0: {"stream": False, "sel_folder": True, "record": "", "play": False, "in_perf": True},
                    1: {"stream": False, "sel_folder": True, "record": "", "play": False, "in_perf": True},
                    2: {"stream": False, "sel_folder": True, "record": "", "play": False, "in_perf": True},
                    3: {"stream": False, "sel_folder": True, "record": "", "play": False, "in_perf": True},
                    4: {"stream": False, "sel_folder": True, "record": "", "play": False, "in_perf": True},
                    5: {"stream": False, "sel_folder": True, "record": "", "play": False, "in_perf": True},
                }
            }
        }
    },
    "double": {#the order of the pair is the press order
            # MENU CHANGE COMBINATIONS
            (0,1): "nav",
            (0,2): "video_sel",
            (0,3): {"stream": "", "sel_folder": True, "record": "", "play": "", "in_perf": ""},
            # -------------//--------
            # LOOP COMBINATIONS
            (4,8): "loopr",
            (4,9): "loopl",
            (5,8): "loopr",
            (5,9): "loopl",
            (6,8): "loopr",
            (6,9): "loopl",
            (7,8): "loopr",
            (7,9): "loopl"
            # -------------//--------
    }
}


menu_labels = {
    "nav": {
        "down": {
            "button_hand_1": "WAV",
            "button_hand_2": "",
            "button_hand_3": "",
            "button_hand_4": ""
        },
        "center": {
            "button_hand_1": "STREAM",
            "button_hand_2": "INIT\nPERF",
            "button_hand_3": "END\nPERF",
            "button_hand_4": "EXIT"
        }, 
        "up": {
            "button_hand_1": "PRESET",
            "button_hand_2": "",
            "button_hand_3": "",
            "button_hand_4": ""
        }, 
        "left": {
            "button_hand_1": "FPS\n",
            "button_hand_2": "BLK\n",
            "button_hand_3": "EXP\n",
            "button_hand_4": ""
        }, 
        "right": {
            "button_hand_1": "FPS\n",
            "button_hand_2": "EXP\n",
            "button_hand_3": "STOP\nREC",
            "button_hand_4": ""
        }
    },
    "audio": {
        "down": {
            "button_hand_1": "OD LEVEL\n",
            "button_hand_2": "MAX\n",
            "button_hand_3": "MIN\n",
            "button_hand_4": "CYC\n"
        },
        "center": {
            "button_hand_1": "GAIN\n",
            "button_hand_2": "MAX\n",
            "button_hand_3": "MIN\n",
            "button_hand_4": "CYC\n"
        }, 
        "up": {
            "button_hand_1": "CROSS2\n",
            "button_hand_2": "MAX\n",
            "button_hand_3": "MIN\n",
            "button_hand_4": "CYC\n"
        }, 
        "left": {
            "button_hand_1": "CROSS\n",
            "button_hand_2": "MAX\n",
            "button_hand_3": "MIN\n",
            "button_hand_4": "CYC\n"
        }, 
        "right": {
            "button_hand_1": "CROSS3\n",
            "button_hand_2": "MAX\n",
            "button_hand_3": "MIN\n",
            "button_hand_4": "CYC\n"
        }
    },
    "video_play": {
        "down": {
            "button_hand_1": "LABELg",
            "button_hand_2": "LABELa",
            "button_hand_3": "LABELr",
            "button_hand_4": "LABELq" 
        },
        "center": {
            "button_hand_1": "Play\nNormal",
            "button_hand_2": "BLK\n",
            "button_hand_3": "EDT\n",
            "button_hand_4": ""
        }, 
        "up": {
            "button_hand_1": "LABELp",
            "button_hand_2": "LABELi",
            "button_hand_3": "LABELu",
            "button_hand_4": "LABELn"
        }, 
        "left": {
            "button_hand_1": "LABELc",
            "button_hand_2": "LABEL,",
            "button_hand_3": "LABELu",
            "button_hand_4": "LABEL,"
        }, 
        "right": {
            "button_hand_1": "LABEL1",
            "button_hand_2": "LABEL2",
            "button_hand_3": "LABEL3",
            "button_hand_4": "LABEL4"
        }
    }
}
