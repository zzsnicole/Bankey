import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {MobilePage} from "../mobile/mobile";
import {EnterAmountKeyPage} from "../enter-amount-key/enter-amount-key";
import {PersonalDetailAddressKeyPage} from "../personal-detail-address-key/personal-detail-address-key";

/**
 * Generated class for the HomeKeyPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-home-key',
  templateUrl: 'home-key.html',
})
export class HomeKeyPage {

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad HomeKeyPage');
  }

  public slides = [
      {
          title: "Create Key Profile",
          description: "To become a key, safely link your bank account to the Bankey app and set up your fee",
          image: "assets/img/key-swipe-1.png",
      },
      {
          title: "Help friends and family",
          description: "Receive notification request from unbanked users and decide which transaction you want to pursue ",
          image: "assets/img/key-swipe-2.png",
      },
      {
          title: "Make extra money",
          description: "Accept the request and schedule a meet-up directly by texting or calling the user",
          image: "assets/img/key-swipe-3.png",
      }
  ];

  public goToNextPage(){
      this.navCtrl.push(PersonalDetailAddressKeyPage);
  }
  public goBack(){
      this.navCtrl.pop();
  }
}
