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
  addressInfo = {
    "line1": "",
    "line2": "",
    "city": "",
    "state": "",
    "country": "US",
    "pin_code": ""
  };
  userInfo:any;
  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad PersonalDetailAddressKeyPage');
  }

  Submit(){
    this.navCtrl.push(PersonalDetailEmailKeyPage,{"addressInfo":this.addressInfo});
  }

  goToEmailPage(){
    this.navCtrl.push(PersonalDetailEmailKeyPage);
  }

  goBack(){
    this.navCtrl.pop();
  }
}
