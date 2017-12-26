import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {HomeKeyPage} from "../home-key/home-key";

/**
 * Generated class for the CallTellerPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-call-teller',
  templateUrl: 'call-teller.html',
})
export class CallTellerPage {

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad CallTellerPage');
  }

  GoPageKeyHome(){
      this.navCtrl.push(HomeKeyPage);
  }

}
