import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {ConfirmationCodePage} from "../confirmation-code/confirmation-code";
import {MyAccountPage} from "../my-account/my-account";

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
    if(this.navParams.get("accepted")){
        this.navCtrl.push(ConfirmationCodePage);
    }else{
        this.navCtrl.push(MyAccountPage);
    }

  }

  goBack(){
      this.navCtrl.pop();
  }
}
