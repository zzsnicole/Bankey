import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {ConfirmationCodePage} from "../confirmation-code/confirmation-code";

/**
 * Generated class for the KeyRequestConfirmPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-key-request-confirm',
  templateUrl: 'key-request-confirm.html',
})
export class KeyRequestConfirmPage {

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad KeyRequestConfirmPage');
  }

  Confirm() {
    this.navCtrl.push(ConfirmationCodePage);
  }
}
