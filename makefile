debug :
	@echo "Debugging with Android Emulator"
	$$ANDROID_HOME/emulator/emulator  -avd  Pixel_2_API_28 & sleep 3 && tns --path vue-snek debug android --emulator
