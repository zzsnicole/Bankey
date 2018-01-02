import { InviteFriendsPage } from './../invite-friends/invite-friends';
import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { Camera, CameraOptions } from '@ionic-native/camera';
import { HttpClientProvider } from "../../providers/http-client/http-client";
import { FileTransfer, FileUploadOptions, FileTransferObject } from '@ionic-native/file-transfer';
import { File } from '@ionic-native/file';
/**
 * Generated class for the PersonalDetailsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */


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
  }
  constructor(  public navCtrl: NavController,
                public navParams: NavParams,
                public camera: Camera,
                public httpClient: HttpClientProvider,
                private transfer: FileTransfer,
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
  const fileTransfer: FileTransferObject = this.transfer.create();

  let options: FileUploadOptions = {
     fileKey: 'file',
     fileName: 'name.jpg',
     headers: {}
  }

  fileTransfer.upload('<file path>', '<api endpoint>', options)
   .then((data) => {
     // success
   }, (err) => {
     // error
   })
  }


  signUp() {

    if(this.userInfo.name == ''){
     //replace by alert controller of ionic
      alert("pelase enter valid name!")
    }

    this.httpClient.postService('signup/',this.userInfo).then((result:any) => {
        console.log(result);
        if(result.success){
            this.navCtrl.push(InviteFriendsPage)
            localStorage.userData = result.data;
        }else{
            //replace by alert controller of ionic
            alert(result.message);
        }
    }, (err) => {
        console.log(err);
    });

  }

  goBack(){
      this.navCtrl.pop();
  }
}
