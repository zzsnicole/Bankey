import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {PersonalDetailKeyPage} from "../personal-detail-key/personal-detail-key";
import {InviteFriendsKeyPage} from "../invite-friends-key/invite-friends-key";
import {HttpClientProvider} from "../../providers/http-client/http-client";
import {SettingPage} from "../setting/setting";
import {CommonFunctionsProvider} from "../../providers/common-functions/common-functions";
import {MobilePage} from "../mobile/mobile";

/**
 * Generated class for the SetServiceFeePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-set-service-fee',
  templateUrl: 'set-service-fee.html',
})
export class SetServiceFeePage {
  feeValue = 2;
  numberBtnValue = 2;
  addressInfo:any;
  emailID:String;
  constructor(public navCtrl: NavController,
              public commonFn: CommonFunctionsProvider,
              public httpClient: HttpClientProvider,
              public navParams: NavParams) {
  }

  ionViewDidLoad() {
    this.emailID = this.navParams.get("emailID");
    this.addressInfo = this.navParams.get("addressInfo")
    console.log('ionViewDidLoad SetServiceFeePage');
  }

  GoPersonDetail() {
    localStorage.feeValue = this.feeValue.toFixed(2);
    this.doSignUP();
    //this.navCtrl.push(InviteFriendsKeyPage,{"userListNumber":result.data.count});
  }

  addFee(){
    this.feeValue += 0.10;
  }
  minusFee(){
    this.feeValue -= 0.10;
  }

  doSignUP(){
      let params = {
          "email":this.emailID,
          "address":this.addressInfo,
          "fee":Number(localStorage.feeValue)
      }
      console.log(params);
      this.httpClient.postService("teller/",params).then(
          (result:any) => {
              console.log(result);
              if(result.success){
                  this.commonFn.showConfirm("Add Balance","Later","yes","You do not have enough balance to activate key service. you need minimum $100 in your wallet. Do you want to add balance?").then(
                      (result) =>{
                          if(result == "Later"){
                              this.navCtrl.remove(2,3);
                              this.navCtrl.pop();
                          }
                      }
                  )
              }
          },
          err => {
              console.log(err);
          });
  }
  goBack(){
    this.navCtrl.pop();
  }
  numberBtn(index){
    console.log("you clicked button"+index);
    this.numberBtnValue = index;
    this.feeValue = index;
  }
}
