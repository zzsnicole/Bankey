import { EnterOtpPage } from './../enter-otp/enter-otp';
import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { CountryCode } from "./CountryCode";
import { SelectSearchable } from '../../components/select-searchable/select-searchable';
import { HttpClientProvider } from "../../providers/http-client/http-client";
import { PasscodeLoginPage } from "./../passcode-login/passcode-login";
import { CommonFunctionsProvider } from "../../providers/common-functions/common-functions";
/**
 * Generated class for the MobilePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-mobile',
  templateUrl: 'mobile.html',
})
export class MobilePage {
  countryList:any;
  selectedCountry: any = '';
  mobileNumber: any = '';
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public httpClient: HttpClientProvider,
              public commonFn: CommonFunctionsProvider) {
    //this.countryList = new CountryCode().allCountries;
    console.log(this.countryList);
  }

  countryChange(event: { component: SelectSearchable, value: any }) {
      console.log('value:', event.value);
      this.selectedCountry = event.value;
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad MobilePage');
    this.getCountry();
  }

  getCountry(){
    this.httpClient.getService('listcountries/').then((result:any) => {
        console.log(result);
        if(result.success){
            this.countryList = result.data;
        }
    }, (err) => {
        console.log(err);
    });
  }

  GetOtpForMobile() {

    if(this.selectedCountry == ''){
      this.commonFn.showAlert('Pelase select country!');
      return false;
    }
    else if(this.mobileNumber == ''){
      this.commonFn.showAlert('Pelase enter valid mobile number!');
      return false;
    }
    var mobile_number = String(this.selectedCountry.std_code) + String(this.mobileNumber);

    console.log(this.mobileNumber);

    var otpRequestParams = {
        "mobile_number": mobile_number
    };
    this.httpClient.postService('verificationrequest/',otpRequestParams).then((result:any) => {
        console.log(result);
        if(result.success){
            this.navCtrl.push(EnterOtpPage);
            localStorage.mobileNumber = otpRequestParams.mobile_number;
        }else{
            //replace by alert controller of ionic
            if(result.message == "User Exist."){
                this.navCtrl.push(PasscodeLoginPage,{"userName":"","profilePic":""});
            }else{                
                this.commonFn.showAlert(result.message);
            }
        }
    }, (err) => {
        console.log(err);
    });

  }

  typeaheadOnSelect($event) {
    this.selectedCountry = $event.item;
  }
}
