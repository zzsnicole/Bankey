import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {KeyProfilePage} from "../key-profile/key-profile";
import {PendingRequestPage} from "../pending-request/pending-request";
import {ConfirmationCodePage} from "../confirmation-code/confirmation-code";
import {KeyRequestConfirmPage} from "../key-request-confirm/key-request-confirm";

/**
 * Generated class for the MyAccountPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-my-account',
  templateUrl: 'my-account.html',
})
export class MyAccountPage {
  requestStatusString = "Pending request to add money from Name Surname";
  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad MyAccountPage');
    if(this.navParams.get("acceptedrequest")){
        this.requestStatusString = "Accepted request to add money from Name Surname";
    }
  }

  GoProfile(){
    this.navCtrl.push(KeyProfilePage);
  }
  goToPendingRequest(){
      if(this.navParams.get("acceptedrequest")){
          this.navCtrl.push(KeyRequestConfirmPage,{accepted:true});
      }else{
          this.navCtrl.push(PendingRequestPage);
      }

  }
}
