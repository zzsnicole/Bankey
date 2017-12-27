import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {MyAccountPage} from "../my-account/my-account";

/**
 * Generated class for the ConfirmationCodePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-confirmation-code',
  templateUrl: 'confirmation-code.html',
})
export class ConfirmationCodePage {

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ConfirmationCodePage');
  }

  Confirm() {
    this.navCtrl.push(MyAccountPage);
  }
}
