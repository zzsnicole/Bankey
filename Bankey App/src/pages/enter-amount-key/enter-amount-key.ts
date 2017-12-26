import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {PersonalDetailKeyPage} from "../personal-detail-key/personal-detail-key";

/**
 * Generated class for the EnterAmountKeyPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-enter-amount-key',
  templateUrl: 'enter-amount-key.html',
})
export class EnterAmountKeyPage {

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad EnterAmountKeyPage');
  }

  GoPersonalDetailKey(){
    this.navCtrl.push(PersonalDetailKeyPage);
  }
}
