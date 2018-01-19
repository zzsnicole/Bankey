import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {PersonalDetailKeyPage} from "../personal-detail-key/personal-detail-key";
import {SetServiceFeePage} from "../set-service-fee/set-service-fee";
/**
 * Generated class for the EnterAmountKeyPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-enter-amount-key',
  templateUrl: 'enter-amount-key.html',
})
export class EnterAmountKeyPage {
  ExpiryDate:any;
  card = {
   number: '',
   expMonth:"",
   expYear:"",
   cvc: ''
  };
  constructor(public navCtrl: NavController,
              public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad EnterAmountKeyPage');
  }

  GoPersonalDetailKey(){
    console.log(this.ExpiryDate);
    if(this.ExpiryDate){
      this.card["expMonth"] = this.ExpiryDate.split("-")[1];
      this.card["expYear"] = this.ExpiryDate.split("-")[0];
    }
    this.navCtrl.push(SetServiceFeePage);
  }
  goBack(){
    this.navCtrl.pop();
  }
}
