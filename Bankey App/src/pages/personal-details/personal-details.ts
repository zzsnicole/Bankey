import { InviteFriendsPage } from './../invite-friends/invite-friends';
import { Component } from '@angular/core';
import { NavController, NavParams, ActionSheetController, Platform, normalizeURL } from 'ionic-angular';
import { Camera, CameraOptions } from '@ionic-native/camera';
import { HttpClientProvider } from "../../providers/http-client/http-client";
import { CommonFunctionsProvider } from "../../providers/common-functions/common-functions";
import { File } from '@ionic-native/file';
import {DomSanitizer} from '@angular/platform-browser';
/**
 * Generated class for the PersonalDetailsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var formdata = new FormData();
@Component({
  selector: 'page-personal-details',
  templateUrl: 'personal-details.html',
})



export class PersonalDetailsPage {

  headerLabel = 'Your personal details';
  userInfo = {
    "phone_no": "",
    "password": "",
    "name": "",
    "address": {
        "country": "US",
    }
  };
  imagePath = "";
  cameraOption: any = {
      quality: 20,
      sourceType: '',
      saveToPhotoAlbum: false,
      correctOrientation: true,
      destinationType: this.platform.is('ios') ? this.camera.DestinationType.DATA_URL : this.camera.DestinationType.DATA_URL,
      encodingType: this.camera.EncodingType.JPEG,
      mediaType: this.camera.MediaType.PICTURE,
  };
  CameraParams:any;
  public window = window;
  constructor(  public navCtrl: NavController,
                public navParams: NavParams,
                public camera: Camera,
                public httpClient: HttpClientProvider,
                public commonFn: CommonFunctionsProvider,
                private file: File,
                public actionSheetCtrl: ActionSheetController,
                public platform: Platform,
                public _DomSanitizer: DomSanitizer) {
  }

  ionViewDidLoad() {
    this.userInfo.phone_no = localStorage.mobileNumber;
    this.userInfo.password = this.navParams.get('password_');
    console.log(this.userInfo);
    console.log('ionViewDidLoad PersonalDetailsPage');

  }

    presentActionSheet = function() {
        let actionSheet = this.actionSheetCtrl.create({
            title: 'Select Image Source',
            buttons: [{
                text: 'Load from Library',
                handler: () => {
                    this.takePicture(this.camera.PictureSourceType.PHOTOLIBRARY);
                }
            }, {
                text: 'Use Camera',
                handler: () => {
                    this.takePicture(this.camera.PictureSourceType.CAMERA);
                }
            }, {
                text: 'Cancel',
                role: 'cancel'
            }]
        });
        actionSheet.present();
    };

    fileSelect(event) {
        console.log(event);
        console.log(event.target.files[0]);
        // this.file.readAsDataURL(event.target.files[0],).then((result)=>{
        //     console.log(result);
        // })
        var oFReader = new FileReader();
        var params ={
            "phone_no":localStorage.mobileNumber,
            "imagePath":''
        }
        oFReader.onload = (event:any) => {
            this.imagePath = event.target.result;
            params.imagePath = event.target.result.replace(/^data:image\/[a-z]+;base64,/, "");
            this.fileUpload(params);
        };
        oFReader.readAsDataURL(event.target.files[0]);
        // this.FormData.append("phone_no",localStorage.mobileNumber);
        // this.FormData.append("photo",event.target.files[0].name);


    }
    fileUpload(params){
        this.httpClient.putService('uploadphoto/',JSON.stringify(params)).then((result:any) => {
            console.log(result);
            if(result.success){
                localStorage.imageData = this.imagePath;
                this.navCtrl.push(InviteFriendsPage);
            }else{
                this.commonFn.showAlert(result.message);
            }
        }, (err) => {
            console.log(err);
        });
    }

  public takePicture(sourceType) {
        // Create options for the Camera Dialog

        this.cameraOption.sourceType = sourceType;
        // Get the data of an image
        this.camera.getPicture(this.cameraOption).then((imagePath) => {
            // Special handling for Android library
            //console.log(imagePath);

            if (this.platform.is('android') && sourceType === this.camera.PictureSourceType.PHOTOLIBRARY) {
                // this.filePath.resolveNativePath(imagePath)
                //     .then(filePath => {
                //         let correctPath = filePath.substr(0, filePath.lastIndexOf('/') + 1);
                //         let currentName = imagePath.substring(imagePath.lastIndexOf('/') + 1, imagePath.lastIndexOf('?'));
                //         this.copyFileToLocalDir(correctPath, currentName, this.createFileName(), type);
                //     });
                let base64Image = 'data:image/jpeg;base64,' + imagePath;
                this.imagePath = base64Image;
                this.CameraParams = {
                    "phone_no":"+15713353690",
                    "photo":imagePath
                }
            } else {

                let base64Image = 'data:image/jpeg;base64,' + imagePath;
                this.imagePath = base64Image;
                this.CameraParams = {
                    "phone_no":"+15713353690",
                    "photo":imagePath
                }
                //this.fileUpload(this.CameraParams);
                //file:///Users/webwerks/Library/Developer/CoreSimulator/Devices/9353B417-E8E3-4784-AEB9-68D35EA71781/data/Containers/Data/Application/B687241E-3386-404E-ABFD-09B09B22BB6A/tmp/cdv_photo_005.jpg

                // var currentName = imagePath.substr(imagePath.lastIndexOf('/') + 1);
                // var correctPath = imagePath.substr(0, imagePath.lastIndexOf('/') + 1);
                // this.upload(correctPath,currentName);

            }
        }, (err) => {
            //alert('Error while selecting image.');
        });
  }
   // upload(imagepath,fileName) {
   //
   //     this.file.readAsArrayBuffer(imagepath,fileName).then((result)=>{
   //
   //
   //         this.FormData.append("phone_no",localStorage.mobileNumber);
   //
   //                 //console.log(imagepath);
   //                 // Create a blob based on the FileReader "result", which we asked to be retrieved as an ArrayBuffer
   //                 var blob = new Blob([new Uint8Array(result)], { type: "image/png" });
   //                 this.FormData.append("photo",blob);
   //
   //                 var oReq = new XMLHttpRequest();
   //                 oReq.open("PUT", "http://54.91.82.248/api/uploadphoto/", true);
   //                 oReq.setRequestHeader("Content-type","multipart/form-data");
   //                 oReq.onload = function (result) {
   //                     // all done!
   //                      console.log(result);
   //                 };
   //                 // Pass the blob in to XHR's send method
   //                 oReq.send(this.FormData);
   //      },(err)=>{
   //          console.log(err);
   //      })
   //
   // }


  signUp() {

    if(this.userInfo.name == ''){
      this.commonFn.showAlert("Please enter your name!");
      return false;
    }

    this.httpClient.postService('signup/',this.userInfo).then((result:any) => {
        console.log(result);
        if(result.success){
            this.navCtrl.push(InviteFriendsPage,{"userName":result.data.name,"userCount":result.data.count})
            //localStorage.userData = result.data;
            localStorage.userObject = JSON.stringify(result.data);
            if(this.imagePath){
                this.fileUpload(this.CameraParams);
            }

        }else{
            this.commonFn.showAlert(result.message);
        }
    }, (err) => {
        console.log(err);
    });

  }

  goBack(){
      this.navCtrl.pop();
  }
}
