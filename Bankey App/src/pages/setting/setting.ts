import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {TermsAndConditionPage} from "../terms-and-condition/terms-and-condition";
import {PrivacyPolicyPage} from "../privacy-policy/privacy-policy";
import {MobilePage} from "../mobile/mobile";
import {CommonFunctionsProvider} from "../../providers/common-functions/common-functions";
import {HttpClientProvider} from "../../providers/http-client/http-client";

/**
 * Generated class for the SettingPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-setting',
  templateUrl: 'setting.html',
})
export class SettingPage {
  KeyServiceStatus:boolean = false;
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public commonFn: CommonFunctionsProvider,
              public httpClient: HttpClientProvider) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad SettingPage');
    this.getStatusOfKeyService();
  }
  getStatusOfKeyService () {
      this.httpClient.getService("teller/activationmode/").then(
          (result:any) => {
              console.log(result);
              if(result.success){
                 this.KeyServiceStatus = result.data.activation_mode;
              }
          }
      )
  }
  updateStatusOfKeyService (){
      let displayKeyword = "ON"
      if(this.KeyServiceStatus){
          displayKeyword = "OFF"
      }
      this.commonFn.showConfirm("Turning Key Service "+displayKeyword,"Yes","No","Are you sure you want to turn Key Service"+displayKeyword+"?").then(
          (result) =>{
              if(result == "Yes"){
                  this.httpClient.putService("teller/activationmode/",{"service_activation":this.KeyServiceStatus}).then(
                      (result:any) => {
                          console.log(result);
                          if(result.success){
                              this.commonFn
                          }
                      }
                  )

              }
          }
      )
  }

  goBack(){
    this.navCtrl.pop();
  }
  ChangePage(pageName){
    switch (pageName){
        case "terms-condition":
          this.navCtrl.push(TermsAndConditionPage);
          break;
        case "privacy-policy":
          this.navCtrl.push(PrivacyPolicyPage);
          break;
    }
  }
  SignOut(){
    //do api call
      this.commonFn.showConfirm("Sign Out","Yes","No","Are you sure you want to sign out from the bankey app now?").then(
          (result) =>{
            if(result == "Yes"){
                this.httpClient.getService("logout/").then(
                    (result:any) =>{
                        if(result.success){
                            this.navCtrl.setRoot(MobilePage);
                        }
                    }
                )

            }
          }
      )

  }
}
