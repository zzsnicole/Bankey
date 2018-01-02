import { CreatePasswordPage } from './../create-password/create-password';
import { HttpClientProvider } from "../../providers/http-client/http-client";

import {
  Component, ViewChild
  , ElementRef
} from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';

/**
 * Generated class for the EnterOtpPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-enter-otp',
  templateUrl: 'enter-otp.html',
})
export class EnterOtpPage {

  headerLabel = 'Enter the 6-digit code';
  otpCode = '';

  @ViewChild('input') input: ElementRef;
  @ViewChild('inputHidden') inputHidden: ElementRef;

  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public httpClient: HttpClientProvider) {
  }

  onKeyup(event) {
    console.log(this.otpCode.length)
    if (this.otpCode.length == 6) {
      // console.log('666')
      // debugger
      // if(this.inputHidden){
      //   this.inputHidden.nativeElement.focus();
      // }

      // var e = new Event('blur')
      // this.input.nativeElement.dispatchEvent(e);
    }

  }

  ValidateOtpForMobile() {

      if(this.otpCode = ''){
          //replace by alert controller of ionic
          alert("pelase enter OTP!")
      }

      var otpVerificationParams = {
          "mobile_number":localStorage.mobileNumber,
          "verification_code":this.otpCode
      };
      this.httpClient.postService('verificationrequest/',otpVerificationParams).then((result:any) => {
          console.log(result);
          if(result.success){
              this.navCtrl.push(CreatePasswordPage);
          }else{
              //replace by alert controller of ionic
              alert(result.message);
          }
      }, (err) => {
          console.log(err);
      });

  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad EnterOtpPage');
  }

  goBack(){
    this.navCtrl.pop();
  }

}
