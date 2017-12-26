import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {InviteFriendsPage} from "../invite-friends/invite-friends";
import {Camera, CameraOptions} from "@ionic-native/camera";
import {PersonalDetailAddressKeyPage} from "../personal-detail-address-key/personal-detail-address-key";

/**
 * Generated class for the PersonalDetailKeyPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-personal-detail-key',
  templateUrl: 'personal-detail-key.html',
})
export class PersonalDetailKeyPage {

    headerLabel = 'Your personal details';

    constructor(public navCtrl: NavController, public navParams: NavParams, public camera: Camera) {
    }

    ionViewDidLoad() {
        console.log('ionViewDidLoad PersonalDetailKey Page');
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

    goToAddressPage() {
        this.navCtrl.push(PersonalDetailAddressKeyPage);
    }

    goBack(){
        this.navCtrl.pop();
    }

}
