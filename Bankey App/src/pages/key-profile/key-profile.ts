import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {ConfirmationCodePage} from "../confirmation-code/confirmation-code";
import {KeyRequestConfirmPage} from "../key-request-confirm/key-request-confirm";

/**
 * Generated class for the KeyProfilePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-key-profile',
  templateUrl: 'key-profile.html',
})
export class KeyProfilePage {
  ratingValue = 4;
  constructor(public navCtrl: NavController,
              public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad KeyProfilePage');
  }

  GoConfirmpage(){
    this.navCtrl.push(KeyRequestConfirmPage);
  }

  onModelChange(e){
    console.log(e);
  }
  goBack(){
      this.navCtrl.pop();
  }

}
