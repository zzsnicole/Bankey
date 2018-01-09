import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {MyAccountPage} from "../my-account/my-account";
import {TransactionReferencePage} from "../transaction-reference/transaction-reference";

/**
 * Generated class for the ConfirmationCodePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-confirmation-code',
  templateUrl: 'confirmation-code.html',
})
export class ConfirmationCodePage {
  pageTitle = "Confirmation Code";
  messageText = "Your confirmation code is";
  codeText = "A2c45694";
  constructor(public navCtrl: NavController, public navParams: NavParams) {

  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ConfirmationCodePage');
  }

  Confirm() {
          this.navCtrl.push(TransactionReferencePage);
  }
}
