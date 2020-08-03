<template>
    <Page>
        <ActionBar title="Welcome to NativeScript-Vue!"/>
        <StackLayout orientation="vertical">
            <Label class="message" :text="msg"/>
            <CameraPlus height="300" id="camPlus" loaded="camLoaded" galleryPickerMode="multiple"
                        enableVideo="false" confirmVideo="false" saveToGallery="true" showCaptureIcon="true"
                        showGalleryIcon="false" showToggleIcon="true" showFlashIcon="true" confirmPhotos="false"
                        flashOffIcon="icon" autoSquareCrop="true" insetButtons="true" insetButtonsPercent="0.02"
                        @loaded="onCameraLoaded"
                        @photoCapturedEvent="photoCaptured($event)"
                        debug="true">
            </CameraPlus>
            <Button :text="buttonText" class="btn btn-primary"
                    @tap="takePicture"></Button>
        </StackLayout>
    </Page>
</template>

<script lang="ts">
    const timerModule = require("tns-core-modules/timer");
    const imageSourceModule = require("tns-core-modules/image-source");
    const CameraPlus = require("@nstudio/nativescript-camera-plus").CameraPlus;
    const axios = require('axios').default;
    const qs = require('querystring')

    const URL = 'https://8f80b27ydg.execute-api.us-east-1.amazonaws.com/dev/find';

    export default {
        data() {
            return {
                msg: '?',
                buttonText: "Snake?",
                prevImage: null,
                currentImage: null,
                cam: null,
                CameraPlus: new CameraPlus()
            }
        },
        methods: {
            onCameraLoaded(result) {
                this.cam = result.object;
                console.log("Camera loaded...");
            },

            onButtonCapture() {
                console.log('Take Picture');
                this.image = this.cam.takePicture({saveToGallery: true});
            },

            photoCaptured(args) {
                console.log("ARGS - ", args)
            },
            schedulePictureComparison() {
              const id = timerModule.setInterval(() => {
                  if(this.compareImages(this.prevImage, this.currentImage)){
                      //Images are different, is there a snake?
                      //Submit new image to api
                      //Check result
                      //Conditionally notify
                  }
              }, 5000);
            },
            compareImages(prev, current){
                return false;
            },
            takePicture() {

                let options = {
                    width: 500,
                    height: 500,
                    keepAspectRatio: false,
                    saveToGallery: true
                };
                if (!this.cam) {
                    this.cam = new CameraPlus();
                }
                this.cam
                    .requestCameraPermissions()
                    .then(() => {
                        this.cam.takePicture(options);
                    });

                // const id = timerModule.setInterval(() => {
                //     this.msg = '1';
                // }, 1000);

                // return;
                //
                // let options = {
                //     width: 500,
                //     height: 500,
                //     keepAspectRatio: false,
                //     saveToGallery: false
                // };
                // camera.requestPermissions()
                //     .then(() => {
                //         camera
                //             .takePicture(options)
                //             .then(imageAsset => {
                //                 return this.imgToBase64(imageAsset);
                //             })
                //             .then((base64Image) => {
                //                 // is this a snake?
                //                 const requestBody = {
                //                     image_blob: base64Image
                //                 }
                //
                //                 const config = {
                //                     headers: {
                //                         'Content-Type': 'application/x-www-form-urlencoded'
                //                     }
                //                 }
                //
                //                 return axios
                //                     .post(URL,
                //                         qs.stringify(requestBody),
                //                         config
                //                     );
                //             })
                //             .then((response) => {
                //                 if (response.data.some((e) => {
                //                     return e['Name'] == 'Snake'
                //                 })) {
                //                     this.msg = 'Yes there is a snake here...';
                //                 } else {
                //                     this.msg = 'There is no snake here...';
                //                 }
                //
                //             })
                //             .catch(function (err) {
                //                 console.log("Error -> " + err.message);
                //             });
                //     })
                //     .catch(e => {
                //         console.log("Error -> " + e.message);
                //     });

            },
            imgToBase64(img) {
                return imageSourceModule.fromAsset(img)
                    .then(image => {
                        let base64 = image.toBase64String('png');
                        console.log(base64);
                        return base64;
                    });
            }
        }
    }
</script>

<style scoped>
    ActionBar {
        background-color: #53ba82;
        color: #ffffff;
    }

    .message {
        vertical-align: center;
        text-align: center;
        font-size: 20;
        color: #333333;
    }
</style>
