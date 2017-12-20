import { InviteFriendsPage } from './../invite-friends/invite-friends';
import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { Camera, CameraOptions } from '@ionic-native/camera';

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

  constructor(public navCtrl: NavController, public navParams: NavParams, public camera: Camera) {
  }

  ionViewDidLoad() {
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

  goToNextPage() {
    this.navCtrl.push(InviteFriendsPage)
  }

}
