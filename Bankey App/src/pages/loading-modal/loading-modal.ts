import {Component, EventEmitter, Input} from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';

/**
 * Generated class for the LoadingModalPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-loading-modal',
  templateUrl: 'loading-modal.html',
})
export class LoadingModalPage {
    constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad LoadingModalPage');
      this.closeModal();
  }
  closeModal() {
    //setTimeout(() => {this.navCtrl.pop();},3000)
  }
}
