import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {InviteFriendsKeyPage} from "../invite-friends-key/invite-friends-key";

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

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad PersonalDetailEmailKeyPage');
  }

  goInviteFriends(){
    this.navCtrl.push(InviteFriendsKeyPage);
  }

}
