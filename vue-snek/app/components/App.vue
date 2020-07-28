<template>
    <Page>
        <ActionBar title="Welcome to NativeScript-Vue!"/>
        <GridLayout columns="*" rows="*">
            <Label class="message" :text="msg" col="0" row="0"/>
            <Button :text="buttonText" class="btn btn-primary" marginTop="20"
                    @tap="takePicture"></Button>
        </GridLayout>
    </Page>
</template>

<script lang="ts">
    const camera = require("nativescript-camera");
    const axios = require('axios').default;
    const qs = require('querystring')
    const imageSourceModule = require("tns-core-modules/image-source");

    const URL = 'https://8f80b27ydg.execute-api.us-east-1.amazonaws.com/dev/find';

    export default {
        data() {
            return {
                msg: 'Hello Hugo!',
                buttonText: "Snake?",
                picture: null
            }
        },
        methods: {
            takePicture() {
                let options = {
                    width: 300,
                    height: 300,
                    keepAspectRatio: false,
                    saveToGallery: true
                };
                camera.requestPermissions()
                    .then(() => {
                        camera
                            .takePicture(options)
                            .then(imageAsset => {
                                return this.imgToBase64(imageAsset);
                            })
                            .then((base64Image) => {
                                // is this a snake?
                                const requestBody = {
                                    image_blob: base64Image
                                }

                                const config = {
                                    headers: {
                                        'Content-Type': 'application/x-www-form-urlencoded'
                                    }
                                }

                                return axios
                                    .post(URL,
                                        qs.stringify(requestBody),
                                        config
                                    );
                            })
                            .catch(function (err) {
                                console.log("Error -> " + err.message);
                            });
                    })
                    .catch(e => {
                        console.log("Error -> " + e.message);
                    });

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
