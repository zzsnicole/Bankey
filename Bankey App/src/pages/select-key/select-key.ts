import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {KeyRequestConfirmPage} from "../key-request-confirm/key-request-confirm";

/**
 * Generated class for the SelectKeyPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-select-key',
  templateUrl: 'select-key.html',
})
export class SelectKeyPage {

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad SelectKeyPage');
  }

  GoConfirmKey() {
    this.navCtrl.push(KeyRequestConfirmPage);
  }
}
