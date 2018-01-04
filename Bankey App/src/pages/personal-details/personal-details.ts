import { InviteFriendsPage } from './../invite-friends/invite-friends';
import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
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

function _window() : any {
    // return the global native browser window object
    return window;
}

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
    "country": "USA"
    }
  };
  public window = window;
  constructor(  public navCtrl: NavController,
                public navParams: NavParams,
                public camera: Camera,
                public httpClient: HttpClientProvider,
                public commonFn: CommonFunctionsProvider,
                private file: File) {
  }

  ionViewDidLoad() {
    this.userInfo.phone_no = localStorage.mobileNumber;
    this.userInfo.password = this.navParams.get('password_');
    console.log(this.userInfo);
    console.log('ionViewDidLoad PersonalDetailsPage');

  }

  options: CameraOptions = {
    quality: 100,
    destinationType: this.camera.DestinationType.DATA_URL,
    encodingType: this.camera.EncodingType.JPEG,
    mediaType: this.camera.MediaType.PICTURE
  }
  base64Image = ''

  openCamera() {
    this.camera.getPicture(this.options).then((imageData) => {

      // imageData is either a base64 encoded string or a file URI
      // If it's base64:
      this.base64Image = 'data:image/jpeg;base64,' + imageData;
    }, (err) => {
      // Handle error
    });
  }
   upload() {
       // _window().requestFileSystem(LocalFileSystem.PERSISTENT, 0, function (fs) {
       //     console.log('file system open: ' + fs.name);
       //     fs.root.getFile('bot.png', { create: true, exclusive: false }, function (fileEntry) {
       //         fileEntry.file(function (file) {
       //             var reader = new FileReader();
       //             reader.onloadend = function() {
       //                 // Create a blob based on the FileReader "result", which we asked to be retrieved as an ArrayBuffer
       //                 var blob = new Blob([new Uint8Array(this.result)], { type: "image/png" });
       //                 var oReq = new XMLHttpRequest();
       //                 oReq.open("POST", "http://mysweeturl.com/upload_handler", true);
       //                 oReq.onload = function (oEvent) {
       //                     // all done!
       //                 };
       //                 // Pass the blob in to XHR's send method
       //                 oReq.send(blob);
       //             };
       //             // Read the file as an ArrayBuffer
       //             reader.readAsArrayBuffer(file);
       //         }, function (err) { console.error('error getting fileentry file!' + err); });
       //     }, function (err) { console.error('error getting file! ' + err); });
       // }, function (err) { console.error('error getting persistent fs! ' + err); });
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
