import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';

/**
 * Generated class for the RateKeyPopoverPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-rate-key-popover',
  templateUrl: 'rate-key-popover.html',
})
export class RateKeyPopoverPage {
  ratingValue = 4;
  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad RateKeyPopoverPage');
  }

  onModelChange(e){
    console.log(e);
  }
}
