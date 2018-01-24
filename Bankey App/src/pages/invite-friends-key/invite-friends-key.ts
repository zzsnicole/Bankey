import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {PasscodeLoginPage} from "../passcode-login/passcode-login";
import {MyAccountPage} from "../my-account/my-account";

/**
 * Generated class for the InviteFriendsKeyPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-invite-friends-key',
  templateUrl: 'invite-friends-key.html',
})
export class InviteFriendsKeyPage {
  userName:any;
  userListNumber:any;
  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    this.userName = this.navParams.get("userName");
      this.userListNumber = this.navParams.get("userListNumber");
    console.log('ionViewDidLoad InviteFriendsKeyPage');
  }

  goLogin(){
    this.navCtrl.push(PasscodeLoginPage);
  }

  goMyAccount(){
    this.navCtrl.push(PasscodeLoginPage);
  }
}
