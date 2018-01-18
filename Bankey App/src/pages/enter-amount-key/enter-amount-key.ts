import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {PersonalDetailKeyPage} from "../personal-detail-key/personal-detail-key";
import { StripeServiceProvider } from "../../providers/stripe-service/stripe-service"
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
              public navParams: NavParams,
              public stripeService:StripeServiceProvider) {
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
    this.stripeService.createCardTokend(this.card).then((result)=>{
      console.log(result);
    },(err)=>{
      console.log(err);
    });
    this.navCtrl.push(PersonalDetailKeyPage);
  }
  goBack(){
    this.navCtrl.pop();
  }
}
