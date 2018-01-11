import { InviteFriendsPage } from './../invite-friends/invite-friends';
import { Component } from '@angular/core';
import { NavController, NavParams, ActionSheetController, Platform } from 'ionic-angular';
import { Camera, CameraOptions } from '@ionic-native/camera';
import { HttpClientProvider } from "../../providers/http-client/http-client";
import { CommonFunctionsProvider } from "../../providers/common-functions/common-functions";
import { File } from '@ionic-native/file';
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
        "line1": null,
        "line2": null,
        "city": null,
        "state": null,
        "country": "USA",
        "pin_code": null
    }
  };
  imagePath = "";
  cameraOption: any = {
      quality: 100,
      sourceType: '',
      saveToPhotoAlbum: false,
      correctOrientation: true,
  };
  FormData:any= formdata;
  public window = window;
  constructor(  public navCtrl: NavController,
                public navParams: NavParams,
                public camera: Camera,
                public httpClient: HttpClientProvider,
                public commonFn: CommonFunctionsProvider,
                private file: File,
                public actionSheetCtrl: ActionSheetController,
                public platform: Platform) {
  }

  ionViewDidLoad() {
    this.userInfo.phone_no = localStorage.mobileNumber;
    this.userInfo.password = this.navParams.get('password_');
    console.log(this.userInfo);
    console.log('ionViewDidLoad PersonalDetailsPage');

  }

    presentActionSheet = function(type) {
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

        oFReader.onload = (event:any) => {
            this.imagePath = event.target.result;
        };
        oFReader.readAsDataURL(event.target.files[0]);
        this.FormData.append("phone_no",localStorage.mobileNumber);
        this.FormData.append("photo",event.target.files[0]);
        //this.fileUpload();
    }
    fileUpload(){
        this.httpClient.putService('uploadphoto/',this.FormData).then((result:any) => {
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

  public takePicture(sourceType) {
        // Create options for the Camera Dialog

        this.cameraOption.sourceType = sourceType;
        // Get the data of an image
        this.camera.getPicture(this.cameraOption).then((imagePath) => {
            // Special handling for Android library
            console.log(imagePath);
            if (this.platform.is('android') && sourceType === this.camera.PictureSourceType.PHOTOLIBRARY) {
                // this.filePath.resolveNativePath(imagePath)
                //     .then(filePath => {
                //         let correctPath = filePath.substr(0, filePath.lastIndexOf('/') + 1);
                //         let currentName = imagePath.substring(imagePath.lastIndexOf('/') + 1, imagePath.lastIndexOf('?'));
                //         this.copyFileToLocalDir(correctPath, currentName, this.createFileName(), type);
                //     });
            } else {
                var currentName = imagePath.substr(imagePath.lastIndexOf('/') + 1);
                var correctPath = imagePath.substr(0, imagePath.lastIndexOf('/') + 1);
                this.upload(correctPath,currentName);
            }
        }, (err) => {
            //alert('Error while selecting image.');
        });
  }
   upload(imagepath,fileName) {

       this.file.readAsArrayBuffer(imagepath,fileName).then((result)=>{
                   //console.log(imagepath);
                   // Create a blob based on the FileReader "result", which we asked to be retrieved as an ArrayBuffer
                   //var blob = new Blob([new Uint8Array(result)], { type: "image/png" });
                   var oReq = new XMLHttpRequest();
                   oReq.open("PUT", "http://54.91.82.248/api/uploadphoto/", true);
                   oReq.setRequestHeader("Content-type","form-data");
                   oReq.setRequestHeader("Authorization","Basic KzE1NzEzMzUzNjkwOjEyMzQ=");
                   // oReq.setRequestHeader("Username","+15713353690");
                   // oReq.setRequestHeader("Password","1234");
                   oReq.onload = function (result) {
                       // all done!
                        console.log(result);
                   };
                   // Pass the blob in to XHR's send method
                   oReq.send({
                       "photo":imagepath,
                       "phone_no":"+15713353690"
                   });
        },(err)=>{
            console.log(err);
        })

   }


  signUp() {

    if(this.userInfo.name == ''){
      this.commonFn.showAlert("Please enter your name!");
      return false;
    }

    this.httpClient.postService('signup/',this.userInfo).then((result:any) => {
        console.log(result);
        if(result.success){
            this.navCtrl.push(InviteFriendsPage,{"userName":result.data.name})
            localStorage.userData = result.data;
            if(this.imagePath){
                this.fileUpload();
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
