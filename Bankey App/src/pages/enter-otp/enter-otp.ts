import { CreatePasswordPage } from './../create-password/create-password';
import { HttpClientProvider } from "../../providers/http-client/http-client";
import { CommonFunctionsProvider } from "../../providers/common-functions/common-functions";
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
              public httpClient: HttpClientProvider,
              public commonFn: CommonFunctionsProvider) {
  }

  onKeyup(event) {
    console.log(this.otpCode.length)
    if (this.otpCode.length == 6) {

    }

  }

  ValidateOtpForMobile() {

      if(this.otpCode == ''){
          this.commonFn.showAlert("Please enter OTP!");
          return false;
      }

      var otpVerificationParams = {
          "mobile_number":localStorage.mobileNumber,
          "verification_code":Number(this.otpCode),
          "process":"signup"
      };
      this.httpClient.postService('phoneverification/',otpVerificationParams).then((result:any) => {
          console.log(result);
          if(result.success){
              this.navCtrl.push(CreatePasswordPage);
          }else{
              this.commonFn.showAlert(result.message);
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
