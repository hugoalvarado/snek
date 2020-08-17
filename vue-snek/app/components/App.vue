<template>
  <Page>
    <ActionBar title="Welcome to NativeScript-Vue Snake Detector 🐍!"/>
    <StackLayout orientation="vertical">
      <Label class="message" :text="msg"/>
      <CameraPlus height="300"
                  id="camPlus"
                  loaded="camLoaded"
                  galleryPickerMode="single"
                  enableVideo="false"
                  confirmVideo="false"
                  saveToGallery="true"
                  showCaptureIcon="false"
                  showGalleryIcon="false"
                  showToggleIcon="true"
                  showFlashIcon="true"
                  confirmPhotos="false"
                  flashOffIcon="icon"
                  autoSquareCrop="true"
                  insetButtons="false"
                  insetButtonsPercent="0.02"
                  @loaded="onCameraLoaded"
                  @photoCapturedEvent="photoCaptured"
                  @errorEvent="onCameraError">
      </CameraPlus>
      <Button :text="buttonText" class="btn btn-primary"
              @tap="takePicture"></Button>
    </StackLayout>
  </Page>
</template>

<script lang="ts">
const TimerModule = require("tns-core-modules/timer");
const ImageSource = require("tns-core-modules/image-source");
import BitmapFactory = require("nativescript-bitmap-factory");
const CameraPlus = require("@nstudio/nativescript-camera-plus").CameraPlus;
const axios = require('axios').default;
const qs = require('querystring')

const URL = 'https://8f80b27ydg.execute-api.us-east-1.amazonaws.com/dev/find';

const FIRST_IMAGE = 0;
const SECOND_IMAGE = 1;
const PICTURE_INTERVAL = 5 * 1000; // 5 seconds
const FIND_THIS = 'snake'

export default {
  data() {
    return {
      msg: '?',
      buttonText: "Snake?",
      cam: null,
      options: {
        width: 500,
        height: 500,
        keepAspectRatio: false,
        saveToGallery: false
      },
      imageIndex: 0,
      images: [null, null]
    }
  },
  mounted() {
    this.schedulePictureComparison();
  },
  methods: {
    onCameraLoaded(result) {
      this.cam = result.object;
      console.log("Camera loaded...");
    },
    onCameraError(result) {
      console.log("Camera error...");
      console.log(result);
    },
    photoCaptured(args) {
      // image  (args.data)is an imageAsset
      this.loadImage(args.data);
      console.log("Camera photoCaptured...");
    },
    loadImage(image) {
      ImageSource.fromAsset(image)
          .then(res => {
            this.images[this.imageIndex] = res;
            this.imageIndex++;
            if (this.imageIndex > 1)
              this.imageIndex = 0;
          });
    },
    schedulePictureComparison() {
      const id = TimerModule.setInterval(() => {
        this.takePicture();
        if (this.images[FIRST_IMAGE] != null && this.images[SECOND_IMAGE] != null) {

          let pixelsFromImage1 = this.pixelate(40, this.images[FIRST_IMAGE]);
          let pixelsFromImage2 = this.pixelate(40, this.images[SECOND_IMAGE]);

          if (this.compareImagePixels(pixelsFromImage1, pixelsFromImage2)) {
            //Images are different, is there a snake?
            //Submit new image to api
            //Check result
            //Conditionally notify
            console.log("Camera movement detected.");
            this.detectObject(this.images[SECOND_IMAGE]);
          } else {
            console.log("Camera no movement detected.");
          }
        }
      }, PICTURE_INTERVAL);
    },
    detectObject(image) {
      let base64Image = image.toBase64String('png');
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
          )
          .then((response) => {
            if (response.data.some((e) => {
              return e['Name'].toLowerCase == FIND_THIS
            })) {
              this.msg = 'Yes there is a snake here...';
            } else {
              this.msg = 'There is no snake here...';
            }
          })
          .catch(function (err) {
            console.log("Error -> " + err.message);
          });
    },
    pixelate(sample_size, image) {

      let pixels = [];

      let mutable = BitmapFactory.makeMutable(image);
      BitmapFactory.asBitmap(mutable).dispose((bmp) => {

        for (let y = 0; y < image.height; y += sample_size) {
          for (let x = 0; x < image.width; x += sample_size) {

            let pixel = bmp.getPoint({"x": x, "y": y});
            pixels.push(pixel);
          }
        }
      });

      return pixels;
    },
    compareImagePixels(prev, current) {
      /*
      Do simple comparison of the pixel arrays to detect movement
       */
      // threshold must be between 0 and 255
      const threshold = 20;
      for (let i = 0; i < prev.length; i++) {
        let pPixel = prev[i];
        let cPixel = current[i];
        if (
            Math.abs(pPixel.r - cPixel.r) > threshold
            || Math.abs(pPixel.g - cPixel.g) > threshold
            || Math.abs(pPixel.b - cPixel.b) > threshold
        ) {
          return true;
        }
      }
      return false;
    }
    ,
    takePicture() {
      if (!this.cam) {
        this.cam = new CameraPlus();
      }
      this.cam
          .requestCameraPermissions()
          .then(() => {
            this.cam.takePicture(this.options);
          });
    },
    imgToBase64(img) {
      return ImageSource.fromAsset(img)
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
