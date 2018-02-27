import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {EnterOtpPage} from "../enter-otp/enter-otp";
import {EnterAmountPage} from "../enter-amount/enter-amount";
import { HttpClientProvider } from "../../providers/http-client/http-client";
import {SettingPage} from "../setting/setting";
import {CommonFunctionsProvider} from "../../providers/common-functions/common-functions";
import {MobilePage} from "../mobile/mobile";
import {MyAccountPage} from "../my-account/my-account";
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
  userName:any = '';
  profilePic:any = '';
  userInfo = {
    "mobile_number": "",
    "password": "",
  }
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public httpClient: HttpClientProvider,
              public commanFn: CommonFunctionsProvider) {
  }
  enteredPasscode = '';
  firstPassword = '';
  ionViewDidLoad() {
    this.userInfo.mobile_number = localStorage.mobileNumber;
    this.userName = this.navParams.get("userName");
    this.profilePic = this.navParams.get("profilePic");
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
            this.navCtrl.setRoot(MyAccountPage);
            localStorage.userObject = JSON.stringify(result.data);
            //localStorage.userData = result.data;
        }else{
            //replace by alert controller of ionic
            this.commanFn.showAlert(result.message);
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

  GoSettingPage(){
    //  this.navCtrl.push(SettingPage);
  }

  ResetPass() {
      this.commanFn.showConfirm('Reset Password',"Yes","No","Are you sure you want to reset password.").then(
          result =>{
              if(result == "Yes"){
                  this.httpClient.postService("forgotpasswordrequest/",{"mobile_number":this.userInfo.mobile_number}).then(
                      (result:any) =>{
                          console.log(result);
                          if(result.success){
                              this.navCtrl.push(EnterOtpPage,{"pass_change":true});
                          }
                      }
                  )
              }
          }
      )
  }
}
