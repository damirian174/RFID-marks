extends Node


enum MARK_STAGES {GET_BOX,ATTACH_STICKER,PRESS_MARK_BUTTON,SCAN}
var current_stage: MARK_STAGES = MARK_STAGES.GET_BOX
