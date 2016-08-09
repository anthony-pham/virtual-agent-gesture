
# Add asset paths
scene.addAssetPath('mesh', 'mesh')
scene.addAssetPath('motion', 'ChrRachel')
scene.addAssetPath("script", "behaviorsets")
scene.addAssetPath('script', 'scripts')
scene.loadAssets()

# Set scene parameters and camera
print 'Configuring scene parameters and camera'
scene.setScale(1.0)
scene.setBoolAttribute('internalAudio', True)
scene.run('default-viewer.py')
camera = getCamera()
camera.setEye(0, 1.71, 1.86)
camera.setCenter(0, 1, 0.01)
camera.setUpVector(SrVec(0, 1, 0))
camera.setScale(1)
camera.setFov(1.0472)
camera.setFarPlane(100)
camera.setNearPlane(0.1)
camera.setAspectRatio(0.966897)
cameraPos = SrVec(0, 1.6, 10)
scene.getPawn('camera').setPosition(cameraPos)

# Set up joint map for Rachel
print 'Setting up joint map and configuring Rachel\'s skeleton'
scene.run('zebra2-map.py')
zebra2Map = scene.getJointMapManager().getJointMap('zebra2')
RachelSkeleton = scene.getSkeleton('ChrRachel.sk')
zebra2Map.applySkeleton(RachelSkeleton)
zebra2Map.applyMotionRecurse('ChrRachel')

# Establish lip syncing data set
print 'Establishing lip syncing data set'
scene.run('init-diphoneDefault.py')

# Set up face definition
print 'Setting up face definition'
# Rachel's face definition
RachelFace = scene.createFaceDefinition('ChrRachel')
RachelFace.setFaceNeutral('ChrRachel@face_neutral')
RachelFace.setAU(1,  "left",  "ChrRachel@001_inner_brow_raiser_lf")
RachelFace.setAU(1,  "right", "ChrRachel@001_inner_brow_raiser_rt")
RachelFace.setAU(2,  "left",  "ChrRachel@002_outer_brow_raiser_lf")
RachelFace.setAU(2,  "right", "ChrRachel@002_outer_brow_raiser_rt")
RachelFace.setAU(4,  "left",  "ChrRachel@004_brow_lowerer_lf")
RachelFace.setAU(4,  "right", "ChrRachel@004_brow_lowerer_rt")
RachelFace.setAU(5,  "both",  "ChrRachel@005_upper_lid_raiser")
RachelFace.setAU(6,  "both",  "ChrRachel@006_cheek_raiser")
RachelFace.setAU(7,  "both",  "ChrRachel@007_lid_tightener")
RachelFace.setAU(10, "both",  "ChrRachel@010_upper_lip_raiser")
RachelFace.setAU(12, "left",  "ChrRachel@012_lip_corner_puller_lf")
RachelFace.setAU(12, "right", "ChrRachel@012_lip_corner_puller_rt")
RachelFace.setAU(25, "both",  "ChrRachel@025_lips_part")
RachelFace.setAU(26, "both",  "ChrRachel@026_jaw_drop")
RachelFace.setAU(45, "left",  "ChrRachel@045_blink_lf")
RachelFace.setAU(45, "right", "ChrRachel@045_blink_rt")

RachelFace.setViseme("open",    "ChrRachel@open")
RachelFace.setViseme("W",       "ChrRachel@W")
RachelFace.setViseme("ShCh",    "ChrRachel@ShCh")
RachelFace.setViseme("PBM",     "ChrRachel@PBM")
RachelFace.setViseme("FV",      "ChrRachel@FV")
RachelFace.setViseme("wide",    "ChrRachel@wide")
RachelFace.setViseme("tBack",   "ChrRachel@tBack")
RachelFace.setViseme("tRoof",   "ChrRachel@tRoof")
RachelFace.setViseme("tTeeth",  "ChrRachel@tTeeth")

print 'Adding character into scene'
# Set up Rachel
Rachel = scene.createCharacter('ChrRachel', '')
RachelSkeleton = scene.createSkeleton('ChrRachel.sk')
Rachel.setSkeleton(RachelSkeleton)
# Set position
RachelPos = SrVec(0, 0, 0)
Rachel.setPosition(RachelPos)
# Set facing direction
RachelFacing = SrVec(0, 0, 0)
Rachel.setHPR(RachelFacing)
# Set face definition
Rachel.setFaceDefinition(RachelFace)
# Set standard controller
Rachel.createStandardControllers()
# Deformable mesh
Rachel.setDoubleAttribute('deformableMeshScale', .01)
Rachel.setStringAttribute('deformableMesh', 'ChrRachel.dae')

# Lip syncing diphone setup
Rachel.setStringAttribute('lipSyncSetName', 'default')
Rachel.setBoolAttribute('usePhoneBigram', True)
Rachel.setVoice('remote')

import platform
if platform.system() == "Windows":
	windowsVer = platform.platform()
	if windowsVer.find("Windows-7") == 0:
		Rachel.setVoiceCode('Microsoft|Anna')
	else:
		if windowsVer.find("Windows-8") == 0 or windowsVer.find("Windows-post2008Server") == 0:
			Rachel.setVoiceCode('Microsoft|Zira|Desktop')
else: # non-Windows platform, use Festival voices
	Rachel.setVoiceCode('voice_kal_diphone')

