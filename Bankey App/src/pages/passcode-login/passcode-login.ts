import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {EnterOtpPage} from "../enter-otp/enter-otp";
import {EnterAmountPage} from "../enter-amount/enter-amount";

/**
 * Generated class for the PasscodeLoginPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-passcode-login',
  templateUrl: 'passcode-login.html',
})
export class PasscodeLoginPage {

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }
  enteredPasscode = '';
  firstPassword = '';
  ionViewDidLoad() {
    console.log('ionViewDidLoad PasscodeLoginPage');
  }

  digit(d) {
      if(d == -1){
          this.delete();
      }else{
          this.enteredPasscode += '' + d;
      }

      if (this.enteredPasscode.length == 4) {
          this.navCtrl.push(EnterAmountPage);
      }
  }

  delete() {
      this.enteredPasscode = this.enteredPasscode.slice(0, -1);

  }

  clear() {
      this.enteredPasscode = "";
  };
}
