import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {InviteFriendsKeyPage} from "../invite-friends-key/invite-friends-key";
import {HttpClientProvider} from "../../providers/http-client/http-client";
import {CommonFunctionsProvider} from "../../providers/common-functions/common-functions";

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
  userInfo:any;
  addressInfo:any;
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public httpClient: HttpClientProvider,
              public commonFn: CommonFunctionsProvider ) {
  }

  ionViewDidLoad() {
      this.userInfo = this.navParams.get("userInfo");
      this.addressInfo = this.navParams.get("addressInfo");
      console.log('ionViewDidLoad PersonalDetailEmailKeyPage');
  }

  Submit(){
    if(!this.email_id || this.email_id == ''){
        this.commonFn.showAlert("Please enter Email ID");
    }
    this.DoSignUP();
  }

  DoSignUP(){
      let params = {
          "email":this.email_id,
          "name": this.userInfo.name,
          "birth_date": this.userInfo.birth_date,
          "address":this.addressInfo,
          "fee":Number(localStorage.feeValue)
      }
      console.log(params);
      this.httpClient.postService("teller/",params).then(
          (result:any) => {
            console.log(result);
            if(result.success){
                this.navCtrl.push(InviteFriendsKeyPage,{"userName":this.userInfo.name,"userListNumber":result.data.count});
            }
          },
          err => {
            console.log(err);
          });
  }
  goBack(){
      this.navCtrl.pop();
  }
}
