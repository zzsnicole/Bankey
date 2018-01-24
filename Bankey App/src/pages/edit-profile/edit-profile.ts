import { Component } from '@angular/core';
import {ActionSheetController, IonicPage, NavController, NavParams, Platform} from 'ionic-angular';
import { Camera, CameraOptions } from '@ionic-native/camera';
import {HttpClientProvider} from "../../providers/http-client/http-client";
import {File} from "@ionic-native/file";
import {CommonFunctionsProvider} from "../../providers/common-functions/common-functions";
import {DomSanitizer} from '@angular/platform-browser';
/**
 * Generated class for the EditProfilePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-edit-profile',
  templateUrl: 'edit-profile.html',
})
export class EditProfilePage {
    headerLabel = 'Your personal details';
    userInfo = {
        "name":"",
        "email": "",
        "line1": "",
        "line2": "",
        "birth_date": "",
        "country":"US"
    };
    userPostObj:any;
    imagePath = "";
    CameraParams:any;
    cameraOption: any = {
        quality: 20,
        sourceType: '',
        saveToPhotoAlbum: false,
        correctOrientation: true,
        destinationType: this.camera.DestinationType.DATA_URL,
        encodingType: this.camera.EncodingType.JPEG,
        mediaType: this.camera.MediaType.PICTURE,
    };
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public camera: Camera,
              public httpClient: HttpClientProvider,
              public commonFn: CommonFunctionsProvider,
              private file: File,
              public actionSheetCtrl: ActionSheetController,
              public platform: Platform,
              public _DomSanitizer: DomSanitizer){
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad EditProfilePage');
    this.getUserInfo();
  }
  getUserInfo(){
    this.httpClient.getService("userdetails/"+JSON.parse(localStorage.userObject).user_id+"/").then(
        result => {
          console.log(result);
            this.userPostObj = result;
            this.userInfo.email = this.userPostObj.email;
            this.userInfo.name = this.userPostObj.name;
            this.userInfo.birth_date = this.userPostObj.birth_date;
            this.userInfo.line1 = this.userPostObj.address.line1;
            this.userInfo.line2 = this.userPostObj.address.line2;
            this.imagePath =  this.userPostObj.photo;
        },
        err => {
          console.log(err);
        }
    )
  }
    UpdateUser(){
        if(this.userInfo.name == ''){
          this.commonFn.showAlert("Please enter name.");
          return false;
        }
        if(this.userInfo.email == ''){
            this.commonFn.showAlert("Please enter email.");
            return false;
        }
        if(this.userInfo.birth_date == ''){
            this.commonFn.showAlert("Please enter birth date.");
            return false;
        }

        this.userPostObj.email = this.userInfo.email;
        this.userPostObj.name = this.userInfo.name;
        this.userPostObj.birth_date = this.userInfo.birth_date;
        this.userPostObj.address.line1 = this.userInfo.line1;
        this.userPostObj.address.line2 = this.userInfo.line2;
        this.userPostObj.address.country = this.userInfo.country;
        delete(this.userPostObj.photo);
        this.httpClient.putService("userdetails/"+JSON.parse(localStorage.userObject).user_id+"/",this.userPostObj).then(
        result => {
            console.log(result);
        },
        err => {
            console.log(err);
        }
        );
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
                this.fileUpload(this.CameraParams);
                //file:///Users/webwerks/Library/Developer/CoreSimulator/Devices/9353B417-E8E3-4784-AEB9-68D35EA71781/data/Containers/Data/Application/B687241E-3386-404E-ABFD-09B09B22BB6A/tmp/cdv_photo_005.jpg

                // var currentName = imagePath.substr(imagePath.lastIndexOf('/') + 1);
                // var correctPath = imagePath.substr(0, imagePath.lastIndexOf('/') + 1);
                // this.upload(correctPath,currentName);

            }
        }, (err) => {
            //alert('Error while selecting image.');
        });
    }

    fileUpload(params){
        this.httpClient.putService('uploadphoto/',JSON.stringify(params)).then((result:any) => {
            console.log(result);
            if(result.success){
                localStorage.imageData = this.imagePath;
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
