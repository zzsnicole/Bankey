import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {SelectKeyPage} from "../select-key/select-key";
import {KeyRequestConfirmPage} from "../key-request-confirm/key-request-confirm";
import {SendConfirmPage} from "../send-confirm/send-confirm";

/**
 * Generated class for the EnterAmountPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-enter-amount',
  templateUrl: 'enter-amount.html',
})
export class EnterAmountPage {
  enteredAmount:string ='40';
  pageTitle:string = "Add Money";
  constructor(public navCtrl: NavController, public navParams: NavParams) {
      if(this.navParams.get("send")){
          this.pageTitle = "Enter Amount"
      }
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad EnterAmountPage');
  }

  digit(d) {
      if(d == -1){
          this.delete();
      }else{
          this.enteredAmount += '' + String(d);
      }
  }

  delete() {
      this.enteredAmount = this.enteredAmount.slice(0, -1);

  }

  clear() {
      this.enteredAmount = "";
  };

  GoKeyList() {
      if(this.navParams.get("send")){
          this.navCtrl.push(SendConfirmPage,{"send":true});
      }else{
          this.navCtrl.push(SelectKeyPage);
      }
  }

}
