import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {EnterOtpPage} from "../enter-otp/enter-otp";
import {EnterAmountPage} from "../enter-amount/enter-amount";
import { HttpClientProvider } from "../../providers/http-client/http-client";
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
  userInfo = {
    "mobile_number": "",
    "password": "",
  }
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public httpClient: HttpClientProvider) {
  }
  enteredPasscode = '';
  firstPassword = '';
  ionViewDidLoad() {
    this.userInfo.mobile_number = localStorage.mobileNumber;
    console.log('ionViewDidLoad PasscodeLoginPage');
  }

  digit(d) {
      if(d == -1){
          this.delete();
      }else{
          this.enteredPasscode += '' + d;
      }

      if (this.enteredPasscode.length == 4) {
          this.userInfo.password = this.enteredPasscode;
          this.signIn();
      }
  }

  signIn() {
    
    this.httpClient.postService('login/',this.userInfo).then((result:any) => {
        console.log(result);
        if(result.success){
            this.navCtrl.push(EnterAmountPage);
            //localStorage.userData = result.data;
        }else{
            //replace by alert controller of ionic
            alert(result.message);
        }
    }, (err) => {
        console.log(err);
    });

  }

  delete() {
      this.enteredPasscode = this.enteredPasscode.slice(0, -1);

  }

  clear() {
      this.enteredPasscode = "";
  };
}
