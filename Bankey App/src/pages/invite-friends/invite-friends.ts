import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { SocialSharing } from '@ionic-native/social-sharing';
import {CreatePasswordPage} from "../create-password/create-password";
import {CallTellerPage} from "../call-teller/call-teller";

/**
 * Generated class for the InviteFriendsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-invite-friends',
  templateUrl: 'invite-friends.html',
})
export class InviteFriendsPage {

  options = {
    message: 'share this', // not supported on some apps (Facebook, Instagram)
    subject: 'the subject', // fi. for email
    files: ['', ''], // an array of filenames either locally or remotely
    url: 'https://www.website.com/foo/#bar?a=b',
    chooserTitle: 'Pick an app' // Android only, you can override the default share sheet title
  }

  constructor(public navCtrl: NavController, public navParams: NavParams, public socialSharing: SocialSharing) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad InviteFriendsPage');
  }

  openSharing() {
    console.log(this.socialSharing)
    this.socialSharing.shareWithOptions(this.options).then(() => {
      // Sharing via email is possible
      console.log('ok')
    }).catch(() => {
      // Sharing via email is not possible
      console.log('not ok');
      //this.navCtrl.push(PostSharePage)
      
    });

  }

  goKeyUserSliderPage() {
      this.navCtrl.push(CallTellerPage);
  }

}