# setup locomotion
scene.run('BehaviorSetMaleMocapLocomotion.py')
setupBehaviorSet()
retargetBehaviorSet('ChrRachel')

# setup gestures
scene.run('BehaviorSetGestures.py')
setupBehaviorSet()
retargetBehaviorSet('ChrRachel')

# setup reach 
scene.run('BehaviorSetReaching.py')
setupBehaviorSet()
retargetBehaviorSet('ChrRachel')
# Turn on GPU deformable geometry
Rachel.setStringAttribute("displayType", "GPUmesh")

# Set up steering
print 'Setting up steering'
steerManager = scene.getSteerManager()
steerManager.setEnable(False)
Rachel.setBoolAttribute('steering.pathFollowingMode', False) # disable path following mode so that obstacles will be respected
steerManager.setEnable(True)
# Start the simulation
print 'Starting the simulation'
sim.start()

bml.execBML('ChrRachel', '<body posture="ChrBrad@Idle01"/>')
#bml.execBML('ChrRachel', '<saccade mode="listen"/>')
#bml.execBML('ChrRachel', '<gaze sbm:handle="Rachel" target="camera"/>')

print 'Setting saccade mode to talk'
bml.execBML('ChrRachel', '<saccade mode="talk"/>')


bml.execBMLAt(1,'ChrRachel', '<speech type="application/ssml+xml" id="myspeech"> \
<mark name="T0"/>"Go" \
<mark name="T1"/> \
<mark name="T2"/>"to" \
<mark name="T3"/> \
<mark name="T4"/>"my" \
<mark name="T5"/> \
<mark name="T6"/>"Right" \
<mark name="T7"/> \
</speech> \
<gaze direction="RIGHT" sbm:joint-range="HEAD CHEST" start="myspeech:T6" sbm:joint-speed="2000" target="ChrRachel"/> \
<gesture name="ChrBrad@Idle01_PointRt01" stroke="myspeech:T6"/>')


bml.execBMLAt(3,'ChrRachel', '<speech type="application/ssml+xml" id="myspeech"> \
<mark name="T0"/>"Go" \
<mark name="T1"/> \
<mark name="T2"/>"up" \
<mark name="T3"/> \
<mark name="T4"/>"the" \
<mark name="T5"/> \
<mark name="T6"/>"stairs" \
<mark name="T7"/> \
</speech> \
<gesture name="ChrBrad@Idle01_BeatHighLf01" stroke="myspeech:T5"/> \
<gaze sbm:joint-range="HEAD CHEST" start="myspeech:T0" sbm:joint-speed="2000" target="ChrRachel"/>')


bml.execBMLAt(6.5,'ChrRachel', '<speech type="application/ssml+xml" id="myspeech"> \
<mark name="T0"/>"at" \
<mark name="T1"/> \
<mark name="T2"/>"the" \
<mark name="T3"/> \
<mark name="T4"/>"top" \
<mark name="T5"/> \
<mark name="T6"/>"go" \
<mark name="T7"/> \
<mark name="T8"/>"straight" \
<mark name="T9"/> \
<mark name="T10"/>"and" \
<mark name="T11"/> \
<mark name="T12"/>"then" \
<mark name="T13"/> \
<mark name="T14"/>"through" \
<mark name="T15"/> \
<mark name="T16"/>"the" \
<mark name="T17"/> \
<mark name="T18"/>"double" \
<mark name="T19"/> \
<mark name="T20"/>"doors" \
<mark name="T21"/> \
</speech> \
<gesture name="ChrBrad@Idle01_ChopBoth01" stroke="myspeech:T8"/> \
<gesture name="ChrBrad@Idle01_ChopLf01" stroke="myspeech:T15"/>')

bml.execBMLAt(11,'ChrRachel', '<speech type="application/ssml+xml" id="myspeech"> \
<mark name="T0"/>"Follow" \
<mark name="T1"/> \
<mark name="T2"/>"the" \
<mark name="T3"/> \
<mark name="T4"/>"hallway" \
<mark name="T5"/> \
<mark name="T6"/>"to" \
<mark name="T7"/> \
<mark name="T8"/>"the" \
<mark name="T9"/> \
<mark name="T10"/>"left" \
<mark name="T11"/> \
<mark name="T12"/>"and" \
<mark name="T13"/> \
<mark name="T14"/>"the" \
<mark name="T15"/> \
<mark name="T16"/>"location" \
<mark name="T17"/> \
<mark name="T18"/>"will" \
<mark name="T19"/> \
<mark name="T20"/>"be" \
<mark name="T21"/> \
<mark name="T22"/>"on" \
<mark name="T23"/> \
<mark name="T24"/>"your" \
<mark name="T25"/> \
<mark name="T26"/>"right" \
<mark name="T27"/> \
</speech> \
<gesture name="ChrBrad@Idle01_IndicateLeftLf01" stroke="myspeech:T10"/> \
<gesture name="ChrBrad@Idle01_IndicateRightRt01" stroke="myspeech:T26"/>')



## <gesture name="ChrBrad@Idle01_IndicateLeftLf01"/> #Slight Left

## <gesture name="ChrBrad@Idle01_IndicateRightRt01"/> #Slight Right

## <gesture name="ChrBrad@Idle01_PointRt01"/> #Right

## <gesture name="ChrBrad@Idle01_PointLf01"/> #Left

## <gesture name="ChrBrad@Idle01_ChopBoth01"/> #Straight

sim.resume()
