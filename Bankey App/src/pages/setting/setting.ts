import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {TermsAndConditionPage} from "../terms-and-condition/terms-and-condition";
import {PrivacyPolicyPage} from "../privacy-policy/privacy-policy";
import {MobilePage} from "../mobile/mobile";
import {CommonFunctionsProvider} from "../../providers/common-functions/common-functions";
import {HttpClientProvider} from "../../providers/http-client/http-client";
import {HomeKeyPage} from "../home-key/home-key";
import {EditProfilePage} from "../edit-profile/edit-profile";
import {SocialSharing} from "@ionic-native/social-sharing";

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
  userName:any = "Achraf Alobaid";
  oldKeyServiceStatus:boolean = false;
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public commonFn: CommonFunctionsProvider,
              public httpClient: HttpClientProvider,
              public socialSharing: SocialSharing) {
      //this.userName = JSON.parse(localStorage.userObject).name;
  }
  options = {
    message: 'share this', // not supported on some apps (Facebook, Instagram)
    subject: 'the subject', // fi. for email
    files: ['', ''], // an array of filenames either locally or remotely
    url: 'https://www.website.com/foo/#bar?a=b',
    chooserTitle: 'Pick an app' // Android only, you can override the default share sheet title
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
                 this.oldKeyServiceStatus = result.data.activation_mode;
              }
          }
      )
  }

  updateStatusOfKeyService (ctl, oldValue){
      if(this.oldKeyServiceStatus == this.KeyServiceStatus){
          return;
      }
      let displayKeyword = "ON"
      if(!this.KeyServiceStatus){
          displayKeyword = "OFF"
      }
      this.commonFn.showConfirm("Turning Key Service "+displayKeyword,"Yes","No","Are you sure you want to turn Key Service"+displayKeyword+"?").then(
          (result) =>{
              if(result == "Yes"){
                  this.httpClient.putService("teller/activationmode/",{"service_activation":this.KeyServiceStatus}).then(
                      (result:any) => {
                          console.log(result);
                          if(result.success){
                              this.commonFn.showAlert("Key service turned "+displayKeyword);
                              this.oldKeyServiceStatus = this.KeyServiceStatus;
                          }
                      }
                  )

              }else{
                  this.KeyServiceStatus = !this.KeyServiceStatus;
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
        case "become-key":
            this.navCtrl.push(HomeKeyPage);
            break;
        case "edit-profile":
            this.navCtrl.push(EditProfilePage);
            break;
    }
  }

    openSharing() {
        console.log(this.socialSharing)
        this.socialSharing.shareWithOptions(this.options).then(() => {
            // Sharing via email is possible
            console.log("Share done");

        }).catch(() => {
            // Sharing via email is not possible
            console.log('not ok');
            //this.navCtrl.push(PostSharePage)

        });

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
                            localStorage.clear();
                        }
                    }
                )

            }
          }
      )

  }
}
