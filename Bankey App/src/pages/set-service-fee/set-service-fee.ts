import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {PersonalDetailKeyPage} from "../personal-detail-key/personal-detail-key";

/**
 * Generated class for the SetServiceFeePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-set-service-fee',
  templateUrl: 'set-service-fee.html',
})
export class SetServiceFeePage {
  feeValue = 2;
  numberBtnValue = 2;
  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad SetServiceFeePage');
  }

  GoPersonDetail() {
    localStorage.feeValue = this.feeValue.toFixed(2);
    this.navCtrl.push(PersonalDetailKeyPage);
  }

  addFee(){
    this.feeValue += 0.10;
  }
  minusFee(){
    this.feeValue -= 0.10;
  }

  goBack(){
    this.navCtrl.pop();
  }
  numberBtn(index){
    console.log("you clicked button"+index);
    this.numberBtnValue = index;
    this.feeValue = index;
  }
}
