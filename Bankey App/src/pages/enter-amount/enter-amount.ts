import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {SelectKeyPage} from "../select-key/select-key";

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
  constructor(public navCtrl: NavController, public navParams: NavParams) {
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
      this.navCtrl.push(SelectKeyPage);
  }

}
