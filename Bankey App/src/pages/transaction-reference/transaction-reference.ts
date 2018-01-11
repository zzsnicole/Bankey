import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, PopoverController } from 'ionic-angular';
import { RateKeyPopoverPage} from "../../pages/rate-key-popover/rate-key-popover"
/**
 * Generated class for the TransactionReferencePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-transaction-reference',
  templateUrl: 'transaction-reference.html',
})
export class TransactionReferencePage {

  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public popoverCtrl: PopoverController) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad TransactionReferencePage');
  }
  ShowRating(){
    this.presentPopover();
  }
  presentPopover() {
      let popover = this.popoverCtrl.create(RateKeyPopoverPage);
      popover.present();
  }
  goBack(){
      this.navCtrl.pop();
  }
}
