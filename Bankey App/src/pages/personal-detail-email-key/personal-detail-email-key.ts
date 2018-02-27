import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {InviteFriendsKeyPage} from "../invite-friends-key/invite-friends-key";
import {HttpClientProvider} from "../../providers/http-client/http-client";
import {CommonFunctionsProvider} from "../../providers/common-functions/common-functions";
import {SetServiceFeePage} from "../set-service-fee/set-service-fee";

/**
 * Generated class for the PersonalDetailEmailKeyPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-personal-detail-email-key',
  templateUrl: 'personal-detail-email-key.html',
})
export class PersonalDetailEmailKeyPage {
  email_id:String= "";
  addressInfo:String;
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public httpClient: HttpClientProvider,
              public commonFn: CommonFunctionsProvider ) {
  }

  ionViewDidLoad() {;
      this.addressInfo = this.navParams.get("addressInfo");
      console.log('ionViewDidLoad PersonalDetailEmailKeyPage');
  }

  Submit(){
    if(!this.email_id || this.email_id == ''){
        this.commonFn.showAlert("Please enter Email ID");
        return false;
    }
    this.navCtrl.push(SetServiceFeePage,{"emailID":this.email_id,"addressInfo":this.addressInfo});
    //this.DoSignUP();
  }
  goBack(){
      this.navCtrl.pop();
  }
}
