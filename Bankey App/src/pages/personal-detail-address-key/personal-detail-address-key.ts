import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {PersonalDetailEmailKeyPage} from "../personal-detail-email-key/personal-detail-email-key";

/**
 * Generated class for the PersonalDetailAddressKeyPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-personal-detail-address-key',
  templateUrl: 'personal-detail-address-key.html',
})
export class PersonalDetailAddressKeyPage {

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad PersonalDetailAddressKeyPage');
  }

  goToEmailPage(){
    this.navCtrl.push(PersonalDetailEmailKeyPage);
  }
}
